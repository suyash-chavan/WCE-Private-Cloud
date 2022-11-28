from mongoengine import *

class Image(Document):
    imageId = StringField(unique=True)
    imageName = StringField(unique=True)
    imageType = StringField()
    imageRam = IntField()
    imageCreated = DateTimeField()
    meta = {"allow_inheritance": True}

class Instance(Document):
    instanceId = IntField(required=True)
    instanceName = StringField(unique=True)
    instanceType = StringField()
    instanceIp = StringField()
    instanceRam = IntField()
    instanceCreated = DateTimeField()
    instanceDeleted = DateTimeField()
    meta = {"allow_inheritance": True}

class User(Document):
    moodleId = LongField(unique=True)
    maxRam = IntField(default=4096)
    maxInstances = IntField(default=2)
    instances = ListField(default=[])
    sshKey = StringField()
    meta = {"allow_inheritance": True}