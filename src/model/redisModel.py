from datetime import datetime
import json
from flask_socketio import emit, join_room
from socketio_instance import socketio
from config.redis_config import (redis_config_)
from model.member import (
    check_user_in_team
)
# from config.redis_config import redis_config_connect
redis = redis_config_()

def create_room_chat(team_id, team_name):
    try: 
        groupKey = f"group:{team_id}:info"
        result = redis.hset(groupKey, mapping={
             "name": team_name,
            "created_at": datetime.now().isoformat()
        })
        return result 

    except Exception as e:
        print("Error creating room task:", str(e))
        return None

def join_room_chat(room_id, user_id, user_name):
    try:    
        members_key = f"group:{room_id}:members"
        member_data = json.dumps({
            "user_id": user_id,
            "user_name": user_name,
            "joined_at": datetime.now().isoformat()
        })
        print("member_data", member_data)
        redis.sadd(members_key, member_data)
        return {
            "success": True,
            "message": "Tham gia phòng chat thành công",
        }
    except Exception as e:
        print("Error joining room:", str(e))
        return None
def chat_room_exists(room_id, user_id , user_name, message):
    try:
        check_user_of_team = check_user_in_team(user_id=user_id, team_id=room_id)
        if isinstance(check_user_of_team, dict) and not check_user_of_team.get("success", False):
            return check_user_of_team 

        chat_of_user = {
            "user_id": user_id,
            "user_name": user_name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        socketio.emit("message", chat_of_user, to=f"room_{room_id}")

        redis.rpush(f"group:{room_id}:messages", json.dumps(chat_of_user))

        return {
            "success": True,
        }
    except Exception as e:
        print("Error checking chat room existence:", str(e))
        return False

def get_his_mes(room_id):
    """Retrieves the message history for a specific room from Redis."""
    try:
        messages_key = f"group:{room_id}:messages"
        messages_json = redis.lrange(messages_key, 0, -1)
        print("Sample type:", type(messages_json[0]) if messages_json else None)

        if isinstance(messages_json[0], bytes):
            messages = [json.loads(msg.decode('utf-8')) for msg in messages_json]
        else:
            messages = [json.loads(msg) for msg in messages_json]
        return messages
    except Exception as e:
        print(f"Error getting room messages: {e}")
        return None
