import logging, os
import logging.config

def setupLoggers(config):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.config.fileConfig(config, disable_existing_loggers=False)
