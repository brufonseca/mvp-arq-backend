from logging.config import dictConfig
import logging
import os


LOG_PATH = "log/"
# Verifica se o diretorio para armazenar os logs não existe
if not os.path.exists(LOG_PATH):
    # cria o diretorio
    os.makedirs(LOG_PATH)


dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        'default': {
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)-8s; %(name)s; %(message)s;'
        },
        'single-line': {
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)-8s; %(asctime)s; %(name)s; %(module)s:%(funcName)s;%(lineno)d: %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s; [%(process)d]; %(threadName)s; %(name)s; %(module)s:%(funcName)s;%(lineno)d'
                      ': %(message)s'
        },
        'multiline': {
            'format': 'Level: %(levelname)s\nTime: %(asctime)s\nProcess: %(process)d\nThread: %(threadName)s\nLogger'
                      ': %(name)s\nPath: %(module)s:%(lineno)d\nFunction :%(funcName)s\nMessage: %(message)s\n'
        }
    },
    "handlers": {
        'default': {
            'level': 'WARNING',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        }
    },
    "loggers": {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
    }
})


logger = logging.getLogger(__name__)
