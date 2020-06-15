import os
import OpenSSL
import logging

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def renewCertificactes():
    logging.info("Renew or create new certificates...")
    os.system("openssl req -x509 -nodes -days 90 -newkey rsa:2048 -keyout /home/ssl/server.key -out /home/ssl/server.crt -subj \"/C=DE/ST=BW/L=ULM /O=-/OU=.CN=Andreas Schwarzkopf/emailAddress=schwarzkopf.and@gmail.com\"")
    logging.info("Certificate succesfully created.")

def checkCertificates(): 
    logging.info("Checking current certificates...")

    if not os.path.exists('/home/ssl/server.crt'):
        logging.warning("No certificates found, will be created...")
        renewCertificactes()
    try:
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open('/home/ssl/server.crt').read())
    except FileNotFoundError:
        logging.error("No certificates!")
        raise FileNotFoundError

    currentTime = datetime.now().replace(microsecond=0)
    logging.info("Current time and date is: %s " % currentTime)

    certTimeString = str(cert.get_notAfter()).replace("Z","").replace("b","").replace("'","")
    certTime = datetime.strptime(certTimeString,'%Y%m%d%H%M%S')
    logging.info("Certificates expire on this date: %s" % certTime)
    
    timeDifference = certTime - currentTime
    logging.info("Timedifference is: %s" % timeDifference)

    if timeDifference.days <= 1:
        renewCertificactes()
        logging.info("Certificates need to be renewed")
    else:
        logging.info("Certificates are still valid")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
    logging.info('Started')
    checkCertificates()
    scheduler = BlockingScheduler()
    scheduler.add_job(checkCertificates, 'interval', hours=12)
    scheduler.start()