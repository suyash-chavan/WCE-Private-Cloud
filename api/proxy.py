import requests
import os

def setPort(dIp, dPort):
    try:
        res = requests.post(
            os.getenv("PROXY_API"),
            data={
                "dIp": dIp,
                "dPort": dPort,
            },
        )

        status = res.json()["status"]

        if status == "SUCCESS":
            return res.json()["port"]

    except Exception as e:
        pass
    
    return -1

def deletePort(sPort):
    try:
        res = requests.delete(
            os.getenv("PROXY_API"),
            data={
                "sPort": sPort,
            },
        )

        status = res.json()["status"]

        if status == "SUCCESS":
            return True

    except Exception as e:
        pass
    
    return False
