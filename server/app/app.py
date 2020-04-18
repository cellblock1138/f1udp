#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask.ext.login import LoginManager, UserMixin, login_required
import socket
import threading
import sys
import struct
from teams import teams
from tracks import tracks
from flags import vehicle_fia_flags
from tyres import tyres
from gears import gears
from udppacket import UDPPacket
import logging

# Cause logs...
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
# eventlet and gevent seem to be broken on OS X at the moment
async_mode = "threading"

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

# Thread voodo
nc_thread = None
nc_thread_lock = Lock()

udp_thread = None
udp_thread_lock = Lock()


class User(UserMixin):
    # proxy for a database of users
    user_database = {"user": ("user", "secret")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    #client.send(response)
                    try:
                        print("sending {} to {} from {}".format(data, request.sid, address))
                    except Exception as e:
                        logger.error(e)
                    socketio.emit('my_response', {'data': response, 'count': 0}, namespace='/test')
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


def background_thread():
    """Example of how to send server generated events to clients."""
    ThreadedServer('',5001).listen()
    # count = 0
    # while True:
    #     socketio.sleep(10)
    #     count += 1
    #     socketio.emit('my_response', {'data': 'Server generated event', 'count': count}, namespace='/test')

def udp_ingest():
    # Configure listener IP & Port for UDP transmission of packed values
    UDP_IP = "0.0.0.0"
    UDP_PORT = 20777
    BUFFER = 1289

    # Receive packet from wire
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    def net_rx():
        data, addr = sock.recvfrom(BUFFER)  # receiving from socket
        return data, addr

    # Display helpers
    def displaygear(gear):
        response = "{}".format(gears[gear])
        # socketio.emit('my_response', {'data': response, 'count': 0}, namespace='/test')
        return response

    def displayspeed(mps):
        response = "Speed KPH: {:f}".format(mps * 3.6)
        # socketio.emit('my_response', {'data': response, 'count': 0}, namespace='/test')
        return response

    session_type = ["Unknown", "Practice", "Qualifying", "Race"]
    era = {2017: "Modern", 1980: "Classic"}

    def receiver():
        fmt = '<76f24bf5b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b13f' # define structure of packed data
        s = struct.Struct(fmt) # declare structure
        while True:
            # Get packets off wire
            rx_data, addr = net_rx()
            unpacked_data = s.unpack(rx_data)

            # Parse packet
            p = UDPPacket(unpacked_data)

            # Send data chunk to websocket
            socketio.emit('my_response', {'rpm': "{}".format(int(p.m_engineRate/p.m_max_rpm*100)),
                                          'throttle': "{}".format(int(p.m_throttle/1*100)),
                                          'brake': "{}".format(int(p.m_brake/1*100)),
                                          'gear': displaygear(p.m_gear),
                                          'speed': displayspeed(p.m_speed)

                                          }, namespace='/test')

            # Output to console for sanity check
            # print("RPM -- current: {} max: {} percent: {}".format(int(p.m_engineRate), int(p.m_max_rpm), int(p.m_engineRate/p.m_max_rpm*100)))


    # Start UDP listener
    receiver()


@app.route('/')
@login_required
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global nc_thread
    global udp_thread

    with nc_thread_lock:
        if nc_thread is None:
            nc_thread = socketio.start_background_task(target=background_thread)

    with udp_thread_lock:
        if udp_thread is None:
            udp_thread = socketio.start_background_task(target=udp_ingest)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
