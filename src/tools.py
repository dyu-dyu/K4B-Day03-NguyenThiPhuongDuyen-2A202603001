"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "doctor_schedule_query",
        "description": "Tra cứu lịch làm việc và các khung giờ khám của bác sĩ tại Vinmec.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_name": {
                    "type": "string",
                    "description": "Tên bác sĩ cần tra cứu."
                },
                "specialty": {
                    "type": "string",
                    "description": "Chuyên khoa của bác sĩ, ví dụ: Tim mạch, Nội tiết, Nhi khoa."
                },
                "date": {
                    "type": "string",
                    "description": "Ngày muốn tra cứu lịch khám, ví dụ: '20/09/2026'."
                }
            },
            "required": ["doctor_name"]
        }
    },
    
    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch khám bệnh tại Vinmec với bác sĩ theo thời gian được yêu cầu.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_id": {
                    "type": "string",
                    "description": "Mã bệnh nhân cần đặt lịch khám."
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Ngày và giờ muốn đặt lịch khám, ví dụ: '2026-09-20 09:00'."
                },
                "doctor_name": {
                    "type": "string",
                    "description": "Tên bác sĩ muốn đặt lịch khám."
                }
            },
            "required": ["patient_id", "datetime_str", "doctor_name"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "BS001": {
        "doctor_name": "Phạm Văn Khoa",
        "specialty": "Tim mạch",
        "hospital": "Vinmec Times City",
        "working_schedule": {
            "20/09/2026": [
                "08:00",
                "09:00",
                "10:00",
                "14:00"
            ],
            "21/09/2026": [
                "08:00",
                "09:00",
                "14:00",
                "15:00"
            ]
        }
    },

    "BS002": {
        "doctor_name": "Trần Thị Bình",
        "specialty": "Nội tiết",
        "hospital": "Vinmec Times City",
        "working_schedule": {
            "20/09/2026": [
                "08:30",
                "10:00",
                "14:00",
                "15:30"
            ],
            "21/09/2026": [
                "09:00",
                "10:30",
                "14:30"
            ]
        }
    },

    "BS003": {
        "doctor_name": "Huỳnh Thế Thiện",
        "specialty": "Nhi khoa",
        "hospital": "Vinmec Central Park",
        "working_schedule": {
            "20/09/2026": [
                "08:00",
                "09:30",
                "14:00",
                "15:00"
            ]
        }
    }
}

# ==============================================================================
# 3. TOOL 1 - TRA CỨU LỊCH KHÁM BỆNH

def execute_doctor_schedule_query(
    doctor_name: str,
    specialty: str = None,
    date: str = None
) -> str:
    """
    Tra cứu thông tin và lịch làm việc của bác sĩ.
    """

    doctor_name = doctor_name.strip().lower()

    found_doctor = None

    for doctor in MOCK_DATABASE.values():
        if doctor["doctor_name"].lower() == doctor_name:
            found_doctor = doctor
            break

    # Không tìm thấy bác sĩ
    if not found_doctor:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy thông tin bác sĩ '{doctor_name}'."
        }, ensure_ascii=False)

    # Kiểm tra chuyên khoa nếu người dùng cung cấp
    if specialty:
        if found_doctor["specialty"].lower() != specialty.strip().lower():
            return json.dumps({
                "status": "NOT_FOUND",
                "message": (
                    f"Bác sĩ {found_doctor['doctor_name']} "
                    f"không thuộc chuyên khoa {specialty}."
                )
            }, ensure_ascii=False)

    # Nếu có ngày cụ thể
    if date:
        available_slots = found_doctor["working_schedule"].get(date, [])

        return json.dumps({
            "status": "SUCCESS",
            "doctor": found_doctor["doctor_name"],
            "specialty": found_doctor["specialty"],
            "hospital": found_doctor["hospital"],
            "date": date,
            "available_slots": available_slots
        }, ensure_ascii=False)

    # Nếu không có ngày cụ thể → trả toàn bộ lịch
    return json.dumps({
        "status": "SUCCESS",
        "doctor": found_doctor["doctor_name"],
        "specialty": found_doctor["specialty"],
        "hospital": found_doctor["hospital"],
        "working_schedule": found_doctor["working_schedule"]
    }, ensure_ascii=False)

# 4. TOOL 2 - ĐẶT LỊCH KHÁM

def execute_schedule_appointment(
    patient_id: str,
    datetime_str: str,
    doctor_name: str
) -> str:
    """
    Thực thi đặt lịch khám bệnh.
    """

    # Tách ngày và giờ từ chuỗi
    parts = datetime_str.strip().split()

    if len(parts) != 2:
        return json.dumps({
            "status": "INVALID_DATETIME",
            "message": (
                "Thời gian không đúng định dạng. "
                "Vui lòng sử dụng dạng '09:00 20/09/2026'."
            )
        }, ensure_ascii=False)

    time_str = parts[0]
    date_str = parts[1]

    # Tìm bác sĩ
    doctor = None

    for item in MOCK_DATABASE.values():
        if item["doctor_name"].lower() == doctor_name.strip().lower():
            doctor = item
            break

    # Không tìm thấy bác sĩ
    if not doctor:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy bác sĩ '{doctor_name}'."
        }, ensure_ascii=False)

    # Kiểm tra ngày có lịch
    available_slots = doctor["working_schedule"].get(date_str, [])

    if not available_slots:
        return json.dumps({
            "status": "NO_AVAILABLE_SLOT",
            "message": (
                f"Bác sĩ {doctor['doctor_name']} "
                f"không có lịch khám vào ngày {date_str}."
            )
        }, ensure_ascii=False)

    # Kiểm tra giờ có trống
    if time_str not in available_slots:
        return json.dumps({
            "status": "SLOT_UNAVAILABLE",
            "message": (
                f"Khung giờ {time_str} ngày {date_str} "
                f"không có trong lịch khám của bác sĩ "
                f"{doctor['doctor_name']}.",
            ),
            "available_slots": available_slots
        }, ensure_ascii=False)

    # Đặt lịch thành công
    booking_id = f"VM-{patient_id}-{date_str.replace('/', '')}-{time_str.replace(':', '')}"

    return json.dumps({
        "status": "SUCCESS",
        "booking_id": booking_id,
        "patient_id": patient_id,
        "doctor": doctor["doctor_name"],
        "specialty": doctor["specialty"],
        "hospital": doctor["hospital"],
        "datetime": datetime_str,
        "message": (
            f"Đặt lịch khám thành công cho bệnh nhân {patient_id} "
            f"với bác sĩ {doctor['doctor_name']} "
            f"vào lúc {datetime_str}."
        )
    }, ensure_ascii=False)




# Router gọi tool thực tế
TOOL_ROUTER = {
    "doctor_schedule_query": execute_doctor_schedule_query,
    "schedule_appointment": execute_schedule_appointment
}


def dispatch_tool_call(
    tool_name: str,
    arguments: Dict[str, Any]
) -> str:
    """
    Hàm trung chuyển thực thi Tool.
    """

    if tool_name in TOOL_ROUTER:

        try:
            return TOOL_ROUTER[tool_name](**arguments)

        except Exception as e:
            return json.dumps({
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }, ensure_ascii=False)

    return json.dumps({
        "status": "UNKNOWN_TOOL",
        "error": f"Tool '{tool_name}' không tồn tại!"
    }, ensure_ascii=False)