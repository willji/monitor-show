import logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename='/usr/local/apache/htdocs/monitor-show/logs/error.log',
                    filemode='a')
mylog = logging.getLogger()
