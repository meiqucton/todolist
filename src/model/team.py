from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from config.database import db
from model.member import Membership
from dotenv import load_dotenv
import os
import jwt 
from flask import request
from model.member import (
    join_team
)
from model.redisModel import (
    join_room_chat
)

from model.user import (
    get_user_by_id
)


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

class Team(db.Model):
    __tablename__ = 'Team' 

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(255), nullable=False)
    total_point = Column(Integer, nullable=True)
 
def create_team_and_add_leader(user_id ,team_name ,role_user ,total_point = None):
    try:
        
        new_team = Team(team_name=team_name, total_point=total_point)
        db.session.add(new_team)
        db.session.commit()  
        new_team_id = new_team.team_id
        new_membership = Membership(
            user_id=user_id,
            role_user=role_user,         
            team_id=new_team_id
        )
        
        db.session.add(new_team)
        db.session.add(new_membership)
        
        db.session.commit()
        
        return {
            "success": True,
            "team_id": new_team.team_id
        }

    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!! LỖI KHI TẠO TEAM !!!!!!!!!!!!!!!")
        import traceback
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return {
            "success": False,
            "error_detail": str(e)
        }
def get_team_by_id(team_id):
    """Lấy thông tin  theo ID"""
    return Team.query.get(team_id)

def acces_join_team(data):
    data = request.get_json()
    token = data.get("token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        team_id = payload["team_id"]
        role_user = "member"
        user_name = get_user_by_id(user_id).user_name
        add_member = join_team(user_id, team_id, role_user)
        print("🚀 Thêm thành viên vào team:", add_member)
        add_member_chat = join_room_chat(room_id = team_id, user_id=user_id, user_name=user_name)
        if not add_member.get('success') or not add_member_chat.get('success'):
            raise Exception("Lỗi khi thêm vào team hoặc nhóm chat")

        return {
            "success": True,
            "message": "Bạn đã tham gia nhóm thành công"
        }

    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token đã hết hạn"}

    except jwt.InvalidTokenError:
        return {"success": False, "message": "Token không hợp lệ"}

    except Exception as e:
        print("❌ Lỗi:", str(e))
        return {"success": False, "message": "Có lỗi xảy ra khi tham gia nhóm"}
