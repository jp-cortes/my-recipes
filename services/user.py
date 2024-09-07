from models.user import User as UserModel
from schemas.user import User, CreateUser

class UserService():
    def __init__(self, db) -> None:
        self.db = db


    def check_user(self, user):
        verify_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        return verify_user
    
    def get_user_role(self, user):
        verify_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        return verify_user.role

    def create_user(self, user: CreateUser, encode_password):
         # Check if this is the first user in the database
        user_count = self.db.query(UserModel).count()
        
        # Assign the role based on whether there are any users already
        role = "admin" if user_count == 0 else "user"
        
        hashed_password = encode_password(user.password)
        newUser = UserModel(name= user.name, email= user.email, password=hashed_password, role=role)

        self.db.add(newUser)
        self.db.commit() 
        self.db.refresh(newUser)
        return