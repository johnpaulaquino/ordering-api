import logging
import os
from logging.config import dictConfig


# Apply logging config
# Example logs

class AppLogger:
     __BASE_DIR = os.path.dirname(os.path.abspath(__file__))

     @classmethod
     def get_logger(cls):
          log_config = {
                  "version"                 : 1,
                  "disable_existing_loggers": False,
                  "formatters"              : {
                          "simple": {  # human-readable logs for console
                                  "format": "%(levelname)s: \t\t%(asctime)s -  %(name)s  %(message)s"
                          },
                          "json"  : {  # structured JSON logs for file
                                  "()"    : "pythonjsonlogger.jsonlogger.JsonFormatter",
                                  "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
                          }
                  },

                  "handlers"                : {
                          "console": {  # human-readable console logs
                                  "class"    : "logging.StreamHandler",
                                  "level"    : "DEBUG",
                                  "formatter": "simple",
                                  "stream"   : "ext://sys.stdout",
                          },
                          "file"   : {  # JSON logs saved to file
                                  "class"    : "logging.FileHandler",
                                  "level"    : "WARNING",
                                  "formatter": "json",
                                  "filename" : f"{cls.__BASE_DIR}/app.json",
                                  "mode"     : "a",
                          },
                  },
                  "root"                    : {
                          "level"   : "INFO",
                          "handlers": ["console", "file"],
                  },
          }
          dictConfig(log_config)
          logger = logging.getLogger("e-commerce-app", )
          return logger
