"""
Logging Utility
---------------
Provides a production-grade logging setup with both console and rotating
file handlers. Supports structured formatting for easy log aggregation.

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Processing started")
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from config.settings import Config


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance with console and file handlers.

    The logger writes to both stdout (console) and a rotating log file
    at ``{Config.LOG_DIR}/app.log``. Each handler uses a structured
    format including timestamp, level, module name, and message.

    Args:
        name: The logger name, typically ``__name__`` of the calling module.

    Returns:
        logging.Logger: A fully configured logger instance.
    """
    logger = logging.getLogger(name)

    # Only configure if handlers haven't been set (prevent duplicates)
    if not logger.handlers:
        logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))

        # ── Formatter ─────────────────────────────────────────────
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # ── Console Handler ──────────────────────────────────────
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # ── Rotating File Handler ────────────────────────────────
        try:
            log_dir = Config.LOG_DIR
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "app.log")

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB per file
                backupCount=5,              # Keep 5 backup files
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)  # File captures all levels
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, PermissionError) as exc:
            logger.warning(f"Could not create file log handler: {exc}")

    return logger


def log_agent_step(logger: logging.Logger, agent_name: str, action: str, details: str = "") -> None:
    """
    Log a structured agent pipeline step for easy tracing.

    Args:
        logger: The logger instance to write to.
        agent_name: Name of the agent (e.g., "PlannerAgent").
        action: Action being performed (e.g., "STARTED", "COMPLETED").
        details: Optional extra context.
    """
    msg = f"[{agent_name}] {action}"
    if details:
        msg += f" | {details}"
    logger.info(msg)
