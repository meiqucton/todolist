from config.Gmail import send_email
# from model.user import get_email_by_user_id

def send_email_late_task(subject, email, body):
    print("emmmm",email)
    """
    Gửi email thông báo trễ hạn nộp bài tập (có hình).
    """
    email = email
    recipients = email
    if recipients:
        try:
            image_url = "https://i.pinimg.com/736x/1f/3f/4c/1f3f4ce973d946578567f190e2773709.jpg"  # Đổi sang ảnh bạn muốn

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
                        <div style="text-align: center;">
                            <img src="{image_url}" alt="Thông báo" style="max-width: 150px; margin-bottom: 20px;" />
                        </div>
                        <h2 style="color: #e74c3c; margin-top: 0;">📢 THÔNG BÁO</h2>
                        
                        <p style="font-size: 16px; color: #333333; line-height: 1.5; white-space: pre-wrap;">{body}</p>
                        
                        <p style="margin-top: 30px; font-size: 12px; color: #999999;">Đây là email tự động. Vui lòng không phản hồi.</p>
                    </div>
                </body>
            </html>
            """

            send_email(subject, [recipients], body, html)
            print(f"✅ Email sent to {recipients} with subject '{subject}'")
            return {"success": True}
        except Exception as e:
            print(f"❌ Failed to send email to {recipients}: {e}")
            return {"success": False, "error": str(e)}
    else:
        print(f"⚠️ No email found for user ID {email}")
        return {"success": False, "error": "No email found"}
