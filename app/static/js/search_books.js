async function searchBooks() {
    const keyword = document.getElementById("search").value.trim();

    if (!keyword) return;

    try {
        const response = await fetch(
            `/api/books/search?q=${encodeURIComponent(keyword)}`
        );

        const books = await response.json();

        let html = "";

        if (books.length === 0) {
            html = `
                <div class="alert alert-warning">
                    No books found.
                </div>
            `;
        } else {
            books.forEach((book) => {
                const image =
                    book.image_url ||
                    "https://via.placeholder.com/100x140?text=Book";

                html += `
                    <div class="card mb-3 shadow-sm">
                        <div class="row g-0">
                            <div class="col-4 col-sm-3 col-md-2 text-center p-2">
                                <img
                                    src="${image}"
                                    class="img-fluid rounded book-cover"
                                    alt="${book.title}"
                                    onerror="this.src='https://via.placeholder.com/100x140?text=Book'"
                                >
                            </div>

                            <div class="col-8 col-sm-9 col-md-10">
                                <div class="card-body">
                                    <h5 class="card-title mb-2">
                                        ${book.title}
                                    </h5>

                                    <p class="mb-1 book-meta">
                                        <strong>Author:</strong>
                                        ${book.author || "-"}
                                    </p>

                                    <p class="mb-1 book-meta">
                                        <strong>Shelf:</strong>
                                        ${book.shelf_code || "-"}
                                    </p>

                                    <p class="mb-0 book-meta">
                                        <strong>Available:</strong>
                                        ${book.available_quantity}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
        }

        document.getElementById("results").innerHTML = html;
    } catch (error) {
        console.error("Search failed:", error);

        document.getElementById("results").innerHTML = `
            <div class="alert alert-danger">
                Something went wrong while searching.
            </div>
        `;
    }
}