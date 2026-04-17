from datetime import datetime

class User:
    def __init__(self, name, email, password, age=None, goal=''):
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.goal = goal
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'goal': self.goal,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            age=data.get('age'),
            goal=data.get('goal', '')
        )
        if '_id' in data:
            user.id = str(data['_id'])
        return user

class UserModel:
    def __init__(self, db):
        self.collection = db.users
    
    def create(self, user):
        result = self.collection.insert_one(user.to_dict())
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id):
        return self.collection.find_one({'_id': user_id})
    
    def update(self, user_id, data):
        self.collection.update_one({'_id': user_id}, {'$set': data})
    
    def delete(self, user_id):
        self.collection.delete_one({'_id': user_id})
