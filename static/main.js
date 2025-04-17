function OpenAddUserModal() {
    const modal = document.getElementById("addUserModal");
    modal.style.display = "block"; // Show the modal
}

// document.getElementById("closeModal").onclick = function () {
//     const modal = document.getElementById("addUserModal");
//     modal.style.display = "none"; // Hide the modal
// };

function ViewUsers() {
    // Logic to view users
    window.location.href = "/admin/view_users";
}

window.addEventListener("error", function (event) {
    fetch("/log-js-error", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: event.message,
        source: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack
      })
    });
  });
  