"""program to track my books"""

from datetime import date
from typing import List, Dict, Any
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
        if date_finished is None:
            return f"{title} by {author}: Started {date_began} and in progress"
        return f"{title} by {author}: Started {date_began} and finished {date_finished}"

    def to_dict(self):
        """returns a book as a dict"""
        return {
            "author": self.author,
            "title": self.title,
            "date_began": self.date_began,
            "date_finished": self.date_finished,
        }


def get_log() -> List[Dict[str, Any]]:
    """gets log and returns a list of dicts"""
    try:
        with open("log.yaml", "r", encoding="utf-8") as log_file:
            log = yaml.safe_load(log_file)
            if log is not None:
                return log
            return []
    except FileNotFoundError:
        return []
    except yaml.YAMLError:
        print("Corrupted YAML. Returning an empty list.")
        return []


def parse_date(given_date: str | date | None) -> date | None:
    """parses a date from yaml"""
    if given_date is None:
        return None
    if isinstance(given_date, date):
        return given_date
    if isinstance(given_date, str):
        try:
            formatted_date = date.fromisoformat(given_date)
            return formatted_date
        except ValueError:
            print("Failed to format date from ISO format")
            return None
    return None


def book_from_dict(book_dict: dict) -> Book:
    """creates a book from a dict"""
    title = book_dict["title"]
    author = book_dict["author"]
    date_began = parse_date(book_dict["date_began"])
    date_finished = parse_date(book_dict["date_finished"])

    if date_began is None:
        raise ValueError("date_began cannot be None")

    return Book(title, author, date_began, date_finished)


def start_book(new_book: Book):
    """starts a book by adding it to the log with today's date as its starts
    date"""
    new_log = get_log()
    if new_book.title in [x["title"] for x in new_log]:
        print("Book already started")
        return
    new_log.append(new_book.to_dict())

    with open("log.yaml", "w", encoding="utf-8") as new_log_file:
        yaml.dump(new_log, new_log_file)


def finish_book(title: str):
    """finishes a book by adding a finished date"""
    log = get_log()
    for book in log:
        if book["title"] == title:
            if book["date_finished"] is None:
                book["date_finished"] = date.today()
                with open("log.yaml", "w", encoding="utf-8") as new_log_file:
                    yaml.dump(log, new_log_file)
                print(f"Finished book: {title}")
                return
            print("Book already finished")
            return
        print("Error: Book not found")


def print_logs():
    """prints all books in logs"""
    log = get_log()
    for book in log:
        print(book_from_dict(book).to_string())


parser = argparse.ArgumentParser(
    prog="library",
    description="library management software",
)

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
