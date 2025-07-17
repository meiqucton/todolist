from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,and_, or_, update
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
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
    def to_dict(self):
        """Chuyển đổi đối tượng Task thành một dictionary."""
        return {
            'task_id': self.task_id,
            'user_id': self.user_id,
            'team_id': self.team_id,
            'task_title': self.task_title,
            'task_description': self.task_description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status_task': self.status_task,
            'point_task': self.point_task
        }
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
        if team_id is None: 
            task = Task.query.filter(
                Task.task_id == task_id,
                Task.user_id == user_id,
                Task.team_id.is_(None)
            ).first()
        else:
            task = Task.query.filter(
                Task.task_id == task_id,
                Task.team_id == team_id
            ).first()

        if not task:
            return {"success": False, "message": "Task không tồn tại hoặc bạn không có quyền truy cập."}
        
        target_object = None
        if team_id is None:
            target_object = get_user_by_id(user_id)
            if not target_object:
                return {"success": False, "message": "Không tìm thấy user."}
        else:
            
      
            target_object = get_team_by_id(team_id)
            if not target_object:
                return {"success": False, "message": "Không tìm thấy team."}
       
        task_points = task.point_task or 0
        current_total_points = target_object.total_point or 0

        if task.status_task == "unfinished":
            task.status_task = "finished"
            target_object.total_point = current_total_points + task_points
        
        elif task.status_task == "finished":
            task.status_task = "unfinished"
            target_object.total_point = max(current_total_points - task_points, 0)
        
        else:
            return {"success": False, "message": f"Trạng thái task không hợp lệ: '{task.status_task}'."}

        db.session.commit()

        return {
            "success": True,
            "message": "Cập nhật trạng thái thành công.",
            "task": {
                "task_title": task.task_title,
                "status_task": task.status_task,
                "point_task": task.point_task,
                "updated_total_point": target_object.total_point
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

# Bạn cần tự định nghĩa hàm này dựa trên model của mình
# def is_user_in_team(user_id, team_id):
#     # ... logic để kiểm tra xem user có tồn tại trong team không ...
#     return True or False
def count_task_by_status(user_id=None, team_id=None):
    query = db.session.query(
        Task.status_task,
        db.func.count(Task.task_id).label("count")
    )

    if user_id:
        query = query.filter(Task.user_id == user_id,  Task.team_id.is_(None))
    if team_id:
        query = query.filter(Task.team_id == team_id)

    query = query.group_by(Task.status_task)

    results = query.all()

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
def getreport(team_id, days_filter= None):
    """
    Lấy danh sách công việc cho một team.
    
    - Bắt buộc phải có `team_id`.
    - Nếu `days_filter` là một con số, chỉ lấy các task có ngày bắt đầu 
      trong khoảng `days_filter` ngày trở lại đây.
    """
    if team_id is None:
        return []

    conditions = [Task.team_id == team_id]

    if isinstance(days_filter, int) and days_filter > 0:
        filter_date = datetime.utcnow() - timedelta(days=days_filter)
        conditions.append(Task.start_date >= filter_date)

    query = Task.query.filter(and_(*conditions))
    
    return query.order_by(Task.start_date.desc()).all()
def delete_task(task_id):
    """
    Xóa một task và trừ điểm tương ứng khỏi total_point của user hoặc team
    nếu task đó đã ở trạng thái 'finished'.
    """
    try:
        task = Task.query.filter_by(task_id=task_id).first()

        if not task:
            return {"success": False, "message": "Task không tồn tại hoặc bạn không có quyền"}

        if task.status_task == 'finished':
            target_object = None
            task_points_to_deduct = task.point_task or 0

            if task.team_id:
                target_object = get_team_by_id(task.team_id)
            elif task.user_id:
                if task.team_id is None:
                    target_object = get_user_by_id(task.user_id)

            if target_object:
                current_total_points = target_object.total_point or 0
                target_object.total_point = max(current_total_points - task_points_to_deduct, 0)
                db.session.add(target_object)

        db.session.delete(task)

        db.session.commit()

        return {"success": True, "message": "Xóa task thành công."}

    except Exception as e:
        db.session.rollback() 
        import traceback
        traceback.print_exc()
        return {
            "success": False, 
            "message": "Lỗi hệ thống khi xóa task.",
            "error_detail": str(e)
        }
def update_task(task_id, **kwargs):
    """
    Cập nhật các trường của một task dựa trên task_id.
    
    !!! CẢNH BÁO: Hàm này KHÔNG tự kiểm tra quyền truy cập.
    Luôn kiểm tra quyền của người dùng ở tầng Controller TRƯỚC KHI gọi hàm này.
    """
    try:
        task = Task.query.get(task_id) 
        if not task:
            return {
                "success": False, 
                "message": "Task không tồn tại."
            }

        for key, value in kwargs.items():  
            if hasattr(task, key):
                setattr(task, key, value)
        
        db.session.commit()
        return {
            "success": True,
            "message": "Cập nhật task thành công.",
            "task": task.to_dict() 
        }
        
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": "Lỗi hệ thống khi cập nhật task.",
            "error_detail": str(e)
        }