from flask import Flask, jsonify, request
from flask_cors import CORS
from operator import itemgetter
import helper

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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
            return jsonify({"error": "Invalid post title or content"}), 400
        if POSTS:
            new_id = max(post['id'] for post in POSTS) + 1
        else:
            new_id = 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        helper.save_all_posts_to_file(POSTS)
        return jsonify(new_post), 201
    else:
        title = request.args.get('title')
        content = request.args.get('content')
        sort = request.args.get('sort')
        direction = request.args.get('direction')

        if title and content:
            filtered_posts = [post for post in POSTS if title in post['title'].casefold()
                              and content in post['content'].casefold()]
            return jsonify(filtered_posts)
        elif title:
            filtered_posts = [post for post in POSTS if title in post['title'].casefold()]
            return jsonify(filtered_posts)
        elif content:
            filtered_posts  = [post for post in POSTS if content in post['content'].casefold()]
            return jsonify(filtered_posts)
        if sort or direction:
            if helper.validate_filters(sort, direction):
                if sort and direction:
                    sorted_posts = sorted(POSTS, key=itemgetter(sort), reverse=direction == 'desc')
                    return jsonify(sorted_posts)
                elif sort:
                    sorted_posts = sorted(POSTS, key=itemgetter(sort))
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
    post.update(new_data)
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
