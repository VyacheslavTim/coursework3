import json

'''
Функция, что считывает JSON файл
'''

def open_json(file):
    with open(file, encoding="UTF-8") as f:
        json_data = json.load(f)

    return json_data

'''
Функция, что добавляет новые записи в  JSON файл
'''

def write_json(file, data):
    with open(file, "w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False)

'''
Функция, что считает кол-во комментарий
'''

def comments_count(posts_data, comments_data):
    comments_match = []
    for post in posts_data:
        for comment in comments_data:
            if comment["post_id"] == post["pk"]:
                comments_match.append(post["pk"])
            post["comments"] = comments_match.count(post["pk"])

    return posts_data


'''
Функция, задаёт ограничения к комментариям не более 50 символов
'''

def string_crop(posts_data):
    for post in posts_data:
        post["content"] = post["content"][:50]

    return posts_data

'''
Функция, что выводит определенный пост
'''

def get_post(posts_data, post_id):
    output_post = {}
    for post in posts_data:
        if post_id == post["pk"]:
            output_post = post

    return output_post


'''
Функция, что выводит пост пользователя
'''

def get_posts_by_user(posts_data, user_name):
    output_post = []
    is_exists = False
    for post in posts_data:
        if user_name == post["poster_name"]:
            is_exists = True
            output_post.append(post)

    '''
    Если будет указан неверный пользователь, то будет ошибка
    '''

    if not is_exists:
        raise ValueError

    return output_post

'''
Функция, что получает комментарии по id_post
'''

def get_comments_by_post_id(comment_data, id_post):
    output_post = []
    is_exists = False
    for post in comment_data:
        if id_post == comment_data["post_id"]:
            is_exists = True
            output_post.append(post)

    '''
        Если будет указан неверный id_post, то будет ошибка
    '''

    if not is_exists:
        raise ValueError

    return output_post

'''
    Функция, что ведёт подсчёт количества постов и выводит пост по ключевому слову
'''

def search_for_posts(posts_data, query):
    output_post = []
    i = 1
    for post in posts_data:
        if i == 10:
            break
        if query in posts_data["content"]:
            i += 1
            output_post.append(post)

    return output_post

'''
    Функция, что определяет теги по #
'''

def get_tags(post):
    tags = []
    text = post["context"].split(" ")
    for word in text:
        if "#" in word:
            tag = word.replace("#", "")
            tags.append(tag)

    return tags