import requests
import logging
import hashlib
import time
import uuid
import json
import os
import re

import bs4
import functools

from urllib.parse import urlparse
from datetime import datetime

from tornado import ioloop, web, gen, httpclient
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId


MONGODB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'linksave'

# MONGODB_URL = 'mongodb://localhost:27017/'
# MONGODB_NAME = 'linksave'

client = MongoClient(MONGODB_URL)
db = client[MONGODB_NAME]

log = logging.getLogger('linksave')
log.setLevel(logging.DEBUG)
log.d = log.debug
log.i = log.info
log.w = log.warn
log.e = log.error
log.c = log.critical

regex = re.compile(
    r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')


def mes(fun):
    def a(*args, **kwargs):
        t = time.time()
        res = fun(*args, **kwargs)
        log.i('Done {} in {:.2}s'.format(fun.__name__, time.time()-t))
        return res
    return a


class IndexHandler(web.RequestHandler):    
    def get(self):
        with open('templates/index.html') as f:
            self.write(f.read())


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            return ret_error(self, 'Unauthenticated', 403)
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        token = self.get_argument('token', None)
        return db.tokens.find_one(token) if token else None


class UserHandler(BaseHandler):    
    @authenticated
    def get(self):
        user = db.users.find_one(self.current_user['user_id'])
        if user:
            del user['password']
            self.write(json.dumps(user, default=json_util.default))
        else:
            ret_error(self, 'Can not find user')

    @authenticated
    def delete(self):
        params = json.loads(self.request.body.decode())
        user = db.users.find_one(self.current_user['user_id'])
        if not user:
            ret_error(self, 'Can not find user')
        pswd = hashlib.sha512(params['password'].encode()).hexdigest()
        if not user or not params or pswd != user['password']:
            return ret_error(self, 'Invalid password, can not delete user')
        db.tokens.remove(self.current_user['_id'])
        db.users.remove(self.current_user['user_id'])


class RegisterHandler(BaseHandler):
    def post(self):
        if not self.request.body:
            return ret_error(self, 'Empty fields')
        fields = json.loads(self.request.body.decode())
        try:
            user = {k: v.strip() for k,v in fields.items()}
        except AttributeError:
            return ret_error(self, 'Invalid field type')

        if 'email' not in user:
            return ret_error(self, 'No email field')
        if 'pswd0' not in user:
            return ret_error(self, 'No password field')
        if 'pswd1' not in user:
            return ret_error(self, 'No confirmation password field')
        if user['pswd0'] != user['pswd1']:
            return ret_error(self, 'Passwords do not match')
        if not regex.match(user['email']):
            return ret_error(self, 'Not valid email')
        if not 8 <= len(user['pswd0']) <= 32:
            return ret_error(self, 'Invalid password length, must be between 8 and 32')
        if 'nick' not in user or not user['nick']:
            user['nick'] = user['email']
        u = db.users.find_one({"email": user['email']})
        if u:
            return ret_error(self, 'User with such email exist already')
        user['password'] = hashlib.sha512(user['pswd0'].encode()).hexdigest()
        user['date'] = datetime.now()
        del user['pswd1']
        del user['pswd0']
        db.users.insert_one(user)


class LoginHandler(BaseHandler):
    def post(self):
        if not self.request.body:
            ret_error(self, 'Empty body')
        user = json.loads(self.request.body.decode())
        if 'email' not in user:
            return ret_error(self, 'No email field')
        if 'password' not in user:
            return ret_error(self, 'No password field')
        u = db.users.find_one({"email": user['email']})
        pswd = hashlib.sha512(user['password'].encode()).hexdigest()
        if not u or pswd != u['password'] or user['email'] != u['email']:
            return ret_error(self, 'Invalid email or password')

        t = db.tokens.find_one({'user_id': u['_id']})
        if t:
            self.write(json.dumps({'token': t['_id']},default=json_util.default))
            return
        token = {}
        token['_id'] = uuid.uuid4().hex
        token['user_id'] = u['_id']
        token['date'] = datetime.now()
        db.tokens.save(token)
        self.write(json.dumps({'token': token['_id']},default=json_util.default))


class LogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        db.tokens.remove(self.current_user['_id'])


class LinksHandler(BaseHandler):
    @authenticated
    def get(self):
        # log.i(self.current_user['user_id'])
        offset = int(self.get_argument('offset', 0))
        limit = int(self.get_argument('limit', 40))
        links = db.__getattr__('links{}'.format(
            self.current_user['user_id'])).find().sort([
                ('$natural', -1)
            ]).skip(offset).limit(limit)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(list(links),default=json_util.default))

    @authenticated
    @gen.coroutine
    def post(self):
        t = time.time()

        link_data = json.loads(self.request.body.decode())
        if 'link' not in link_data:
            return ret_error(self, 'Missing field <link>')

        link = link_data['link']

        link_data['date'] = datetime.now()
        link_data['title'], link_data['favicon'] = yield [get_title(link), get_favicon(link)]

        if not link.startswith('http'):
            link_data['link'] = ''

        db.__getattr__('links{}'.format(self.current_user['user_id'])).save(link_data)
        
        self.set_header('Content-Type', 'application/json')
        self.set_status(201)
        self.write(json.dumps(link_data,default=json_util.default))

        log.i('Done in {:.2}s'.format(time.time() - t))


    def delete(self, id):
        if id:
            db.__getattr__('links{}'.format(
                self.current_user['user_id'])).remove(
                    {'_id':ObjectId(str(id))})
        else:
            ret_error(self, 'Invalid link id')


def ret_error(s, msg, code=400):
    error = {
        "code": code,
        "error": msg
        }
    s.set_status(code)
    s.write(json.dumps(error,default=json_util.default))
    s.finish()

@gen.coroutine
def get_favicon(url):
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        path = '{uri.scheme}://{uri.netloc}/favicon.ico'.format(uri=parsed)

        client = httpclient.AsyncHTTPClient()
        try:
            yield client.fetch(path)
            return path
        except:
            pass
    return '/static/img/default'

@gen.coroutine
def get_title(url):
    # if link don't starts with http try with one
    try:
        client = httpclient.AsyncHTTPClient()
        response = yield client.fetch(url)
        html = bs4.BeautifulSoup(response.body, 'html.parser')
        return html.title.text
    except:
        return url[:64]


settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'debug': True,
    # 'login_url': '/api/v1.0/login'
}

def make_app():
    return web.Application([
    (r'/', IndexHandler),
    (r'/index', IndexHandler),
    (r'/api/v1.0/links/?', LinksHandler),
    (r'/api/v1.0/links/(.*)', LinksHandler),
    (r'/api/v1.0/login', LoginHandler),
    (r'/api/v1.0/logout', LogoutHandler),
    (r'/api/v1.0/register', RegisterHandler),
    (r'/api/v1.0/user', UserHandler)
], **settings)


if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    ioloop.IOLoop.current().start()
