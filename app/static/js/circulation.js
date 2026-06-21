
async function loadBooks() {

    const response =
        await fetch("/api/books");

    const books =
        await response.json();

    const list =
        document.getElementById("book_list");

    books.forEach(book => {

        const option =
            document.createElement("option");

        option.value =
            `${book.title} (ID:${book.id})`;

        list.appendChild(option);

    });

}

loadBooks();


document
.getElementById("borrowForm")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const selected =
        document.getElementById("book_search").value;

    const match =
        selected.match(/ID:(\d+)/);

    if (!match) {
        alert("Please select a valid book from the list.");
        return;
    }

    const book_id =
        parseInt(match[1]);

    const response =
        await fetch("/api/borrow", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({

                university_id:
                    document.getElementById("university_id").value,

                book_id: book_id,

                borrow_days:
                    parseInt(
                        document.getElementById("borrow_days").value
                    )

            })
        });

    const data =
        await response.json();

    alert(data.message);
});


document
.getElementById("returnForm")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const response =
        await fetch("/api/return", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({

                borrow_id:
                    parseInt(
                        document.getElementById("borrow_id").value
                    )

            })
        });

    const data =
        await response.json();

    alert(data.message || "Returned");
});
