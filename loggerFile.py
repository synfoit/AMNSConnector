# importing module
import logging

# Create and configure logger
class LoggerData:

    def __init__(self):
        logging.basicConfig(filename="error.log",
                            format='%(asctime)s %(levelname)s-%(message)s',
                            filemode='w',
                            datefmt='%Y-%m-%d %H:%M:%S')

        # Creating an object
        self.logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.ERROR)

    # Test messages
    # logger.debug("Harmless debug Message")
    # logger.info("Just an information")
    # logger.warning("Its a Warning")
    # logger.error("Did you try to divide by zero")
    # logger.critical("Internet is down")
