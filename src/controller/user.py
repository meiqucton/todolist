from model.user import User_register_model, login_user_model,update_user
from flask import session
import uuid
from datetime import datetime
from model.member import (
    join_team,
)

def User_register_function(user_name, email, password):
    if not user_name or not email or not password:
        return {"success": False, "error": "All fields are required"}
    total_point = 0
    if len(password) < 8:
        return {"success": False, "error": "Password must be at least 8 characters long"}
    new_user = User_register_model(user_name=user_name, email=email, pass_user=password, total_point = total_point)
    return new_user

def login_user_function(email, password):
    if not email or not password:
        return {"success": False, "error": "Email and password are required"}
    user = login_user_model(email=email, pass_user=password)
    if user["success"]:
        return {
            "success": True, 
            "user_id": user["user_id"],
            "user_name": user["user_name"],
            "email": user["email"]
        }
    return {"success": False, "error": user.get("error", "Login failed")}

def create_user_session(user_id, user_name, email):
    """Tạo session cho user với thông tin cần thiết"""
    session.permanent = True  
    session['user_id'] = user_id
    session['user_name'] = user_name
    session['email'] = email
    session['session_id'] = str(uuid.uuid4()) 
    session['login_time'] = datetime.now().isoformat()
    session['last_activity'] = datetime.now().isoformat()

def update_session_activity():
    """Cập nhật thời gian hoạt động cuối cùng"""
    if 'user_id' in session:
        session['last_activity'] = datetime.now().isoformat()

def clear_user_session():
    """Xóa toàn bộ session của user"""
    session.clear()

def is_user_logged_in():
    """Kiểm tra user đã đăng nhập chưa"""
    return 'user_id' in session

def get_current_user_id():
    """Lấy user_id hiện tại từ session"""
    return session.get('user_id')

def get_current_user_info():
    """Lấy thông tin user hiện tại từ session"""
    if is_user_logged_in():
        return {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'email': session.get('email'),
            'login_time': session.get('login_time'),
            'last_activity': session.get('last_activity')
        }
    return None
def update_user_controller(user_name, passwork):
    if user_name:  # nếu user_name không phải None hoặc chuỗi rỗng
        user_name = user_name

    if passwork:  # nếu passwork không phải None hoặc chuỗi rỗng
        passwork = passwork
    
    
    return None
def check_session_timeout():
    """Kiểm tra session có bị timeout không (24 giờ)"""
    if 'last_activity' in session:
        last_activity = datetime.fromisoformat(session['last_activity'])
        current_time = datetime.now()
        time_diff = current_time - last_activity
        

        if time_diff.total_seconds() > 24 * 3600:
            clear_user_session()
            return True
    return False
def jointeam_function(user_id, team_id ):
    """nhu ten"""
    role_user = 'Member'
    result= join_team(user_id, team_id ,role_user)
    
    return result 