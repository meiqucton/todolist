
import uuid
from datetime import datetime
from model.team import create_team_and_add_leader
from model.task import create_task
from model.member import check_role, join_team
from model.redisModel import create_room_chat, join_room_chat

def create_team_function(user_id, team_name, user_name):
    if not team_name:
        return {"success": False, "error": "Team name is required"}

    team_result = None
    room_result = None

    try:
    
        team_result = create_team_and_add_leader(
            user_id=user_id,
            team_name=team_name,
            role_user='Leader',
            total_point=0
        )
        if not team_result or not team_result.get('team_id'):
            raise Exception("Failed to create team in database.")

        team_id = team_result['team_id']

        room_result = create_room_chat(
            team_id=team_id,
            team_name=team_name
        )
        join_result = join_room_chat(
            room_id=team_id,
            user_id=user_id,
            user_name =user_name
        )
        if not room_result or not room_result.get('success'):
            raise Exception("Failed to create chat room.")

      
        if not join_result or not join_result.get('success'):
             raise Exception("Failed to join chat room.")

        return {
            "success": True,
            "team_id": team_id,
            "team_name": team_name,
            "message": "Team created successfully"
        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")

        if team_result and team_result.get('team_id'):
            print(f"Rolling back: Deleting team {team_result['team_id']}")
        
        if room_result and room_result.get('room_id'):
            print(f"Rolling back: Deleting chat room {room_result['room_id']}")


        return {"success": False, "error": f"Could not create team. Reason: {str(e)}"}

