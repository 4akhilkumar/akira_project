document.getElementById("resendEmailOption").style.display = "none";
var lastMailTimeFormatData = document.querySelector(".wac-container").getAttribute("data-last-mail-time");
var last_mail_time = new Date(lastMailTimeFormatData);
// calculate the time 10 minutes from last_mail_time
var time_to_wait = new Date(last_mail_time.getTime() + 600000);
// make a count down timer to wait for 10 minutes from last_mail_time
var countDownDate = new Date(time_to_wait).getTime();
// Update the count down every 1 second and if the time is up then show the div id="resendEmailOption"
var x = setInterval(function() {
    // Get todays date and time
    var now = new Date().getTime();
    // Find the distance between now an the count down date
    var distance = countDownDate - now;
    // Time calculations for days, hours, minutes and seconds

    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Output the result in an element with id="showMessage"
    // If minutes and seconds are less than 10, add a 0 in front of them
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    // if minutes are zero then show the message seconds
    if (minutes == 0) {
        $("#showMessage").html(`About <span class="showing-time">${seconds} sec</span> to resend email`);
    } else {
        // create a span tag with class "showing-time"
        var showTime = `About <span class="showing-time">${minutes} min : ${seconds} sec</span> to resend email`;
        // display the span tag to the div id="showMessage" using JQuery
        $("#showMessage").html(showTime);
    }

    // If the count down is over, write some text 
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("showMessage").classList.remove("showing-time");
        $("#showMessage").html("If you didn't recieve any email, please check your spam folder or check your internet connection");
        document.getElementById("resendEmailOption").style.display = "block";
    }
}, 1000);

function isStaffRegConfirmed() {
    var enusername = document.querySelector(".wac-container").getAttribute("data-enusername");
    var isStaff_confirmed_url = document.querySelector(".wac-container").getAttribute("data-isStaff-confirmed-url");
    var login_url = document.querySelector(".wac-container").getAttribute("data-login-url");
    var csrf_token_data = document.querySelector(".wac-container").getAttribute("data-csrf-token");

    $.ajax({
        url: isStaff_confirmed_url,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf_token_data
        },
        data: {
            EnUsername: enusername
        },
        success: function(dataResponse) {
            if (dataResponse.status == "success") {
                window.location.replace(login_url);
            }
        }
    });
}
setInterval(isStaffRegConfirmed, 10000);