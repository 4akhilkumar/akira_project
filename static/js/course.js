$('.course-btn').click(function() {
    $(this).attr('disabled', true);
    $(this).val('Please wait...');
    $(this).closest('form').submit();
});

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
        $("textarea").each(function () {
            var $input = $(this);
            var $parent = $input.closest(".input-box");
            if ($input.val()) $parent.addClass("focus");
           else $parent.removeClass("focus");
        });
    }
}

$(document).ready(function() {
    $("#course-btn").prop("disabled", true);
    var course_btn = false;

    var code = false; var name = false;
    var description = false;
    var branch = false; var semester = false;
    var specialization = false; var faculty = false;

    $('#id_course_code').on('keyup keydown blur change', function() {
        if ($("#id_course_code").val() == "") {
            $("#id_course_code").parent().find(".error-text").css("display", "block");
            code = false;
        } else if (!/^[A-Za-z0-9-\s]*$/.test($("#id_course_code").val())) {
            $("#id_course_code").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course code correctly&#x0003F;");
            $("#id_course_code").parent().find(".error-text").css("display", "block");
            code = false;
        } else {
            $("#id_course_code").parent().find(".error-text").css("display", "none");
            code = true;
        }
    });

    $('#id_course_name').on('keyup keydown blur change', function() {
        if($("#id_course_name").val() == "") {
            $("#id_course_name").parent().find(".error-text").html("Enter the course name");
            $("#id_course_name").parent().find(".error-text").css("display", "block");
            name = false;
        }
        else if (!$("#id_course_name").val().match(/^[A-Za-z&\-\s]*$/)) {
            $("#id_course_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course name correctly&#x0003F;");
            $("#id_course_name").parent().find(".error-text").css("display", "block");
            name = false;
        }
        else if ($("#id_course_name").val().match(/^\s+$/)) {
            $("#id_course_name").parent().find(".error-text").html("Sorry, but the course name cannot be empty");
            $("#id_course_name").parent().find(".error-text").css("display", "block");
            name = false;
        }
        else {
            $("#id_course_name").parent().find(".error-text").css("display", "none");
            name = true;
        }
    });

    $('#id_course_desc').on('keyup keydown change', function() {
        if (!$("#id_course_desc").val().match(/^\s+$/)) {
            var chars = $('#id_course_desc').val().length;
            var max = $('#id_course_desc').attr('maxlength');
            var remaining = max - chars;
            var char_text = remaining == 1 ? 'character' : 'characters';
            $('#id_course_desc').parent().find(".help-text").css("display", "none");
            $('#id_course_desc').parent().find(".info-text").html("You have " + remaining + " " + char_text + " remaining");
            $('#id_course_desc').parent().find(".info-text").css("display", "block");
        }
    });

    $('#id_course_desc').on('keyup keydown blur change', function() {
        if($("#id_course_desc").val() == "") {
            $("#id_course_desc").parent().find(".error-text").html("Enter the course description");
            $("#id_course_desc").parent().find(".error-text").css("display", "block");
            description = false;
        }
        else if (!$("#id_course_desc").val().match(/^[A-Za-z0-9-/\s]*$/)) {
            $("#id_course_desc").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course description correctly&#x0003F;");
            $("#id_course_desc").parent().find(".error-text").css("display", "block");
            description = false;
        }
        else if ($("#id_course_desc").val().match(/^\s+$/)) {
            $("#id_course_desc").parent().find(".error-text").html("Sorry, but the course description cannot be empty");
            $("#id_course_desc").parent().find(".error-text").css("display", "block");
            description = false;
        }        
        else if ($("#id_course_desc").val().length > 500) {
            $("#id_course_desc").parent().find(".error-text").html("Sorry, but the course description cannot be more than 500 characters");
            $("#id_course_desc").parent().find(".error-text").css("display", "block");
            description = false;
        }
        else {
            $("#id_course_desc").parent().find(".error-text").css("display", "none");
            description = true;
        }
    });

    $('#id_branch').on('keyup keydown blur change', function() {
        if ($("#id_branch").val() == "") {
            $("#id_branch").parent().find(".error-text").css("display", "block");
            branch = false;
        } else {
            $("#id_branch").parent().find(".error-text").css("display", "none");
            branch = true;
        }
    });

    $('#id_semester').on('keyup keydown blur change', function() {
        if ($("#id_semester").val() == "") {
            $("#id_semester").parent().find(".error-text").css("display", "block");
            semester = false;
        } else {
            $("#id_semester").parent().find(".error-text").css("display", "none");
            semester = true;
        }
    });

    $('#id_specialization').on('keyup keydown blur change', function() {
        if ($("#id_specialization").val() == "") {
            $("#id_specialization").parent().find(".error-text").css("display", "block");
            specialization = false;
        } else {
            $("#id_specialization").parent().find(".error-text").css("display", "none");
            specialization = true;
        }
    });

    $('#id_course_coordinator').on('keyup keydown blur change', function() {
        if ($("#id_course_coordinator").val() == "") {
            $("#id_course_coordinator").parent().find(".error-text").css("display", "block");
            faculty = false;
        } else {
            $("#id_course_coordinator").parent().find(".error-text").css("display", "none");
            faculty = true;
        }
    });

    $('input, select, textarea').on('keyup keydown blur change', function() {
        if (code == true && name == true && description == true && branch == true && semester == true && specialization == true && faculty == true) {
            course_btn = true;
        }
        else {
            course_btn = false;
        }
        if (course_btn == true) {
            $("#course-btn").prop("disabled", false);
        }
        else {
            $("#course-btn").prop("disabled", true);
        }
    });
});