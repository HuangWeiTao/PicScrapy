# -*- encoding:utf-8 -*-

class TopicView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.post_count = None #主题下的帖子总数
        self.create_time = None

class PostView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.pic_count = None #帖子下的图片总数
        self.pic_ready_count = None #帖子下已下载的图片数
        self.create_time = None

class PicView:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.thumb_path = None #缩略图路径
        self.full_path = None #大图图片路径
        self.create_time = None

class PagerResponse:
    def __init__(self):
        self.current_page = None
        self.page_size = None
        self.total = None #总数

class TopicListResponse(PagerResponse):
    def __init__(self):
        PagerResponse.__init__(self)
        self.topic_view_list = []

class PostListResponse(PagerResponse):
    def __init__(self):
        PagerResponse.__init__(self)
        self.topic_view = None
        self.post_view_list = []

class PicListResponse(PagerResponse):
    def __init__(self):
        PagerResponse.__init__(self)
        self.post_view = None
        self.pic_view_list = []



