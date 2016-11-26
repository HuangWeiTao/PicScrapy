from peewee import *
from PicScrapy.model.model import *
from PicScrapy.config import db_config

from scrapy import cmdline

database = db_config.get_db()
database.create_tables([Pic,Post,Topic],safe=True)

cmdline.execute("scrapy crawl jpcn1-post".split())

