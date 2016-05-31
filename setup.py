from setuptools import setup

setup(
    name='linksave',
    version='0.1',
    description='Server with rest api to save links',
    author='Paul Klym',
    author_email='klym.paul@gmail.com',
    url='http://links-appsdfasfwewwg.rhcloud.com/',
    # py_modules=['linksave'],
    # scripts=['linksave'],
    install_requires=['tornado', 'pymongo', 'requests', 'bs4'],
    license='MIT',
)
