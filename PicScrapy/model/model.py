# -*- coding:utf-8 -*-
from peewee import *
import datetime
from PicScrapy.config import db_config

db = db_config.get_db()

class BaseModel(Model):
    class Meta:
        database = db


class Pic(BaseModel):
    id = PrimaryKeyField()
    url = CharField()
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())
    status = IntegerField(default=False)
    store_path = CharField(null = True)
    post_id = IntegerField()

    class Meta:
        constraints = [SQL('Unique(url)')]


class Post(BaseModel):
    id = PrimaryKeyField()
    url = CharField()
    name = CharField(null = True)
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())
    topic_id = IntegerField()
    status = IntegerField()# 1.下载完成 2.下载中 0.未下载

    class Meta:
        constraints = [SQL('Unique(url)'),SQL('Foreign Key(topic_id) References Topic(id)')]

class Topic(BaseModel):
    id = PrimaryKeyField()
    start_url = CharField()
    name = CharField()
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())
    class Meta:
        constraints = [SQL('Unique(start_url)'),SQL('Unique(name)')]

