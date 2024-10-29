from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from database import insert_book, search_book_by_isbn, borrow_book, return_book, connect, fetch_all_books, search_books_by_title
from barcode_scanner import start_barcode_scanner

def add_book_window():
    add_window = Toplevel()
    add_window.title("Add New Book")

    Label(add_window, text="Title").grid(row=0, column=0)
    title_entry = Entry(add_window)
    title_entry.grid(row=0, column=1)

    Label(add_window, text="Author").grid(row=1, column=0)
    author_entry = Entry(add_window)
    author_entry.grid(row=1, column=1)

    Label(add_window, text="Year").grid(row=2, column=0)
    year_entry = Entry(add_window)
    year_entry.grid(row=2, column=1)

    isbn_label = Label(add_window, text="Scan the barcode")
    isbn_label.grid(row=3, column=1)

    def scan_barcode():
        isbn = start_barcode_scanner()
        isbn_label.config(text=f"ISBN: {isbn}")
        return isbn

    scan_button = Button(add_window, text="Scan Barcode", command=scan_barcode)
    scan_button.grid(row=4, column=1)

    def save_book():
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()
        isbn = isbn_label.cget("text").replace("ISBN: ", "")

        if isbn and title and author and year:
            success = insert_book(isbn, title, author, year)
            if success:
                messagebox.showinfo("Success", "Book added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror("Error", "Book did not get added, as it already exists in Database.")
                add_window.destroy()
        else:
            messagebox.showwarning("Error", "Please fill in all fields and scan the barcode")

    save_button = Button(add_window, text="Add Book", command=save_book)
    save_button.grid(row=5, column=1)


def display_all_books_window():
    display_window = Toplevel()
    display_window.title("Library Books")

    tree = ttk.Treeview(display_window, columns=("ISBN", "Title", "Author", "Year", "Status", "Borrow Time", "Return Time"), show='headings')
    tree.heading("ISBN", text="ISBN")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("Status", text="Status")
    tree.heading("Borrow Time", text="Borrow Time")
    tree.heading("Return Time", text="Return Time")

    tree.column("ISBN", width=100)
    tree.column("Title", width=150)
    tree.column("Author", width=100)
    tree.column("Year", width=50)
    tree.column("Status", width=80)
    tree.column("Borrow Time", width=120)
    tree.column("Return Time", width=120)

    tree.pack(fill=BOTH, expand=True)

    # Fetch all books from the database
    books = fetch_all_books()
    for book in books:
        status = "Borrowed" if book[5] else "Available"
        tree.insert("", END, values=(book[1], book[2], book[3], book[4], status, book[6], book[7]))


def borrow_book_window():
    borrow_window = Toplevel()
    borrow_window.title("Borrow Book by Barcode")

    isbn_label = Label(borrow_window, text="Scan the barcode to borrow the book")
    isbn_label.pack()

    def scan_and_borrow():
        isbn = start_barcode_scanner()
        book = search_book_by_isbn(isbn)
        if book and book[5] == 0:  # Check if the book is available
            borrow_book(isbn)
            messagebox.showinfo("Success", "Book borrowed successfully!")
        elif book and book[5] == 1:
            messagebox.showwarning("Error", "Book is already borrowed")
        else:
            messagebox.showwarning("Error", "Book not found")

    scan_button = Button(borrow_window, text="Scan Barcode", command=scan_and_borrow)
    scan_button.pack()

def return_book_window():
    return_window = Toplevel()
    return_window.title("Return Book by Barcode")

    isbn_label = Label(return_window, text="Scan the barcode to return the book")
    isbn_label.pack()

    def scan_and_return():
        isbn = start_barcode_scanner()
        book = search_book_by_isbn(isbn)
        if book and book[5] == 1:  # Check if the book is borrowed
            return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully!")
        elif book and book[5] == 0:
            messagebox.showwarning("Error", "Book is not borrowed")
        else:
            messagebox.showwarning("Error", "Book not found")

    scan_button = Button(return_window, text="Scan Barcode", command=scan_and_return)
    scan_button.pack()

def check_availability_by_title_window():
    check_window = Toplevel()
    check_window.title("Check Book Availability by Title")

    title_label = Label(check_window, text="Enter part of the title:")
    title_label.pack()

    title_entry = Entry(check_window)
    title_entry.pack()

    def search_and_display():
        title = title_entry.get()
        if title:
            books = search_books_by_title(title)
            if books:
                result_text = ""
                for book in books:
                    isbn, title, author, year, borrowed = book
                    availability = "Available" if borrowed == 0 else "Not Available"
                    result_text += f"Title: {title}\nAuthor: {author}\nYear: {year}\nISBN: {isbn}\nStatus: {availability}\n\n"
                result_label.config(text=result_text)
            else:
                messagebox.showwarning("Not Found", "No books found matching that title.")
        else:
            messagebox.showwarning("Error", "Please enter a part of the title to search.")

    search_button = Button(check_window, text="Search", command=search_and_display)
    search_button.pack(pady=10)

    result_label = Label(check_window, text="", justify=LEFT)
    result_label.pack(pady=10)


def start_gui():
    connect()
    window = Tk()
    window.title("Library Management System")

    # Set the window size
    window.geometry("400x300")

    # Center the window on the screen
    window_width = 400
    window_height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    add_book_button = Button(window, text="Add New Book", command=add_book_window, width=20)
    add_book_button.pack(pady=10)

    borrow_book_button = Button(window, text="Borrow Book", command=borrow_book_window, width=20)
    borrow_book_button.pack(pady=10)

    return_book_button = Button(window, text="Return Book", command=return_book_window, width=20)
    return_book_button.pack(pady=10)

    display_books_button = Button(window, text="Display All Books", command=display_all_books_window, width=20)
    display_books_button.pack(pady=10)

    check_availability_button = Button(window, text="Check if a Book is in Library", command=check_availability_by_title_window, width=25)
    check_availability_button.pack(pady=10)

    window.mainloop()