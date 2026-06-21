async function requestRenewal(borrowId) {

    try {

        const response = await fetch("/api/renew-request", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                borrow_id: parseInt(borrowId),
                requested_days: 7
            })
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message || "Renewal request failed");
        }

    } catch (err) {
        console.error(err);
        alert("Error sending renewal request");
    }
}

document.querySelectorAll(".renew-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        requestRenewal(this.dataset.borrowId);
    });
});