document
    .getElementById("registerForm")
    .addEventListener("submit", async function (e) {
        e.preventDefault();

        const submitBtn = this.querySelector("button");

        submitBtn.disabled = true;
        submitBtn.innerText = "Registering...";

        try {
            const response = await fetch("/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    university_id: document
                        .getElementById("university_id")
                        .value.trim(),

                    name: document
                        .getElementById("name")
                        .value.trim(),

                    email: document
                        .getElementById("email")
                        .value.trim(),

                    password: document
                        .getElementById("password")
                        .value,

                    department: document
                        .getElementById("department")
                        .value.trim(),

                    role: document
                        .getElementById("role")
                        .value,
                }),
            });

            const data = await response.json();

            if (data.success) {
                alert("Registration Successful");
                window.location.href = "/login";
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error("Registration failed:", error);
            alert("Registration failed. Please try again.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = "Register";
        }
    });