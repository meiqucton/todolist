from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from config.database import db
from model.member import Membership
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
    """Lấy thông tin user theo ID"""
    return Team.query.get(team_id)

