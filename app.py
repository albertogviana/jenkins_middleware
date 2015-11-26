from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from middleware import create_app

http_server = HTTPServer(WSGIContainer(create_app()))
http_server.bind(5000)
http_server.start(0)
IOLoop.current().start()
