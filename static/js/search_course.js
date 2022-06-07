$(document).ready(function() {
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