$(document).ready(function() {
  var placeholderArray = ['Course Code', 'Course Name', 'Anything related to it!'];
  setInterval(function() {
      var searchQueryInput = $('.searchQueryInput').attr('placeholder', "Search " + placeholderArray[Math.floor(Math.random() * placeholderArray.length)]);
      var searchQueryInputList = $('.searchQueryInputList');
      searchQueryInputList.empty();
      searchQueryInput.show();
  }
  , 1000);
});

$(document).keypress(function(e) {
  if (e.which == 47 && !$('.searchQueryInput').is(':focus')) {
      $('.searchQueryInput').focus();
      return false;
  }
});

$("#searchQuerySubmit").prop("disabled", true);
var searchQuery = false;

$('.searchQueryInput').on('keyup keydown blur change', function() {
  if($(".searchQueryInput").val() == "") {
      $(".searchQueryInput").parent().find(".error-text").css("display", "block");
      searchQuery = false;
  }
  else if ($(".searchQueryInput").val().match(/^\s+$/)) {
      $(".searchQueryInput").parent().find(".error-text").css("display", "block");
      searchQuery = false;
  }
  else {
      $(".searchQueryInput").parent().find(".error-text").css("display", "none");
      searchQuery = true;
  }
});

$('input').on('keyup keydown blur change', function() {
  if (searchQuery == true) {
      $("#searchQuerySubmit").prop("disabled", false);
  }
  else {
      $("#searchQuerySubmit").prop("disabled", true);
  }
});

$("#searchQuerySubmit").click(function(e) {
  e.preventDefault();
});

document.addEventListener("DOMContentLoaded", () => {
  $("#id_searchSemCourseData").on("keyup", function() {
      var searchQuery = $(this).val().toLowerCase().trim();
      var ResultStatus = true;
      $("#id_SemCourseMngTable tr").filter(function() {
          $(this).toggle($(this).text()
          .toLowerCase().indexOf(searchQuery) > -1)
          if ($(this).text().toLowerCase().indexOf(searchQuery) == -1) {
              ResultStatus = false;
          }
      });
      if (ResultStatus == false) {
          // change the css nodatafound display to block
          console.log("noDataFound");
      }
  });
});

function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));

    // Sort each row
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();

        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
    });

    // Remove all existing TRs from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }

    // Re-add the newly sorted rows
    tBody.append(...sortedRows);

    // Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table-sortable .table-header-title").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});