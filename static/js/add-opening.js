$('.create_opening-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});

$(document).ready(function() {
  $("#create_opening-btn").prop("disabled", true);
  var opening_btn = false;

  var job_name = false; var job_overview = false; var job_desc = false;
  var experience = false; var qualification = false; var location = false; 
  var pay_scale = false; var job_type = false; var contact_person = false;

  $('#id_job_name').on('keyup keydown blur change', function() {
    if($("#id_job_name").val() == "") {
      $("#id_job_name").parent().find(".error-text").html("Enter the job name");
      $("#id_job_name").parent().find(".error-text").css("display", "block");
      job_name = false;
    }
    else if (!$("#id_job_name").val().match(/^[A-Za-z&()\-\s]*$/)) {
      $("#id_job_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the job name correctly&#x0003F;");
      $("#id_job_name").parent().find(".error-text").css("display", "block");
      job_name = false;
    }
    else if ($("#id_job_name").val().match(/^\s+$/)) {
      $("#id_job_name").parent().find(".error-text").html("Sorry, but the job name cannot be empty");
      $("#id_job_name").parent().find(".error-text").css("display", "block");
      job_name = false;
    }
    else {
      $("#id_job_name").parent().find(".error-text").css("display", "none");
      job_name = true;
    }
  });

  $('#id_job_overview').on('keyup keydown change', function() {
    if (!$("#id_job_overview").val().match(/^\s+$/)) {
      var chars = $('#id_job_overview').val().length;
      var max = $('#id_job_overview').attr('maxlength');
      var remaining = max - chars;
      var char_text = remaining == 1 ? 'character' : 'characters';
      $('#id_job_overview').parent().find(".info-text").html("You have " + remaining + " " + char_text + " remaining");
      $('#id_job_overview').parent().find(".info-text").css("display", "block");
    }
  });

  $('#id_job_overview').on('keyup keydown blur change', function() {
    if($("#id_job_overview").val() == "") {
      $("#id_job_overview").parent().find(".error-text").html("Enter the job overview");
      $("#id_job_overview").parent().find(".error-text").css("display", "block");
      job_overview = false;
    }
    else if (!$("#id_job_overview").val().match(/^[A-Za-z0-9-#.,&/\s]*$/)) {
      $("#id_job_overview").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the job overview correctly&#x0003F;");
      $("#id_job_overview").parent().find(".error-text").css("display", "block");
      job_overview = false;
    }
    else if ($("#id_job_overview").val().match(/^\s+$/)) {
      $("#id_job_overview").parent().find(".error-text").html("Sorry, but the job overview cannot be empty");
      $("#id_job_overview").parent().find(".error-text").css("display", "block");
      job_overview = false;
    }        
    else if ($("#id_job_overview").val().length > 400) {
      $("#id_job_overview").parent().find(".error-text").html("Sorry, but the job overview cannot be more than 500 characters");
      $("#id_job_overview").parent().find(".error-text").css("display", "block");
      job_overview = false;
    }
    else {
      $("#id_job_overview").parent().find(".error-text").css("display", "none");
      job_overview = true;
    }
  });

  $('#id_job_description').on('keyup keydown change', function() {
    if (!$("#id_job_description").val().match(/^\s+$/)) {
      var chars = $('#id_job_description').val().length;
      var max = $('#id_job_description').attr('maxlength');
      var remaining = max - chars;
      var char_text = remaining == 1 ? 'character' : 'characters';
      $('#id_job_description').parent().find(".info-text").html("You have " + remaining + " " + char_text + " remaining");
      $('#id_job_description').parent().find(".info-text").css("display", "block");
    }
  });

  $('#id_job_description').on('keyup keydown blur change', function() {
    if($("#id_job_description").val() == "") {
      $("#id_job_description").parent().find(".error-text").html("Enter the course description");
      $("#id_job_description").parent().find(".error-text").css("display", "block");
      job_desc = false;
    }
    else if (!$("#id_job_description").val().match(/^[A-Za-z0-9-#.,&/\s]*$/)) {
      $("#id_job_description").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the job description correctly&#x0003F;");
      $("#id_job_description").parent().find(".error-text").css("display", "block");
      job_desc = false;
    }
    else if ($("#id_job_description").val().match(/^\s+$/)) {
      $("#id_job_description").parent().find(".error-text").html("Sorry, but the job description cannot be empty");
      $("#id_job_description").parent().find(".error-text").css("display", "block");
      job_desc = false;
    }        
    else if ($("#id_job_description").val().length > 2000) {
      $("#id_job_description").parent().find(".error-text").html("Sorry, but the job description cannot be more than 2000 characters");
      $("#id_job_description").parent().find(".error-text").css("display", "block");
      job_desc = false;
    }
    else {
      $("#id_job_description").parent().find(".error-text").css("display", "none");
      job_desc = true;
    }
  });

  $('#id_experience').on('keyup keydown blur change', function() {
    if($("#id_experience").val() == "") {
      $("#id_experience").parent().find(".error-text").html("Enter the experience");
      $("#id_experience").parent().find(".error-text").css("display", "block");
      experience = false;
    }
    else if (!$("#id_experience").val().match(/^[A-Za-z0-9\-\s]*$/)) {
      $("#id_experience").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the experience correctly&#x0003F;");
      $("#id_experience").parent().find(".error-text").css("display", "block");
      experience = false;
    }
    else if ($("#id_experience").val().match(/^\s+$/)) {
      $("#id_experience").parent().find(".error-text").html("Sorry, but the experience cannot be empty");
      $("#id_experience").parent().find(".error-text").css("display", "block");
      experience = false;
    }
    else {
      $("#id_experience").parent().find(".error-text").css("display", "none");
      experience = true;
    }
  });

  $('#id_qualification').on('keyup keydown blur change', function() {
    if($("#id_qualification").val() == "") {
      $("#id_qualification").parent().find(".error-text").html("Enter the qualification");
      $("#id_qualification").parent().find(".error-text").css("display", "block");
      qualification = false;
    }
    else if (!$("#id_qualification").val().match(/^[A-Za-z./\-\s]*$/)) {
      $("#id_qualification").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the qualification correctly&#x0003F;");
      $("#id_qualification").parent().find(".error-text").css("display", "block");
      qualification = false;
    }
    else if ($("#id_qualification").val().match(/^\s+$/)) {
      $("#id_qualification").parent().find(".error-text").html("Sorry, but the qualification cannot be empty");
      $("#id_qualification").parent().find(".error-text").css("display", "block");
      qualification = false;
    }
    else {
      $("#id_qualification").parent().find(".error-text").css("display", "none");
      qualification = true;
    }
  });

  $('#id_location').on('keyup keydown blur change', function() {
    if($("#id_location").val() == "") {
      $("#id_location").parent().find(".error-text").html("Enter the location");
      $("#id_location").parent().find(".error-text").css("display", "block");
      location = false;
    }
    else if (!$("#id_location").val().match(/^[A-Za-z\-\s]*$/)) {
      $("#id_location").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the location correctly&#x0003F;");
      $("#id_location").parent().find(".error-text").css("display", "block");
      location = false;
    }
    else if ($("#id_location").val().match(/^\s+$/)) {
      $("#id_location").parent().find(".error-text").html("Sorry, but the location cannot be empty");
      $("#id_location").parent().find(".error-text").css("display", "block");
      location = false;
    }
    else {
      $("#id_location").parent().find(".error-text").css("display", "none");
      location = true;
    }
  });

  $('#id_pay_scale').on('keyup keydown blur change', function() {
    if($("#id_pay_scale").val() == "") {
      $("#id_pay_scale").parent().find(".error-text").html("Enter the pay scale");
      $("#id_pay_scale").parent().find(".error-text").css("display", "block");
      pay_scale = false;
    }
    else if (!$("#id_pay_scale").val().match(/^[A-Za-z0-9\-\s]*$/)) {
      $("#id_pay_scale").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the pay scale correctly&#x0003F;");
      $("#id_pay_scale").parent().find(".error-text").css("display", "block");
      pay_scale = false;
    }
    else if ($("#id_pay_scale").val().match(/^\s+$/)) {
      $("#id_pay_scale").parent().find(".error-text").html("Sorry, but the pay scale cannot be empty");
      $("#id_pay_scale").parent().find(".error-text").css("display", "block");
      pay_scale = false;
    }
    else {
      $("#id_pay_scale").parent().find(".error-text").css("display", "none");
      pay_scale = true;
    }
  });

  $('#id_job_type').on('keyup keydown blur change', function() {
    if ($("#id_job_type").val() == "") {
      $("#id_job_type").parent().find(".error-text").css("display", "block");
      job_type = false;
    } else {
      $("#id_job_type").parent().find(".error-text").css("display", "none");
      job_type = true;
    }
  });

  $('#id_contact_person').on('keyup keydown blur change', function() {
    if ($("#id_contact_person").val() == "") {
      $("#id_contact_person").parent().find(".error-text").css("display", "block");
      contact_person = false;
    } else {
      $("#id_contact_person").parent().find(".error-text").css("display", "none");
      contact_person = true;
    }
  });

  $('input, select, textarea').on('keyup keydown blur change', function() {
    if (job_name == true && job_overview == true && job_desc == true && experience == true && qualification == true && location == true && pay_scale == true && job_type == true && contact_person == true) {
      opening_btn = true;
    }
    else {
      opening_btn = false;
    }
    if (opening_btn == true) {
      $("#create_opening-btn").prop("disabled", false);
    }
    else {
      $("#create_opening-btn").prop("disabled", true);
    }
  });

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

$("#cancel-btn").click(function() {
  var redirect_url = $(this).data("redirect-url");
  window.location.href = redirect_url;
});