import utils
from flask import Flask, request, render_template, redirect, jsonify

app = Flask("skyprogram")


@app.route("/")
def main_page():
    posts_data = utils.open_json("data/posts.json")
    comments_data = utils.open_json("data/comments.json")
    bookmarks = utils.open_json("data/bookmarks.json")

    posts_data = utils.string_crop(posts_data)
    posts_data = utils.comments_count(posts_data, comments_data)

    bookmarks_quantity = len(bookmarks)

    return render_template("index.html", posts=posts_data, bookmarks_quantity=bookmarks_quantity)


@app.route("/post/<postid>")
def post_page(postid):
    posts_data = utils.open_json("data/posts.json")
    comments_data = utils.open_json("data/comments.json")

    postid = int(postid)

    output_post = utils.get_post(posts_data, postid)
    tags = utils.get_tags(output_post)

    try:
        output_comments = utils.get_comments_by_post_id(comments_data, postid)
    except ValueError:
        return "Такого поста нет"

    comments_quantity = len(output_comments)
    return render_template("post.html", post=output_post, comments=output_comments, quantity=comments_quantity, tags=tags)


@app.route("/search")
def search_page():
    posts_data = utils.open_json("data/posts.json")
    comments_data = utils.open_json("data/comments.json")

    s = request.args.get("s")
    if s is None:
        return "Укажите данные для поиска"
    s = s.lower()

    match = utils.search_for_posts(posts_data, s)
    posts = utils.comments_count(match, comments_data)
    if len(match):
        quantity = len(match)
        return render_template("search.html", posts=posts, s=s, quantity=quantity)
    return "Ничего не найдено"


@app.route("/users/<username>")
def user_feed(username):
    posts_data = utils.open_json("data/posts.json")
    comments_data = utils.open_json("data/comments.json")

    match = []
    match = utils.get_posts_by_user(posts_data, username)
    posts = utils.comments_count(match, comments_data)
    return render_template("user-feed.html", posts=posts)


@app.route('/tag/<tagname>')
def tag_page(tagname):
    posts_data = utils.open_json("data/posts.json")

    tagname = "#" + tagname
    output_posts = []
    for post in posts_data:
        text = post["content"].split(" ")
        if tagname in text:
            output_posts.append(post)

    return render_template("tag.html", output_posts=output_posts, tagname=tagname)


@app.route("/bookmarks/add/<postid>")
def add_bookmark(postid):
    postid = int(postid)
    posts_data = utils.open_json("data/posts.json")

    bookmarked_posts = utils.open_json("data/bookmarks.json")
    for bookmark in bookmarked_posts:
        if postid == bookmark["pk"]:
            return redirect("/", code=302)

    for post in posts_data:
        if postid == post["pk"]:
            bookmarked_posts.append(post)

    utils.write_json("data/bookmarks.json", bookmarked_posts)
    return redirect("/", code=302)


@app.route("/bookmarks/remove/<postid>")
def remove_bookmark(postid):
    postid = int(postid)
    bookmarks = utils.open_json("data/bookmarks.json")

    for bookmark in bookmarks:
        if postid == bookmark["pk"]:
            bookmarks.remove(bookmark)

    utils.write_json("data/bookmarks.json", bookmarks)
    return redirect("/", code=302)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def resource_not_found(e):
    return jsonify(error=str(e)), 500

@app.route("/bookmarks")
def bookmarks_page():
    bookmarks = utils.open_json("data/bookmarks.json")
    comments_data = utils.open_json("data/comments.json")

    bookmarks = utils.string_crop(bookmarks)
    bookmarks = utils.comments_count(bookmarks, comments_data)

    return render_template("bookmarks.html", bookmarks=bookmarks)


if __name__ == "__main__":
    app.run(debug=True)