    // Bootstrap validation
    (function() {
        'use strict'

        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
            .forEach(function(form) {
                form.addEventListener('submit', function(event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }

                    form.classList.add('was-validated')
                }, false)
            })
    })()



    // Function to hide the success message after 3 seconds
    function hideSuccessMessage() {
        var message = document.getElementById("message");
        if (message) {
            setTimeout(function() {
                message.style.display = "none";
            }, 3000); // 3000 milliseconds (3 seconds)
        }
    }

    // Call the function when the page loads
    window.onload = hideSuccessMessage;








    // Get references to the buttons and confirmation box
    const deleteButtons = document.querySelectorAll(".show_confirm_delete");
    const confirmationBox = document.querySelector(".confirm_delete");
    const cancelDeleteButton = document.querySelector(".cancel_delete");
    const confirmDeleteButton = document.querySelector("#confirm_delete");
    // Add a click event listener to the delete button
    deleteButtons.forEach((deleteButton) => {
        deleteButton.addEventListener("click", function() {
            confirmationBox.classList.toggle("show_confirm_delete")
        });
    })

    // Add a click event listener to the cancel button
    cancelDeleteButton.addEventListener("click", function() {
        // Hide the confirmation box
        confirmationBox.classList.remove("show_confirm_delete")
    });

    // Add a click event listener to the confirm delete button
    confirmDeleteButton.addEventListener("click", function() {
        // Perform the delete operation here (e.g., send an AJAX request)
        // Once the delete operation is successful, you can hide the confirmation box
        confirmationBox.classList.toggle("show_confirm_delete")
    });