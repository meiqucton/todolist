from flask import Flask
from config.database import Config, db
from router.server import server_blueprint
from dotenv import load_dotenv
from socketio_instance import socketio

from config.Gmail import init_mail
import os
from datetime import timedelta

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.getenv("SECRET_KEY") 

    # Cấu hình session bảo mật
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    db.init_app(app)
    init_mail(app)

    with app.app_context():
        from model.user import Users
        from model.task import Task
        from model.member import Membership
        from model.team import Team
        db.create_all()

    app.register_blueprint(server_blueprint)
    socketio.init_app(app)

    return app

# Chạy app
if __name__ == "__main__":
    print("⚡ Khởi tạo app...")
    app = create_app()
    
    print("⚡ Import socket handlers...")
    from controller.chat_controller import *  # nếu có lỗi ở đây, sẽ dừng tại đây
    
    print("⚡ Chạy socketio...")
    socketio.run(app, debug=False, port=3001)
