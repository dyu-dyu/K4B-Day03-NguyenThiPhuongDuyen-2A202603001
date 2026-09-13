"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPVinmecServer:
    """
    Giả lập MCP Server cho Trợ lý Tư vấn Sức khỏe Vinmec.
    Cung cấp các Tool tra cứu lịch bác sĩ và đặt lịch khám.
    """
    def __init__(self, server_name: str = "vinmec-health-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        [TASK 2.1] HỌC VIÊN HOÀN THIỆN HÀM THỰC THI TOOL TRÊN MCP SERVER
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC
        """
        # --------------------------------------------------------------------------
        # TODO 2.1: HỌC VIÊN HOÀN THIỆN HÀM GỌI TOOL CHUẨN MCP JSON-RPC
        # 🎯 YÊU CẦU THỰC THI THUẬT TOÁN:
        # 1. Gọi hàm dispatch_tool_call(tool_name, arguments) để lấy chuỗi JSON kết quả từ Tool Router.
        # 2. Chuyển đổi chuỗi JSON kết quả thành Python Dictionary (dùng json.loads).
        # 3. Đóng gói phản hồi và trả về Dict theo đúng chuẩn giao thức MCP JSON-RPC 2.0:
        #    - Các trường bắt buộc: "jsonrpc": "2.0", "server": self.server_name, "tool": tool_name, "result": content
        # --------------------------------------------------------------------------
        content = dispatch_tool_call(tool_name, arguments)
        content = json.loads(content)
        return {
        "jsonrpc": "2.0",
        "server": self.server_name,
        "tool": tool_name,
        "result": content
        }


if __name__ == "__main__":

    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (vinmec-health-mcp-server)")
    print("==========================================================")

    server = MCPVinmecServer()

    # --------------------------------------------------------------------------
    # Kiểm tra Server
    # --------------------------------------------------------------------------

    tools = server.list_tools()

    print(
        f"✅ Khởi tạo thành công MCP Server: "
        f"{server.server_name} "
        f"(Version: {server.version})"
    )

    print(f"📦 Số lượng Tools công bố: {len(tools)}")

    # --------------------------------------------------------------------------
    # Kiểm tra Tool Schema
    # --------------------------------------------------------------------------

    schedule_tool = next(
        (
            t for t in tools
            if t.get("name") == "schedule_appointment"
        ),
        None
    )

    if (
        schedule_tool
        and not schedule_tool.get("parameters", {}).get("properties")
    ):
        print(
            " Tool 'schedule_appointment' "
            "chưa được định nghĩa properties."
        )
    else:
        print(
            " Tool 'schedule_appointment' "
            "đã có schema đầy đủ."
        )

    # --------------------------------------------------------------------------
    # Kiểm tra Tool Dispatch
    # --------------------------------------------------------------------------

    test_result = server.call_tool(
        "doctor_schedule_query",
        {
            "doctor_name": "Phạm Văn Khoa",
            "specialty": "Tim mạch",
            "date": "20/09/2026"
        }
    )

    if not test_result:

        print(
            "Hàm call_tool() đang trả về rỗng. "
            "Hãy kiểm tra lại Tool Dispatch."
        )

    else:

        print(
            "Test dispatch tool 'doctor_schedule_query' thành công:"
        )

        print(
            f"   Phản hồi JSON-RPC: "
            f"{json.dumps(test_result, ensure_ascii=False)}"
        )