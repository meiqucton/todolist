from model.user import User_register_model, login_user_model,update_user
from flask import session
import uuid
from datetime import datetime

from model.user import ( create_jwt_token, get_user_by_id, check_email_model, get_user_by_email)
from model.team import (get_team_by_id)
from model.member import (
    check_role,
    get_member
)
from controller.email import (
    send_email_late_task
    ,
)   
from controller.task import(
    count_task_by_status
)

def User_register_function(user_name, email, password):
    if not user_name or not email or not password:
        return {"success": False, "error": "All fields are required"}
    total_point = 0
    if len(password) < 8:
        return {"success": False, "error": "Password must be at least 8 characters long"}
    if check_email_model(email):
        return {"success": False, "error": "Gmail này đã được sử dụng rồi"}
    else: 
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
            "email": user["email"],
            "total_point": user["total_point"]
        }
    return {"success": False, "error": user.get("error", "Login failed")}

def create_user_session(user_id, user_name, email, total_point):
    """Tạo session cho user với thông tin cần thiết"""
    session.permanent = True  
    session['user_id'] = user_id
    session['user_name'] = user_name
    session['email'] = email
    session['total_point'] = total_point
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
            'total_point': session.get('total_point'),
            'login_time': session.get('login_time'),
            'last_activity': session.get('last_activity')
        }
    return None
def update_user_controller(user_name, passwork):
    if user_name: 
        user_name = user_name

    if passwork:  
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
def Mail_jointeam_function(user_id ,email, team_id):
    """nhu ten"""
    check_leader = check_role(user_id, team_id)
    if not check_leader:
        return check_leader
    in4_team = get_team_by_id(team_id)
    print("email___", email) 
    get_name_user = get_user_by_email(email= email)
    print("thong tin ", get_name_user)
    print(type(get_name_user))
    member_id = get_name_user.user_id
    token_user = create_jwt_token(member_id, team_id)
    
    if not in4_team:
        return {"success": False, "error": "Team not found"}
    team_name = in4_team.team_name
    body = f"""
    <p>Bạn được mời tham gia nhóm <strong>{team_name}</strong>.</p>
    <p>Vui lòng nhấn nút dưới đây để tham gia nhóm:</p>
    <a href="{token_user}" style="display:inline-block;padding:10px 20px;background-color:#1e90ff;color:white;text-decoration:none;border-radius:5px;">Tham gia nhóm</a>
"""
    subject = f"Tham gia nhóm {team_name}"
    
    return send_email_late_task(subject, email, body)

def get_list_team_of_user(user_id): 
    members = get_member(user_id)
    result = []

    for m in members:
        team_list = get_team_by_id(m.team_id)  # team_list là dạng: [{'team_name': ..., 'team_id': ...}]
        print(team_list) 
        result.append(team_list)
    print()
    return result
