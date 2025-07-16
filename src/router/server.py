from flask import Blueprint, request, render_template, session, redirect, url_for, flash, jsonify
import os
from datetime import datetime
import jwt
from pyvi import ViTokenizer

from dotenv import load_dotenv
from controller.user import (
    User_register_function, 
    login_user_function, 
    create_user_session, 
    clear_user_session, 
    is_user_logged_in, 
    get_current_user_info,
    update_session_activity,
    check_session_timeout,
    update_user_controller,
    Mail_jointeam_function,
    get_list_team_of_user
)
from controller.task import(
    create_task_function,
    get_task_function,
    update_Status_task_function,
    get_task_status_summary
)

from model.team import( 
    acces_join_team, get_team_by_id
    )
from model.redisModel import(
    get_his_mes
)
from model.member import(
    check_role
) 
load_dotenv()

from controller.team import(create_team_function)
from controller.email import send_email_late_task

SECRET_KEY = os.getenv('SECRET_KEY')
server_blueprint = Blueprint("server", __name__)
# USER
@server_blueprint.before_request
def check_session():
    """Kiểm tra session trước mỗi request"""
    if is_user_logged_in():
        # Kiểm tra timeout
        if check_session_timeout():
            flash("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
            return redirect(url_for("server.hello"))
        # Cập nhật activity
        update_session_activity()

@server_blueprint.route("/")
def hello():
   return render_template("mainPage.html")

@server_blueprint.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")

@server_blueprint.route("/register", methods=["POST"])
def handle_register():
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    pass_user = request.form.get("password")

    result = User_register_function(user_name, email, pass_user)

    if result["success"]:
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("server.hello"))
    else:
        flash(f"Lỗi đăng ký: {result['error']}", "error")
        return redirect(url_for("server.hello"))

@server_blueprint.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("email")
    pass_user = request.form.get("password")
    
    result = login_user_function(email, pass_user)
    
    if result["success"]:
        create_user_session(
            user_id=result["user_id"],
            user_name=result["user_name"],
            email=result["email"],
            total_point = result["total_point"]
        )
        session.pop("team_id", None)  
        session.modified = True       
        flash(f"Chào mừng {result['user_name']}!", "success")

        return redirect(url_for("server.home"))

    else:
        flash(f"Lỗi đăng nhập: {result['error']}", "error")
        return redirect(url_for("server.hello"))

@server_blueprint.route("/logout")
def logout():
    """Đăng xuất và xóa session"""
    if is_user_logged_in():
        user_info = get_current_user_info()
        clear_user_session()
        flash("Đã đăng xuất thành công!", "info")
    return redirect(url_for("server.hello"))

@server_blueprint.route("/home", methods=["GET"])
def home():
    if not is_user_logged_in():
        flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
        return redirect(url_for("server.hello"))

    user_info = get_current_user_info()
    user_id = user_info['user_id']
    team_id = session.get("team_id")
    result = get_task_function(user_id, team_id)
    task_list = result.get("data", []) if result and result.get("success") else []
    return render_template("home.html", user_info=user_info, task=task_list)
@server_blueprint.route("/profile")
def profile():
    """Trang thông tin cá nhân"""
    if not is_user_logged_in():
        flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
        return redirect(url_for("server.hello"))

    user_info = get_current_user_info()
    print(type(user_info)) 
    status_info = get_task_status_summary(user_id=user_info["user_id"])
    print(status_info)
    return render_template("profile.html", user_info=user_info , status_info = status_info)

@server_blueprint.route("/update", methods=["POST"])
def update_function():
    user_name = request.form.get("user_name")
    pass_user = request.form.get("password")

    result = User_register_function(user_name, pass_user)

    if result["success"]:
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("server.hello"))
    else:
        flash(f"Lỗi đăng ký: {result['error']}", "error")
        return redirect(url_for("server.hello"))
    
@server_blueprint.route("/invite_members/<int:team_id>", methods=["POST"])
def semd_join_team(team_id):
        user_id = session.get("user_id")
        email = request.form.get("email")
        result = Mail_jointeam_function(user_id ,email, team_id)
        if result and result.get("success"):
            flash("Đã gửi email mời tham gia nhóm thành công!", "success")
            return redirect(url_for("server.team_list"))
        else:
            error_msg = result.get("error", "Bạn đã tham gia nhóm này rồi hoặc gửi email thất bại.") if result else "Bạn đã tham gia nhóm này rồi hoặc gửi email thất bại."
            flash(error_msg, "error")
            return render_template("team_list.html", teams=team_id)
@server_blueprint.route("/join_team/<token>", methods=["GET"])
def join_team_with_token(token):
        
    return render_template("join_team.html", token=token)
@server_blueprint.route("/api/accept-invite", methods=["POST"])
def api_accept_invite():
    data = request.get_json()
    try:
        return acces_join_team(data)
    except jwt.ExpiredSignatureError:
        return {"success": False, "error": "Token đã hết hạn"}, 400
    except jwt.InvalidTokenError:
        return {"success": False, "error": "Token không hợp lệ"}, 400

@server_blueprint.route("/team_list", methods=["GET"])
def team_list():
    if not is_user_logged_in():
        flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
        return redirect(url_for("server.hello"))

    user_id = session.get("user_id")
    
    teams = get_list_team_of_user(user_id=user_id)

  
    return render_template("team_list.html", teams=teams)
#TASK

@server_blueprint.route("/create/task", methods=["POST"])
def create_task():
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))

    try:
        # Lấy dữ liệu từ form
        task_title = request.form.get("task_title")
        task_description = request.form.get("task_description")
        start_str = request.form.get("start_date")
        end_str = request.form.get("end_date")
        start_dt = datetime.fromisoformat(start_str) 
        end_st = datetime.fromisoformat(end_str)  
        task_title_ = ViTokenizer.tokenize(task_title)
        task_description_ = ViTokenizer.tokenize(task_description)
        if not task_title or not start_str or not end_str:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))
        print(f"DEBUG_DATE: start_str = '{start_str}'") # Dòng này rất quan trọng
        print(f"DEBUG_DATE: end_str = '{end_str}'")   # Dòng này cũng rất quan trọng
        # Ép kiểu datetime từ định dạng HTML datetime-local
        start_dt = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S")
        end_st = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S")

        user_id = session.get("user_id")
        team_id = session.get("team_id")  

        result = create_task_function(
            user_id=user_id,
            team_id=team_id,
            task_title=task_title_,
            task_description=task_description_,
            start_date=start_dt,
            end_date=end_st,
        )

        if result and result.get("success"):
            flash("Task created successfully!", "success")
        else:
            flash(f" Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    except Exception as e:
        flash(f" Lỗi không mong muốn: {str(e)}", "error")

    return redirect(url_for("server.home"))
@server_blueprint.route("/update/task/<int:task_id>", methods=["POST"])
def update_status(task_id):
    if not is_user_logged_in():
        return redirect(url_for("server.home"))

    user_id = session.get("user_id")
    team_id = None
    result = update_Status_task_function(task_id ,user_id, team_id)
    if result and result.get("success"):
        flash("Task created successfully!", "success")
    else:
        flash(f" Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    return redirect(url_for("server.home"))
@server_blueprint.route("/task", methods=["GET"])
def get_task():
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))
    user_id = session.get("user_id")
    team_id = None
    if user_id != session.get("user_id"):   
        flash("Không có quyền truy cập task của người khác.", "danger")
        return redirect(url_for("server.home"))


    result = get_task_function(user_id, team_id)
    print(result)
    return render_template("home.html", tasks=result)
@server_blueprint.route("/task_of_team/<int:team_id>", methods=["GET"])
def get_task_task(team_id):
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))

    user_id = session.get("user_id")
    user_name = session.get("user_name")
    check_member = check_role(user_id, team_id )
    
    team_object = get_team_by_id(team_id=team_id)

    if not team_object:
        flash("Team không tồn tại.", "danger")
        return redirect(url_for("server.team_list"))

    result = get_task_function(user_id, team_id)
    task_list = []
    if result and result.get("success") and "data" in result:
        task_list = result["data"]
    
    
    return render_template(
        "groupPage.html",
        tasks=task_list,    
        team_name=team_object.team_name,
        team_id=team_id,
        user_name=user_name,
        check = check_member
    )
#TEAM

@server_blueprint.route("/createTeam", methods=["POST"])
def create_team():
    try:
        team_name = request.form.get("team_name")

        if not team_name:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))
        user_id = session.get("user_id")
        user_name = session.get("user_name")
        result = create_team_function(user_id,team_name,user_name)

        if result and result.get("success"):
            flash("Task created successfully!", "success")
        else:
            flash(f"Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    except Exception as e:
        flash(f"Lỗi không mong muốn: {str(e)}", "error")

    return redirect(url_for("server.team_list"))
#
@server_blueprint.route("/create/team/task/<int:team_id>", methods=["POST"])
def create_task_team(team_id):
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))

    try:
        # Lấy dữ liệu từ form
        task_title = request.form.get("task_title")
        task_description = request.form.get("task_description")
        start_str = request.form.get("start_date")
        end_str = request.form.get("end_date")
        print(f"DEBUG_DATE: start_str = '{start_str}'") # Dòng này rất quan trọng
        print(f"DEBUG_DATE: end_str = '{end_str}'")   # Dòng này cũng rất quan trọng
        if not task_title or not start_str or not end_str:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))
        start_dt = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S")
        end_st = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S")
        user_id = session.get("user_id")

        result = create_task_function(
            user_id=user_id,
            team_id=team_id,
            task_title=task_title,
            task_description=task_description,
            start_date=start_dt,
            end_date=end_st,
        )

        if result and result.get("success"):
            flash("Task created successfully!", "success")
        else:
            flash(f" Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    except Exception as e:
        flash(f" Lỗi không mong muốn: {str(e)}", "error")

    return redirect(url_for("server.get_task_task", team_id=team_id))

@server_blueprint.route("/update/task_team/<int:team_id>/<int:task_id>", methods=["POST"])
def update_status_team(team_id, task_id):
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))

    user_id = session.get("user_id")

    if not user_id:
        flash("Không tìm thấy thông tin người dùng. Vui lòng đăng nhập lại.", "danger")
        return redirect(url_for("server.home"))

    result = update_Status_task_function(task_id, user_id, team_id)

    if result and result.get("success"):
        flash("Cập nhật trạng thái công việc thành công!", "success")
    else:
        error_message = result.get('error', 'Có lỗi không xác định xảy ra khi cập nhật công việc.') if result else 'Có lỗi không xác định xảy ra.'
        flash(f"Lỗi cập nhật: {error_message}", "error")
    
    return redirect(url_for("server.get_task_task", team_id=team_id))
# CHAT 
@server_blueprint.route("/get_chat/<int:room_id>", methods=["POST"])
def get_db_chat_by_redis(room_id):
    chat =  get_his_mes(room_id=room_id)
    
    print("chatDayyyy", chat)
    if chat:
        return jsonify(chat)
    else:
        return jsonify({'error': 'Không tìm thấy cuộc trò chuyện'}), 404