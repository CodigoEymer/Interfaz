import socketio
import json

# create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')

# wrap with a WSGI application
app = socketio.WSGIApp(sio, static_files={'/':{'countent_type':'text/html', 'filename':'mapa.html'}})



@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def my_event(sid, data):
    sio.emit('my event', {'data': 'foobar'})

@sio.on('wp_region')
def another_event(sid, data):
    print("Data: ")
    print("sid",sid)
    print("data",data)
    #sio.emit('wp_region', {'data': 'si se recibio'})


if __name__ == '__main__':
   import eventlet
   eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)
   #socketio.run(app)


""" # client.py
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('message', 'Hello from Python client!')

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def message(sid, data):
    print('Received message:', data)
    sio.emit('message', data)


sio.connect('http://localhost:5000')
sio.wait() """

