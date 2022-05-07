var branchModal = document.getElementById("branchModalForm");
var showFormCreateBranchbtn = document.getElementById("showFormCreateBranch");
var branchModalSpan = document.getElementById("close-branchModal");

var semesterModal = document.getElementById("semesterModalForm");
var semesterModalbtn = document.getElementById("showFormCreateSemester");
var semesterModalspan = document.getElementById("close-semesterModalForm");

showFormCreateBranchbtn.onclick = function() {
  branchModal.style.display = "block";
}
semesterModalbtn.onclick = function() {
  semesterModal.style.display = "block";
}

branchModalSpan.onclick = function() {
  branchModal.style.display = "none";
}
semesterModalspan.onclick = function() {
  semesterModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == branchModal) {
    branchModal.style.display = "none";
  }
  if (event.target == semesterModal) {
    semesterModal.style.display = "none";
  }
});

$(document).ready(function() {
  $("#branch-btn").prop("disabled", true);
  var branch_btn = false;
  var branch_name = false; var branch_description = false;

  $('#id_branch_name').on('keyup keydown blur change', function() {
      if($("#id_branch_name").val() == "") {
          $("#id_branch_name").parent().find(".error-text").html("Enter the branch name");
          $("#id_branch_name").parent().find(".error-text").css("display", "block");
          branch_name = false;
      }
      else if (!$("#id_branch_name").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
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
      else if (!$("#id_branch_desc").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
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
});

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

$("#fetchBranchesforSemester").click(function(){
  getAllBranchesForSemesterFunc.call(this);
});

$(document).on('click', '.semRegStatus', function() {
    var semester_id = $(this).attr('name');
    var setSemRegStatusURL = $(this).data('set-sem-reg-status-url');
    
    $.ajax({
        type: "POST",
        url: setSemRegStatusURL,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'semester_id': semester_id
        },
        success: function (data) {
            
        },
        error: function (data) {
            console.log("Something went wrong");
        }
    });
});

$(document).on('click', '.semester_status', function() {
    var semester_id = $(this).attr('name');
    var setSemesterStatusURL = $(this).data('set-semester-status-url');

    $.ajax({
        type: "POST",
        url: setSemesterStatusURL,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'semester_id': semester_id
        },
        success: function (data) {
            console.log(data);
            if (data.status == "success") {
                toastr.success(data.message);
            }
            else {
                toastr.error(data.message);
            }
        },
        error: function (data) {
            console.log("Something went wrong");
        }
    });
});
