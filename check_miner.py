import subprocess
import json
import logging
import logging.config
import os


def setup_logging(
        default_path='logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if os.path.exists('conf.json'):
    with open("conf.json") as json_file:
        json_data = json.load(json_file)


def check_service():
    ps = subprocess.check_output(['ps', '-ef']).decode()
    list_services = json_data["service"]
    for service in list_services:
        if service in ps:
            logger.info("%s it is UP" % service)
        else:
            logger.error("%s it is DOWN" % service)
            try_count = 1
            while try_count < 4:
                logger.info("Starting %s ... %d" % (service, try_count))
                try:
                    cmd = json_data["service"][service]["cmd"]
                    subprocess.call(cmd, shell=True)
                    cps = subprocess.check_output(['ps', '-A']).decode()
                    if service in cps:
                        logger.info("Service %s started" % service)
                        break
                    else:
                        logger.error("Service %s not started .. %d" % (service, try_count))
                        try_count += 1
                except:
                    logger.error("I am unable to start service %s .. %d" % (service, try_count), exc_info=True)
                    try_count += 1


setup_logging()

logger = logging.getLogger()

check_service()
