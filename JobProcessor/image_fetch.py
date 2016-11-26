#-*- encoding:utf-8 -*-
import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir))
print (os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir))
from PicScrapy.repository.repository import *
from celery import Celery
import pika
import cPickle
import requests
import uuid


app = Celery('image_fetch', broker='pyamqp://guest:guest@localhost:5672')

def push_tasks_to_queue():
    credentials = pika.PlainCredentials('guest','guest')
    queue_task = 'image_download'
    params = pika.ConnectionParameters('localhost',5672,'/',credentials)
    #params.socket_timeout = 5
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_task)

    with db_config.get_sqlite_db() as db_conn:
        cursor = db_conn.execute('select id from pic')
        for row in cursor:
            pic_id = row[0]
            channel.basic_publish(exchange='', routing_key='image_download', body=cPickle.dumps({'pic_id': pic_id}))


    connection.close()#没有close时,消息并不会真正写入队列
    print('push pic download task to queue completed!')

def start_jobs():
    with db_config.get_sqlite_db() as db_conn:
        cursor = db_conn.execute('select id from pic')
        for row in cursor:
            pic_id = row[0]
            download_pic.delay(pic_id)
    print ('end jobs')

@app.task
def download_pic(pic_id):
    repository = PicRepository()
    pic = repository.get_pic(pic_id)
    if pic.status == downloadstatus.notdownload:
        response = requests.get(pic.url)
        if response.status_code == 200:
            data = response.content
            path = save_to_disk(data)

            pic.status = downloadstatus.downloaded
            pic.store_path = path
            repository.save_pic(pic)
            print ('pic {} completed.'.format(pic.url))

def save_to_disk(data):
    pic_root_dir = 'D:/pic_root'
    if not os.path.exists(pic_root_dir):#应该考虑使用锁
        os.makedirs(pic_root_dir)

    pic_name = str(uuid.uuid1())+'.jpg'
    path = os.path.join(pic_root_dir, pic_name)
    if os.path.exists(path):
        os.remove(path)

    with open(path, mode='wb') as file:
        file.write(data)

    return pic_name

if __name__ == "__main__":
    #app.start()
    #push_tasks_to_queue()
    start_jobs()


