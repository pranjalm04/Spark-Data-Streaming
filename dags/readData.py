import json
import os
import random
from datetime import datetime, time
import time
from logger import logger
from dotenv import load_dotenv
from kafka_config import kafkaProducer
import requests

# load_dotenv('/opt/airflow/dags/config.env')
load_dotenv('config.env')
def getData():
    try:

        url='https://randomuser.me/api/'

        if not url:
            raise ValueError("The url could not be fetched")
        res=requests.get(url)
        res.raise_for_status()
        userData=res.json()['results'][0]
        logger.info(json.dumps(userData,indent=3))
        return userData
    except requests.exceptions.RequestException as e:
        logger.exception("Failed to fetch data from API. URL: %s, Error: %s",url,str(e))
        return None
    except ValueError as e:
        logger.exception("Failed to fetch data from API. URL: %s, Error: %s", url, str(e))
        return None

def formatData(res:requests)->dict:
    userData = dict()
    if res is None:
        return userData

    location=res['location']
    userData['first_name']=res['name']['first']
    userData['last_name']=res['name']['last']
    userData['gender']=res['gender']
    userData['address']=f"{str(location['street']['number'])} {location['street']['name']}"\
                        f"{location['city']},{location['state']},{location['country']}"
    userData['zipcode']=location['postcode']
    userData['email']=res['email']
    userData['username']=res['login']['username']
    userData['dob']=res['dob']
    userData['registered']=res['registered']['date']
    userData['phone']=res['phone']
    userData['image']=res['picture']['medium']
    return userData

def streamData():
    current_time=time.time()

    while True:
        if time.time()>current_time+5000:
            break
        try:
            userData=getData()
            userData=formatData(userData)
            logger.info("------formatted_data----------%s",userData)
            kafka_instance=kafkaProducer()
            kafka_instance.send(topic='users',key=random.randint(0,100000),value=json.dumps(userData).encode('utf-8'))
        except Exception as e:
            logger.error(f"some error occured {e}")
            continue
    kafka_instance.close()

