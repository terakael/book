# app.py
import threading
from flask import Flask, redirect, render_template, jsonify, request
import os
import base64

from generator import StoryImageGenerator

app = Flask(__name__)

generator = StoryImageGenerator()

jobs = {}


def run_job(job_id, description):
    jobs[job_id]["status"] = "in progress"
    generator.generate(job_id, description)
    del jobs[job_id]


def get_book_list():
    books = []
    static_dir = os.path.join(app.static_folder)
    for book in os.listdir(static_dir):
        if os.path.isdir(os.path.join(static_dir, book)):
            pages = [
                int(page)
                for page in os.listdir(os.path.join("static", book))
                if page.isdigit()
            ]
            if pages:  # If the book has any pages
                last_page = max(pages)
                _, cover = get_page_content(book, last_page)
            else:
                cover = ""

            books.append({"title": book, "cover": cover})

    return books


def get_page_content(book, page):
    page_dir = os.path.join(app.static_folder, book, str(page))

    # Read text content
    with open(os.path.join(page_dir, "text.txt"), "r") as f:
        text = f.read()

    # Read and encode image
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
        title = request.form.get("title")
        description = request.form.get("description")

        job_id = title
        jobs[job_id] = {"status": "queued"}
        thread = threading.Thread(target=run_job, args=(job_id, description))
        thread.start()

        return redirect("/")

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
