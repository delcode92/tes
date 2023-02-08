import logging

class ErrInfo:
    def __init__(self) -> None:
        logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                filename='log_file.log'
        )
    def errMSG(self, msg):
        logging.warning(msg)
    
    def infoMSG(self, msg):
        logging.info(msg)
        

# err_info = ErrInfo()
# err_info.infoMSG("info test 123 ...")
# err_info.errMSG("ttest1 12312")

