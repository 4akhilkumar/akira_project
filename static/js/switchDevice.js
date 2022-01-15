const inputContainers = document.querySelectorAll(".app-input");

inputContainers.forEach((container) => {
    const input = container.querySelector("input");
    const events = ["focus", "blur"];

    events.forEach((event) => {
        input.addEventListener(event, () => {
            if (!input.value) {
                toggleClass(container, "input-active");
            }
        });
    });
});

function toggleClass(element, className) {
    const isActive = element.classList.contains(className);

    if (isActive) {
        element.classList.remove(className);
    } else {
        element.classList.add(className);
    }
}

// const submitButton = document.querySelector('.app-login-button');
// submitButton.disabled = true
// function isEmpty() {
//     let username = document.getElementById('id_username').value;

//     if (username.length > 7) {
//         submitButton.disabled = false;
//     }
//     else {
//         submitButton.disabled = true;
//     }
// }

$('.app-login-button').click(function() {
    $(this).attr('disabled', true);
    $('.app-input input').attr('readonly', true);
    $(this).html('<i class="fas fa-spinner fa-spin"></i>');
    $(this).closest('form').submit();
});