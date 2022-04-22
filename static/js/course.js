var IGNORE_KEYS_LIST = [
    "Tab",
    "Escape",
    "Control",
    "Shift",
    "Alt",
    "CapsLock",
    "Enter",
    "Meta",
    "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "Home", "End", "Insert", "PageUp", "PageDown",
    "PrintScreen", "ScrollLock", "Pause", "NumLock", "LaunchApplication2"
];

function getAllCOTFunc() {
    if($(this).hasClass('anchor-disabled')){
        return false;
    }
    $(this).addClass('anchor-disabled');
    setTimeout(function(){
        $("#fetchcurrentcot").removeClass('anchor-disabled');
    }, 5000);

    var get_current_cot_url = $("#fetchcurrentcot").data('get-currentcot-url');
    var current_cot = $(this).data('current_course_id');

    $.ajax({
        type: "POST",
        url: get_current_cot_url,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'course_id': current_cot,
        },
        success: function (data) {
            if(data.length == 0) {
                html_data = '<option value=""> Data Not Available </option>';
                $("#id_current_course_cot").html(html_data);
                toastr.info("No COT available")
            }
            else {
                toastr.success("COT list fetched successfully")
                let html_data = '<option value=""> Select field for...? </option>';
                data.forEach(function (data) {
                    html_data += `<option value="${data.id}">${data.final_obj}</option>`
                });
                $("#id_current_course_cot").html(html_data);

                $("#id_current_course_cot").parent().find(".error-text").css("display", "block");
                $("#cotextrafield-btn").prop("disabled", true);
            }
        },
        error: function (data) {
            toastr.error(data);
        }
    });
}

// if user types in input,textarea data-cot-dynamic-field-value attribute value will be updated and print typed in console
$(document).on('keyup', 'input[data-dynamic-field-value], textarea[data-dynamic-field-value]', function(event) {
    var field_id = $(this).data('dynamic-field-value');
    var field_value = $('[data-dynamic-field-value="' + field_id + '"]').val();
    var setDynamicValueURL = $(this).data('set-dynamic-value-url');

    // If event.key is in IGNORE_KEYS_LIST then return false else true
    if(IGNORE_KEYS_LIST.includes(event.key)) {
        return false;
    }
    else {
        // If user type ctrl + A then return false
        if(event.ctrlKey && event.key == 'a' || event.ctrlKey && event.key == 'c') {
            return false;
        }

        // // If cursor is at beginning of textarea and user is typing backspace then return false
        // if($('[data-dynamic-field-value="' + field_id + '"]').get(0).selectionStart == 0 && event.key == 'Backspace') {
        //     return false;
        // }

        // if(field_value == '' && event.key == 'Backspace') {
        //     return false;
        // }
    }

    if(/^[a-zA-Z0-9!@#$%^&*()-=_+{}[\];':",./\\<>?|\s]*$/.test(field_value)) {
        $.ajax({
            type: "POST",
            url: setDynamicValueURL,
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'course_extra_field_id': field_id,
                'course_extra_field_value': field_value,
            },
            success: function (data) {
                if(data.status == 'success') {
                    // Change the style of span tag with data-cot-dynamic-value-id="field_id" to visible and change to none after 2 seconds
                    $('[data-cot-dynamic-value-id="' + field_id + '"]').css('display', 'contents');
                    setTimeout(function() {
                        $('[data-cot-dynamic-value-id="' + field_id + '"]').css('display', 'none');
                    }, 1400);
                    
                    // $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

});

// // If user clicked on anchor tag then get the data-save-dynamic-field_id attribute value
// $(document).on('click', 'a[data-save-dynamic-field_id]', function() {
//     var field_id = $(this).data('save-dynamic-field_id');
//     // Now get the value of the field having same value data-dynamic-field-value attribute 
//     var field_value = $('[data-dynamic-field-value="' + field_id + '"]').val();
    
//     // Now get the value in data-dynamic-field-value attribute of anchor tag
//     var setDynamicValueURL = $(this).data('set-dynamic-value-url');

//     $.ajax({
//         type: "POST",
//         url: setDynamicValueURL,
//         data: {
//             'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
//             'course_extra_field_id': field_id,
//             'course_extra_field_value': field_value,
//         },
//         success: function (data) {
//             if(data.status == 'success') {
//                 toastr.success(data.message)
//                 $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
//             }
//             else {
//                 toastr.warning(data.message)
//             }
//         },
//         error: function (data) {
//             toastr.error(data.message)
//         }
//     }); 
// });

$(document).on('click', 'a[data-delete-dynamic-field_id]', function() {
    var field_id = $(this).data('delete-dynamic-field_id');
    
    // Now get the value in data-dynamic-field-value attribute of anchor tag
    var deleteDynamicValueURL = $(this).data('delete-dynamic-value-url');

    $.ajax({
        type: "POST",
        url: deleteDynamicValueURL,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'course_extra_field_id': field_id,
        },
        success: function (data) {
            if(data.status == 'success') {
                toastr.success(data.message)
                $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
            }
            else {
                toastr.warning(data.message)
            }
        },
        error: function (data) {
            toastr.error(data.message)
        }
    }); 
});

// if user types in input,textarea data-cot-dynamic-field-value attribute value will be updated and print typed in console
$(document).on('keyup', 'input[data-cot-dynamic-field-value], textarea[data-cot-dynamic-field-value]', function(event) {
    var cot_field_id = $(this).data('cot-dynamic-field-value');
    var cot_field_value = $('[data-cot-dynamic-field-value="' + cot_field_id + '"]').val();
    var setCOTDynamicValueURL = $(this).data('set-cot-dynamic-value-url');

    // If event.key is in IGNORE_KEYS_LIST then return false else true
    if(IGNORE_KEYS_LIST.includes(event.key)) {
        return false;
    }
    else {
        // If user type ctrl + A then return false
        if(event.ctrlKey && event.key == 'a' || event.ctrlKey && event.key == 'c') {
            return false;
        }

        // // If cursor is at beginning of textarea and user is typing backspace then return false
        // if($('[data-cot-dynamic-field-value="' + cot_field_id + '"]').get(0).selectionStart == 0 && event.key == 'Backspace') {
        //     return false;
        // }

        // if(cot_field_value == '' && event.key == 'Backspace') {
        //     return false;
        // }
    }

    if(/^[a-zA-Z0-9!@#$%^&*()-=_+{}[\];':",./\\<>?|\s]*$/.test(cot_field_value)) {
        $.ajax({
            type: "POST",
            url: setCOTDynamicValueURL,
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'cot_extra_field_id': cot_field_id,
                'cot_extra_field_value': cot_field_value.trim(),
            },
            success: function (data) {
                if(data.status == 'success') {
                    // Change the style of span tag with data-ds-cot-dynamic-value-id="cot_field_id" to visible and change to none after 2 seconds
                    $('[data-ds-cot-dynamic-value-id="' + cot_field_id + '"]').css('display', 'contents');
                    setTimeout(function() {
                        $('[data-ds-cot-dynamic-value-id="' + cot_field_id + '"]').css('display', 'none');
                    }, 1400);
                    
                    // $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

});

// $(document).on('click', 'a[data-save-cot-dynamic-field_id]', function() {
//     var cot_field_id = $(this).data('save-cot-dynamic-field_id');
//     // Now get the value of the field having same value data-dynamic-field-value attribute 
//     var cot_field_value = $('[data-cot-dynamic-field-value="' + cot_field_id + '"]').val();
    
//     // Now get the value in data-dynamic-field-value attribute of anchor tag
//     var setCOTDynamicValueURL = $(this).data('set-cot-dynamic-value-url');

//     $.ajax({
//         type: "POST",
//         url: setCOTDynamicValueURL,
//         data: {
//             'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
//             'cot_extra_field_id': cot_field_id,
//             'cot_extra_field_value': cot_field_value,
//         },
//         success: function (data) {
//             if(data.status == 'success') {
//                 toastr.success(data.message)
//                 $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
//             }
//             else {
//                 toastr.warning(data.message)
//             }
//         },
//         error: function (data) {
//             toastr.error(data.message)
//         }
//     }); 
// });

$(document).on('click', 'a[data-delete-cot-dynamic-field_id]', function() {
    var cot_extra_field_id = $(this).data('delete-cot-dynamic-field_id');

    var deleteCOTExtraFieldURL = $(this).data('delete-cot-dynamic-value-url');

    $.ajax({
        type: "POST",
        url: deleteCOTExtraFieldURL,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'cot_extra_field_id': cot_extra_field_id,
        },
        success: function (data) {
            if(data.status == 'success') {
                toastr.success(data.message)
                $("#id_append_cot_external_fields").load(location.href + " #id_append_cot_external_fields");
            }
            else {
                toastr.warning(data.message)
            }
        },
        error: function (data) {
            toastr.error(data.message)
        }
    }); 
});

$(document).on('click', 'a[data-set-cot-field_id]', function() {
    var setCreatedCOTFieldID = $(this).data('set-cot-field_id');
    var created_cot_mos_value = $('[data-created-cot-mos="' + setCreatedCOTFieldID + '"]').val();
    var created_cot_ltps_value = $('[data-created-cot-ltps="' + setCreatedCOTFieldID + '"]').val();
    
    var setCreatedCOTFieldURL = $(this).data('set-cot-field-url');

    $.ajax({
        type: "POST",
        url: setCreatedCOTFieldURL,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'setCreatedCOTFieldID': setCreatedCOTFieldID,
            'created_cot_mos_value': created_cot_mos_value,
            'created_cot_ltps_value': created_cot_ltps_value,
        },
        success: function (data) {
            if(data.status == 'success') {
                toastr.success(data.message)
                var cotfield_btn_as_this = document.getElementsByClassName('get-all-current-cot')[0];
                getAllCOTFunc.call(cotfield_btn_as_this);
                $("#id_append_course_cot").load(location.href + " #id_append_course_cot");
                $("#id_append_cot_external_fields").load(location.href + " #id_append_cot_external_fields");
            }
            else {
                toastr.warning(data.message)
            }
        },
        error: function (data) {
            toastr.error(data.message)
        }
    }); 
});

$(document).on('click', 'a[data-delete-cot-field_id]', function() {
    var created_cot_field_id = $(this).data('delete-cot-field_id');

    var deleteCreatedCOTField = $(this).data('delete-cot-field-url');

    $.ajax({
        type: "POST",
        url: deleteCreatedCOTField,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'created_cot_field_id': created_cot_field_id,
        },
        success: function (data) {
            if(data.status == 'success') {
                toastr.success(data.message)
                var cotfield_btn_as_this = document.getElementsByClassName('get-all-current-cot')[0];
                getAllCOTFunc.call(cotfield_btn_as_this);
                $("#id_append_course_cot").load(location.href + " #id_append_course_cot");
                $("#id_append_cot_external_fields").load(location.href + " #id_append_cot_external_fields");
            }
            else {
                toastr.warning(data.message)
            }
        },
        error: function (data) {
            toastr.error(data.message)
        }
    }); 
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

// If user click on input with id=back-course then print clicked in console
$("#back-course").click(function () {
    // get the data-back-to-courses-url attribute of the clicked element
    var backToCourses = $(this).data('back-to-courses-url');
    // disable the button for 5 seconds
    $("#back-course").prop("disabled", true);
    setTimeout(function () {
        $("#back-course").prop("disabled", false);
    }, 5000);
    // return the user to the courses page
    window.location.href = backToCourses;
});

$(document).ready(function() {
    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;

    function nextFieldSet() {
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //Add Class Active
        if ($(this).prop('id') == 'create-design-course-next') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("account-section");
            $(".main-container-fluid").removeClass();
            $(".main-container-fluid").addClass("accountsection");
        } else if ($(this).prop('id') == 'account-next') {
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("institute-section");
            $(".main-container-fluid").removeClass();
            $(".main-container-fluid").addClass("institutesection");
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
    }

    function previousFieldSet() {
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //Remove class active
        if ($(this).prop('id') == 'account-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("account-section");
            $(".main-container-fluid").removeClass();
            $(".main-container-fluid").addClass("personalsection");
        } else if ($(this).prop('id') == 'institute-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("institute-section");
            $(".main-container-fluid").removeClass();
            $(".main-container-fluid").addClass("accountsection");
        } else if ($(this).prop('id') == 'tandc-previous') {
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("tandc-section");
            $(".main-container-fluid").removeClass();
            $(".main-container-fluid").addClass("institutesection");
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
    }

    $(".previous").click(function(){
        previousFieldSet.call(this);
    });
    
    $("input[data-create-design='true']").prop('disabled', true);
    $("#course-btn").prop("disabled", true);
    var course_btn = false;

    var code = false; var name = false;
    var description = false;
    var branch = false; var semester = false;
    var faculty = false; var course_type = false;

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
        // else if (!$("#id_course_desc").val().match(/^[A-Za-z0-9-,.-/\s]*$/)) {
        //     $("#id_course_desc").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course description correctly&#x0003F;");
        //     $("#id_course_desc").parent().find(".error-text").css("display", "block");
        //     description = false;
        // }
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

    $('#id_course_coordinator').on('keyup keydown blur change', function() {
        if ($("#id_course_coordinator").val() == "") {
            $("#id_course_coordinator").parent().find(".error-text").css("display", "block");
            faculty = false;
        } else {
            $("#id_course_coordinator").parent().find(".error-text").css("display", "none");
            faculty = true;
        }
    });

    $('#id_course_type').on('keyup keydown blur change', function() {
        if ($("#id_course_type").val() == "") {
            $("#id_course_type").parent().find(".error-text").css("display", "block");
            course_type = false;
        } else {
            $("#id_course_type").parent().find(".error-text").css("display", "none");
            course_type = true;
        }
    });

    $('input, select, textarea').on('keyup keydown blur change', function() {
        if (code == true && name == true && description == true && branch == true && semester == true && faculty == true && course_type == true) {
            course_btn = true;
        }
        else {
            course_btn = false;
        }
        if (course_btn == true) {
            $("#course-btn").prop("disabled", false);
            $("input[data-create-design='true']").prop('disabled', false);
        }
        else {
            $("#course-btn").prop("disabled", true);
            $("input[data-create-design='true']").prop('disabled', true);
        }
    });

    $("#branch-btn").prop("disabled", true);
    var branch_btn = false;
    var branch_name = false; var branch_description = false;

    $('#id_branch_name').on('keyup keydown blur change', function() {
        if($("#id_branch_name").val() == "") {
            $("#id_branch_name").parent().find(".error-text").html("Enter the branch name");
            $("#id_branch_name").parent().find(".error-text").css("display", "block");
            branch_name = false;
        }
        else if (!$("#id_branch_name").val().match(/^[A-Za-z&\-\s]*$/)) {
            $("#id_branch_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the branch name correctly&#x0003F;");
            $("#id_branch_name").parent().find(".error-text").css("display", "block");
            branch_name = false;
        }
        else if ($("#id_branch_name").val().match(/^\s+$/)) {
            $("#id_branch_name").parent().find(".error-text").html("Sorry, but the branch name cannot be empty");
            $("#id_branch_name").parent().find(".error-text").css("display", "block");
            branch_name = false;
        }
        else {
            $("#id_branch_name").parent().find(".error-text").css("display", "none");
            branch_name = true;
        }
    });

    $('#id_branch_desc').on('keyup keydown change', function() {
        if (!$("#id_branch_desc").val().match(/^\s+$/)) {
            var chars = $('#id_branch_desc').val().length;
            var max = $('#id_branch_desc').attr('maxlength');
            var remaining = max - chars;
            var char_text = remaining == 1 ? 'character' : 'characters';
            $('#id_branch_desc').parent().find(".info-text").html("You have " + remaining + " " + char_text + " remaining");
            $('#id_branch_desc').parent().find(".info-text").css("display", "block");
        }
    });

    $('#id_branch_desc').on('keyup keydown blur change', function() {
        if($("#id_branch_desc").val() == "") {
            $("#id_branch_desc").parent().find(".error-text").html("Enter the branch description");
            $("#id_branch_desc").parent().find(".error-text").css("display", "block");
            branch_description = false;
        }
        else if (!$("#id_branch_desc").val().match(/^[A-Za-z0-9-/\s]*$/)) {
            $("#id_branch_desc").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the branch description correctly&#x0003F;");
            $("#id_branch_desc").parent().find(".error-text").css("display", "block");
            branch_description = false;
        }
        else if ($("#id_branch_desc").val().match(/^\s+$/)) {
            $("#id_branch_desc").parent().find(".error-text").html("Sorry, but the branch description cannot be empty");
            $("#id_branch_desc").parent().find(".error-text").css("display", "block");
            branch_description = false;
        }        
        else if ($("#id_branch_desc").val().length > 500) {
            $("#id_branch_desc").parent().find(".error-text").html("Sorry, but the branch description cannot be more than 500 characters");
            $("#id_branch_desc").parent().find(".error-text").css("display", "block");
            branch_description = false;
        }
        else {
            $("#id_branch_desc").parent().find(".error-text").css("display", "none");
            branch_description = true;
        }
    });

    $('input, textarea').on('keyup keydown blur change', function() {
        if (branch_name == true && branch_description == true) {
            branch_btn = true;
        }
        else {
            branch_btn = false;
        }
        if (branch_btn == true) {
            $("#branch-btn").prop("disabled", false);
        }
        else {
            $("#branch-btn").prop("disabled", true);
        }
    });

    $("#semester-btn").prop("disabled", true);
    var semester_btn = false;
    var sem_mode = false; var sem_sy = false; var sem_ey = false;
    var sem_branch = false;

    $('#id_semester_mode').on('keyup keydown blur change', function() {
        if ($("#id_semester_mode").val() == "") {
            $("#id_semester_mode").parent().find(".error-text").css("display", "block");
            sem_mode = false;
        } else {
            $("#id_semester_mode").parent().find(".error-text").css("display", "none");
            sem_mode = true;
        }
    });

    $('#id_start_year').on('keyup keydown blur change', function() {
        if ($("#id_start_year").val() == "") {
            $("#id_start_year").parent().find(".error-text").css("display", "block");
            sem_sy = false;
        }
        else {
            $("#id_start_year").parent().find(".error-text").css("display", "none");
            sem_sy = true;
        }
    });

    $('#id_end_year').on('keyup keydown blur change', function() {
        if ($("#id_end_year").val() == "") {
            $("#id_end_year").parent().find(".error-text").css("display", "block");
            sem_ey = false;
        }
        else {
            $("#id_end_year").parent().find(".error-text").css("display", "none");
            sem_ey = true;
        }
    });

    $('#id_semester_branch').on('keyup keydown blur change', function() {
        if ($("#id_semester_branch").val() == "") {
            $("#id_semester_branch").parent().find(".error-text").css("display", "block");
            sem_branch = false;
        } else {
            $("#id_semester_branch").parent().find(".error-text").css("display", "none");
            sem_branch = true;
        }
    });

    $('input, select, textarea').on('keyup keydown blur change', function() {
        if (sem_mode == true && sem_sy == true && sem_ey == true && sem_branch == true) {
            semester_btn = true;
        }
        else {
            semester_btn = false;
        }
        if (semester_btn == true) {
            $("#semester-btn").prop("disabled", false);
        }
        else {
            $("#semester-btn").prop("disabled", true);
        }
    });

    $("#cotfield-btn").prop("disabled", true);
    var current_cmos_btn = false;
    var course_mos = false; var course_ltps = false;

    $('#id_mode_of_study_modal').on('keyup keydown blur change', function() {
        if($("#id_mode_of_study_modal").val() == "") {
            $("#id_mode_of_study_modal").parent().find(".error-text").html("Enter the course mode of study");
            $("#id_mode_of_study_modal").parent().find(".error-text").css("display", "block");
            course_mos = false;
        }
        else if (!$("#id_mode_of_study_modal").val().match(/^[A-Za-z&\-\s]*$/)) {
            $("#id_mode_of_study_modal").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course mode of study correctly&#x0003F;");
            $("#id_mode_of_study_modal").parent().find(".error-text").css("display", "block");
            course_mos = false;
        }
        else if ($("#id_mode_of_study_modal").val().match(/^\s+$/)) {
            $("#id_mode_of_study_modal").parent().find(".error-text").html("Sorry, but the course mode of study cannot be empty");
            $("#id_mode_of_study_modal").parent().find(".error-text").css("display", "block");
            course_mos = false;
        }
        else {
            $("#id_mode_of_study_modal").parent().find(".error-text").css("display", "none");
            course_mos = true;
        }
    });

    $('#id_course_ltps_modal').on('keyup keydown blur change', function() {
        if($("#id_course_ltps_modal").val() == "") {
            $("#id_course_ltps_modal").parent().find(".error-text").html("Enter the course L-T-P-S");
            $("#id_course_ltps_modal").parent().find(".error-text").css("display", "block");
            course_ltps = false;
        }
        else if (!$("#id_course_ltps_modal").val().match(/^[0-9]{1}-[0-9]{1}-[0-9]{1}-[0-9]{1}$/)) {
            $("#id_course_ltps_modal").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course L-T-P-S correctly&#x0003F;");
            $("#id_course_ltps_modal").parent().find(".error-text").css("display", "block");
            course_ltps = false;
        }
        else if ($("#id_course_ltps_modal").val().match(/^\s+$/)) {
            $("#id_course_ltps_modal").parent().find(".error-text").html("Sorry, but the course L-T-P-S cannot be empty");
            $("#id_course_ltps_modal").parent().find(".error-text").css("display", "block");
            course_ltps = false;
        }
        else {
            $("#id_course_ltps_modal").parent().find(".error-text").css("display", "none");
            course_ltps = true;
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (course_mos == true && course_ltps == true) {
            current_cmos_btn = true;
        }
        else {
            current_cmos_btn = false;
        }
        if (current_cmos_btn == true) {
            $("#cotfield-btn").prop("disabled", false);
        }
        else {
            $("#cotfield-btn").prop("disabled", true);
        }
    });

    $("#cotextrafield-btn").prop("disabled", true);
    var current_course_cot_ef_btn = false;
    var current_course_cot = false; var current_course_field_name_cot = false;  var current_course_field_type_cot = false;

    $('#id_current_course_cot').on('keyup keydown blur change', function() {
        if ($("#id_current_course_cot").val() == "") {
            $("#id_current_course_cot").parent().find(".error-text").css("display", "block");
            current_course_cot = false;
        } else {
            $("#id_current_course_cot").parent().find(".error-text").css("display", "none");
            current_course_cot = true;
        }
    });

    $('#id_course_cot_extra_field_name').on('keyup keydown blur change', function() {
        if($("#id_course_cot_extra_field_name").val() == "") {
            $("#id_course_cot_extra_field_name").parent().find(".error-text").html("Enter the course mode of study");
            $("#id_course_cot_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_field_name_cot = false;
        }
        else if (!$("#id_course_cot_extra_field_name").val().match(/^[A-Za-z&\-\s]*$/)) {
            $("#id_course_cot_extra_field_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course mode of study correctly&#x0003F;");
            $("#id_course_cot_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_field_name_cot = false;
        }
        else if ($("#id_course_cot_extra_field_name").val().match(/^\s+$/)) {
            $("#id_course_cot_extra_field_name").parent().find(".error-text").html("Sorry, but the course mode of study cannot be empty");
            $("#id_course_cot_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_field_name_cot = false;
        }
        else {
            $("#id_course_cot_extra_field_name").parent().find(".error-text").css("display", "none");
            current_course_field_name_cot = true;
        }
    });

    $('#id_course_cot_extra_field_type').on('keyup keydown blur change', function() {
        if ($("#id_course_cot_extra_field_type").val() == "") {
            $("#id_course_cot_extra_field_type").parent().find(".error-text").css("display", "block");
            current_course_field_type_cot = false;
        } else {
            $("#id_course_cot_extra_field_type").parent().find(".error-text").css("display", "none");
            current_course_field_type_cot = true;
        }
    });

    $('input, select, textarea').on('keyup keydown blur change', function() {
        if (current_course_cot == true && current_course_field_name_cot == true && current_course_field_type_cot == true) {
            current_course_cot_ef_btn = true;
        }
        else {
            current_course_cot_ef_btn = false;
        }
        if (current_course_cot_ef_btn == true) {
            $("#cotextrafield-btn").prop("disabled", false);
        }
        else {
            $("#cotextrafield-btn").prop("disabled", true);
        }
    });

    $("#extrafield-btn").prop("disabled", true);
    var current_course_ef_btn = false;
    var current_course_extra_field_name = false;  var current_course_extra_field_type = false;

    $('#id_course_extra_field_name').on('keyup keydown blur change', function() {
        if($("#id_course_extra_field_name").val() == "") {
            $("#id_course_extra_field_name").parent().find(".error-text").html("Enter the course mode of study");
            $("#id_course_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_extra_field_name = false;
        }
        else if (!$("#id_course_extra_field_name").val().match(/^[A-Za-z&\-\s]*$/)) {
            $("#id_course_extra_field_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the course mode of study correctly&#x0003F;");
            $("#id_course_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_extra_field_name = false;
        }
        else if ($("#id_course_extra_field_name").val().match(/^\s+$/)) {
            $("#id_course_extra_field_name").parent().find(".error-text").html("Sorry, but the course mode of study cannot be empty");
            $("#id_course_extra_field_name").parent().find(".error-text").css("display", "block");
            current_course_extra_field_name = false;
        }
        else {
            $("#id_course_extra_field_name").parent().find(".error-text").css("display", "none");
            current_course_extra_field_name = true;
        }
    });

    $('#id_course_extra_field_type').on('keyup keydown blur change', function() {
        if ($("#id_course_extra_field_type").val() == "") {
            $("#id_course_extra_field_type").parent().find(".error-text").css("display", "block");
            current_course_extra_field_type = false;
        } else {
            $("#id_course_extra_field_type").parent().find(".error-text").css("display", "none");
            current_course_extra_field_type = true;
        }
    });

    $('input, select').on('keyup keydown blur change', function() {
        if (current_course_extra_field_name == true && current_course_extra_field_type == true) {
            current_course_ef_btn = true;
        }
        else {
            current_course_ef_btn = false;
        }
        if (current_course_ef_btn == true) {
            $("#extrafield-btn").prop("disabled", false);
        }
        else {
            $("#extrafield-btn").prop("disabled", true);
        }
    });

    function createDesignCourse() {
        if($(this).hasClass('createCourseAjax-disabled')){
            return false;
        }
        $(this).addClass('createCourseAjax-disabled');
        setTimeout(function(){
            $("#create-design-course-next").removeClass('createCourseAjax-disabled');
        }, 5000);

        var getCreateDesignCourseURL = $("#create-design-course-next").data('create-course-ajax');
        var form = $('.create-course-form')[0];
        var form_data = new FormData(form);

        $.ajax({
            method: "POST",
            enctype: 'multipart/form-data',
            url: getCreateDesignCourseURL,
            data: form_data,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    var course_id = data.course_id;
                    var course_id_cookie = "course_id=" + course_id + "; path=/";
                    if(document.cookie.indexOf("course_id") != -1) {
                        document.cookie = "course_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    }
                    document.cookie = course_id_cookie;
                    // var before_value = $(".create-course-form").data('created-course-id');
                    $(".create-course-form").data('created-course-id', course_id);
                    // var after_value = $(".create-course-form").data('created-course-id');

                    document.getElementById("id_course_id").value = course_id;
                    // var inputincourse_id = document.getElementById("id_course_id").value;

                    document.getElementById("id_course_cot_id").value = course_id;
                    // var inputincoursecot_id = document.getElementById("id_course_cot_id").value;

                    $(".get-all-current-cot").data('current_course_id', course_id);
                    // var data_current_course_id = $(".get-all-current-cot").data('current_course_id');

                    // delete the cookie with name course_cot_id
                    if(document.cookie.indexOf("course_cot_id") != -1) {
                        document.cookie = "course_cot_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    }

                    $('#id_course_code').prop('readonly', true);
                    $("#id_course_code").parent().find(".help-text").html("Can be modified while editing course");
                    $("#id_course_code").parent().find(".help-text").css("display", "block");
                    
                    $('#id_course_name').prop('readonly', true);
                    $("#id_course_name").parent().find(".help-text").html("Can be modified while editing course");
                    $("#id_course_name").parent().find(".help-text").css("display", "block");

                    var next = document.getElementsByClassName('next')[0];
                    nextFieldSet.call(next);
                    console.log(data);
                }
                else if(data.status == 'error') {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    function createBranchFunc() {
        var branch_name = $('#id_branch_name').val();
        var branch_desc = $('#id_branch_desc').val();
        
        if($(this).hasClass('create-branch-disabled')){
            return false;
        }
        $(this).addClass('create-branch-disabled');
        setTimeout(function(){
            $("#branch-btn").removeClass('create-branch-disabled');
        }, 5000);

        var create_branch_url = $("#branch-btn").data('create-branch-url');

        $.ajax({
            type: "POST",
            url: create_branch_url,
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'name': branch_name,
                'desc': branch_desc,
            },
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    getAllBranchesFunc.call(this);
                    getAllBranchesForSemesterFunc.call(this);
                    setTimeout(function(){
                        $("#myModal").fadeOut(500);
                    }, 250);
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    function getAllBranchesFunc() {

        if($(this).hasClass('anchor-disabled')){
            return false;
        }
        $(this).addClass('anchor-disabled');
        setTimeout(function(){
            $("#fetchBranches").removeClass('anchor-disabled');
        }, 5000);

        var get_branches_url = $("#fetchBranches").data('get-branch-url');

        $.ajax({
            type: "GET",
            url: get_branches_url,
            success: function (data) {
                if(data.length == 0) {
                    toastr.info("No branches available")
                }
                else {
                    toastr.success("Branches list fetched successfully")
                    let html_data = '<option value=""> Select Branch </option>';
                    data.forEach(function (data) {
                        html_data += `<option value="${data.id}">${data.name}</option>`
                    });
                    $("#id_branch").html(html_data);

                    $("#id_branch").parent().find(".error-text").css("display", "block");
                    $("#course-btn").prop("disabled", true);
                    $("input[data-create-design='true']").prop('disabled', true);
                }
            },
            error: function (data) {
                toastr.error(data);
            }
        });
    }

    function getAllBranchesForSemesterFunc() {

        if($(this).hasClass('anchor-disabled')){
            return false;
        }
        $(this).addClass('anchor-disabled');
        setTimeout(function(){
            $("#fetchBranchesforSemester").removeClass('anchor-disabled');
        }, 5000);

        var get_branches_url = $("#fetchBranchesforSemester").data('get-branch-url');

        $.ajax({
            type: "GET",
            url: get_branches_url,
            success: function (data) {
                if(data.length == 0) {
                    toastr.info("No branches available")
                }
                else {
                    toastr.success("Branches list fetched successfully")
                    let html_data = '<option value=""> Select Branch </option>';
                    data.forEach(function (data) {
                        html_data += `<option value="${data.id}">${data.name}</option>`
                    });
                    $("#id_semester_branch").html(html_data);

                    $("#id_semester_branch").parent().find(".error-text").css("display", "block");
                    $("#semester-btn").prop("disabled", true);
                }
            },
            error: function (data) {
                toastr.error(data);
            }
        });
    }

    function createSemesterFunc() {
        var semester_mode = $('#id_semester_mode').val();
        var start_year = $('#id_start_year').val();
        var end_year = $('#id_end_year').val();
        var semester_branch = $('#id_semester_branch').val();
        var semester_is_active = $('#id_semester_is_active').val();
        
        if($(this).hasClass('create-semester-disabled')){
            return false;
        }
        $(this).addClass('create-semester-disabled');
        setTimeout(function(){
            $("#semester-btn").removeClass('create-semester-disabled');
        }, 5000);

        var create_semester_url = $("#semester-btn").data('create-semester-url');

        $.ajax({
            type: "POST",
            url: create_semester_url,
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'mode': semester_mode,
                'start_year': start_year,
                'end_year': end_year,
                'branch': semester_branch,
                'is_active': semester_is_active,
            },
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    getAllSemestersFunc.call(this);
                    setTimeout(function(){
                        $("#myModal2").fadeOut(500);
                    }, 250);
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message);
            }
        });
    }

    function getAllSemestersFunc() {

        if($(this).hasClass('anchor-disabled')){
            return false;
        }
        $(this).addClass('anchor-disabled');
        setTimeout(function(){
            $("#fetchSemester").removeClass('anchor-disabled');
        }, 5000);

        var get_semesters_url = $("#fetchSemester").data('get-semester-url');

        $.ajax({
            type: "GET",
            url: get_semesters_url,
            success: function (data) {
                if(data.length == 0) {
                    html_data = '<option value=""> Data Not Available </option>';
                    $("#id_semester").html(html_data);
                    toastr.info("No semesters available")
                }
                else {
                    toastr.success("Semesters list fetched successfully")
                    let html_data = '<option value=""> Select Semester </option>';
                    data.forEach(function (data) {
                        html_data += `<option value="${data.id}">${data.mode} ${data.start_year.substring(0, 4)}</option>`
                    });
                    $("#id_semester").html(html_data);

                    $("#id_semester").parent().find(".error-text").css("display", "block");
                    $("#course-btn").prop("disabled", true);
                    $("input[data-create-design='true']").prop('disabled', true);
                }
            },
            error: function (data) {
                toastr.error(data);
            }
        });
    }

    function createExtraFieldFunc() {
        if($(this).hasClass('create-extra-field-disabled')){
            return false;
        }
        $(this).addClass('create-extra-field-disabled');
        setTimeout(function(){
            $("#extrafield-btn").removeClass('create-extra-field-disabled');
        }, 5000);

        var getCreateExtraFieldURL = $("#extrafield-btn").data('create-externalfield-url');
        var createCourseExtraField = $('.create-course-extra-field')[0];
        var createCourseExtraFieldform_data = new FormData(createCourseExtraField);

        $.ajax({
            method: "POST",
            enctype: 'multipart/form-data',
            url: getCreateExtraFieldURL,
            data: createCourseExtraFieldform_data,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    $("#id_append_external_fields").load(location.href + " #id_append_external_fields");
                    setTimeout(function(){
                        $("#myModal3").fadeOut(500);
                    }, 250);
                }
                else if(data.status == 'error') {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    function createCOTFunc() {
        if($(this).hasClass('create-cot-disabled')){
            return false;
        }
        $(this).addClass('create-cot-disabled');
        setTimeout(function(){
            $("#cotfield-btn").removeClass('create-cot-disabled');
        }, 5000);

        var getCreateCOTURL = $("#cotfield-btn").data('create-cot-url');
        var createCourseCOT = $('.create-course-cot')[0];
        var createCourseCOTform_data = new FormData(createCourseCOT);

        $.ajax({
            method: "POST",
            enctype: 'multipart/form-data',
            url: getCreateCOTURL,
            data: createCourseCOTform_data,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if(data.status == 'success') {
                    var coursecot_id = data.courseCOTObjID;
                    var course_cot_id_cookie = "course_cot_id=" + coursecot_id + "; path=/";
                    if(document.cookie.indexOf("course_cot_id") != -1) {
                        document.cookie = "course_cot_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
                    }
                    document.cookie = course_cot_id_cookie;
                    // var cot_before_value = $(".create-course-cot-form").data('created-course-cot-id');
                    $(".create-course-cot-form").data('created-course-cot-id', coursecot_id);
                    // var cot_after_value = $(".create-course-cot-form").data('created-course-cot-id');
                    
                    var cotfield_btn_as_this = document.getElementsByClassName('get-all-current-cot')[0];
                    getAllCOTFunc.call(cotfield_btn_as_this);
                    
                    toastr.success(data.message)
                    $("#id_append_course_cot").load(location.href + " #id_append_course_cot");
                    setTimeout(function(){
                        $("#myModal4").fadeOut(500);
                    }, 250);
                }
                else if(data.status == 'error') {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    function createCOTExtraFieldFunc() {
        if($(this).hasClass('create-cot-extra-field-disabled')){
            return false;
        }
        $(this).addClass('create-cot-extra-field-disabled');
        setTimeout(function(){
            $("#cotextrafield-btn").removeClass('create-cot-extra-field-disabled');
        }, 5000);

        var getCreateCOTExtraFieldURL = $("#cotextrafield-btn").data('create-cot-externalfield-url');
        var createCOTExtraField = $('.create-course-cot-extra-field')[0];
        var createCOTExtraFieldform_data = new FormData(createCOTExtraField);

        $.ajax({
            method: "POST",
            url: getCreateCOTExtraFieldURL,
            data: createCOTExtraFieldform_data,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    $("#id_append_cot_external_fields").load(location.href + " #id_append_cot_external_fields");
                    setTimeout(function(){
                        $("#myModal5").fadeOut(500);
                    }, 250);
                }
                else if(data.status == 'error') {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    function submitCourseFormFunc() {
        if($(this).hasClass('submit_course_form_disabled')){
            return false;
        }
        $(this).addClass('submit_course_form_disabled');
        setTimeout(function(){
            $("#course-btn").removeClass('submit_course_form_disabled');
        }, 5000);

        var submitCourseForm = $("#course-btn").data('submit-course-url');
        var submitCourseFormObject = $('.create-course-form')[0];
        var submitCourseFormData = new FormData(submitCourseFormObject);
        var submitCourseSuccessURL = $("#course-btn").data('course-create-success-url');

        $.ajax({
            method: "POST",
            enctype: 'multipart/form-data',
            url: submitCourseForm,
            data: submitCourseFormData,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if(data.status == 'success') {
                    toastr.success(data.message)
                    setTimeout(function(){
                        window.location.href = submitCourseSuccessURL;
                    }
                    , 2500);
                }
                else if(data.status == 'error') {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                toastr.error(data.message)
            }
        }); 
    }

    $("#branch-btn").click(function(){
        createBranchFunc.call(this);
    });
    $("#fetchBranches").click(function(){
        getAllBranchesFunc.call(this);
    });
    $("#fetchBranchesforSemester").click(function(){
        getAllBranchesForSemesterFunc.call(this);
    });

    $("#semester-btn").click(function(){
        createSemesterFunc.call(this);
    });
    $("#fetchSemester").click(function(){
        getAllSemestersFunc.call(this);
    });

    $("#create-design-course-next").click(function(){
        if($(".create-course-form").data('created-course-id') == 'empty') {
            createDesignCourse.call(this);
        }
        else {
            var next = document.getElementsByClassName('next')[0];
            nextFieldSet.call(next);
        }
    });

    $("#extrafield-btn").click(function() {
        createExtraFieldFunc.call(this);
    });

    $("#fetchcurrentcot").click(function(){
        getAllCOTFunc.call(this);
    });
    $("#cotfield-btn").click(function() {
        createCOTFunc.call(this);
    });
    $("#cotextrafield-btn").click(function() {
        createCOTExtraFieldFunc.call(this);
    });
    $("#course-btn").click(function() {
        $(this).html('Please wait...');
        submitCourseFormFunc.call(this);
    });

});

var modal = document.getElementById("myModal"); 
var modal2 = document.getElementById("myModal2");
var modal3 = document.getElementById("myModal3");
var modal4 = document.getElementById("myModal4");
var modal5 = document.getElementById("myModal5");
var btn = document.getElementById("showFormCreateBranch");
var btn2 = document.getElementById("showFormCreateSemester");
var btn3 = document.getElementById("showFormCreateExternalField");
var btn4 = document.getElementById("showFormCreateCOTField");
var btn5 = document.getElementById("showFormCreateCOTExtraField");
var span = document.getElementById("close-model");
var span2 = document.getElementById("close-model2");
var span3 = document.getElementById("close-model3");
var span4 = document.getElementById("close-model4");
var span5 = document.getElementById("close-model5");

btn.onclick = function() {
  modal.style.display = "block";
}
btn2.onclick = function() {
  modal2.style.display = "block";
}
btn3.onclick = function() {
  modal3.style.display = "block";
}
btn4.onclick = function() {
  modal4.style.display = "block";
}
btn5.onclick = function() {
    modal5.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}
span2.onclick = function() {
  modal2.style.display = "none";
}
span3.onclick = function() {
  modal3.style.display = "none";
}
span4.onclick = function() {
  modal4.style.display = "none";
}
span5.onclick = function() {
  modal5.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
  if (event.target == modal2) {
    modal2.style.display = "none";
  }
  if (event.target == modal3) {
    modal3.style.display = "none";
  }
  if (event.target == modal4) {
    modal4.style.display = "none";
  }  
  if (event.target == modal5) {
    modal5.style.display = "none";
  }
}