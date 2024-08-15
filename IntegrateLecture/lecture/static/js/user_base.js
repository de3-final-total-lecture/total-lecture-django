document.addEventListener("DOMContentLoaded", function() {
    const deleteButton = document.querySelectorAll('.delete-btn');

    deleteButton.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const confirmation = confirm("정말로 탈퇴하시겠습니까?");

            if (confirmation) {
                this.closest('form').submit();
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const removeButtons = document.querySelectorAll(".remove-wishlist-item");

    removeButtons.forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            const listItem = this.closest(".wishlist-item");
            const lectureId = listItem.getAttribute("data-lecture-id")

            fetch("{% url 'wishlist_remove' pk=user.pk %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: JSON.stringify({ lecture: lectureId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    listItem.remove();
                    location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
});