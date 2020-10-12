from conexao.conexao import mongodb

class UserModel(mongodb):
  def __init__(self, user_id, login, senha):
    self.user_id = user_id 
    self.login = login
    self.senha = senha

  def json(self):
    return {
      'user_id': self.user_id,
      'login': self.login
    }

  def find_user(user_id):
    user = mongodb.db.usuarios.find_one({"user_id": user_id})
    if user:
      del(user['_id'])
      return user
    return None

  def find_by_login(login):
    user = mongodb.db.usuarios.find_one({"login": login})
    if user:
      print(user)
      del(user['_id'])
      return user
    return None

  def save_user(self):
    user = self.json()
    user['senha'] = self.senha
    mongodb.db.usuarios.insert_one(user)

  def delete_user(user_id):
    return mongodb.db.usuarios.delete_one({"user_id": user_id}).deleted_count
