from config.Gmail import send_email
from model.user import get_email_by_user_id

def send_email_late_task(subject, id_user, body):
    """
    Gửi email thông báo trễ hạn nộp bài tập.
    """
    # email = get_email_by_user_id(id_user)
    recipients = "quctonnn@gmail.com"
    if recipients:
        try:
            html = f"""
            <html>
                <body>
                    <h3 style="color:red;">📢 THÔNG BÁO</h3>
                    <p>{body}</p>
                </body>
            </html>
            """
            send_email(subject, [recipients], body, html)
            print(f" Email sent to {recipients} with subject '{subject}'")
        except Exception as e:
            print(f" Failed to send email to {recipients}: {e}")
    else:
        print(f" No email found for user ID {id_user}")
