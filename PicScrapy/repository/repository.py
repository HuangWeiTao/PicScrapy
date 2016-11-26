from peewee import fn
from PicScrapy.model.model import *
from PicScrapy.model import  downloadstatus

class PicRepository:
    def save_pic(self, pic):
        pic.save()

    def get_pic(self, id):
        pic = Pic.get(Pic.id == id)
        return pic

    def save_post(self, post):
        post.save()

    def get_post(self, id):
        post = Post.get(Post.id == id)
        return post

    def get_topic_by_name(self, name):
        try:
            return Topic.get(Topic.name == name)
        except DoesNotExist:
            return None

    def save_topic(self, topic):
        topic.save()

    def get_unready_post(self, count):
        return Post.select().where(Post.status == downloadstatus.notdownload ).order_by(Post.update_time.desc()).limit(count)

    def save_post_detail(self, post_detail):
        db = Post._meta.database
        post = post_detail['post']
        img_list = post_detail['img_list']
        with db.atomic() as txn:
            post.save()
            for img in img_list:
                pic = Pic.create(url=img,post_id=post.id)
                pic.save()

    def get_topic_count(self):
        return Topic.select(fn.Count()).scalar()

    def get_topic_list(self, page, size):
        return Topic.select().order_by(Topic.create_time).paginate(page, size)

    def get_post_count_by_topic(self,topic_id):
        return Post.select().where(Post.topic_id == topic_id).count()

    def get_post_list_by_topic(self, topic_id, page, size):
        return Post.select().where(Post.topic_id == topic_id).order_by(Post.create_time).paginate(page, size)

    def get_pic_count_by_post_id(self, post_id):
        return Pic.select().where(Pic.post_id == post_id).count()

    def get_pic_list_by_post_id(self, post_id):
        return Pic.select().where(Pic.post_id == post_id)

if __name__ == "__main__":
    query = (Post.select().join(Pic,join_type=JOIN_INNER).switch(Post).annotate(Pic))
    for row in query:
        print ('id:{} name:{} post count:{}'.format(row[0],row[1],row[-1]))



