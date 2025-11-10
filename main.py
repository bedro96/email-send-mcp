import datetime
import os
import sys
import dotenv
import logging
from src.server import create_server
from src.config import get_settings

# ===== 로깅 설정 =====
def setup_logging():
    """Azure Container Apps용 로깅 설정"""
    # 로그 레벨 설정 (환경변수로 제어 가능)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # 기존 로거 제거
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # 포맷터 설정 (JSON 형태로 구조화된 로그)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # 콘솔 핸들러 (Azure Container Apps는 stdout을 수집)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 로그 디렉토리 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 파일 핸들러 설정 (flask_app_log_yyyymmdd.log 형식으로 날짜별 로그 파일 생성)
    log_filename = os.path.join(log_dir, f"email-send-mcp_{datetime.datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_filename,
        when='midnight',
        interval=1,
        backupCount=0,
        encoding='utf-8'
    )
    file_handler.suffix = "%Y%m%d"
    file_handler.setFormatter(formatter)

    # 루트 로거 설정
    logging.root.setLevel(getattr(logging, log_level))
    logging.root.addHandler(console_handler)
    logging.root.addHandler(file_handler)

    return logging.getLogger("email-send-mcp")

# Load environment variables from .env file
dotenv.load_dotenv()
# Create the server instance at the global scope
server = create_server()
# Initialize logger
logger = setup_logging()
# Set configuration values from environment variables
def set_values_from_env(settings):
    """Set configuration values from environment variables."""
    env_vars = {
        "SMTP_SERVER": os.getenv("SMTP_SERVER"),
        "SMTP_PORT": os.getenv("SMTP_PORT"),
        "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        "IMAP_SERVER": os.getenv("IMAP_SERVER"),
        "IMAP_PORT": os.getenv("IMAP_PORT"),
        "IMAP_USERNAME": os.getenv("IMAP_USERNAME"),
        "IMAP_PASSWORD": os.getenv("IMAP_PASSWORD"),
        "DEFAULT_FROM_EMAIL": os.getenv("DEFAULT_FROM_EMAIL"),
    }
    for key, value in env_vars.items():
        if value is not None:
            field_type = type(getattr(settings, key))
            try:
                if field_type is bool:
                    casted_value = value.lower() in ("true", "1", "yes")
                else:
                    casted_value = field_type(value)
                setattr(settings, key, casted_value)
            except ValueError as e:
                print(f"Invalid value for {key}: {value}. Error: {str(e)}", file=sys.stderr)

def main():
    """Main entry point for the MCP server."""
    try:
        settings = get_settings()
        logger.info("Starting Email Send/Receive MCP Server...")
        set_values_from_env(settings)
        logger.info("Configuration values set from environment variables.")
        
        # Verify SMTP credentials are configured
        if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            logger.error("SMTP credentials not configured. Email will not work.")
            print("Warning: SMTP credentials not configured. Email sending may not work.", file=sys.stderr)
        
        # Run the FastMCP server (handles asyncio internally)
        server.run(transport="http", host="0.0.0.0", port=8888, path="/mcp")
            
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"Failed to start server: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
