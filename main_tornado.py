import os
import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import sys
import django.core.handlers.wsgi


def main():
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    application = django.core.handlers.wsgi.WSGIHandler()
    container = tornado.wsgi.WSGIContainer(application)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()