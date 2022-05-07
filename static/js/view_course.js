$(document).ready(function() {
    $("#id_teachingstaffenrollcourse").click(function() {
        var teachingstaffcourseenrollURL = $(this).data('teaching-staff-enroll-course-url');
        var course_id = $(this).data('course-id');
        // make a ajax call to post data to the server
        $.ajax({
            url: teachingstaffcourseenrollURL,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
                'course_id': course_id,
            },
            success: function(data) {
                if (data.status == 'success') {
                    toastr.success(data.message);
                }
                else {
                    toastr.error(data.message);
                }
            },
            error: function(data) {
                console.log("Faild to enroll course");
            }
        });
    });
});