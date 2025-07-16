from flask import request, session
from flask_socketio import emit, join_room
from model.redisModel import get_his_mes, chat_room_exists
from socketio_instance import socketio

# Handler: Client yêu cầu lịch sử tin nhắn
@socketio.on('db_message')
def get_message(data):
    """
    Lấy lịch sử tin nhắn từ database, chuyển đổi định dạng
    và gửi lại cho client yêu cầu.
    """
    team_id = data.get('team_id')
    
    message_history = get_his_mes(team_id)
    
    formatted_messages = [
        {'sender': msg['user_name'], 'message': msg['message']}
        for msg in message_history
    ]
    
    emit('chat_history', {'messages': formatted_messages}, to=request.sid)

# Handler: Client yêu cầu tham gia phòng chat
@socketio.on('join')
def handle_join(data):
    """
    Xử lý việc user tham gia vào một phòng chat cụ thể.
    """
    team_id = data.get('team_id')
    if team_id:
        room_name = f"room_{team_id}"
        join_room(room_name)
        print(f"[SOCKET] User {request.sid} joined {room_name}")
        emit('joined_room', {'room': team_id}, to=request.sid)

# Handler: Client gửi tin nhắn mới
@socketio.on('chat_message')
def handle_chat_message(data):
    """
    """
    team_id = data.get('team_id')
    message = data.get('message')
    
    # Lấy thông tin user từ session để đảm bảo an toàn
    user_id = session.get('user_id')
    user_name = session.get('user_name')

    if not all([team_id, message, user_id, user_name]):
        # Bỏ qua nếu thiếu thông tin cần thiết
        return

    # Lưu tin nhắn vào database
    chat_room_exists(team_id, user_id, user_name, message)
    
    # Gửi tin nhắn tới tất cả client trong phòng
    room_name = f"room_{team_id}"
    payload = {'sender': user_name, 'message': message}
    emit('receive_message', payload, to=room_name)
