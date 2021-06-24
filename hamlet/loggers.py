import logging
from logging.config import dictConfig


LOGGING = {
    'version': 1,
    'disableExistingLoggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        }
    }
}


dictConfig(LOGGING)

root = logging.getLogger()
