// ====================== Skeleton CSS ====================== //
const allSkeleton = document.querySelectorAll('.skeleton')
window.addEventListener('load', function() {
  allSkeleton.forEach(item=> {
    item.classList.remove('skeleton')
  })
})
// ====================== Skeleton CSS ====================== //

// ====================== Top Button ====================== //
var mybutton = document.getElementById("myTopButton");
window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
// ====================== End Top Button ====================== //

$(document).ready(function() {
  var current_fs, next_fs, previous_fs; //fieldsets
  var opacity;

  function nextFieldSet() {
      current_fs = $(this).parent();
      next_fs = $(this).parent().next();

      //Add Class Active
      if ($(this).prop('id') == 'create-urlshortener-next') {
          $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("shortened-url-section");
          $(".main-container-fluid").removeClass();
          $(".main-container-fluid").addClass("shortenedurlsection");
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
    if ($(this).prop('id') == 'short-another-url') {
      $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("shortened-url-section");
      $(".main-container-fluid").removeClass();
      $(".main-container-fluid").addClass("personalsection");
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

  $(".previous_new_long_url").click(function(){
    previousFieldSet.call(this);
  });

  function createURLShortener() {
    var getCreateURLShortenerURL = $("#create-urlshortener-next").data('create-urlshortener-ajax');
    var form = $('.create-urlshortener-form')[0];
    var form_data = new FormData(form);

    $.ajax({
      method: "POST",
      url: getCreateURLShortenerURL,
      data: form_data,
      processData: false,
      contentType: false,
      cache: false,
      success: function (data) {
        if(data.status == 'success') {
          toastr.success(data.message)
          var next = document.getElementsByClassName('next_to_sortened_url')[0];
          nextFieldSet.call(next);
          $('.create-urlshortener-form')[0].reset();
          $("#id_shortened_url").val(data.shortened_url);
        }
        else if(data.status == 'error') {
          toastr.warning(data.message)
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

  $("#create-urlshortener-next").click(function(){
    createURLShortener.call(this);
  });
});

$("input[type=text], input[type=number], textarea").each(function () {
  var $input = $(this);
  var $parent = $input.closest(".input-box");
  if ($input.val()) $parent.addClass("focus");
  else $parent.removeClass("focus");
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
    $("input[type=text], input[type=number], textarea").each(function () {
        var $input = $(this);
        var $parent = $input.closest(".input-box");
        if ($input.val()) $parent.addClass("focus");
        else $parent.removeClass("focus");
    });
  }
}

// ====================== Widgets Modal ====================== //
var widgetsModal = document.getElementById("widgetsModal"); 
var widgetsModal_btn = document.getElementById("showWidgetsModal");
var widgetsModal_span = document.getElementById("close-widgetModal");

widgetsModal_btn.onclick = function() {
  widgetsModal.style.display = "block";
}

widgetsModal_span.onclick = function() {
  widgetsModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == widgetsModal) {
    widgetsModal.style.display = "none";
  }
}
// ====================== End Widgets Modal ====================== //

/* ====================== Dark Mode ===================== */
const themeBtn = document.querySelector('.theme');

function getCurrentTheme(){
  let theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  localStorage.getItem('chosenTheme') ? theme = localStorage.getItem('chosenTheme') : null;
  return theme;
}

function loadTheme(theme){
  const root = document.querySelector(':root');
  if(theme === "light"){
    themeBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" class="bkg2--stroke" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
  } else {
    themeBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" class="bkg2--stroke" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sun"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`;
  }
  root.setAttribute('color-scheme', `${theme}`);
}

themeBtn.addEventListener('click', () => {
  let theme = getCurrentTheme();
  let audio;
  if(theme === 'dark'){
    audio = document.querySelector('.theme-audio--light-on');
    theme = 'light';
  } else {
    audio = document.querySelector('.theme-audio--light-off');
    theme = 'dark';
  }
  audio.currentTime = 0;
  audio.play();
  localStorage.setItem('chosenTheme', `${theme}`);
  loadTheme(theme);
})

window.addEventListener('DOMContentLoaded', () => {
  loadTheme(getCurrentTheme());
})
/* ====================== End Dark Mode ====================== */

// ====================== URL Shortener Modal ====================== //
var urlShortenerModal = document.getElementById("urlShortenerModal"); 
var URLShortenerModal_btn = document.getElementById("showURLShortenerModal");
var URLShortenerModal_span = document.getElementById("close-urlshortener");

URLShortenerModal_btn.onclick = function() {
  urlShortenerModal.style.display = "block";
}

URLShortenerModal_span.onclick = function() {
  urlShortenerModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == urlShortenerModal) {
    urlShortenerModal.style.display = "none";
  }
}

$("#create-urlshortener-next").prop("disabled", true);
var createus_next_btn = false;

var long_url = false; var custom_path = true;
var expire_status = true; var expire_date = true; var expire_time = true;

$('#id_long_url').on('keyup keydown blur change', function() {
  if($("#id_long_url").val() == "") {
    $("#id_long_url").parent().find(".error-text").html("Enter the long URL");
    $("#id_long_url").parent().find(".error-text").css("display", "block");
    long_url = false;
  }
  else if ($("#id_long_url").val().match(/^\s+$/)) {
    $("#id_long_url").parent().find(".error-text").html("Sorry, but the Long URL cannot be empty");
    $("#id_long_url").parent().find(".error-text").css("display", "block");
    long_url = false;
  }
  else {
    $("#id_long_url").parent().find(".error-text").css("display", "none");
    long_url = true;
  }
});

$('#id_customize_path').on('keyup keydown blur change', function() {
  if ($("#id_customize_path").val().match(/^\s+$/)) {
    $("#id_customize_path").parent().find(".error-text").html("Sorry, but the Custom path cannot be empty");
    $("#id_customize_path").parent().find(".error-text").css("display", "block");
    custom_path = false;
  }
  else if (!$("#id_customize_path").val().match(/^[A-Za-z0-9]*$/)) {
    $("#id_customize_path").parent().find(".error-text").html("Sorry, but the Custom path can only contain letters and numbers");
    $("#id_customize_path").parent().find(".error-text").css("display", "block");
    custom_path = false;
  }
  else {
    $("#id_customize_path").parent().find(".error-text").css("display", "none");
    custom_path = true;
  }
});

$('#id_expire_date').on('keyup keydown blur change', function() {
  if($("#id_expire_date").val() != "") {
    $("#id_expire_date").parent().find(".error-text").css("display", "none");
    expire_date = true;
    expire_status = true;
    if ($("#id_expire_date").val() == dateFromNowOn()) {
      var today = new Date();
      var h = today.getHours();
      var m = today.getMinutes();
      if (h < 10) {
        h = '0' + h;
      }
      if (m < 10) {
        m = '0' + m;
      }
      var fromNow = h + ':' + m;
      document.getElementById("id_expire_time").setAttribute("min", fromNow);
      
      if ($("#id_expire_time").val() != "") {
        if ($("#id_expire_time").val() < timeFromNowOn()) {
          $("#id_expire_time").parent().find(".error-text").css("display", "block");
          $("#id_expire_time").parent().find(".error-text").html("Sorry, but the Expire time cannot be earlier than the current time");
          expire_time = false;
        }
        else {
          expire_time = true;
          expire_status = true;
        }
      }
      if($("#id_expire_time").val() == "") {
        $("#id_expire_time").parent().find(".error-text").css("display", "block");
        expire_time = false;
      }
      else {
        expire_time = true;
        expire_status = true;
      }
    }
    else {
      if ($("#id_expire_time").val() != "") {
        $("#id_expire_time").parent().find(".error-text").css("display", "none");
        expire_time = true;
        expire_status = true;
      }
    }
  }
  else {
    expire_date = false;
  }
});

$('#id_expire_time').on('keyup keydown blur change', function() {
  var expire_time_value = $("#id_expire_time").val();
  if (expire_time_value != "") {
    if($("#id_expire_date").val() == "") {
      $("#id_expire_date").parent().find(".error-text").css("display", "block");
      expire_date = false;
    }
    else {
      $("#id_expire_time").parent().find(".error-text").css("display", "none");
      expire_date = true;
      expire_status = true;
      if ($("#id_expire_date").val() == dateFromNowOn()) {
        if (expire_time_value < timeFromNowOn()) {
          $("#id_expire_time").parent().find(".error-text").css("display", "block");
          $("#id_expire_time").parent().find(".error-text").html("Sorry, but the Expire time cannot be earlier than the current time");
          expire_time = false;
        }
        else {
          expire_time = true;
          expire_status = true;
        }
      }
    }
  }
  else {
    if($("#id_expire_date").val() != "") {
      if ($("#id_expire_date").val() == dateFromNowOn()) {
        $("#id_expire_time").parent().find(".error-text").css("display", "block");
        expire_time = false;
      }
      else {
        expire_time = true;
        expire_status = true;
      }
    }
  }
});

$('#resetDate').on('click', function() {
  $("#id_expire_date").val("");
  $("#id_expire_date").parent().find(".error-text").css("display", "none");
  expire_date = true;
});

$('#resetTime').on('click', function() {
  $("#id_expire_time").val("");
  $("#id_expire_time").parent().find(".error-text").css("display", "none");
  expire_time = true;
});

function dateFromNowOn() {
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth() + 1; //January is 0!
  var yyyy = today.getFullYear();
  if (dd < 10) {
    dd = '0' + dd;
  }
  if (mm < 10) {
      mm = '0' + mm;
  }
  var fromNow = yyyy + '-' + mm + '-' + dd;
  document.getElementById("id_expire_date").setAttribute("min", fromNow);
  return fromNow;
}
window.onload = dateFromNowOn();

function timeFromNowOn() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  if (h < 10) {
    h = '0' + h;
  }
  if (m < 10) {
    m = '0' + m;
  }
  var fromNow = h + ':' + m;
  return fromNow;
}

onload = function() {
  localStorage.removeItem("today");
}

var expire_status_btn = document.getElementById('id_expire_status');
$(".url-expire-section").css("display", "none");
expire_status_btn.addEventListener('click', function() {
    if (expire_status_btn.checked) {
      $("#create-urlshortener-next").prop("disabled", false);
      expire_status = true;
      $(".url-expire-section").css("display", "none");
    } else {
      $("#create-urlshortener-next").prop("disabled", true);
      expire_status = false;
      $(".url-expire-section").css("display", "block");
    }
});

$('input, select, textarea').on('keyup keydown blur change', function() {
  if(long_url == true && expire_status == true && expire_time == true && expire_date == true && custom_path == true) {
    createus_next_btn = true;
  }
  else {
    createus_next_btn = false;
  }
  if(createus_next_btn == true) {
    $("#create-urlshortener-next").prop("disabled", false);
  }
  else {
    $("#create-urlshortener-next").prop("disabled", true);
  }
});

$('#short-another-url').on('click', function() {
  $("#qrcode-container").css("display", "none");
  if($("#id_long_url").val() == "") {
    long_url = false;
  }
  else if ($("#id_long_url").val().match(/^\s+$/)) {
    long_url = false;
  }
  else {
    long_url = true;
  }
});
// ====================== URL Shortener Modal ====================== //

// ============================= QR Code ================================ //
// Copy Shortened URL
$("#copy_shortened_url").click(function() {
  var shortenedURLField = document.getElementById("id_shortened_url");
  shortenedURLField.select();
  shortenedURLField.setSelectionRange(0, 99999); /* For mobile devices */
  navigator.clipboard.writeText(shortenedURLField.value);
  toastr.success('Shortened URL copied to clipboard')
});

// Share Shortened URL
var shortenedURLField = document.getElementById("id_shortened_url");
const shareData = {
  title: 'URL Shortener - AkirA',
  text: 'Short Long URLs using AkirA',
  url: shortenedURLField.value
}
const shareURLShortened_btn = document.getElementById('share_shortened_url');
shareURLShortened_btn.addEventListener('click', async () => {
  try {
    await navigator.share(shareData)
    toastr.success('Shortened URL shared successfully')
  } catch(err) {
    toastr.error(err)
  }
});

// QR Code
var qr_as_image;
$('#generate_qr_shorturl').click(function() {
  let shortenedURLField = document.getElementById("id_shortened_url");
  if (shortenedURLField.value) {
    let qrcodeContainer = document.getElementById("qrcode");
    qrcodeContainer.textContent = "";
    var qr = new QRious({
      element: qrcodeContainer,
      value: shortenedURLField.value,
      size: 200
    });
    qr_as_image = qr.toDataURL('image/jpeg');
    document.getElementById("qrcode-container").style.display = "block";
  } else {
    toastr.error('Unable to generate QR Code.')
  }
});

// QR Code as Image Save
$('#save_qr_code_image').click(function() {
  if (qr_as_image) {
    var link = document.createElement('a');
    link.download = 'qrcode.jpg';
    link.href = qr_as_image;
    link.click();
    toastr.success('QR Code saved successfully')
  } else {
    toastr.error('Please generate QR Code first')
  }
});
// ============================= QR Code ================================ //

// ====================== Full Screen ====================== //
var fullexitscreen = document.getElementById("fullexitscreen");
var elem = document.documentElement;

function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  }
}

function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen) { /* Safari */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE11 */
    document.msExitFullscreen();
  }
}

function setFS() {
  $('.set_mat_icon').html('fullscreen');
  $('.set_fullexitscreen').html('Full screen');
}

function setNormal() {
  $('.set_mat_icon').html('fullscreen_exit');
  $('.set_fullexitscreen').html('Normal');
}

fullexitscreen.addEventListener("click", function() {
  if(localStorage.getItem('fullscreen') === 'true'){
    localStorage.setItem('fullscreen', 'false');
    closeFullscreen();
    setFS();
  } 
  else {
    localStorage.setItem('fullscreen', 'true');
    openFullscreen();
    setNormal();
  }
}, false);

addEventListener('fullscreenchange', event => { 
  if (document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement || document.msFullscreenElement) {
    localStorage.setItem('fullscreen', 'true');
    setNormal();
  } else {
    localStorage.setItem('fullscreen', 'false');
    setFS();
  }
});

window.addEventListener('DOMContentLoaded', () => {
  if(localStorage.getItem('fullscreen') === 'true'){
    setFS();
    localStorage.setItem('fullscreen', 'false');
  }
});
// ====================== End Full Screen ====================== //