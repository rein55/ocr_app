# utils/logger.py
import logging
from datetime import datetime
from pathlib import Path

def setup_logger(name):
    """Setup logger dengan file dan console handlers"""
    # Buat folder logs jika belum ada
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Cek agar tidak menambahkan handler berulang
    if not logger.handlers:
        # Buat handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_dir / f'{name}_{datetime.now():%Y%m%d}.log')
    
        # Buat formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
    
        # Tambahkan handler ke logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
    
    return logger
