import logging

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Singleton pattern to ensure only one instance of the logger is created """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.logger = logging.getLogger("jsc-dia-mcp")
        self.logger.setLevel(logging.INFO)
        logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        self.info(__name__ + " instance created.")

    def info(self, message):
        self.logger.info(" " + str(message))