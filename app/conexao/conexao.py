import pymongo

class mongodb:
  try:
    client = pymongo.MongoClient(
      host="db",
      port=27017,
      username='admin',
      password='admin'
    )
    db = client.tFlask
    print("Banco de dados conectado!")
  except:
    print("ERRO - Não foi possivel se conectar ao banco de dados")
  def __init__(self):
    self.existeColecao()

  def existeColecao(self):
    colecoes = self.db.list_collection_names()
    if "hoteis" not in colecoes:
      self.db.create_collection('hoteis')
    if "usuarios" not in colecoes:
      self.db.create_collection('usuarios')