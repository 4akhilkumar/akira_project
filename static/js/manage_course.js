$(document).ready(function() {
    var createCourseUrl = $('#createCourse').data('create-course-url');

    $('#createCourse').click(function() {
        window.location.href = createCourseUrl;
    });
});