var admissionProgrammeModal = document.getElementById("admissionProgrammeModalForm");
var showFormCreateAdmissionProgrammebtn = document.getElementById("showFormCreateAdmissionProgramme");
var admissionProgrammeModalFormModalSpan = document.getElementById("close-admissionProgrammeModalForm");

showFormCreateAdmissionProgrammebtn.onclick = function() {
  admissionProgrammeModal.style.display = "block";
}

admissionProgrammeModalFormModalSpan.onclick = function() {
  admissionProgrammeModal.style.display = "none";
}

$(window).click(function(event) {
  if (event.target == admissionProgrammeModal) {
    admissionProgrammeModal.style.display = "none";
  }
});