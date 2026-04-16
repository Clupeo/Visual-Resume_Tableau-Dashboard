"""
logging_util.py
===============

Logging configuration and utilities for the ETL pipeline.

Provides structured logging with:
- File and console output
- Configurable log levels
- Formatted messages for clarity
- Audit trail for debugging
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configure logging for the pipeline.
    
    Args:
        log_level: logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Configures:
    - Console output with colored formatting
    - File output to pipeline.log
    - Structured format with timestamps and levels
    """
    
    # Create logs directory if needed
    log_dir = Path(__file__).parent.parent
    log_file = log_dir / "pipeline.log"
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Formatter with timestamp and level
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Log startup message
    logger.info(f"Logging configured (level: {logging.getLevelName(log_level)})")
    logger.info(f"Log file: {log_file}")
"""
Logging Utility for Visual Resume Dashboard
===========================================

Centralized logging configuration for all modules.
Provides consistent formatting and output handling.
"""

import logging
from pathlib import Path
from datetime import datetime


def configure_logging(
    log_level: int = logging.INFO,
    log_file: str = "pipeline.log"
) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (logging.DEBUG, INFO, etc.)
        log_file: Optional log file path
    """
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(__file__).parent.parent / log_file
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


if __name__ == "__main__":
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
