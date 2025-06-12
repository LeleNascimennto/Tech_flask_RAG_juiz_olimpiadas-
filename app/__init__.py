from flask import Flask
from flask_socketio import SocketIO 
import os
from dotenv import load_dotenv

load_dotenv()
# a aplicacao que estah sendo implementada eh uma instancia da classe Flask
app = Flask(__name__)

# a importacao de "routes" eh feita no final
# para evitar referencia circular nos imports
# (no arquivo routes eh necessario importar app)

app.secret_key = os.getenv("SECRET_KEY", "chave_seguranca")
ASYNC_MODE = os.getenv("ASYNC_MODE", "threading")
socketio = SocketIO(app, async_mode=ASYNC_MODE)
from routes import bp
app.register_blueprint(bp)
