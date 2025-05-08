import logging

class Log():
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging service initialized.")
    
    def message(self, str):
        self.logger.info(str)
        
    def error(self, str):
        self.logger.error(str)
        
    def warning(self, str): 
        self.logger.warning(str)