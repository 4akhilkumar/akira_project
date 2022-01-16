var modal = document.getElementById("myModal");
var btn = document.getElementById("showFormCreateSemester");
var span = document.getElementById("close-model");

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}