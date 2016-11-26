from flask import Flask
app = Flask(__name__)

@app.route('topic/list')
def topic_list(page = 1, size = 20):
    return None

@app.route('post/list')
def post_list(page = 1, size = 20):
    return None

@app.route('pic/list')
def pic_list(page = 1, size = 20):
    return None

