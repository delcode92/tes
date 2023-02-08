import logging

class Debug:
    def __init__(self, write_file=True) -> None:
        
        self.logger = logging.getLogger(__name__)
        self.logger.level(logging.DEBUG)
        self.logger.
        # logging.basicConfig(
        #     level=logging.DEBUG,
        #     format="%(asctime)s %(levelname)s %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        #     filename='log_file.log'
        # )

        if not write_file:
            self.logger.removeHandler( logging.FileHandler("log_file.log") )

    def debugMSG(self, msg):
        logging.debug(msg)
    
    def infoMSG(self, msg):
        logging.info(msg)
    
    def errMSG(self, msg):
        logging.warning(msg)



# d = Debug(logging.DEBUG)
# d.debugMSG("test 123")
