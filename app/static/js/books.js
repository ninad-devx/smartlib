
        async function loadShelves() {
            try {
                const res = await fetch("/api/shelves");
                const shelves = await res.json();

                let html = `<option value="">Select Shelf</option>`;

                shelves.forEach(shelf => {
                    html += `
                <option value="${shelf.id}">
                    ${shelf.shelf_code}
                </option>
            `;
                });

                document.getElementById("shelf_id").innerHTML = html;

            } catch (err) {
                console.error("Failed to load shelves:", err);
            }
        }

        loadShelves();
        async function loadBooks() {
    try {
        const response = await fetch("/api/books");

        if (!response.ok) {
            console.error("Failed to load books");
            return;
        }

        const books = await response.json();

        let html = "";

        books.forEach(book => {

            const image = book.image_url
                ? book.image_url
                : "https://via.placeholder.com/60x90?text=Book";

            html += `
            <tr>
                <td>
                    <img
    src="${image}"
    width="60"
    height="90"
    style="object-fit:cover;border-radius:4px;"
    onerror="this.src='https://via.placeholder.com/60x90?text=Book'"
>
                </td>
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author || "-"}</td>
                <td>${book.available_quantity}</td>
            </tr>
            `;
        });

        document.getElementById("bookTable").innerHTML = html;

    } catch (err) {
        console.error("Error loading books:", err);
    }
}
        loadBooks();

        document.getElementById("bookForm").addEventListener("submit", async (e) => {
            e.preventDefault();

            const payload = {
    isbn: document.getElementById("isbn").value,
    title: document.getElementById("title").value,
    author: document.getElementById("author").value,
    publisher: document.getElementById("publisher").value,
    category: document.getElementById("category").value,
    shelf_id: parseInt(document.getElementById("shelf_id").value),
    quantity: parseInt(document.getElementById("quantity").value),
    image_url: document.getElementById("image_url").value
};

            try {
                const res = await fetch("/api/books", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                // 🔥 IMPORTANT: check backend response
                if (!res.ok) {
                    const errorText = await res.text();
                    console.error("BOOK CREATE FAILED:", errorText);
                    alert("Failed to add book. Check console.");
                    return;
                }

                const data = await res.json();
                console.log("SUCCESS:", data);

                alert("Book Added Successfully");

                loadBooks();

                document.getElementById("bookForm").reset();

            } catch (err) {
                console.error("Network error:", err);
                alert("Server not reachable");
            }
        });
