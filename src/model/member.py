from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,and_, or_, update
from sqlalchemy.orm import relationship,joinedload

from datetime import datetime
from config.database import db
# from model.team import Team
from model.user import get_user_by_id

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
        check_member = check_user_in_team(user_id, team_id)
        if check_member['success']:
            return {
                "success": False,
                "error": "Bạn đã là thành viên của nhóm này rồi"
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
    check_member = Membership.query.filter_by(user_id=user_id, team_id=team_id).first()
    
    if not check_member:
        return {
            "success": False,
            "error": "Bạn không phải thành viên trong nhóm này."
        }

    role = check_member.role_user.lower()

    if role == 'leader':
        return {"success": True, "role": "Leader"}
    elif role == 'member':
        return {"success": True, "role": "Member"}
    else:
        return {
            "success": False,
            "error": "Bạn không có quyền truy cập."
        }

            
def check_user_in_team(user_id, team_id):
    try:
        membership = Membership.query.filter(
            and_(
                Membership.user_id == user_id,
                Membership.team_id == team_id
            )
        ).first()
        if membership:
            return {
                "success": True,
                "message": "Bạn đã tham gia vào nhóm này",
            }
        else:
            return {
                "success": False,
                "message": "Bạn Không có quyền hạn truy cập vào nhóm này"
            }
    except Exception as e:
        db.session.rollback()
        print("!!!!!!!!!!!!!!! LỖI KHI KIỂM TRA THÀNH VIÊN !!!!!!!!!!!!!!!")
        import traceback
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return {
            "success": False,
            "error_detail": str(e)
        }
def get_member(user_id):
    check_membe = Membership.query.filter_by(user_id = user_id).all()
    return check_membe

def get_member_team(team_id):
    """
    Retrieves a structured list of members for a given team.
    This version is more efficient as it pre-loads user data to avoid multiple queries.
    """
    try:
        # Use joinedload to fetch members and their related user data in a single, efficient query.
        # This prevents the "N+1 query problem" from calling the database in a loop.
        memberships = Membership.query.options(
            joinedload(Membership.user)
        ).filter_by(team_id=team_id).all()

        members_list = []
        for member in memberships:
            # Check that the related user exists to prevent errors
            if member.user:
                # Create a dictionary with the correct syntax: "key": value
                member_data = {
                    "user_id": member.user_id,
                    "user_name": member.user.user_name, # Assumes your User model has a 'user_name' field
                    "role": member.role_user,
                    "team_id": member.team_id
                }
                members_list.append(member_data)

        return members_list

    except Exception as e:
        print(f"An error occurred while fetching team members: {e}")
        return []
