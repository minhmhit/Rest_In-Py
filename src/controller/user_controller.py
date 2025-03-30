from sqlalchemy.exc import IntegrityError 
from passlib.context import CryptContext   
from database import Session                  
from model import User                  

#mã hoá

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(username, password, role,tenant_id=None):
   
    session = Session()
    try:
        hashed_password = pwd_context.hash(password)  #mã hóa mật khẩu
        new_user = User(username=username, password=hashed_password, role=role)
        session.add(new_user)  
        session.commit()     
    except IntegrityError:   
        session.rollback()    
        raise ValueError("Username đã tồn tại")
    finally:
        session.close()      
def get_user_by_id(user_id):
   
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()  
    session.close()
    return user

def get_user_by_username(username):
   
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def update_user(user_id, **kwargs):
   
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        for key, value in kwargs.items():  
            if key == 'password':          
                value = pwd_context.hash(value)
            setattr(user, key, value)     
        session.commit()
    else:
        raise ValueError("Không tìm thấy người dùng")
    session.close()

def delete_user(user_id):
   
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)  
        session.commit()
    else:
        raise ValueError("Không tìm thấy người dùng")
    session.close()

def login(username, password):
  
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if user and pwd_context.verify(password, user.password):  
        session.close()
        return user
    session.close()
    return None