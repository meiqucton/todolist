from config.corehere import getAPI_AI

def get_db_for_AI(db_json):
    request_json = f"""🎯 Hãy phân tích và đưa ra kết luận những yêu cầu sau(ghi HTML làm đẹp lồng lộn lên)):

1️⃣ **✅ Tổng số task chưa hoàn thành**  
2️⃣ **📅 Tổng số task theo từng ngày bắt đầu (`start_date`)**  
3️⃣ **🗓️ Số lượng và tổng điểm task theo từng ngày kết thúc (`end_date`)**  
4️⃣ **⏰ Các task quá hạn tính đến thời điểm hiện tại**  
5️⃣ **🚨 Gợi ý các task nên xử lý trước** (dựa vào deadline gần và point_task cao)  
 =>> Đánh giá: 
🔍 Dữ liệu JSON cần phân tích và đánh giá tiến độ:  
(Dùng Tiếng Việt)  
{db_json}
"""
    try:
        co = getAPI_AI()
        response = co.chat(
            model="command-r",
            message=request_json
        )
        print(response)
        return response
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gọi API Chat: {e}")
        return None
