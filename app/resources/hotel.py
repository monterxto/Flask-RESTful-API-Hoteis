from models.hotel import HotelModel
from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrela_min', type=float)
path_params.add_argument('estrela_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=int)
path_params.add_argument('offset', type=int)

def normalize_path_params(cidade=None,estrela_min = 0, estrela_max = 5,diaria_min = 0, diaria_max = 10000, limit = 50, offset = 0, **dados ):
  if cidade:
    return [{ 
        'cidade': {'$eq': cidade},
        'estrela': {'$gte': estrela_min}, 
        'estrela': {'$lte':estrela_max},
        'diaria': {'$gte': diaria_min}, 
        'diaria': {'$lte': diaria_max}
      }, limit, offset]
  return [{
      'estrela': {'$gte': estrela_min}, 
      'estrela': {'$lte':estrela_max},
      'diaria': {'$gte': diaria_min}, 
      'diaria': {'$lte': diaria_max}
    }, limit, offset]

class Hoteis(Resource):
  def get(self):
    dados = path_params.parse_args()
    dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
    parametros = normalize_path_params(**dados_validos) 
    hoteis = {"hoteis":[]}
    for hotel in HotelModel.db.hoteis.find(parametros[0]).limit(parametros[1]).skip(parametros[2]):
      del hotel["_id"]
      hoteis["hoteis"].append(hotel)
    return hoteis

class Hotel(Resource):
  def __init__(self):
    self.argumentos = reqparse.RequestParser()
    self.argumentos.add_argument('nome', type=str, required=True, help="Precisa do nome")
    self.argumentos.add_argument('estrela', type=str, required=True, help="Precisa das estrelas")
    self.argumentos.add_argument('diaria', type=str, required=True, help="Precisa da diaria")
    self.argumentos.add_argument('cidade', type=str, required=True, help="Precisa da cidade")

  def get(self, hotel_id):
    try:
      hotel = HotelModel.find_hotel(hotel_id) #Procura se já existe um hotel com esse id
    except:
      return {'message': 'Não foi possivel consultar o banco'}, 500 #Internal Error
    if hotel:
      return hotel
    return {'message': 'Não achou nenhum Hotel.'}, 404

  @jwt_required
  def post(self, hotel_id):
    try:
      if HotelModel.find_hotel(hotel_id): #Procura se já existe um hotel com esse id
        return {'message': 'Já existe'},400 #bad request #409 #Conflito
    except:
      return {'message': 'Não foi possivel consultar o banco'}, 500 #Internal Error
      
    dados = self.argumentos.parse_args()
    hotel_objeto = HotelModel(hotel_id, **dados)
    try:
      hotel_objeto.save_hotel()
    except:
      return {'message': 'Não foi possivel consultar no banco'} , 500 #Internal Error
    
    return hotel_objeto.json(), 200

  @jwt_required
  def put(self, hotel_id):
    dados = self.argumentos.parse_args()
    hotel_objeto = HotelModel(hotel_id, **dados)
    try:
      hotel_encontrado = HotelModel.find_hotel(hotel_id) #Procura se já existe um hotel com esse id
    except:
      return {'ERROR': 'Não foi possivel consultar o banco'}
    
    if hotel_encontrado:
      hotel_objeto.update_hotel()
      return hotel_objeto.json(), 200 #Certo

    try:
      hotel_objeto.save_hotel()
    except:
      return {'message': 'Não foi possivel consultar no banco'} , 500 #Internal Error
      
    return hotel_objeto.json(), 201 #Criado

  @jwt_required
  def delete(self, hotel_id):
    try:
      deletado = HotelModel.delete_hotel(hotel_id)
    except:
      return {'message': 'Não foi possivel deletar'} , 500 #Internal Error
    if deletado:
      return {'message': 'Hotel Deletado.'}, 200 #ok
    return {'message': 'Hotel não existe'}, 404 #Not Found