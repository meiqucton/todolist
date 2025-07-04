from model.team import create_team_and_add_leader
from model.task import create_task
from model.member import check_role
from flask import session
import uuid
from datetime import datetime

def create_team_function(team_name, user_id):
    if not team_name :
        return {"success": False, "error": "All fields are required"}
    total_point = 0
    role_user = 'Leader'
    result = create_team_and_add_leader(user_id ,team_name ,role_user ,total_point = total_point)
    return result
