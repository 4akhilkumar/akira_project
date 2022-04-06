$('.register-btn').click(function() {
    $(this).prop('disabled', true);
    $(this).html('Please wait...');
    $(this).closest('form').submit();
});

$('#id_show_password').change(function() {
    if ($(this).is(':checked')) {
        $('#id_password').prop('type', 'text');
        $('#id_confirm_password').prop('type', 'text');
    } else {
        $('#id_password').prop('type', 'password');
        $('#id_confirm_password').prop('type', 'password');
    }
});

function setMinMaxDateOfBirth() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var fiftyYrsAgo = today.getFullYear() - 50;
    var eighteenYrsAgo = today.getFullYear() - 18;

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    }

    fiftyYrsAgo = fiftyYrsAgo + '-' + mm + '-' + dd;
    eighteenYrsAgo = eighteenYrsAgo + '-' + mm + '-' + dd;
    document.getElementById("id_date_of_birth").setAttribute("min", fiftyYrsAgo);
    document.getElementById("id_date_of_birth").setAttribute("max", eighteenYrsAgo);
}

window.onload = setMinMaxDateOfBirth();

function setFocus(on) {
    var element = document.activeElement;
    if (on) {
        setTimeout(function () {
        element.parentNode.classList.add("focus");
        });
    } else {
        let box = document.querySelector(".input-box");
        box.classList.remove("focus");
        $("input").each(function () {
        var $input = $(this);
        var $parent = $input.closest(".input-box");
        if ($input.val()) $parent.addClass("focus");
        else $parent.removeClass("focus");
        });
    }
}

$(document).ready(function() {
    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    // var steps = $("fieldset").length;
    
    $("#personal-next").prop("disabled", true);
    var personal_next_btn = false;

    var nameprefix = false; var firstname = false; var lastname = false; var dateofbirth = false;
    var gender = false; var phone = false; var doorno = false; var zipcode = false;
    var city = false; var district = false; var state = false; var country = false;
    var photo = false;

    $('#id_name_prefix').on('keyup keydown blur change', function() {
        if ($("#id_name_prefix").val() == "") {
            $("#id_name_prefix").parent().find(".error-text").css("display", "block");
            nameprefix = false;
        } else {
            $("#id_name_prefix").parent().find(".error-text").css("display", "none");
            nameprefix = true;
        }
    });

    $('#id_firstname').on('keyup keydown blur change', function() {
        if($("#id_firstname").val() == "") {
            $("#id_firstname").parent().find(".error-text").html("Enter your first name");
            $("#id_firstname").parent().find(".error-text").css("display", "block");
            firstname = false;
        }
        else if (!$("#id_firstname").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_firstname").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your name correctly&#x0003F;");
            $("#id_firstname").parent().find(".error-text").css("display", "block");
            firstname = false;
        }
        else if ($("#id_firstname").val().match(/^\s+$/)) {
            $("#id_firstname").parent().find(".error-text").html("Sorry, but your first name cannot be empty");
            $("#id_firstname").parent().find(".error-text").css("display", "block");
            firstname = false;
        }
        else {
            $("#id_firstname").parent().find(".error-text").css("display", "none");
            firstname = true;
        }
    });

    $('#id_lastname').on('keyup keydown blur change', function() {
        if($("#id_lastname").val() == "") {
            $("#id_lastname").parent().find(".error-text").html("Enter your last name");
            $("#id_lastname").parent().find(".error-text").css("display", "block");
            lastname = false;
        }
        else if (!$("#id_lastname").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_lastname").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your surname correctly&#x0003F;");
            $("#id_lastname").parent().find(".error-text").css("display", "block");
            lastname = false;
        }
        else if ($("#id_lastname").val().match(/^\s+$/)) {
            $("#id_lastname").parent().find(".error-text").html("Sorry, but your last name cannot be empty");
            $("#id_lastname").parent().find(".error-text").css("display", "block");
            lastname = false;
        }
        else {
            $("#id_lastname").parent().find(".error-text").css("display", "none");
            lastname = true;
        }
    });

    $('#id_date_of_birth').on('keyup keydown blur change', function() {
        if ($("#id_date_of_birth").val() == "") {
            $("#id_date_of_birth").parent().find(".error-text").css("display", "block");
            dateofbirth = false;
        }
        else {
            $("#id_date_of_birth").parent().find(".error-text").css("display", "none");
            dateofbirth = true;
        }
    });

    $('#id_gender').on('keyup keydown blur change', function() {
        if ($("#id_gender").val() == "") {
            $("#id_gender").parent().find(".error-text").css("display", "block");
            gender = false;
        } else {
            $("#id_gender").parent().find(".error-text").css("display", "none");
            gender = true;
        }
    });

    $('#id_phone').on('keyup keydown blur change', function() {
        if ($("#id_phone").val() == "") {
            $("#id_phone").parent().find(".error-text").html("Enter your phone number");
            $("#id_phone").parent().find(".error-text").css("display", "block");
            phone = false;
        }
        else if (!/^\d{10}$/.test($("#id_phone").val())) {
            $("#id_phone").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your phone no. correctly&#x0003F;");
            $("#id_phone").parent().find(".error-text").css("display", "block");
            phone = false;
        }
        else {
            $("#id_phone").parent().find(".error-text").css("display", "none");
            phone = true;
        }
    });

    $('#id_door_no').on('keyup keydown blur change', function() {
        if ($("#id_door_no").val() == "") {
            $("#id_door_no").parent().find(".error-text").css("display", "block");
            doorno = false;
        }
        else if (!/^[A-Za-z0-9-/\s]*$/.test($("#id_door_no").val())) {
            $("#id_door_no").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your door no./flat no. correctly&#x0003F;");
            $("#id_door_no").parent().find(".error-text").css("display", "block");
            doorno = false;
        }
        else if ($("#id_door_no").val().match(/^\s+$/)) {
            $("#id_door_no").parent().find(".error-text").html("Sorry, but your door no./flat no. cannot be empty");
            $("#id_door_no").parent().find(".error-text").css("display", "block");
            doorno = false;
        }
        else {
            $("#id_door_no").parent().find(".error-text").css("display", "none");
            doorno = true;
        }
    });

    $('#id_zip_code').on('keyup keydown blur change', function() {
        if ($("#id_zip_code").val() == "") {
            $("#id_zip_code").parent().find(".error-text").css("display", "block");
            zipcode = false;
            reset_fields();
        }
        else if (!/^\d{6}$/.test($("#id_zip_code").val())) {
            $("#id_zip_code").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your zip code correctly&#x0003F;");
            $("#id_zip_code").parent().find(".error-text").css("display", "block");
            zipcode = false;
            reset_fields();
        }
        else {
            $("#id_zip_code").parent().find(".error-text").css("display", "none");
            zipcode = true;
        }
    });

    function reset_fields() {
        $("#id_zip_code").parent().find(".error-text").html("Enter a valid zip code");
        $("#id_zip_code").parent().find(".error-text").css("display", "block");

        $("#id_city").html('<option value="">Select your City</option>');
        
        $("#id_district").parent().removeClass("focus");
        $("#id_district").val("");
        $("#id_district").prop("readonly", false);
        
        $("#id_state").parent().removeClass("focus");
        $("#id_state").val("");
        $("#id_state").prop("readonly", false);
        
        $("#id_country").parent().removeClass("focus");
        $("#id_country").val("");
        $("#id_country").prop("readonly", false);
    }

    function changeSelectInputCity() {
        var city_parent = $("#id_city_parent").get(0);
        city_parent.classList.remove("active-grey");
    
        var select_city = $("#id_city").get(0);
        select_city.setAttribute("hidden", '');

        var new_city = $("#id_new_city").get(0);
        new_city.removeAttribute("hidden");
    }

    $('#id_zip_code').on('keyup', function() {
        if(zipcode == true) {
            var dataByZipCode = $.getJSON("https://api.postalpincode.in/pincode/" + $("#id_zip_code").val(), function (data) {
                if (data[0].Status == "Success") {
                    let html_data = '<option value="">Select your City</option>';
                    for (let i = 0; i < data[0].PostOffice.length; i++) {
                        html_data += '<option value="' + data[0].PostOffice[i].Name + '">' + data[0].PostOffice[i].Name + '</option>';
                    }
                    $("#id_city").html(html_data);
                    city = true;

                    if (data[0].PostOffice[0].District != "" || data[0].PostOffice[0].District != null) {
                        $("#id_district").parent().addClass("focus");
                        $("#id_district").val(data[0].PostOffice[0].District);
                        $("#id_district").prop("readonly", true);
                        district = true;
                    }

                    if (data[0].PostOffice[0].District != "" || data[0].PostOffice[0].District != null) {
                        $("#id_state").parent().addClass("focus");
                        $("#id_state").val(data[0].PostOffice[0].State);
                        $("#id_state").prop("readonly", true);
                        state = true;
                    }

                    if (data[0].PostOffice[0].District != "" || data[0].PostOffice[0].District != null) {
                        $("#id_country").parent().addClass("focus");
                        $("#id_country").val(data[0].PostOffice[0].Country);
                        $("#id_country").prop("readonly", true);
                        country = true;
                    }
                    return;
                }
                else {
                    reset_fields();
                }
            })
            dataByZipCode.fail(function(data) {
            changeSelectInputCity();
            })
        }
    });

    $('#id_city').on('keyup keydown blur change', function() {
        if ($("#id_city").val() == "") {
            $("#id_city").parent().find(".error-text").css("display", "block");
            city = false;
        }
        else {
            $("#id_city").parent().find(".error-text").css("display", "none");
            city = true;
        }
    });

    $('#id_new_city').on('keyup keydown blur change', function() {
        if ($("#id_new_city").val() == "") {
            $("#id_new_city").parent().find(".error-text").html("Enter your city");
            $("#id_new_city").parent().find(".error-text").css("display", "block");
            city = false;
        }
        else if (!$("#id_new_city").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_new_city").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your city name correctly&#x0003F;");
            $("#id_new_city").parent().find(".error-text").css("display", "block");
            city = false;
        }
        else if ($("#id_new_city").val().match(/^\s+$/)) {
            $("#id_new_city").parent().find(".error-text").html("Sorry, but your city name cannot be empty");
            $("#id_new_city").parent().find(".error-text").css("display", "block");
            city = false;
        }
        else {
            $("#id_new_city").parent().find(".error-text").css("display", "none");
            city = true;
        }
    });

    $('#id_district').on('keyup keydown blur change', function() {
        if ($("#id_district").val() == "") {
            $("#id_district").parent().find(".error-text").css("display", "block");
            district = false;
        }
        else if (!$("#id_district").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_district").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your district name correctly&#x0003F;");
            $("#id_district").parent().find(".error-text").css("display", "block");
            district = false;
        }
        else if ($("#id_district").val().match(/^\s+$/)) {
            $("#id_district").parent().find(".error-text").html("Sorry, but your district name cannot be empty");
            $("#id_district").parent().find(".error-text").css("display", "block");
            district = false;
        }
        else {
            $("#id_district").parent().find(".error-text").css("display", "none");
            district = true;
        }
    });

    $('#id_state').on('keyup keydown blur change', function() {
        if ($("#id_state").val() == "") {
            $("#id_state").parent().find(".error-text").css("display", "block");
            state = false;
        }
        else if (!$("#id_state").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_state").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your state name correctly&#x0003F;");
            $("#id_state").parent().find(".error-text").css("display", "block");
            state = false;
        }
        else if ($("#id_state").val().match(/^\s+$/)) {
            $("#id_state").parent().find(".error-text").html("Sorry, but your state name cannot be empty");
            $("#id_state").parent().find(".error-text").css("display", "block");
            state = false;
        }
        else {
            $("#id_state").parent().find(".error-text").css("display", "none");
            state = true;
        }
    });

    $('#id_country').on('keyup keydown blur change', function() {
        if ($("#id_country").val() == "") {
            $("#id_country").parent().find(".error-text").css("display", "block");
            country = false;
        }
        else if (!$("#id_country").val().match(/^[A-Za-z\s]*$/)) {
            $("#id_country").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your country name correctly&#x0003F;");
            $("#id_country").parent().find(".error-text").css("display", "block");
            country = false;
        }
        else if ($("#id_country").val().match(/^\s+$/)) {
            $("#id_country").parent().find(".error-text").html("Sorry, but your country name cannot be empty");
            $("#id_country").parent().find(".error-text").css("display", "block");
            country = false;
        }
        else {
            $("#id_country").parent().find(".error-text").css("display", "none");
            country = true;
        }
    });

    $('#id_photo').on('keyup keydown blur change', function() {
        if ($("#id_photo").val() == "") {
            $("#id_photo").parent().find(".error-text").css("display", "block");
            photo = false;
        } else {
            $("#id_photo").parent().find(".error-text").css("display", "none");
            photo = true;
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (nameprefix == true && firstname == true && lastname == true && dateofbirth == true && gender == true && phone == true && doorno == true && zipcode == true && city == true && district == true && state == true && country == true && photo == true) {
            personal_next_btn = true;
        }
        else {
            personal_next_btn = false;
        }
        if (personal_next_btn == true) {
            $("#personal-next").prop("disabled", false);
        }
        else {
            $("#personal-next").prop("disabled", true);
        }
    });

    $("#account-next").prop("disabled", true);
    var account_next_btn = false;
    var email = false; var username = false; 
    var password = false; var confirmpassword = false;

    $('#id_email').on('keyup keydown blur change', function() {
        if ($("#id_email").val() == "") {
            $("#id_email").parent().find(".error-text").css("display", "block");
            email = false;
        }
        else if (!$("#id_email").val().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/)) {
            $("#id_email").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your email address correctly&#x0003F;");
            $("#id_email").parent().find(".error-text").css("display", "block");
            email = false;
        }
        else if ($("#id_email").val().match(/^\s+$/)) {
            $("#id_email").parent().find(".error-text").html("Sorry, but your email cannot be empty");
            $("#id_email").parent().find(".error-text").css("display", "block");
            email = false;
        }
        else {
            $("#id_email").parent().find(".error-text").css("display", "none");
            email = true;
        }
    });

    $('#id_username').on('keyup keydown blur change', function() {
        if ($("#id_username").val() == "") {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Enter your username");
            username = false;
        }
        else if ($("#id_username").val().length < 6) {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Username must be minimum of 6 characters");
            username = false;
        }
        // if user name contains any period then it should be only one time and it should not be at the beginning or at the end of the string
        else if ($("#id_username").val().match(/\./g) && $("#id_username").val().match(/\./g).length > 1) {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Username should contain only one period");
            username = false;
        }
        else if ($("#id_username").val().match(/^\./)) {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Username should not start with period");
            username = false;
        }
        else if ($("#id_username").val().match(/\.$/)) {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Username should not end with period");
            username = false;
        }
        else if (!$("#id_username").val().match(/^[a-zA-Z0-9\.]*$/)) {
            $("#id_username").parent().find(".error-text").css("display", "block");
            $("#id_username").parent().find(".error-text").html("Sorry, only letters (a-z), numbers (0-9), and periods (.) are allowed.");
            username = false;
        }
        else if ($("#id_username").val().match(/^\s+$/)) {
            $("#id_username").parent().find(".error-text").html("Sorry, but your username cannot be empty");
            $("#id_username").parent().find(".error-text").css("display", "block");
            username = false;
        }
        else {
            $("#id_username").parent().find(".error-text").css("display", "none");
            username = true;
        }
    });

    $('#id_password').on('keyup keydown blur change', function() {
        if ($("#id_password").val() == "") {
            $("#id_password").parent().find(".error-text").css("display", "block");
            $("#id_password").parent().find(".error-text").html("Enter your password");
            password = false;
        }
        else if (!$("#id_password").val().match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#])[A-Za-z\d!@#]{8,18}/)) {
            $("#id_password").parent().find(".error-text").html("Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character [!, @, #]");
            $("#id_password").parent().find(".error-text").css("display", "block");
            password = false;
        }
        else {
            $("#id_password").parent().find(".error-text").css("display", "none");
            password = true;
        }
    });

    $('#id_confirm_password').on('keyup keydown blur change', function() {
        if ($("#id_confirm_password").val() != $("#id_password").val()) {
            $("#id_confirm_password").parent().find(".error-text").html("Those passwords didn&#x00027;t match. Try again.");
            $("#id_confirm_password").parent().find(".error-text").css("display", "block");
            confirmpassword = false;
        }
        else {
            $("#id_confirm_password").parent().find(".error-text").css("display", "none");
            confirmpassword = true;
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (email == true && username == true && password == true && confirmpassword == true) {
            account_next_btn = true;
        }
        else {
            account_next_btn = false;
        }
        if (account_next_btn == true) {
            $("#account-next").prop("disabled", false);
        }
        else {
            $("#account-next").prop("disabled", true);
        }
    });

    $("#institute-next").prop("disabled", true);
    var institute_next_btn = false;
    var institutecode = false; var institutename = false; var instituteaddress = false;

    $('#id_institute_code').on('keyup keydown blur change', function() {
        if ($("#id_institute_code").val() == "") {
            $("#id_institute_code").parent().find(".error-text").html("Enter your institute code");
            $("#id_institute_code").parent().find(".error-text").css("display", "block");
            institutecode = false;
        }
        else if (!$("#id_institute_code").val().match(/^[A-Za-z0-9-\s]*$/)) {
            $("#id_institute_code").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your institute code correctly&#x0003F;");
            $("#id_institute_code").parent().find(".error-text").css("display", "block");
            institutecode = false;
        }
        else if ($("#id_institute_code").val().match(/^\s+$/)) {
            $("#id_institute_code").parent().find(".error-text").html("Sorry, but your institute code cannot be empty");
            $("#id_institute_code").parent().find(".error-text").css("display", "block");
            institutecode = false;
        }
        else {
            $("#id_institute_code").parent().find(".error-text").css("display", "none");
            institutecode = true;
        }
    });

    $('#id_institute_name').on('keyup keydown blur change', function() {
        if ($("#id_institute_name").val() == "") {
            $("#id_institute_name").parent().find(".error-text").css("display", "block");
            institutename = false;
        }
        else if(!$("#id_institute_name").val().match(/^[a-z0-9\d\-_\s]+$/i)) {
            $("#id_institute_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your institute name correctly&#x0003F;");
            $("#id_institute_name").parent().find(".error-text").css("display", "block");
            institutename = false;
        }
        else if ($("#id_institute_name").val().match(/^\s+$/)) {
            $("#id_institute_name").parent().find(".error-text").html("Sorry, but your institute name cannot be empty");
            $("#id_institute_name").parent().find(".error-text").css("display", "block");
            institutename = false;
        }
        else {
            $("#id_institute_name").parent().find(".error-text").css("display", "none");
            institutename = true;
        }
    });

    $('#id_institute_address').on('keyup keydown blur change', function() {
        if ($("#id_institute_address").val() == "") {
            $("#id_institute_address").parent().find(".error-text").css("display", "block");
            instituteaddress = false;
        }
        else if ($("#id_institute_address").val().length < 8) {
            $("#id_institute_address").parent().find(".error-text").html("Enter a valid address");
            $("#id_institute_address").parent().find(".error-text").css("display", "block");
            instituteaddress = false;
        }
        else if(!$("#id_institute_address").val().match(/^[a-z\d\-,_\s]+$/i)) {
            $("#id_institute_address").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered your institute address correctly&#x0003F;");
            $("#id_institute_address").parent().find(".error-text").css("display", "block");
            instituteaddress = false;
        }
        else if ($("#id_institute_address").val().match(/^\s+$/)) {
            $("#id_institute_address").parent().find(".error-text").html("Sorry, but your institute address cannot be empty");
            $("#id_institute_address").parent().find(".error-text").css("display", "block");
            instituteaddress = false;
        }
        else {
            $("#id_institute_address").parent().find(".error-text").css("display", "none");
            instituteaddress = true;
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (institutecode == true && institutename == true && instituteaddress == true) {
            institute_next_btn = true;
        }
        else {
            institute_next_btn = false;
        }
        if (institute_next_btn == true) {
            $("#institute-next").prop("disabled", false);
        }
        else {
            $("#institute-next").prop("disabled", true);
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (personal_next_btn && account_next_btn && institute_next_btn == true) {
            $("#register-btn").prop("disabled", false);
        }
        else {
            $("#register-btn").prop("disabled", true);
        }
    });

    $(".next").click(function() {
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //Add Class Active
        if ($(this).prop('id') == 'personal-next') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("account-section");
            $("body").removeClass();
            $("body").addClass("accountsection");
        } else if ($(this).prop('id') == 'account-next') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("institute-section");
            $("body").removeClass();
            $("body").addClass("institutesection");
        } else if ($(this).prop('id') == 'institute-next') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("tandc-section");
            $("body").removeClass();
            $("body").addClass("tandcsection");
        }

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
            }, duration: 500
        });


    });

    $(".previous").click(function(){
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //Remove class active
        if ($(this).prop('id') == 'account-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("account-section");
            $("body").removeClass();
            $("body").addClass("personalsection");
        } else if ($(this).prop('id') == 'institute-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("institute-section");
            $("body").removeClass();
            $("body").addClass("accountsection");
        } else if ($(this).prop('id') == 'tandc-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("tandc-section");
            $("body").removeClass();
            $("body").addClass("institutesection");
        }

        //show the previous fieldset
        previous_fs.show();

        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function(now) {
                // for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            }, duration: 500
        });
    });

    // If the user clicks the button class "last-next" then hide the class note and if user clicks the button class "last-previous" then show the class note
    $(".last-next").click(function(){
        $(".note").hide();
        // scroll page to bottom
        $('html, body').animate({
            scrollTop: $(document).height()
        }, 'slow');
    });
    
    $(".last-previous").click(function(){
        $(".note").show();
    });

});