from conexao.conexao import mongodb

class HotelModel(mongodb):
  def __init__(self, hotel_id, nome, estrela, diaria, cidade):
    self.hotel_id = hotel_id
    self.nome = nome
    self.estrela = estrela
    self.diaria = diaria
    self.cidade = cidade

  def json(self):
    return {
      'hotel_id': self.hotel_id,
      'nome': self.nome,
      'estrela': float(self.estrela),
      'diaria': float(self.diaria),
      'cidade': self.cidade
    }
  
  def find_hotel(hotel_id):
    hotel = mongodb.db.hoteis.find_one({"hotel_id": hotel_id})
    if hotel:
      del(hotel['_id'])
      return hotel
    return None

  def save_hotel(self):
    mongodb.db.hoteis.insert_one(self.json())

  def update_hotel(self):
    mongodb.db.hoteis.update_one({"hotel_id": self.hotel_id},{"$set":self.json()})

  def delete_hotel(hotel_id):
    return mongodb.db.hoteis.delete_one({"hotel_id": hotel_id}).deleted_count
