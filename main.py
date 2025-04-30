import streamlit as st
import json
import os

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "book_data.json"
        self.read_from_file()

    def read_from_file(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                try:
                    self.book_list = json.load(file)
                except json.JSONDecodeError:
                    self.book_list = []
        else:
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, book):
        self.book_list.append(book)
        self.save_to_file()

    def delete_book(self, index):
        if 0 <= index < len(self.book_list):
            del self.book_list[index]
            self.save_to_file()


# ---------- Streamlit UI ----------
def main():
    st.title("📚 Book Collection Manager")

    collection = BookCollection()

    menu = ["View Books", "Add Book", "Delete Book"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Books":
        st.subheader("📖 Your Book Collection")
        if not collection.book_list:
            st.info("No books found. Try adding some!")
        else:
            for idx, book in enumerate(collection.book_list):
                st.markdown(f"**{idx + 1}. {book['title']}** by {book['author']} ({book['year']})")
                st.markdown(f"Genre: *{book['genre']}* — {'✅ Read' if book['read'] else '❌ Not Read'}")
                st.markdown("---")

    elif choice == "Add Book":
        st.subheader("➕ Add a New Book")
        with st.form("add_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            year = st.text_input("Publication Year")
            genre = st.text_input("Genre")
            read = st.selectbox("Have you read it?", ["No", "Yes"])
            submitted = st.form_submit_button("Add Book")

            if submitted:
                if title and author and year and genre:
                    if not year.isdigit():
                        st.error("Year must be a number.")
                    else:
                        book = {
                            "title": title,
                            "author": author,
                            "year": year,
                            "genre": genre,
                            "read": read == "Yes"
                        }
                        collection.add_book(book)
                        st.success(f"Added '{title}' to your collection!")
                        st.experimental_rerun()
                else:
                    st.warning("Please fill in all fields.")

    elif choice == "Delete Book":
        st.subheader("❌ Delete a Book")
        if not collection.book_list:
            st.info("No books to delete.")
        else:
            book_titles = [f"{book['title']} by {book['author']}" for book in collection.book_list]
            selected = st.selectbox("Select a book to delete", book_titles)
            if st.button("Delete"):
                index = book_titles.index(selected)
                collection.delete_book(index)
                st.success("Book deleted.")
                st.experimental_rerun()

if __name__ == "__main__":
    main()
