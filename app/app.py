import socket
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from conexao.conexao import mongodb

banco = mongodb()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Segredo'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def verificar_blacklist(token):
  return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidade():
  return jsonify({'message': 'Você está deslogado.'}), 401 #Unauthorized

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<string:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
  app.run(socket.gethostbyname(socket.gethostname()), debug=True)