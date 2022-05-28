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
                    html_data += `<option value="${data.id}">${data.mode} ${data.start_year.substring(0, 4)} - ${data.branch__name}</option>`
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

$('.course_checkbox_item').on('click', function() {
    var course_id = $(this).attr("name");
    var courses_stack = [];
    if ($(this).is(':checked')) {
        if (typeof(Storage) !== "undefined") {
            if (localStorage.getItem("courses_stack") !== null) {
                courses_stack = JSON.parse(localStorage.getItem("courses_stack"));
                if (courses_stack.indexOf(course_id) == -1) {
                    courses_stack.push(course_id);
                    localStorage.setItem("courses_stack", JSON.stringify(courses_stack));
                }
            }
            else {
                courses_stack.push(course_id);
                localStorage.setItem("courses_stack", JSON.stringify(courses_stack));
            }
        }
        else {
            toastr.error("Sorry, your browser does not support Web Storage...");
        }
    } else {
        // check course_id is in the array of courses_stack
        if (typeof(Storage) !== "undefined") {
            if (localStorage.getItem("courses_stack") !== null) {
                courses_stack = JSON.parse(localStorage.getItem("courses_stack"));
                var index = courses_stack.indexOf(course_id);
                console.log(index);
                // from courses_stack array remove course_id and update localStorage
                if (index > -1) {
                    courses_stack.splice(index, 1);
                }
                localStorage.setItem("courses_stack", JSON.stringify(courses_stack));
            }
        }
    }
});

function allocateCFS() {
    if($(this).hasClass('button-disabled')){
        return false;
    }
    $(this).addClass('button-disabled');
    setTimeout(function(){
        $("#semester-courses-btn").removeClass('button-disabled');
    }, 5000);

    var allocateCFSURL = $("#semester-courses-btn").data('allocate-courses-for-semester-url');
    if (typeof(Storage) !== "undefined") {
        if (localStorage.getItem("courses_stack") !== null) {
            var courses_stack = JSON.parse(localStorage.getItem("courses_stack"));
            var courses_stack_length = courses_stack.length;
            if (courses_stack_length > 0) {
                var courses_stack_string = courses_stack.join(",");
            }
        }
    }

    $.ajax({
        type: "POST",
        url: allocateCFSURL,
        data: {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'semester_id': $("#id_semester").val(),
            "courses_stack_data": courses_stack_string,
        },
        success: function (data) {
            if (data.status == "success") {
                toastr.success(data.message);
                window.location.href = $("#semester-courses-btn").data('go-to-aca-registration-url');
            }
            else if (data.status == "info") {
                toastr.info(data.message);
            }
            else {
                toastr.error(data.message);
            }
        },
        error: function (data) {
            toastr.error(data);
        }
    });
}

$("#fetchBranchesforSemester").click(function(){
    getAllBranchesForSemesterFunc.call(this);
});
$("#semester-btn").click(function(){
    createSemesterFunc.call(this);
});
$("#fetchSemester").click(function(){
    getAllSemestersFunc.call(this);
});
$("#semester-courses-btn").click(function(){
    allocateCFS.call(this);
});

// If page is reloaded then clear the localStorage
if (typeof(Storage) !== "undefined") {
    if (localStorage.getItem("courses_stack") !== null) {
        localStorage.removeItem("courses_stack");
    }
}

var createSemesterModal = document.getElementById("createSemesterModalForm"); 
var createSemesterModalbtn = document.getElementById("showFormCreateSemester");
var createSemesterModalspan = document.getElementById("close-createSemesterModalForm");
createSemesterModalbtn.onclick = function() {
    createSemesterModal.style.display = "block";
}
createSemesterModalspan.onclick = function() {
    createSemesterModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == createSemesterModal) {
    createSemesterModal.style.display = "none";
  }
});