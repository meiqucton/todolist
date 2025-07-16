from flask import session
import math
import uuid
from datetime import datetime
from model.task import create_task, get_list_task, update_status,count_task_by_status
from model.member import check_role

def task_to_dict(task):
    return {
        "task_id": task.task_id,
        "user_id": task.user_id,
        "team_id": task.team_id,
        "task_title": task.task_title,
        "task_description": task.task_description,
        "start_date": task.start_date.strftime("%Y-%m-%d %H:%M:%S") if task.start_date else None,
        "end_date": task.end_date.strftime("%Y-%m-%d %H:%M:%S") if task.end_date else None,
        "status_task": task.status_task,
        "point_task": task.point_task
    }
def create_task_function(user_id, team_id, task_title, task_description, start_date, end_date, status_task=None):
        try:
            print(f"[DEBUG] user_id={user_id}, team_id={team_id}, title={task_title}, desc={task_description}, start={start_date}, end={end_date}, status={status_task}")
      
                
            if not task_title or not start_date or not end_date:
                return {"success": False, "error": "Missing title or start/end date."}
    
    
            if start_date > end_date:
                return {"success": False, "error": "End date cannot be earlier than start date"}
    
            status_task = "unfinished"
    
            total_minutes = int((end_date - start_date).total_seconds() / 60)
            point_task = max(1, total_minutes // 30)
    
            new_task = create_task(
                user_id=user_id,
                team_id=team_id,
                task_title=task_title,
                task_description=task_description,
                start_date=start_date,
                end_date=end_date,
                status_task=status_task,
                point_task=point_task
            )
    
            if new_task.get("success"):
                return {"success": True}
            else:
                return {"success": False, "error": new_task.get("error", "Không rõ lỗi")}
    
        except Exception as e:
            print(f"[Error] create_task_function: {e}")
            return {"success": False, "error": str(e)}
def get_task_function(user_id, team_id):   
    result = get_list_task(user_id=user_id, team_id=team_id)
    
    if result:
        return {
            "success": True,
            "data": [task_to_dict(task) for task in result]
        }
    else:
        return {
            "success": False,
            "message": "No tasks found"
        }

def update_Status_task_function(task_id, user_id, team_id):
    result = update_status(task_id, user_id, team_id)
    
    if result.get("success"):
        return {
            "success": True,
            "task": result["task"],
        }
    else:
        return {
            "success": False,
            "message": result.get("message", "Không rõ lỗi")
        }

def get_task_status_summary(user_id=None, team_id=None):
    try:
        stats = count_task_by_status(user_id=user_id, team_id=team_id)

        finished = stats.get("finished", 0)
        unfinished = stats.get("unfinished", 0)

        return {
            "success": True,
            "finished": finished,
            "unfinished": unfinished
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
def get_task_status_summary(user_id=None, team_id=None):
    try:
        stats = count_task_by_status(user_id=user_id, team_id=team_id)

        finished = stats.get("finished", 0)
        unfinished = stats.get("unfinished", 0)

        return {
            "success": True,
            "finished": finished,
            "unfinished": unfinished
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }