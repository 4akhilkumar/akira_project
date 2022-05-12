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

$(".toggle-password").click(function() {
    $(this).toggleClass("fa-eye-slash");
    input = $(this).parent().find("input");
    if (input.prop("type") == "password") {
        input.prop("type", "text");
    } else {
        input.prop("type", "password");
    }
});

function ValidateFormResponse() {
    if (username == true && password == true && recaptcha_response == true) {
        $(".app-login-button").prop("disabled", false);
    }
    else {
        $(".app-login-button").prop("disabled", true);
    }
}

$(".app-login-button").prop("disabled", true);
var username = false; var password = false; var recaptcha_response = false;

$('#id_username').on('keyup keydown blur change', function() {
    if ($("#id_username").val() == "") {
        username = false;
    }
    else if ($("#id_username").val().length < 6) {
        username = false;
    }
    else if ($("#id_username").val().match(/^\./)) {
        username = false;
    }
    else if ($("#id_username").val().match(/\.$/)) {
        username = false;
    }
    else if (!$("#id_username").val().match(/^[a-zA-Z0-9\.]*$/)) {
        username = false;
    }
    else if ($("#id_username").val().match(/^\s+$/)) {
        username = false;
    }
    else {
        username = true;
    }
    ValidateFormResponse();
});

$('#id_password').on('keyup keydown blur change', function() {
    if ($("#id_password").val() == "") {
        password = false;
    }
    else if (!$("#id_password").val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#])[A-Za-z\d!@#]{8,18}/)) {
        password = false;
    }
    else {
        password = true;
    }
    ValidateFormResponse();
});

function enableloginbtn() {
    recaptcha_response = true;
    ValidateFormResponse();
}

function disableloginbtn() {
    recaptcha_response = false;
    ValidateFormResponse();
}


$('.app-login-button').click(function() {
    $(this).prop('disabled', true);
    $('.app-input input').prop('readonly', true);
    $('.toggle-password').remove();
    if ($('#id_password').prop('type') != 'password') {
        $('#id_password').prop('type', 'password');
    }
    $(this).html('<i class="fas fa-spinner fa-spin"></i>');
    $(this).closest('form').submit();
});