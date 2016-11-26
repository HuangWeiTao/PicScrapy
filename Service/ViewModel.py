# -*- encoding:utf-8 -*-

class TopicView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.post_count = None #主题下的帖子总数

class PostView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.pic_count = None #帖子下的图片总数
        self.pic_ready_count = None #帖子下已下载的图片数

class PicView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.path = None #图片的加载路径

class PagerResponse:
    def __init__(self):
        self.current_page = None
        self.page_size = None
        self.total = None #总数

class TopicListResponse(PagerResponse):
    def __init__(self):
        super.__init__(self)
        self.topic_list = []

class PostListResponse(PagerResponse):
    def __init__(self):
        super.__init__(self)
        self.topic_view = None
        self.post_list = []

class PicListResponse(PagerResponse):
    def __init__(self):
        super.__init__()
        self.post_view = None
        self.pic_list = []



