var bulkStaffModal = document.getElementById("bulkStaffModalForm");
var showbulkStaffbtn = document.getElementById("showFormStaffBulkImport");
var bulkStaffModalSpan = document.getElementById("close-bulkStaffModal");

showbulkStaffbtn.onclick = function() {
  bulkStaffModal.style.display = "block";
}

bulkStaffModalSpan.onclick = function() {
  bulkStaffModal.style.display = "none";
}

var bulkOpeningModal = document.getElementById("bulkOpeningsModalForm");
var showbulkOpeningbtn = document.getElementById("showBulkOpeningForm");
var bulkOpeningModalSpan = document.getElementById("close-bulkOpeningsModalForm");

showbulkOpeningbtn.onclick = function() {
  bulkOpeningModal.style.display = "block";
}

bulkOpeningModalSpan.onclick = function() {
  bulkOpeningModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == bulkStaffModal) {
    bulkStaffModal.style.display = "none";
  }
  if (event.target == bulkOpeningModal) {
    bulkOpeningModal.style.display = "none";
  }
});