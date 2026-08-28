import os
import sys
import logging
from datetime import datetime
from flask import Request
from typing import Any

# Códigos de Cores ANSI
class LogColors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

class ColoredFormatter(logging.Formatter):
    """Formatador customizado para colorizar logs no console de acordo com o nível."""
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.CYAN,
        logging.INFO: LogColors.BLUE,
        logging.WARNING: LogColors.YELLOW,
        logging.ERROR: LogColors.RED,
        logging.CRITICAL: LogColors.RED + LogColors.BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, LogColors.RESET)
        level_name = f"[{record.levelname}]"
        record.levelname = f"{color}{LogColors.BOLD}{level_name:<9}{LogColors.RESET}"
        
        # Colorir mensagens de inicialização delimitadas por "::"
        message = record.getMessage()
        if message.startswith("::") and message.endswith("::"):
            message = f"{LogColors.CYAN}{message}{LogColors.RESET}"
        record.msg = message
        
        return super().format(record)


class Logger:
    """Gerenciador central de logs unificados para o Bonfire implementado como Singleton."""
    _instance = None
    _initialized = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.bonfire_log_path = "log"
        
        # Setup do console logger nativo
        self._console_logger = logging.getLogger("bonfire_console")
        self._console_logger.setLevel(logging.DEBUG)
        
        # Evita handlers duplicados ao reinicializar
        if not self._console_logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            # Formato: [NÍVEL] MENSAGEM
            formatter = ColoredFormatter("%(levelname)s %(message)s")
            handler.setFormatter(formatter)
            self._console_logger.addHandler(handler)
        self._initialized = True

    def info(self, msg: str) -> None:
        self._console_logger.info(msg)

    def warn(self, msg: str | Exception) -> None:
        self._console_logger.warning(str(msg))

    def error(self, msg: str | Exception) -> None:
        self._console_logger.error(str(msg))

    def write_to_file(self, message: str | Exception, file_type: str) -> None:
        """Grava os logs formatados em disco mantendo o padrão de nomenclatura por data."""
        try:
            os.makedirs(self.bonfire_log_path, exist_ok=True)
            date_str = datetime.now().strftime("%d-%m-%Y")
            file_path = f"{self.bonfire_log_path}/bonfire-{file_type}-{date_str}.log"
            time_str = datetime.now().strftime("%H:%M:%S")
            
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{time_str} - {message}\n")
        except Exception as e:
            # Fallback para o console se a gravação em disco falhar
            self._console_logger.warning(f"Erro ao salvar arquivo de log '{file_type}': {e}")

    def systemLog(self, msg: str | Exception) -> None:
        self.write_to_file(msg, "system")

    def httpLog(self, msg: str | Exception) -> None:
        self.write_to_file(msg, "http")


class HttpLogger(Logger):
    """Logger especializado em requisições HTTP implementado como Singleton."""
    _instance = None
    _initialized = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "HttpLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def request(self, request: Request, status_code: int) -> None:
        ip = request.remote_addr or "unknown"
        method = request.method
        path = request.path

        # Cor semântica baseada no método HTTP
        method_color = LogColors.GREEN if method in ("GET", "HEAD") else LogColors.BLUE
        if method in ("POST", "PUT", "PATCH"):
            method_color = LogColors.MAGENTA
        elif method == "DELETE":
            method_color = LogColors.RED

        # Cor semântica baseada no status HTTP
        status_color = LogColors.GREEN
        if 300 <= status_code < 400:
            status_color = LogColors.BLUE
        elif 400 <= status_code < 500:
            status_color = LogColors.YELLOW
        elif status_code >= 500:
            status_color = LogColors.RED

        # Formatação visual para console
        colored_method = f"{method_color}{LogColors.BOLD}[{method}]{LogColors.RESET}"
        colored_path = f"{LogColors.CYAN}{path}{LogColors.RESET}"
        colored_status = f"{status_color}{LogColors.BOLD}{status_code}{LogColors.RESET}"
        colored_ip = f"{LogColors.WHITE}{ip}{LogColors.RESET}"

        log_msg = f"{colored_method} request to {colored_path} status {colored_status} from {colored_ip}"
        self._console_logger.info(log_msg)

        # Log em texto plano para persistência
        self.httpLog(f"[{method}] request to {path} status {status_code} from {ip}")


logger = Logger()
http_logger = HttpLogger()
