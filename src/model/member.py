from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,and_, or_, update
from sqlalchemy.orm import relationship

from datetime import datetime
from config.database import db
# from model.team import Team
class Membership(db.Model): 
    __tablename__ = 'membership'  

    id_membership = Column(Integer, primary_key=True, autoincrement=True)  
    user_id = Column(Integer, ForeignKey('User_table.user_id'), nullable=False)
    team_id = Column(Integer, ForeignKey('Team.team_id'), nullable=False)
    role_user = Column(String(255), nullable=False)

    user = relationship("Users", backref="memberships")
    team = relationship("Team", backref="members")

def join_team(user_id, team_id ,role_user): 
    try: 
        existing_membership = Membership.query.filter_by(user_id=user_id).first()
        if existing_membership:
            return {
                "success": False,
                "message": f"Người dùng ID {user_id} đã tham gia team ID {existing_membership.team_id}. Không thể tạo team mới."
            }
        new_membership = Membership(
            user_id=user_id,
            role_user=role_user,         
            team_id=team_id
        )
        db.session.add(new_membership)
        db.session.commit()
        return {
            "success": True,
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
def check_role(user_id, team_id): 
    try: 
        check_member = Membership.query.filter_by(user_id = user_id, team_id =team_id).first()
        if check_member.role_user == 'Leader':
            return{
                "success": True
            }
        else: 
            return{
                "success": False,
                "error": f"Ban ko co quyen chinh sua"
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
            
    