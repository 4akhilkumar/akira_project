$(document).ready(function() {
    var createCourseUrl = $('#createCourse').data('create-course-url');
    $('#createCourse').click(function() {
        window.location.href = createCourseUrl;
    });

    var placeholderArray = ['Course Name', 'Course Code', 'Anything related to it!'];
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


var bulkCoursesCreationModal = document.getElementById("bulkCoursesCreationModalForm");
var showFormBulkCourses = document.getElementById("createCourseBulk");
var bulkCoursesCreationSpan = document.getElementById("close-bulkCoursesCreationModal");

showFormBulkCourses.onclick = function() {
  bulkCoursesCreationModal.style.display = "block";
}

bulkCoursesCreationSpan.onclick = function() {
  bulkCoursesCreationModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == bulkCoursesCreationModal) {
    bulkCoursesCreationModal.style.display = "none";
  }
});