"""program to track my books"""

from datetime import date
import argparse
import yaml


class Book:
    """a book"""

    def __init__(
        self, title: str, author: str, date_began: date, date_finished: date | None
    ):
        self.title: str = title
        self.author: str = author
        self.date_began: date = date_began
        self.date_finished: date | None = date_finished

    def to_string(self):
        """returns a book formatted as a string"""
        title = self.title
        author = self.author
        date_began = self.date_began
        date_finished = self.date_finished
        return f"{title} by {author}: Started {date_began} and finished {date_finished}"

    def to_dict(self):
        """returns a book as a dict"""
        return {
            "author": self.author,
            "title": self.title,
            "date_began": self.date_began,
            "date_finished": self.date_finished,
        }


parser = argparse.ArgumentParser(
    prog="library",
    description="library management software",
    usage="%(prog)s {start,finish} [--title TITLE] [--author AUTHOR]",
)


def book_from_dict(book_dict: dict) -> Book:
    """creates a book from a dict"""
    title = book_dict["title"]
    author = book_dict["author"]
    date_began = book_dict["date_began"]
    date_finished = book_dict["date_finished"]
    return Book(title, author, date_began, date_finished)


def start_book(new_book: Book):
    """starts a book by adding it to the log with today's date as its starts
    date"""
    old_log = [{}]
    with open("log.yaml", "r", encoding="utf-8") as old_log_file:
        old_log = yaml.safe_load(old_log_file)

    new_log = old_log
    new_log.append(new_book.to_dict())

    with open("log.yaml", "w", encoding="utf-8") as new_log_file:
        yaml.dump(new_log, new_log_file)


def finish_book(title: str):
    """finishes a book by adding a fininshed date"""
    old_log = [{}]
    with open("log.yaml", "r", encoding="utf-8") as old_log_file:
        old_log = yaml.safe_load(old_log_file)

    new_log = old_log
    finished_book = None
    for book in old_log:
        if book["title"] == title:
            finished_book = book
            break

    if finished_book is None:
        print("Error: Book not found")
        return
    new_log.remove(finished_book)
    finished_book["date_finished"] = date.today()
    new_log.append(finished_book)

    with open("log.yaml", "w", encoding="utf-8") as new_log_file:
        yaml.dump(new_log, new_log_file)


def print_logs():
    """prints all books in logs"""
    with open("log.yaml", "r", encoding="utf-8") as log_file:
        log = yaml.safe_load(log_file)
        for book in log:
            print(book_from_dict(book).to_string())


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="action", help="Available actions")

start_parser = subparsers.add_parser("start", help="Start reading a book")
start_parser.add_argument("title", help="Book title")
start_parser.add_argument("author", help="Book author")

finish_parser = subparsers.add_parser("finish", help="Finish reading a book")
finish_parser.add_argument("title", help="Finish reading a book")

print_parser = subparsers.add_parser("print", help="Print library")

args = parser.parse_args()

if args.action == "start":
    start_book(Book(args.title, args.author, date.today(), None))
    print(f"Started book {args.title}")
if args.action == "finish":
    finish_book(args.title)
    print(f"Finished book {args.title}")
if args.action == "print":
    print_logs()
