from  flask import Blueprint, jsonify

from app.posts.dao.posts_dao import PostsDAO
from app.comment.dao.comments_dao import CommentsDAO
from config import POST_PATH, COMMENTS_PATH

api_blueprint = Blueprint('api_blueprint', __name__)

posts_dao = PostsDAO(POST_PATH)
comments_dao = CommentsDAO(COMMENTS_PATH)


@api_blueprint.route('/api/posts/')
def posts_api():
    posts = posts_dao.open_json()
    return jsonify(posts), 200


@api_blueprint.route('/api/posts/<int:post_id>')
def single_post_api(post_id):
    post = posts_dao.get_post(post_id)
    return jsonify(post), 200