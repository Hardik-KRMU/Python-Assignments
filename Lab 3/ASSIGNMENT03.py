import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("library_manager")


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"

    def __post_init__(self):
        if self.status not in ("available", "issued"):
            self.status = "available"

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return asdict(self)

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if not self.is_available():
            self.status = "available"
            return True
        return False


class LibraryInventory:
    def __init__(self, storage_path=None):
        self.storage_path = Path(storage_path or "catalog.json")
        self.books = []
        self._ensure_storage()
        self.load_from_file()

    def _ensure_storage(self):
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error("Failed to create directory: %s", e)

    def add_book(self, book: Book):
        if any(b.isbn == book.isbn for b in self.books):
            return
        self.books.append(book)
        self.save_to_file()

    def search_by_title(self, query: str):
        q = query.lower().strip()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str):
        return next((b for b in self.books if b.isbn == isbn.strip()), None)

    def display_all(self):
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str):
        book = self.search_by_isbn(isbn)
        if book and book.issue():
            self.save_to_file()
            return True
        return False

    def return_book(self, isbn: str):
        book = self.search_by_isbn(isbn)
        if book and book.return_book():
            self.save_to_file()
            return True
        return False

    def save_to_file(self):
        try:
            with self.storage_path.open("w", encoding="utf-8") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
        except Exception as e:
            logger.error("Save failed: %s", e)

    def load_from_file(self):
        if not self.storage_path.exists():
            self.books = []
            return
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
        except Exception:
            self.books = []


def prompt(msg, required=True):
    while True:
        try:
            value = input(msg).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return ""
        if required and not value:
            continue
        return value


def menu():
    print("\n=== Library Inventory Manager ===")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search")
    print("6. Exit")


def add_book_flow(inv):
    title = prompt("Title: ")
    author = prompt("Author: ")
    isbn = prompt("ISBN: ")
    inv.add_book(Book(title, author, isbn))
    print("Book added.")


def issue_book_flow(inv):
    isbn = prompt("ISBN to issue: ")
    print("Book issued." if inv.issue_book(isbn) else "Issue failed.")


def return_book_flow(inv):
    isbn = prompt("ISBN to return: ")
    print("Book returned." if inv.return_book(isbn) else "Return failed.")


def view_all_flow(inv):
    books = inv.display_all()
    if not books:
        print("No books found.")
    for i, b in enumerate(books, 1):
        print(f"{i}. {b}")


def search_flow(inv):
    choice = prompt("Search by (1) Title or (2) ISBN: ")
    if choice == "1":
        q = prompt("Enter title: ")
        results = inv.search_by_title(q)
        if results:
            for r in results:
                print(r)
        else:
            print("Nothing found.")
    elif choice == "2":
        q = prompt("Enter ISBN: ")
        book = inv.search_by_isbn(q)
        print(book if book else "Nothing found.")
    else:
        print("Invalid option.")


def main():
    inv = LibraryInventory()
    while True:
        menu()
        choice = prompt("Choose option: ")
        if choice == "1":
            add_book_flow(inv)
        elif choice == "2":
            issue_book_flow(inv)
        elif choice == "3":
            return_book_flow(inv)
        elif choice == "4":
            view_all_flow(inv)
        elif choice == "5":
            search_flow(inv)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
