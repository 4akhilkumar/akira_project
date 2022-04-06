$('#course-btn').click(function() {
    $(this).prop('disabled', true);
    $(this).html('Please wait...');
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
        if (code == true && name == true && description == true && branch == true && semester == true && faculty == true) {
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

var modal = document.getElementById("myModal"); 
var modal2 = document.getElementById("myModal2");
// var modal3 = document.getElementById("myModal3");
// var modal4 = document.getElementById("myModal4");
var btn = document.getElementById("showFormCreateBranch");
var btn2 = document.getElementById("showFormCreateSemester");
// var btn3 = document.getElementById("showFormCreateRoom");
// var btn4 = document.getElementById("showFormCreateBulk");
var span = document.getElementById("close-model");
var span2 = document.getElementById("close-model2");
// var span3 = document.getElementById("close-model3");
// var span4 = document.getElementById("close-model4");

btn.onclick = function() {
  modal.style.display = "block";
}
btn2.onclick = function() {
  modal2.style.display = "block";
}
// btn3.onclick = function() {
//   modal3.style.display = "block";
// }
// btn4.onclick = function() {
//   modal4.style.display = "block";
// }

span.onclick = function() {
  modal.style.display = "none";
}
span2.onclick = function() {
  modal2.style.display = "none";
}
// span3.onclick = function() {
//   modal3.style.display = "none";
// }
// span4.onclick = function() {
//   modal4.style.display = "none";
// }

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
  if (event.target == modal2) {
    modal2.style.display = "none";
  }
//   if (event.target == modal3) {
//     modal3.style.display = "none";
//   }
//   if (event.target == modal4) {
//     modal4.style.display = "none";
//   }
}

$(document).ready(function() {
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
                    getAllBranchesForSemesterFunccall.call(this);
                    setTimeout(function(){
                        $("#myModal").fadeOut(500);
                    }, 1000);
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                console.log(data.message);
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
                }
            },
            error: function (data) {
                console.log(data);
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
                }
            },
            error: function (data) {
                console.log(data);
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
                    }, 1000);
                }
                else {
                    toastr.warning(data.message)
                }
            },
            error: function (data) {
                console.log(data.message);
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
                }
            },
            error: function (data) {
                console.log(data);
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
});