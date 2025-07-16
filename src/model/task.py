from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,and_, or_, update
from sqlalchemy.orm import relationship

from datetime import datetime
from config.database import db


from model.user import get_user_by_id
from model.team import get_team_by_id
class Task(db.Model):
    __tablename__ = 'Task'  
    
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User_table.user_id'), nullable=True)
    team_id = Column(Integer, ForeignKey('Team.team_id'), nullable=True)
    task_title = Column(String(255), nullable=False)
    task_description = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status_task = Column(String(50), nullable=False)
    point_task = Column(Integer, nullable=False, default=0)
    
    user = relationship("Users", backref="tasks")
    team = relationship("Team", backref="tasks")
def create_task(user_id, team_id, task_title, task_description, start_date, end_date, status_task, point_task):
    try:
        new_task = Task(
            user_id=user_id,
            team_id=team_id,
            task_title=task_title,
            task_description=task_description,
            start_date=start_date,
            end_date=end_date,
            status_task=status_task,
            point_task=point_task
        )
        db.session.add(new_task)
        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": "SQLAlchemy commit error",
            "error_detail": traceback.format_exc()
        }
def get_list_task(user_id, team_id):

    if team_id is not None:
        query = Task.query.filter(
            and_(       #and là dùng để thêm đk
                Task.team_id == team_id
            )
        )
    else:
        query = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.team_id == None 
            )
        )
        
    return query.all()
def update_status(task_id, user_id, team_id):
    try:
        # Tìm task theo id, user, team
        if team_id is None: 
            task = Task.query.filter(
                Task.task_id == task_id,
                Task.user_id == user_id,
                Task.team_id.is_(None)
            ).first()
        else:
            task = Task.query.filter(
                and_(
                    Task.task_id == task_id,
                    Task.team_id == team_id
                )
            ).first()

        if not task:
            return {"success": False, "message": "Task không tồn tại hoặc không thuộc về user."}
        
        if task.team_id is None: 
            user = get_user_by_id(user_id)
            if not user:
                return {"success": False, "message": "Không tìm thấy user."}
            print(user)
        else:
            team = get_team_by_id(team_id)
            
            if not team:
                return {"success": False, "message": "Không tìm thấy team."}
            print("innnn",team)
            old_total = team.total_point
       
        if task.status_task == "unfinished":
            task.status_task = "finished"
            if task.team_id is None:  # Chỉ cộng điểm nếu task không thuộc team
                user.total_point = (user.total_point or 0) + (task.point_task or 0)
            elif task.team_id is not None:  # Nếu task thuộc team, không cộng điểm cho user
                team.total_point =  (old_total or 0) + (old_total or 0)       
        elif task.status_task == "finished":
            task.status_task = "unfinished"
            if task.team_id is None:  # Chỉ trừ điểm nếu task không thuộc team
                user.total_point = max((user.total_point or 0) - (task.point_task or 0), 0)
            elif task.team_id is not None:  # Nếu task thuộc team, không trừ điểm cho user
                team.total_point = max((old_total or 0) - (old_total or 0), 0)
        else:
            return {"success": False, "message": "Trạng thái task không hợp lệ. Chỉ chấp nhận 'unfinished' hoặc 'finished'."}

        db.session.commit()

        return {
            "success": True,
            "message": "Cập nhật trạng thái thành công.",
            "task": {
                "task_title": task.task_title,
                "status_task": task.status_task,
                "point_task": task.point_task
            },
        }
    except Exception as e:
                db.session.rollback()
                
                print("!!!!!!!!!!!!!!! ĐÃ CÓ LỖI XẢY RA !!!!!!!!!!!!!!!")
                import traceback
                traceback.print_exc() 
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

                return {
                    "success": False,
                    "message": "Lỗi hệ thống khi cập nhật trạng thái task.",
                    "error_detail": str(e)  
                }
                
def count_task_by_status(user_id=None, team_id=None):
    query = db.session.query(
        Task.status_task,
        db.func.count(Task.task_id).label("count")
    )

    if user_id:
        query = query.filter(Task.user_id == user_id)
    if team_id:
        query = query.filter(Task.team_id == team_id)

    query = query.group_by(Task.status_task)

    results = query.all()

    # Chuyển thành dict: {'finished': 5, 'unfinished': 2, ...}
    return {status: count for status, count in results}

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