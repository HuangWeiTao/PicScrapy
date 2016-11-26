from peewee import fn
from PicScrapy.model.model import *
import logging
from ViewModel import *

logger = logging.getLogger(__name__)

class PicDao:

    def get_topic_list_response(self, page, size):

        query = Topic.select(Topic, fn.Count(Post.id).alias('post_count'))\
            .join(Post,join_type=JOIN_INNER,on=(Topic.id==Post.topic_id))\
            .group_by(Topic.id).order_by(Topic.create_time.desc())

        query = query.paginate(page, size)

        logger.info(str(query))

        topic_view_list = []
        for topic in query:
            topic_view = TopicView()
            topic_view.name = topic.name
            topic_view.id = topic.id
            topic_view.post_count = topic.post_count
            topic_view.create_time = topic.create_time
            topic_view_list.append(topic_view)

        topic_total = Topic.select().scalar()

        response = TopicListResponse()
        response.current_page = page
        response.page_size = size
        response.total = topic_total
        response.topic_view_list = topic_view_list

        return response

    def get_post_list_response(self,topic_id, page, size):
        query = Post.select(Post, fn.Count(Pic.id).alias('pic_count')) \
            .where(Post.topic_id == topic_id)\
            .join(Pic, join_type=JOIN_INNER, on=(Post.id == Pic.post_id)) \
            .group_by(Post.id).order_by(Post.create_time.desc())

        query = query.paginate(page, size)

        logger.info(str(query))

        post_view_list = []
        for post in query:
            post_view = PostView()
            post_view.name = post.name
            post_view.id = post.id
            post_view.pic_count = post.pic_count
            post_view.create_time = post.create_time
            post_view_list.append(post_view)

        post_total = Post.select().where(Post.topic_id==topic_id).scalar()

        response = PostListResponse()
        response.current_page = page
        response.page_size = size
        response.total = post_total
        response.post_view_list = post_view_list

        return response
    
    
    def get_pic_list_response(self,post_id):
        query = Pic.select().where(Pic.post_id == post_id).order_by(Pic.create_time)

        logger.info(str(query))

        pic_view_list = []
        for pic in query:
            pic_view = PicView()
            pic_view.name = None
            pic_view.thumb_path = None
            pic_view.full_path = pic.url
            pic_view.id = pic.id
            pic_view.create_time = pic.create_time
            pic_view_list.append(pic_view)

        page = 1
        size = len(pic_view_list)

        response = PicListResponse()
        response.current_page = page
        response.page_size = size
        response.total = size
        response.pic_view_list = pic_view_list

        return response


def test_get_topic_list_response():

    current_page = 1
    page_size = 20

    dao = PicDao()
    response = dao.get_topic_list_response(current_page, page_size)
    print(
    'current page:{}, page size:{}, total count:{}.'.format(response.current_page, response.page_size, response.total))

    for t in response.topic_view_list:
        print(u'topic id:{}, topic name:{}, post count:{}'.format(t.id, t.name, t.post_count))


def test_get_post_list_response():
    current_page = 1
    page_size = 20
    topic_id = 1

    dao = PicDao()
    response = dao.get_post_list_response(topic_id, current_page, page_size)
    print(
        'current page:{}, page size:{}, total count:{}.'.format(response.current_page, response.page_size,
                                                                response.total))

    for t in response.post_view_list:
        print(u'post id:{}, post name:{}, pic count:{}'.format(t.id, t.name, t.pic_count))


def test_get_pic_list_response():
    post_id = 8

    dao = PicDao()
    response = dao.get_pic_list_response(post_id)

    for t in response.pic_view_list:
        print(u'pic id:{}, pic name:{}'.format(t.id, t.full_path))


if __name__ == '__main__':
    test_get_pic_list_response()
