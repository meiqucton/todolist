from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from config.database import db

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

def get_email_by_user_id(user_id):
    user = db.session.query(Users).filter_by(user_id=user_id).first()
    if user:
        return user.email
    return None

def login_user_model(email, pass_user):
    user = db.session.query(Users).filter_by(email=email, pass_user=pass_user).first()
    if user:
        return {
            "success": True, 
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email
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
        
        # Chỉ cập nhật các trường được cung cấp
        if user_name is not None:
            user.user_name = user_name
        if pass_user is not None:
            user.pass_user = pass_user
            
        db.session.commit()
        return {"success": True, "message": "User updated successfully"}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}
