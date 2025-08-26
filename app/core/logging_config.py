import logging.config
import os

LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'email_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'email_operations.log'),
            'formatter': 'default',
            'mode': 'a',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        # هذا هو المُسجِّل الخاص بخدمة الإيميل
        'app.services.email_service': {
            'handlers': ['email_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        # --- الإضافة الجديدة لإيقاف سجلات SQLAlchemy ---
        'sqlalchemy.engine': {
            'handlers': ['console'],
            'level': 'WARNING', # اعرض فقط التحذيرات والأخطاء، وليس المعلومات العادية
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)