import json


def get_all_posts():
    """
    Function fetches all posts from a JSON file and returns them.
    """
    with open("posts.json", "r") as fileobject:
        all_posts = json.load(fileobject)

        return all_posts


def save_all_posts_to_file(posts):
    """
    Function dumps all posts into a JSON file.
    """
    with open("posts.json", "w") as fileobj:
        json.dump(posts, fileobj)


def find_post_by_id(post_id):
    POSTS = get_all_posts()
    post = [post for post in POSTS if post['id'] == post_id]
    if post:
        return post[0]
    else:
        return None


def validate_post_data(data):
    if not data['title'] or not data['content']:
        return False
    return True


def validate_filters(sort, direction):
    if sort in ['', 'title', 'content'] and direction in ['', 'asc', 'desc']:
        return True
    return False