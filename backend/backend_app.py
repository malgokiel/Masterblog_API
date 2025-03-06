from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def validate_post_data(data):
    if not data['title'] or not data['content']:
        return False
    return True

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':

        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post title or content"}), 400
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id

        POSTS.append(new_post)

        return jsonify(new_post), 201
    else:
        title = request.args.get('title')
        content = request.args.get('content')

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
        else:
            return jsonify(POSTS)




@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return '', 404

    global POSTS
    new_posts = [post for post in POSTS if post['id'] != id]
    POSTS = new_posts
    return jsonify(post)


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)

    if post is None:
        return '', 404

    new_data = request.get_json()
    post.update(new_data)

    return jsonify(post)

def find_post_by_id(post_id):
    post = [post for post in POSTS if post['id'] == post_id]
    if post:
        return post[0]
    else:
        return None


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
