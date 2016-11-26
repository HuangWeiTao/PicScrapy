from model.model import Post
from repository.repository import PicRepository
from model import downloadstatus

class PostDbPipeline(object):
    def process_item(self, item, spider):

        if spider.name not in ['jpcn1-post']:
            post = Post()
            post.url = item['url']
            post.topic_id = item['topic_id']
            post.status = downloadstatus.notdownload
            repo = PicRepository()
            repo.save_post(post)

            return item


