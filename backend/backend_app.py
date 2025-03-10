from flask import Flask, jsonify, request
from flask_cors import CORS
from operator import itemgetter
import helper
from datetime import date as get_date
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    Fetches all the posts from API,
    but allows the user to filter or sort them before returning.
    POST method allows the user to add a new post to the API.
    """
    POSTS = helper.get_all_posts()
    if request.method == 'POST':
        new_post = request.get_json()
        if not helper.validate_post_data(new_post):
            return jsonify({"error": "Invalid post title, content or author"}), 400
        if POSTS:
            new_id = max(post['id'] for post in POSTS) + 1
        else:
            new_id = 1
        new_post['id'] = new_id
        new_post['date'] = str(get_date.today())
        POSTS.append(new_post)
        helper.save_all_posts_to_file(POSTS)
        return jsonify(new_post), 201
    else:
        title = request.args.get('title')
        content = request.args.get('content')
        author = request.args.get('author')
        date = request.args.get('date')
        sort = request.args.get('sort')
        direction = request.args.get('direction')

        user_filters = {'title': title, 'content': content, 'author': author, 'date': date}
        filtered_posts = POSTS
        if any(filter_content for filter_content in user_filters.values()):
            for filter_type, filter_content in user_filters.items():
                if filter_content:
                    filtered_posts = [post for post in filtered_posts if filter_content.casefold() in post[filter_type].casefold()]
            return filtered_posts


        if sort or direction:
            if helper.validate_filters(sort, direction):
                if sort and direction:
                    sorted_posts = sorted(POSTS, key= lambda post: post[sort].casefold(), reverse=direction == 'desc')
                    return jsonify(sorted_posts)
                elif sort:
                    sorted_posts = sorted(POSTS, key=lambda post: post[sort].casefold())
                    return jsonify(sorted_posts)
                elif direction:
                    sorted_posts = sorted(POSTS, key=itemgetter('id'), reverse=direction == 'desc')
                    return jsonify(sorted_posts)
            else:
                return jsonify({"error": "Bad Request"}), 400
        return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    If a post with a given id exists, deletes it from API.
    """
    post = helper.find_post_by_id(id)
    if post is None:
        return '', 404
    POSTS = helper.get_all_posts()
    new_posts = [post for post in POSTS if post['id'] != id]
    helper.save_all_posts_to_file(new_posts)
    return jsonify(post)


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    If a post with a given id exists, updates it in API.
    """
    post = helper.find_post_by_id(id)
    if post is None:
        return '', 404
    new_data = request.get_json()

    POSTS = helper.get_all_posts()

    for post in POSTS:
        if post["id"] == id:
            post.update(new_data)

    helper.save_all_posts_to_file(POSTS)
    return jsonify(post)


# Error handlers:
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
