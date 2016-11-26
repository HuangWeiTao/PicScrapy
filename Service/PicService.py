from PicScrapy.repository.repository import PicRepository
from ViewModel import *

class PicService:

    '''返回主题列表'''
    def get_topic_list(self, page, size):
        page, size = self.validate_params(page, size)
        repo = PicRepository()
        topic_count = repo.get_topic_count()
        topic_list = repo.get_topic_list(page, size)

        response = TopicListResponse()
        response.current_page = page
        response.page_size = size
        response.topic_list = 

    '''返回某主题下帖子列表'''
    def get_post_list_by_topic(self, topic_id, page, size):
        page, size = self.validate_params(page, size)

    '''返回某帖子下的所有图片'''
    def get_pic_list_by_post(self, post_id):
        pass

    def validate_params(self, page, size):
        if page <= 0:
            page = 1
        if size <= 0:
            size = 10
        return page,size
