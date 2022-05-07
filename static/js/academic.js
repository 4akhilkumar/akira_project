var blockModal = document.getElementById("blockModalForm");
var floorModal = document.getElementById("floorModalForm");
var roomModal = document.getElementById("roomModalForm");
var bulkBlockFloorRoomModal = document.getElementById("bulkBlockFloorRoomModalForm");

var showFormCreateBlockbtn = document.getElementById("showFormCreateBlock");
var showFormCreateFloorbtn = document.getElementById("showFormCreateFloor");
var showFormCreateRoombtn = document.getElementById("showFormCreateRoom");
var showFormCreateBulkbtn = document.getElementById("showFormCreateBulk");

var blockModalSpan = document.getElementById("close-blockModel");
var floorModalSpan = document.getElementById("close-floorModal");
var roomModalSpan = document.getElementById("close-roomModal");
var bulkBlockFloorRoomSpan = document.getElementById("close-bulkBlockFloorRoomModal");

showFormCreateBlockbtn.onclick = function() {
  blockModal.style.display = "block";
}
showFormCreateFloorbtn.onclick = function() {
  floorModal.style.display = "block";
}
showFormCreateRoombtn.onclick = function() {
  roomModal.style.display = "block";
}
showFormCreateBulkbtn.onclick = function() {
  bulkBlockFloorRoomModal.style.display = "block";
}

blockModalSpan.onclick = function() {
  blockModal.style.display = "none";
}
floorModalSpan.onclick = function() {
  floorModal.style.display = "none";
}
roomModalSpan.onclick = function() {
  roomModal.style.display = "none";
}
bulkBlockFloorRoomSpan.onclick = function() {
  bulkBlockFloorRoomModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == blockModal) {
    blockModal.style.display = "none";
  }
  if (event.target == floorModal) {
    floorModal.style.display = "none";
  }
  if (event.target == roomModal) {
    roomModal.style.display = "none";
  }
  if (event.target == bulkBlockFloorRoomModal) {
    bulkBlockFloorRoomModal.style.display = "none";
  }
});

$("select[name = 'get_block_id']").change(function () {
  const blockId = $(this).val();
  var getFloorbyBlockURL = $("#id_room_block").data('get-floor-by-block');
  $.ajax({
    type: "POST",
    url: getFloorbyBlockURL,
    data: {
      'block': blockId,
      'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function (data) {
      console.log(data);
      let html_data = '<option value=""> Select Floor </option>';
      data.forEach(function (data) {
        html_data += `<option value="${data.id}">${data.name}</option>`
      });
      $("#id_room_floor_name_no").html(html_data);
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

$(document).ready(function() {
  // Block form validation BEGIN
  $("#block-btn").prop("disabled", true);
  var block_btn = false;

  var block_name = false; var block_desc = false;

  $('#id_block_name').on('keyup keydown blur change', function() {
    if($("#id_block_name").val() == "") {
      $("#id_block_name").parent().find(".error-text").html("Enter the block name");
      $("#id_block_name").parent().find(".error-text").css("display", "block");
      block_name = false;
    }
    else if (!$("#id_block_name").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
      $("#id_block_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the block name correctly&#x0003F;");
      $("#id_block_name").parent().find(".error-text").css("display", "block");
      block_name = false;
    }
    else if ($("#id_block_name").val().match(/^\s+$/)) {
      $("#id_block_name").parent().find(".error-text").html("Sorry, but the block name cannot be empty");
      $("#id_block_name").parent().find(".error-text").css("display", "block");
      block_name = false;
    }
    else {
      $("#id_block_name").parent().find(".error-text").css("display", "none");
      block_name = true;
    }
  });

  $('#id_block_desc').on('keyup keydown change', function() {
    if (!$("#id_block_desc").val().match(/^\s+$/)) {
      var chars = $('#id_block_desc').val().length;
      var max = $('#id_block_desc').attr('maxlength');
      var remaining = max - chars;
      var char_text = remaining == 1 ? 'character' : 'characters';
      $('#id_block_desc').parent().find(".info-text").html("You have " + remaining + " " + char_text + " remaining");
      $('#id_block_desc').parent().find(".info-text").css("display", "block");
    }
  });

  $('#id_block_desc').on('keyup keydown blur change', function() {
    if($("#id_block_desc").val() == "") {
      $("#id_block_desc").parent().find(".error-text").html("Enter the block description");
      $("#id_block_desc").parent().find(".error-text").css("display", "block");
      block_desc = false;
    }
    else if (!$("#id_block_desc").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
      $("#id_block_desc").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the block description correctly&#x0003F;");
      $("#id_block_desc").parent().find(".error-text").css("display", "block");
      block_desc = false;
    }
    else if ($("#id_block_desc").val().match(/^\s+$/)) {
      $("#id_block_desc").parent().find(".error-text").html("Sorry, but the block description cannot be empty");
      $("#id_block_desc").parent().find(".error-text").css("display", "block");
      block_desc = false;
    }        
    else if ($("#id_block_desc").val().length > 500) {
      $("#id_block_desc").parent().find(".error-text").html("Sorry, but the block description cannot be more than 500 characters");
      $("#id_block_desc").parent().find(".error-text").css("display", "block");
      block_desc = false;
    }
    else {
      $("#id_block_desc").parent().find(".error-text").css("display", "none");
      block_desc = true;
    }
  });

  $('input, select, textarea').on('keyup keydown blur change', function() {
    if (block_name == true && block_desc == true) {
      block_btn = true;
    }
    else {
      block_btn = false;
    }
    if (block_btn == true) {
      $("#block-btn").prop("disabled", false);
    }
    else {
      $("#block-btn").prop("disabled", true);
    }
  });
  // Block form validation END

  // Floor form validation Begin
  $("#floor-btn").prop("disabled", true);
  var floor_btn = false;

  var floor_name_no = false; var floor_block_id = false;

  $('#id_floor_name').on('keyup keydown blur change', function() {
    if($("#id_floor_name").val() == "") {
      $("#id_floor_name").parent().find(".error-text").html("Enter the floor name/no.");
      $("#id_floor_name").parent().find(".error-text").css("display", "block");
      floor_name_no = false;
    }
    else if (!$("#id_floor_name").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
      $("#id_floor_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the floor name/no. correctly&#x0003F;");
      $("#id_floor_name").parent().find(".error-text").css("display", "block");
      floor_name_no = false;
    }
    else if ($("#id_floor_name").val().match(/^\s+$/)) {
      $("#id_floor_name").parent().find(".error-text").html("Sorry, but the floor name/no. cannot be empty");
      $("#id_floor_name").parent().find(".error-text").css("display", "block");
      floor_name_no = false;
    }
    else {
      $("#id_floor_name").parent().find(".error-text").css("display", "none");
      floor_name_no = true;
    }
  });

  $('#id_floor_block_id').on('keyup keydown blur change', function() {
    if ($("#id_floor_block_id").val() == "") {
      $("#id_floor_block_id").parent().find(".error-text").css("display", "block");
      floor_block_id = false;
    } else {
      $("#id_floor_block_id").parent().find(".error-text").css("display", "none");
      floor_block_id = true;
    }
  });

  $('input, select').on('keyup keydown blur change', function() {
    if (floor_name_no == true && floor_block_id == true) {
      floor_btn = true;
    }
    else {
      floor_btn = false;
    }
    if (floor_btn == true) {
      $("#floor-btn").prop("disabled", false);
    }
    else {
      $("#floor-btn").prop("disabled", true);
    }
  });
  // Floor Form Validation End

  // Room form validation Begin
  $("#room-btn").prop("disabled", true);
  var room_btn = false;

  var room_name = false; var id_room_block = false; var room_floor = false;
  var room_room_type = false; var capacity = false;

  $('#id_room_name').on('keyup keydown blur change', function() {
    if($("#id_room_name").val() == "") {
      $("#id_room_name").parent().find(".error-text").html("Enter the room name");
      $("#id_room_name").parent().find(".error-text").css("display", "block");
      room_name = false;
    }
    else if (!$("#id_room_name").val().match(/^[A-Za-z0-9-#_.,'":;()[\]{}&/\s]*$/)) {
      $("#id_room_name").parent().find(".error-text").html("Are you sure that you&#x00027;ve entered the room name correctly&#x0003F;");
      $("#id_room_name").parent().find(".error-text").css("display", "block");
      room_name = false;
    }
    else if ($("#id_room_name").val().match(/^\s+$/)) {
      $("#id_room_name").parent().find(".error-text").html("Sorry, but the room name cannot be empty");
      $("#id_room_name").parent().find(".error-text").css("display", "block");
      room_name = false;
    }
    else {
      $("#id_room_name").parent().find(".error-text").css("display", "none");
      room_name = true;
    }
  });

  $('#id_room_block').on('keyup keydown blur change', function() {
    if ($("#id_room_block").val() == "") {
      $("#id_room_block").parent().find(".error-text").css("display", "block");
      id_room_block = false;
    } else {
      $("#id_room_block").parent().find(".error-text").css("display", "none");
      id_room_block = true;
    }
  });

  $('#id_room_floor_name_no').on('keyup keydown blur change', function() {
    if ($("#id_room_floor_name_no").val() == "") {
      $("#id_room_floor_name_no").parent().find(".error-text").css("display", "block");
      room_floor = false;
    } else {
      $("#id_room_floor_name_no").parent().find(".error-text").css("display", "none");
      room_floor = true;
    }
  });

  $('#id_room_room_type').on('keyup keydown blur change', function() {
    if ($("#id_room_room_type").val() == "") {
      $("#id_room_room_type").parent().find(".error-text").css("display", "block");
      room_room_type = false;
    } else {
      $("#id_room_room_type").parent().find(".error-text").css("display", "none");
      room_room_type = true;
    }
  });

  $('#id_room_capacity').on('keyup keydown blur change', function() {
    if ($("#id_room_capacity").val() == "") {
      $("#id_room_capacity").parent().find(".error-text").html("Enter room capacity");
      $("#id_room_capacity").parent().find(".error-text").css("display", "block");
      capacity = false;
    }
    else if ($("#id_room_capacity").val() > 200) {
      $("#id_room_capacity").parent().find(".error-text").html("Room capacity can be more than 200&#x0003F;");
      $("#id_room_capacity").parent().find(".error-text").css("display", "block");
      // capacity = true;
    }
    else {
      $("#id_room_capacity").parent().find(".error-text").css("display", "none");
      capacity = true;
    }
  });

  $('input, select').on('keyup keydown blur change', function() {
    if (room_name == true && id_room_block == true && room_floor == true && room_room_type == true && capacity == true) {
      room_btn = true;
    }
    else {
      room_btn = false;
    }
    if (room_btn == true) {
      $("#room-btn").prop("disabled", false);
    }
    else {
      $("#room-btn").prop("disabled", true);
    }
  });
  // Room Form Validation End
});

$('.branch-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});

$('.block-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});

$('.floor-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});

$('.room-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});

$('.academic-bulk-btn').click(function() {
  $(this).prop('disabled', true);
  $(this).html('Please wait...');
  $(this).closest('form').submit();
});