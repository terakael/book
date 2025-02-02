from flask import Flask, redirect, render_template, jsonify, request
import os
import base64

import requests

app = Flask(__name__)


def get_book_list():
    books = []
    static_dir = os.path.join(app.static_folder)
    for book in os.listdir(static_dir):
        books.append({"title": book, "cover": get_thumbnail_b64(book)})

    return books


def get_thumbnail_b64(title):
    book_dir = os.path.join(app.static_folder, title)
    with open(os.path.join(book_dir, "thumbnail.jpg"), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_page_content(book, page):
    page_dir = os.path.join(app.static_folder, book, str(page))

    with open(os.path.join(page_dir, "text.txt"), "r") as f:
        text = f.read()

    image_file = next(
        f for f in os.listdir(page_dir) if f.endswith((".jpg", ".png", ".jpeg"))
    )
    with open(os.path.join(page_dir, image_file), "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    return text, image_data


def get_page_count(book):
    book_dir = os.path.join(app.static_folder, book)
    return len(
        [
            name
            for name in os.listdir(book_dir)
            if os.path.isdir(os.path.join(book_dir, name))
        ]
    )


@app.route("/")
def index():
    books = get_book_list()
    return render_template("index.html", books=books)


@app.route("/book/<book_name>/")
def view_book(book_name):
    page_count = get_page_count(book_name)
    text, image_data = get_page_content(book_name, 0)
    return render_template(
        "book.html",
        book_name=book_name,
        text=text,
        image_data=image_data,
        page_count=page_count,
    )


@app.route("/api/page/<book_name>/<int:page>")
def get_page(book_name, page):
    text, image_data = get_page_content(book_name, page)
    return jsonify({"text": text, "image": image_data})


@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        description = request.form.get("description")

        response = requests.post(
            "http://airflow-scheduler/dags/generate_book/dagRuns",
            json={"conf": {"story_description": description}},
        )

        if response.status != 200:
            print(response.content)

        return redirect("/")

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
