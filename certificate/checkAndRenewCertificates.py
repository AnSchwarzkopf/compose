import os
import OpenSSL
import logging

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def getEnvironmentVariables():
    logging.info("Getting environmentvariables...")
    environmentVariables = {}

    logging.info("Checking VALID_DAYS...")
    environmentVariables["VALID_DAYS"] = os.getenv('VALID_DAYS')
    if environmentVariables["VALID_DAYS"] is None:
        logging.info("Setting default value: 90")
        environmentVariables["VALID_DAYS"] = 90
    
    logging.info("Checking CERT_PATH...")
    environmentVariables["CERT_PATH"] = os.getenv('CERT_PATH')
    if environmentVariables["CERT_PATH"] is None:
        logging.info("Setting default value: /home/ssl")
        environmentVariables["CERT_PATH"] = "/home/ssl"
    if not os.path.exists(environmentVariables["CERT_PATH"]):
        raise FileNotFoundError
    
    logging.info("Checking CERT_NAME...")
    environmentVariables["CERT_NAME"] = os.getenv('CERT_NAME')
    if environmentVariables["CERT_NAME"] is None:
        logging.info("Setting default value: server")
        environmentVariables["CERT_NAME"] = "server"
    
    logging.info("Checking COUNTRY...")
    environmentVariables["COUNTRY"] = os.getenv('COUNTRY')
    if environmentVariables["COUNTRY"] is None:
        raise AttributeError 
    
    logging.info("Checking STATE...")
    environmentVariables["STATE"] = os.getenv('STATE')
    if environmentVariables["STATE"] is None:
            raise AttributeError 

    logging.info("Checking LOCATION...")
    environmentVariables["LOCATION"] = os.getenv('LOCATION')
    if environmentVariables["LOCATION"] is None:
        raise AttributeError 

    logging.info("Checking NAME...")
    environmentVariables["NAME"] = os.getenv('NAME')
    if environmentVariables["NAME"] is None:
        raise AttributeError 

    logging.info("Checking MAIL...")
    environmentVariables["MAIL"] = os.getenv('MAIL')
    if environmentVariables["MAIL"] is None:
        raise AttributeError 

    return environmentVariables

def renewCertificactes(environmentVariables):
    logging.info("Renew or create new certificates...")
    os.system("""openssl req -x509 -nodes \\
        -days %s \\
        -newkey rsa:2048 \\
        -keyout %s/%s.key \\
        -out %s/%s.crt \\
        -subj \"/C=%s/ST=%s/L=%s /O=-/OU=.CN=%s/emailAddress=%s\"""" % (environmentVariables["VALID_DAYS"],
        environmentVariables["CERT_PATH"],
        environmentVariables["CERT_NAME"],
        environmentVariables["CERT_PATH"],
        environmentVariables["CERT_NAME"],
        environmentVariables["COUNTRY"],
        environmentVariables["STATE"],
        environmentVariables["LOCATION"],
        environmentVariables["NAME"],
        environmentVariables["MAIL"]))
    logging.info("Certificate succesfully created.")

def checkCertificates(): 
    logging.info("Checking current certificates...")

    environmentVariables = getEnvironmentVariables()

    if not os.path.exists('/home/ssl/server.crt'):
        logging.warning("No certificates found, will be created...")
        renewCertificactes(environmentVariables)
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
        renewCertificactes(environmentVariables)
        logging.info("Certificates need to be renewed")
    else:
        logging.info("Certificates are still valid")

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
    logging.info('Starting certificate service...')
    
    checkCertificates()

    scheduler = BlockingScheduler()
    scheduler.add_job(checkCertificates,'interval', hours=12)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info("Exiting certificate service...")