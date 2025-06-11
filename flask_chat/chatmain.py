from flask import Flask
from flask_chat.routes import app as routes_app
from ..agents.tutor_agent import responder_com_tutor
from flask_socketio import SocketIO 

if __name__ == "__main__":
    socketio.run(app, debug=True)
