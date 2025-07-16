from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from config.database import db
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
class Users(db.Model):
    
    __tablename__ = 'User_table'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    pass_user = Column(String(255), nullable=False)
    total_point = Column(Integer, nullable=False, default=0)
def User_register_model(user_name, email, pass_user, total_point):
    try:
        new_user = Users(user_name=user_name, email=email, pass_user=pass_user , total_point = total_point)
        db.session.add(new_user)
        db.session.commit()
        return {"success": True }
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}

def login_user_model(email, pass_user):
    user = db.session.query(Users).filter_by(email=email, pass_user=pass_user).first()
    if user:
        return {
            "success": True, 
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "total_point": user.total_point
        }
    return {"success": False, "error": "Invalid email or password"}

def get_user_by_id(user_id):
    """Lấy thông tin user theo ID"""
    return Users.query.get(user_id)

def update_user(user_id, user_name=None, pass_user=None):
    """Cập nhật thông tin User"""
    try:
        user = db.session.query(Users).filter_by(user_id=user_id).first()
        if not user:
            return {"success": False, "error": "User not found"}
        
        if user_name is not None:
            user.user_name = user_name
        if pass_user is not None:
            user.pass_user = pass_user
            
        db.session.commit()
        return {"success": True, "message": "User updated successfully"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}

def create_jwt_token(user_id, team_id ):
    """Tạo JWT token cho user"""
    payload = {
        'user_id': user_id,
        'team_id': team_id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token có hiệu lực trong 1 ngày
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return f"http://127.0.0.1:3001/join_team/{token}"
def check_email_model(email): 
    """check_email"""
    user = db.session.query(Users).filter_by(email = email).first()
    return user is not None
def get_user_by_email(email):
  
    get_name_user = Users.query.filter_by(email=email).first()
    
    return get_name_user