from models.usuario import UserModel
from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from blacklist import BLACKLIST
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Precisa de um login")
atributos.add_argument('senha', type=str, required=True, help="Precisa de um senha")

class User(Resource):
  # /usuarios/{user_id}
  def get(self, user_id):
    try:
      user = UserModel.find_user(user_id) #Procura o usuário
    except:
      return {'message': 'Não foi possivel consultar o banco'}, 500 #Internal Error
    if user:
      return user
    return {'message': 'Não achou nenhum usuário.'}, 404

  @jwt_required
  def delete(self, user_id):
    try:
      deletado = UserModel.delete_user(user_id)
    except:
      return {'message': 'Não foi possivel deletar'} , 500 #Internal Error
    if deletado:
      return {'message': 'Usuário Deletado.'}, 200 #ok
    return {'message': 'Usuário não existe'}, 404 #Not Found

class UserRegister(Resource):
  #Cadastro
  def post(self):
    
    dados = atributos.parse_args()

    if UserModel.find_by_login(dados['login']):
      return  {"message": "O login '{}' já existe".format(dados['login'])}, 400 #bad request

    user = UserModel(dados['login'],**dados)
    user.save_user()
    return {"message": "Usuário criado com sucesso!"}, 201 #criado

class UserLogin(Resource):
  def post(self):
    dados = atributos.parse_args()

    user = UserModel.find_by_login(dados['login'])

    if user and safe_str_cmp(user['senha'], dados['senha']):
      token_de_acesso = create_access_token(identity=user['user_id'])
      return {'access_token': token_de_acesso}, 200
    return {"message": "O usuário ou senha está incorreto."}, 401 #Unathorized

class UserLogout(Resource):
  @jwt_required
  def post(self):
    jwt_id = get_raw_jwt()['jti'] # JTI = "JWT Token Identifier" - Identificar Token JWT
    BLACKLIST.add(jwt_id)
    return {"message": "Você se deslogou com sucesso!"}, 200
