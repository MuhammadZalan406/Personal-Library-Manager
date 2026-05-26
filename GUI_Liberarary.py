# PROJECT 1: Personal Library Manager
# Jaani, yeh file mein DO versions hain:
# PART 1: CLI Version (TERA ORIGINAL CODE - bilkul same)
# PART 2: GUI Version (CustomTkinter - with all features)

import json
import os
import customtkinter as ctk
from tkinter import messagebox

# File name for storing data
BOOKS_FILE = "books.txt"

# ============================================================================
# PART 1: COMMON FUNCTIONS (Load & Save)
# ============================================================================

def load_books():
    """Load books from file when program starts"""
    if os.path.exists(BOOKS_FILE):
        try:
            with open(BOOKS_FILE, "r") as file:
                return json.load(file)
        except:
            return {}
    return {}

def save_books(books):
    """Save books to file permanently"""
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)


# ============================================================================
# PART 2: CLI VERSION (TERA ORIGINAL CODE - BILKUL SAME)
# ============================================================================

def add_book(books):
    """Add a new book to library"""
    print("\n" + "=" * 50)
    print("   ADD NEW BOOK")
    print("=" * 50)
    
    book_id = input("Book ID (e.g., B001): ").strip().upper()
    
    if book_id in books:
        print(f"Book with ID {book_id} already exists!")
        return
    
    title = input("Book Title: ").strip()
    author = input("Author Name: ").strip()
    
    try:
        year = int(input("Publication Year: ").strip())
    except ValueError:
        print("Invalid year! Using 2024 as default.")
        year = 2024
    
    status = input("Have you read this book? (yes/no): ").strip().lower()
    read_status = "Read" if status in ["yes", "y"] else "Unread"
    
    books[book_id] = {
        "title": title,
        "author": author,
        "year": year,
        "status": read_status
    }
    
    save_books(books)
    print(f"\n'{title}' added successfully to your library!")

def remove_book(books):
    """Remove a book from library using Book ID"""
    print("\n" + "=" * 50)
    print("   REMOVE BOOK")
    print("=" * 50)
    
    if not books:
        print("Library is empty! Nothing to remove.")
        return
    
    book_id = input("Enter Book ID to remove: ").strip().upper()
    
    if book_id in books:
        title = books[book_id]["title"]
        del books[book_id]
        save_books(books)
        print(f"'{title}' removed from your library!")
    else:
        print(f"Book with ID {book_id} not found!")

def search_book(books):
    """Search books by Title or Author"""
    print("\n" + "=" * 50)
    print("   SEARCH BOOK")
    print("=" * 50)
    
    if not books:
        print("Library is empty! No books to search.")
        return
    
    print("Search by:")
    print("1. Title")
    print("2. Author")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        keyword = input("Enter book title: ").strip().lower()
        results = {bid: info for bid, info in books.items() 
                   if keyword in info["title"].lower()}
    elif choice == "2":
        keyword = input("Enter author name: ").strip().lower()
        results = {bid: info for bid, info in books.items() 
                   if keyword in info["author"].lower()}
    else:
        print("Invalid choice!")
        return
    
    if results:
        print(f"\nFound {len(results)} book(s):")
        print("-" * 60)
        for bid, info in results.items():
            print(f"  ID: {bid} | {info['title']} by {info['author']} ({info['year']}) - {info['status']}")
    else:
        print("No books found!")

def show_all_books(books):
    """Display all books in library"""
    print("\n" + "=" * 60)
    print("   MY PERSONAL LIBRARY")
    print("=" * 60)
    
    if not books:
        print("\nLibrary is empty! Add some books first.")
        return
    
    print(f"\nTotal Books: {len(books)}\n")
    print("-" * 60)
    
    for book_id, info in books.items():
        status_icon = "[R]" if info["status"] == "Read" else "[U]"
        print(f"  {status_icon} ID: {book_id}")
        print(f"     Title: {info['title']}")
        print(f"     Author: {info['author']}")
        print(f"     Year: {info['year']}")
        print(f"     Status: {info['status']}")
        print("-" * 40)

def show_statistics(books):
    """Show library statistics"""
    print("\n" + "=" * 50)
    print("   LIBRARY STATISTICS")
    print("=" * 50)
    
    if not books:
        print("Library is empty!")
        return
    
    total_books = len(books)
    read_books = len([b for b in books.values() if b["status"] == "Read"])
    unread_books = total_books - read_books
    
    current_year = 2024
    recent_books = len([b for b in books.values() if b["year"] >= current_year - 5])
    classic_books = total_books - recent_books
    
    print(f"\nTotal Books: {total_books}")
    print(f"Books Read: {read_books}")
    print(f"Books Unread: {unread_books}")
    print(f"Reading Progress: {(read_books/total_books)*100:.1f}%")
    print(f"\nRecent Books (last 5 years): {recent_books}")
    print(f"Classic Books (5+ years old): {classic_books}")

def cli_main():
    """CLI version - TERA ORIGINAL CODE"""
    books = load_books()
    
    while True:
        print("\n" + "=" * 50)
        print("   PERSONAL LIBRARY MANAGER (CLI)")
        print("=" * 50)
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Show All Books")
        print("5. Show Statistics")
        print("6. Exit")
        print("=" * 30)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            add_book(books)
        elif choice == "2":
            remove_book(books)
        elif choice == "3":
            search_book(books)
        elif choice == "4":
            show_all_books(books)
        elif choice == "5":
            show_statistics(books)
        elif choice == "6":
            print("\nSaving your library...")
            save_books(books)
            print("Data saved successfully!")
            print("Thank you for using Personal Library Manager!")
            print("=" * 50)
            break
        else:
            print("Invalid choice! Please enter 1-6.")


# ============================================================================
# PART 3: GUI VERSION (CustomTkinter - with ALL features)
# ============================================================================

class LibraryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Library Manager")
        self.root.geometry("1100x750")
        
        # Load books data
        self.books = load_books()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fonts
        self.title_font = ctk.CTkFont(size=26, weight="bold")
        self.header_font = ctk.CTkFont(size=16, weight="bold")
        self.normal_font = ctk.CTkFont(size=12)
        
        self.setup_ui()
        self.refresh_display()
    
    def setup_ui(self):
        """Setup all UI components"""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="PERSONAL LIBRARY MANAGER", 
                                    font=self.title_font)
        title_label.pack(pady=15)
        
        # Content frame (left and right panels)
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ==================== LEFT PANEL ====================
        left_panel = ctk.CTkFrame(content_frame, width=400)
        left_panel.pack(side="left", fill="both", padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        # Form Title
        form_title = ctk.CTkLabel(left_panel, text="ADD NEW BOOK", font=self.header_font)
        form_title.pack(pady=15)
        
        # Book ID
        id_frame = ctk.CTkFrame(left_panel)
        id_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(id_frame, text="Book ID:", width=80).pack(side="left", padx=5)
        self.id_entry = ctk.CTkEntry(id_frame, width=200)
        self.id_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Title
        title_frame = ctk.CTkFrame(left_panel)
        title_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(title_frame, text="Title:", width=80).pack(side="left", padx=5)
        self.title_entry = ctk.CTkEntry(title_frame, width=200)
        self.title_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Author
        author_frame = ctk.CTkFrame(left_panel)
        author_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(author_frame, text="Author:", width=80).pack(side="left", padx=5)
        self.author_entry = ctk.CTkEntry(author_frame, width=200)
        self.author_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Year
        year_frame = ctk.CTkFrame(left_panel)
        year_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(year_frame, text="Year:", width=80).pack(side="left", padx=5)
        self.year_entry = ctk.CTkEntry(year_frame, width=200)
        self.year_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Read Status
        status_frame = ctk.CTkFrame(left_panel)
        status_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkLabel(status_frame, text="Status:", width=80).pack(side="left", padx=5)
        self.status_var = ctk.StringVar(value="Unread")
        read_radio = ctk.CTkRadioButton(status_frame, text="Read", variable=self.status_var, value="Read")
        read_radio.pack(side="left", padx=10)
        unread_radio = ctk.CTkRadioButton(status_frame, text="Unread", variable=self.status_var, value="Unread")
        unread_radio.pack(side="left", padx=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(left_panel)
        button_frame.pack(pady=20, fill="x", padx=20)
        
        self.add_btn = ctk.CTkButton(button_frame, text="Add Book", command=self.add_book, height=40)
        self.add_btn.pack(pady=5, fill="x")
        
        self.remove_btn = ctk.CTkButton(button_frame, text="Remove Book", command=self.remove_book, height=40, fg_color="red")
        self.remove_btn.pack(pady=5, fill="x")
        
        self.clear_btn = ctk.CTkButton(button_frame, text="Clear Fields", command=self.clear_inputs, height=40, fg_color="orange")
        self.clear_btn.pack(pady=5, fill="x")
        
        # ==================== RIGHT PANEL ====================
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Search Section
        search_frame = ctk.CTkFrame(right_panel)
        search_frame.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkLabel(search_frame, text="SEARCH BOOKS", font=self.header_font).pack(pady=5)
        
        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(pady=5, padx=10, fill="x")
        
        self.search_entry = ctk.CTkEntry(search_input_frame, placeholder_text="Enter keyword...")
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.search_by = ctk.CTkComboBox(search_input_frame, values=["Title", "Author"], width=100)
        self.search_by.pack(side="left", padx=5)
        
        self.search_btn = ctk.CTkButton(search_input_frame, text="Search", command=self.search_book, width=100)
        self.search_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(search_input_frame, text="Show All", command=self.refresh_display, width=100)
        self.reset_btn.pack(side="left", padx=5)
        
        # Books Display Area
        display_frame = ctk.CTkFrame(right_panel)
        display_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        ctk.CTkLabel(display_frame, text="BOOKS COLLECTION", font=self.header_font).pack(pady=5)
        
        self.books_display = ctk.CTkTextbox(display_frame, font=self.normal_font, wrap="word")
        self.books_display.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Statistics Bar
        self.stats_frame = ctk.CTkFrame(right_panel, height=50, fg_color="blue")
        self.stats_frame.pack(pady=10, padx=15, fill="x")
        
        self.stats_label = ctk.CTkLabel(self.stats_frame, text="Library Statistics", font=self.header_font, text_color="white")
        self.stats_label.pack(pady=10)
    
    def add_book(self):
        """Add a new book"""
        book_id = self.id_entry.get().strip().upper()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year_str = self.year_entry.get().strip()
        status = self.status_var.get()
        
        if not book_id or not title or not author:
            messagebox.showwarning("Warning", "Please fill Book ID, Title, and Author!")
            return
        
        if book_id in self.books:
            messagebox.showwarning("Warning", f"Book with ID {book_id} already exists!")
            return
        
        try:
            year = int(year_str) if year_str else 2024
        except:
            year = 2024
        
        self.books[book_id] = {
            "title": title,
            "author": author,
            "year": year,
            "status": status
        }
        
        save_books(self.books)
        self.refresh_display()
        self.clear_inputs()
        messagebox.showinfo("Success", f"'{title}' added successfully!")
    
    def remove_book(self):
        """Remove a book"""
        book_id = self.id_entry.get().strip().upper()
        
        if not book_id:
            messagebox.showwarning("Warning", "Please enter Book ID to remove!")
            return
        
        if book_id in self.books:
            title = self.books[book_id]["title"]
            del self.books[book_id]
            save_books(self.books)
            self.refresh_display()
            self.clear_inputs()
            messagebox.showinfo("Success", f"'{title}' removed from library!")
        else:
            messagebox.showwarning("Not Found", f"Book ID '{book_id}' not found!")
    
    def search_book(self):
        """Search books by Title or Author"""
        keyword = self.search_entry.get().strip().lower()
        search_type = self.search_by.get()
        
        if not keyword:
            messagebox.showwarning("Warning", "Please enter search keyword!")
            return
        
        results = {}
        for bid, info in self.books.items():
            if search_type == "Title":
                if keyword in info["title"].lower():
                    results[bid] = info
            else:
                if keyword in info["author"].lower():
                    results[bid] = info
        
        self.books_display.delete("1.0", "end")
        
        if results:
            self.books_display.insert("end", "SEARCH RESULTS\n")
            self.books_display.insert("end", "=" * 55 + "\n")
            self.books_display.insert("end", f"Found {len(results)} book(s)\n\n")
            
            for bid, info in results.items():
                status_icon = "[R]" if info["status"] == "Read" else "[U]"
                self.books_display.insert("end", f"{status_icon} ID: {bid}\n")
                self.books_display.insert("end", f"   Title : {info['title']}\n")
                self.books_display.insert("end", f"   Author: {info['author']}\n")
                self.books_display.insert("end", f"   Year  : {info['year']}\n")
                self.books_display.insert("end", f"   Status: {info['status']}\n")
                self.books_display.insert("end", "-" * 40 + "\n")
        else:
            self.books_display.insert("end", "No books found!\n")
            self.books_display.insert("end", "Try searching with different keywords.")
    
    def refresh_display(self):
        """Refresh the books display (Show All Books)"""
        self.books_display.delete("1.0", "end")
        
        if not self.books:
            self.books_display.insert("end", "LIBRARY IS EMPTY\n")
            self.books_display.insert("end", "=" * 55 + "\n\n")
            self.books_display.insert("end", "Add your first book using the form on the left!")
            self.update_statistics()
            return
        
        self.books_display.insert("end", "MY PERSONAL LIBRARY\n")
        self.books_display.insert("end", "=" * 55 + "\n")
        self.books_display.insert("end", f"Total Books: {len(self.books)}\n\n")
        
        for book_id, info in self.books.items():
            status_icon = "[R]" if info["status"] == "Read" else "[U]"
            self.books_display.insert("end", f"{status_icon} ID: {book_id}\n")
            self.books_display.insert("end", f"   Title : {info['title']}\n")
            self.books_display.insert("end", f"   Author: {info['author']}\n")
            self.books_display.insert("end", f"   Year  : {info['year']}\n")
            self.books_display.insert("end", f"   Status: {info['status']}\n")
            self.books_display.insert("end", "-" * 40 + "\n")
        
        self.update_statistics()
        self.search_entry.delete(0, 'end')
    
    def update_statistics(self):
        """Update library statistics (Show Statistics)"""
        total_books = len(self.books)
        read_books = len([b for b in self.books.values() if b["status"] == "Read"])
        unread_books = total_books - read_books
        
        current_year = 2024
        recent_books = len([b for b in self.books.values() if b["year"] >= current_year - 5])
        classic_books = total_books - recent_books
        
        stats_text = f"TOTAL: {total_books}  |  READ: {read_books}  |  UNREAD: {unread_books}"
        
        if total_books > 0:
            progress = (read_books/total_books)*100
            stats_text += f"  |  PROGRESS: {progress:.1f}%"
        
        stats_text += f"\nRECENT BOOKS (last 5 years): {recent_books}  |  CLASSIC BOOKS: {classic_books}"
        
        self.stats_label.configure(text=stats_text)
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.id_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.author_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.search_entry.delete(0, 'end')
        self.status_var.set("Unread")


# ============================================================================
# PART 4: GUI VERSION MAIN FUNCTION
# ============================================================================

def gui_main():
    """GUI version main function"""
    root = ctk.CTk()
    app = LibraryManagerGUI(root)
    root.mainloop()


# ============================================================================
# PART 5: MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("   PERSONAL LIBRARY MANAGER")
    print("=" * 50)
    print("\nKaunsa version run karna chahte ho?")
    print("1. CLI Version (Terminal - Tera original code)")
    print("2. GUI Version (Modern Window)")
    print("=" * 30)
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        cli_main()
    elif choice == "2":
        try:
            gui_main()
        except Exception as e:
            print(f"\nError: {e}")
            print("Make sure customtkinter is installed:")
            print("python -m pip install customtkinter")
    else:
        print("Invalid choice! Running CLI version...")
        cli_main()