from __future__ import annotations

from pathlib import Path
import sys

from loguru import logger


def configure_logging(log_dir: str = "./logs") -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO", enqueue=False, backtrace=False, diagnose=False)
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    logger.add(log_path / "alfabot.log", rotation="10 MB", retention="7 days", level="INFO", enqueue=True, backtrace=False, diagnose=False)
