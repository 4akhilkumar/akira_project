var bulkStaffModal = document.getElementById("bulkStaffModalForm");
var showbulkStaffbtn = document.getElementById("showFormStaffBulkImport");
var bulkStaffModalSpan = document.getElementById("close-bulkStaffModal");

showbulkStaffbtn.onclick = function() {
  bulkStaffModal.style.display = "block";
}

bulkStaffModalSpan.onclick = function() {
  bulkStaffModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == bulkStaffModal) {
    bulkStaffModal.style.display = "none";
  }
});