async function approveRenewal(renewalId) {
    try {
        const response = await fetch("/api/renew-approve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                renewal_id: renewalId,
            }),
        });

        const data = await response.json();

        alert(data.message);
    } catch (error) {
        console.error("Approval failed:", error);
        alert("Something went wrong.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".approve-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            approveRenewal(btn.dataset.renewalId);
        });
    });
});