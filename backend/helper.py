import json
import sys


def get_all_posts():
    """
    Function fetches all posts from a JSON file and returns them.
    """
    while True:
        try:
            with open("posts.json", "r") as fileobject:
                all_posts = json.load(fileobject)
                return all_posts
        except FileNotFoundError:
            with open("posts.json", 'w') as fileobject:
                fileobject.write("[]")
        except json.JSONDecodeError as e:
            print(f"The file is corrupted. JSONDecodeError was raised: '{e}'")
            sys.exit()
        except PermissionError as e:
            print(f"Check your permissions. PermissionError was raised: '{e}'")
            sys.exit()


def save_all_posts_to_file(posts):
    """
    Function dumps all posts into a JSON file.
    """
    with open("posts.json", "w") as fileobj:
        json.dump(posts, fileobj)


def find_post_by_id(post_id):
    """
    Function searches for a post in database, specified by post_id,
    then returns it
    """
    posts = get_all_posts()
    post = [post for post in posts if post['id'] == post_id]
    if post:
        return post[0]
    else:
        return None


def validate_post_data(data):
    """
    Function checks if user, when adding a new post,
    provided both a post's title and post's content.
    Returns boolean.
    """
    if not data['title'] or not data['content'] or not data['author']:
        return False
    return True


def validate_filters(sort, direction):
    """
    Function checks if user correctly specified sort and direction filters,
    when filtering through the API.
    Returns boolean.
    """
    if sort in [None, '', 'title', 'content', 'author', 'date'] and direction in [None, '', 'asc', 'desc']:
        return True
    return False