from flask import Blueprint, request, render_template, session, redirect, url_for, flash
import os
from datetime import datetime
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
    jointeam_function
)
from controller.task import(
    create_task_function,
    get_task_function,
    update_Status_task_function,
)
from controller.team import(create_team_function)
from controller.email import send_email_late_task

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
        # Tạo session với thông tin đầy đủ
        create_user_session(
            user_id=result["user_id"],
            user_name=result["user_name"],
            email=result["email"]
        )
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
    """Trang chủ sau khi đăng nhập"""
    if not is_user_logged_in():
        flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
        return redirect(url_for("server.hello"))

    user_info = get_current_user_info()
    return render_template("home.html", user_info=user_info)

@server_blueprint.route("/profile")
def profile():
    """Trang thông tin cá nhân"""
    if not is_user_logged_in():
        flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
        return redirect(url_for("server.hello"))

    user_info = get_current_user_info()
    return render_template("profile.html", user_info=user_info)

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
    
@server_blueprint.route("/join/<int:team_id>", methods=["POST"])
def join_team(team_id):
        user_id = session.get("user_id")
        result = jointeam_function(user_id, team_id)
        if result["success"]:
            flash("join success.", "success")
            return redirect(url_for("server.hello"))
        else:
            flash(f"Bạn đã tham gia nhóm này rồi ", "error")
            return redirect(url_for("server.hello"))

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

        if not task_title or not start_str or not end_str:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))

        # Ép kiểu datetime từ định dạng HTML datetime-local
        start_date = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")

        user_id = session.get("user_id")
        team_id = session.get("team_id")  

        result = create_task_function(
            user_id=user_id,
            team_id=team_id,
            task_title=task_title,
            task_description=task_description,
            start_date=start_date,
            end_date=end_date,
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
    return update_Status_task_function(task_id ,user_id, team_id)
@server_blueprint.route("/task/<int:user_id>", methods=["GET"])
def get_task(user_id):
    if not is_user_logged_in():
        flash("Tài khoản đăng nhập đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("server.home"))
    if user_id != session.get("user_id"):
        flash("Không có quyền truy cập task của người khác.", "danger")
        return redirect(url_for("server.home"))

    team_id = session.get("team_id")

    result = get_task_function(user_id, team_id)
    return result

#TEAM

@server_blueprint.route("/createTeam", methods=["POST"])
def create_team():
    try:
        team_name = request.form.get("team_name")

        if not team_name:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))
        user_id = session.get("user_id")
        result = create_team_function(team_name, user_id)

        if result and result.get("success"):
            flash("Task created successfully!", "success")
        else:
            flash(f"Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    except Exception as e:
        flash(f"Lỗi không mong muốn: {str(e)}", "error")

    return redirect(url_for("server.home"))
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

        if not task_title or not start_str or not end_str:
            flash("Vui lòng điền đầy đủ thông tin bắt buộc", "error")
            return redirect(url_for("server.home"))

        start_date = datetime.strptime(start_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_str, "%Y-%m-%dT%H:%M")

        user_id = session.get("user_id")

        result = create_task_function(
            user_id=user_id,
            team_id=team_id,
            task_title=task_title,
            task_description=task_description,
            start_date=start_date,
            end_date=end_date,
        )

        if result and result.get("success"):
            flash("Task created successfully!", "success")
        else:
            flash(f" Lỗi tạo task: {result.get('error', 'Không rõ lỗi')}", "error")

    except Exception as e:
        flash(f" Lỗi không mong muốn: {str(e)}", "error")

    return redirect(url_for("server.home"))

@server_blueprint.route("/update/task_team/<int:team_id>/<int:task_id>", methods=["POST"])
def update_status_team(team_id,task_id):
    if not is_user_logged_in():
        return redirect(url_for("server.home"))

    user_id = session.get("user_id")
    return update_Status_task_function(task_id ,user_id, team_id)