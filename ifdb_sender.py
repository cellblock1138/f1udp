import requests
import time
import random

INFLUX_HOST = "127.0.0.1:8086"

def send_request(p):
    try:
        response = requests.post(
            url="http://{}/write".format(INFLUX_HOST),
            params={
                "db": "http_ingest",
            },
            headers={
                "Content-Type": "text/plain; charset=utf-8",
            },
            data="kph,node=Ferrari value={}\ngear,node=Ferrari value={}\nthrottle,node=Ferrari value={}".format(p.m_speed * 3.6, p.m_gear, p.m_throttle)
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
