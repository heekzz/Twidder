from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from Twidder import app, database_helper

host, port = 'localhost', 5000

database_helper.init_database()
server = WSGIServer(("", port), app, handler_class=WebSocketHandler)
print('Server started at %s:%s' % (host, port))
server.serve_forever()

