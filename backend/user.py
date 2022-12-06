import streamlit
from mongoengine import *
import database.models

def createUser():
    try:
        newUser = database.models.User(
            moodleId=streamlit.session_state.data["moodleId"],
        )

        newUser.save()
        return True
    except Exception as e:
        return False

def getUser(moodleId=None):
    if moodleId != None:
        return database.models.User.objects(moodleId=moodleId).first()

    return database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()

def getInstances():
    user = database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()

    return user.instances

def createInstance(instanceName, instanceType, instanceRam, instanceIp):
    user = database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()

    if user.maxInstances > len(user.instances):
        if user.maxRam >= instanceRam:
            try:
                newInstance = database.models.Instance(
                    instanceId=streamlit.session_state.data["moodleId"],
                    instanceName=instanceName,
                    instanceType=instanceType,
                    instanceRam=instanceRam,
                    instanceIp=instanceIp
                )

                newInstance.save()

                user.instances.append(newInstance)
                user.save()

                return True
            except Exception as e:
                streamlit.write(e)
                return False
        else:
            return False
    else:
        return False


def getKey():
    user = database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()
    
    return user.sshKey

def setKey(privateKey):
    user = database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()

    user.sshKey = privateKey
    user.save()

def deleteInstance(instanceName):
    instance = database.models.Instance.objects(
        instanceName=instanceName
    ).first()

    user = database.models.User.objects(
        moodleId=streamlit.session_state.data["moodleId"]
    ).first()

    user.instances.remove(instance)
    user.save()
    instance.delete()