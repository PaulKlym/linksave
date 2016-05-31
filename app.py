import imp
import os

if __name__ == '__main__':
       ip   = os.environ['OPENSHIFT_PYTHON_IP']
       port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
       app = imp.load_source('app', 'links.py')

       app.app.listen(port , ip)
       app.ioloop.IOLoop.instance().start()
