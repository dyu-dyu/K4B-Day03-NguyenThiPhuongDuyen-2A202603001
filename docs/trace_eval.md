# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Thị Phương Duyên  
> **Mã Sinh Viên / Mã Học viên:** 2A202603001 
> **Chủ đề Lựa chọn:** Trợ lý Tư vấn Sức khỏe Vinmec: Tra cứu lịch làm việc bác sĩ chuyên khoa và đặt lịch khám bệnh.  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4/ 5 | Bài toán cần thực hiện nhiều bước liên tiếp: (1) hiểu nhu cầu bệnh nhân → (2) xác định chuyên khoa → (3) tra cứu bác sĩ phù hợp → (4) kiểm tra lịch làm việc/lịch trống → (5) đề xuất khung giờ → (6) xác nhận thông tin → (7) đặt lịch. Các bước có quan hệ với nhau chứ không chỉ trả lời một câu hỏi đơn lẻ. |
| **2. Tool Interaction** | 5/ 5 | Đây là điểm mạnh nhất. Agent cần tương tác với database/MCP/API để lấy thông tin bác sĩ, chuyên khoa, lịch làm việc và tình trạng slot. Khi đặt lịch, agent còn cần gọi booking tool/API để tạo lịch khám. Nếu có thêm hồ sơ bệnh nhân, notification/email/SMS thì số lượng tool còn tăng. |
| **3. Dynamic Decision** | 5/ 5 | Bước tiếp theo phụ thuộc trực tiếp vào kết quả trước đó. Ví dụ: nếu người dùng muốn khám tim → tìm khoa Tim mạch → tìm các bác sĩ còn lịch → nếu ngày mong muốn hết slot → đề xuất ngày khác → nếu người dùng không xác nhận → không tiến hành booking. |
| **4. Long Horizon Goal** | 4/ 5 | Mục tiêu cuối cùng là “giúp người dùng hoàn tất một lịch khám phù hợp”, không chỉ cung cấp thông tin. Agent phải duy trì mục tiêu và các thông tin đã thu thập như chuyên khoa, bác sĩ, ngày, giờ, cơ sở, thông tin bệnh nhân qua nhiều bước/lượt hội thoại. Tuy nhiên, nếu workflow chỉ 5–7 bước và ít tương tác kéo dài thì chưa đến mức 5/5. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18/ 20** | *không chỉ cần một chatbot trả lời, mà có đủ đặc điểm để Agent phải tự quyết định bước tiếp theo, gọi Tool và dựa vào kết quả Tool để hoàn thành mục tiêu.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
   {
    "step": 1,
    "query": "Đặt lịch khám sức khỏe cho tôi",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Để hỗ trợ bạn đặt lịch khám sức khỏe tại Vinmec, bạn vui lòng cung cấp thêm các thông tin sau:\n\n1. **Mã bệnh nhân / Mã sinh viên** của bạn.\n2. **Tên bác sĩ** hoặc **Chuyên khoa** bạn muốn khám (ví dụ: Tim mạch, Nội tiết, Nhi khoa, Khám tổng quát...).\n3. **Thời gian mong muốn** (Ngày và giờ khám, ví dụ: 20/09/2026 lúc 09:00).\n\nNgay khi nhận được thông tin, tôi sẽ kiểm tra lịch khám và tiến hành đặt lịch cho bạn!",
    "latency_ms": 4386.55
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [+] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5/ 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [+] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
