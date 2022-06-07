var branchModal = document.getElementById("branchModalForm");
var showFormCreateBranchbtn = document.getElementById("showFormCreateBranch");
var branchModalSpan = document.getElementById("close-branchModal");

var semesterModal = document.getElementById("semesterModalForm");
var semesterModalbtn = document.getElementById("showFormCreateSemester");
var semesterModalspan = document.getElementById("close-semesterModalForm");

var createSCORVSCModal = document.getElementById("createSCORVSCModalForm");
var createSCORVSCModalbtn = document.getElementById("showFormCreateSCORVSC");
var createSCORVSCModalspan = document.getElementById("close-createSCORVSCModalForm");

showFormCreateBranchbtn.onclick = function() {
  branchModal.style.display = "block";
}
semesterModalbtn.onclick = function() {
  semesterModal.style.display = "block";
}
createSCORVSCModalbtn.onclick = function() {
  createSCORVSCModal.style.display = "block";
}

branchModalSpan.onclick = function() {
  branchModal.style.display = "none";
}
semesterModalspan.onclick = function() {
  semesterModal.style.display = "none";
}
createSCORVSCModalspan.onclick = function() {
  createSCORVSCModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == branchModal) {
    branchModal.style.display = "none";
  }
  if (event.target == semesterModal) {
    semesterModal.style.display = "none";
  }
  if (event.target == createSCORVSCModal) {
    createSCORVSCModal.style.display = "none";
  }
});

$("#id_viewSemesterCourses").click(function () {
    var viewsemestercoursesurl = $(this).attr('data-view-semester-courses-url');
    window.location.href = viewsemestercoursesurl;
});

$("#id_createSemesterCourses").click(function () {
    var createsemestercoursesurl = $(this).attr('data-create-semester-courses-url');
    window.location.href = createsemestercoursesurl;
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
            if (data.status == "success") {
                toastr.success(data.message);
                $("#id_acaRegTable").load(location.href + " #id_acaRegTable", "");
            }
            else {
                toastr.error(data.message);
                $("#id_acaRegTable").load(location.href + " #id_acaRegTable", "");
            }
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
            if (data.status == "success") {
                toastr.success(data.message);
                $("#id_active_semesters").load(location.href + " #id_active_semesters", "");
                $("#id_acaRegTable").load(location.href + " #id_acaRegTable", "");
            }
            else {
                toastr.error(data.message);
                $("#id_acaRegTable").load(location.href + " #id_acaRegTable", "");
            }
        },
        error: function (data) {
            console.log("Something went wrong");
        }
    });
});

$(document).ready(function() {
    var placeholderArray = ['Semester Duration', 'Semester Mode', 'Anything related to it!'];
    setInterval(function() {
        var searchQueryInput = $('.searchQueryInput').attr('placeholder', "Search " + placeholderArray[Math.floor(Math.random() * placeholderArray.length)]);
        var searchQueryInputList = $('.searchQueryInputList');
        searchQueryInputList.empty();
        searchQueryInput.show();
    }
    , 1000);
});

$(document).keypress(function(e) {
    if (e.which == 47 && !$('.searchQueryInput').is(':focus')) {
        $('.searchQueryInput').focus();
        return false;
    }
});

$("#searchQuerySubmit").prop("disabled", true);
var searchQuery = false;

$('.searchQueryInput').on('keyup keydown blur change', function() {
    if($(".searchQueryInput").val() == "") {
        $(".searchQueryInput").parent().find(".error-text").css("display", "block");
        searchQuery = false;
    }
    else if ($(".searchQueryInput").val().match(/^\s+$/)) {
        $(".searchQueryInput").parent().find(".error-text").css("display", "block");
        searchQuery = false;
    }
    else {
        $(".searchQueryInput").parent().find(".error-text").css("display", "none");
        searchQuery = true;
    }
});

$('input').on('keyup keydown blur change', function() {
    if (searchQuery == true) {
        $("#searchQuerySubmit").prop("disabled", false);
    }
    else {
        $("#searchQuerySubmit").prop("disabled", true);
    }
});

$("#searchQuerySubmit").click(function(e) {
    e.preventDefault();
});

document.addEventListener("DOMContentLoaded", () => {
    $("#id_searchSemData").on("keyup", function() {
        var searchQuery = $(this).val().toLowerCase().trim();
        var ResultStatus = true;
        $("#id_SemMngTable tr").filter(function() {
            $(this).toggle($(this).text()
            .toLowerCase().indexOf(searchQuery) > -1)
            if ($(this).text().toLowerCase().indexOf(searchQuery) == -1) {
                ResultStatus = false;
            }
        });
        if (ResultStatus == false) {
            // change the css nodatafound display to block
            console.log("noDataFound");
        }
    });
});

function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    // Sort each row
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    // Remove all existing TRs from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    // Re-add the newly sorted rows
    tBody.append(...sortedRows);

    // Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table-sortable .table-header-title").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});