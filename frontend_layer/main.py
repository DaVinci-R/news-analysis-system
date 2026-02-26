import sys
import os
from streamlit.web import cli as stcli
from .config import WEB_HOST, WEB_PORT

def run():
    """
    启动 Streamlit 前端服务
    """
    # 获取 app.py 的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")
    
    print(f"正在启动前端界面: http://{WEB_HOST}:{WEB_PORT}")
    
    # 构造 streamlit 运行参数
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.address", WEB_HOST,
        "--server.port", str(WEB_PORT),
        "--server.headless", "true" # 生产环境建议 true，避免自动打开浏览器
    ]
    
    sys.exit(stcli.main())

if __name__ == "__main__":
    run()
