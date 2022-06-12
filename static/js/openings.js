const wrapper = document.querySelector(".wrapper");
const header = document.querySelector(".header");

wrapper.addEventListener("scroll", (e) => {
 e.target.scrollTop > 30
  ? header.classList.add("header-shadow")
  : header.classList.remove("header-shadow");
});

const toggleButton = document.querySelector(".dark-light");

toggleButton.addEventListener("click", () => {
 document.body.classList.toggle("dark-mode");
});

const jobCards = document.querySelectorAll(".job-card");
const logo = document.querySelector(".logo");
const jobLogos = document.querySelector(".job-logos");
const jobDetailTitle = document.querySelector(
 ".job-explain-content .job-card-title"
);
const jobBg = document.querySelector(".job-bg");

$(document).ready(function() {
  var createCourseUrl = $('#createCourse').data('create-course-url');
  $('#createCourse').click(function() {
    window.location.href = createCourseUrl;
  });

  var placeholderArray = ['Job Name', 'Employment Type', 'Experience'];
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

$('.job-card-buttons .card-buttons-more').on('click', function() {
  const number = Math.floor(Math.random() * 10);
  const url = `https://unsplash.it/640/425?image=${number}`;
  jobBg.src = url;
  jobDetailTitle.textContent = $($(this).parent()).parent().find('.job-card-title').text();
  const logo = $($(this).parent()).parent().find('svg')[0];
  const bg = logo.style.backgroundColor;
  jobBg.style.background = bg;
  jobLogos.innerHTML = logo.outerHTML;
  wrapper.classList.add("detail-page");
  wrapper.scrollTop = 0;
  // get the height of div.job-explain
  const height = document.querySelector(".job-explain").offsetHeight;
  // change the max-height of div.job-overview-cards
  document.querySelector(".job-overview-cards").style.maxHeight = `${height}px`;
});

$('.job-overview-card').on('click', function() {
  const number = Math.floor(Math.random() * 10);
  const url = `https://unsplash.it/640/425?image=${number}`;
  jobBg.src = url;
  jobDetailTitle.textContent = $(this).find('.job-card-title').text();
  const logo = $(this).find('svg')[0];
  const bg = logo.style.backgroundColor;
  jobBg.style.background = bg;
  jobLogos.innerHTML = logo.outerHTML;
  wrapper.classList.add("detail-page");
  wrapper.scrollTop = 0;
  // get the height of div.job-explain
  const height = document.querySelector(".job-explain").offsetHeight;
  // change the max-height of div.job-overview-cards
  document.querySelector(".job-overview-cards").style.maxHeight = `${height}px`;
});

// jobCards.forEach((jobCard) => {
//  jobCard.addEventListener("click", () => {
//   const number = Math.floor(Math.random() * 10);
//   const url = `https://unsplash.it/640/425?image=${number}`;
//   jobBg.src = url;
//   const logo = jobCard.querySelector("svg");
//   const bg = logo.style.backgroundColor;
//   jobBg.style.background = bg;
//   const title = jobCard.querySelector(".job-card-title");
//   jobDetailTitle.textContent = title.textContent;
//   jobLogos.innerHTML = logo.outerHTML;
//   wrapper.classList.add("detail-page");
//   wrapper.scrollTop = 0;
//   // get the height of div.job-explain
//   const height = document.querySelector(".job-explain").offsetHeight;
//   // change the max-height of div.job-overview-cards
//   document.querySelector(".job-overview-cards").style.maxHeight = `${height}px`;
//  });
// });

logo.addEventListener("click", () => {
 wrapper.classList.remove("detail-page");
 wrapper.scrollTop = 0;
});

$('.searchQueryInput').on('keyup', function() {
  var filter = $(".searchQueryInput").val().toLowerCase().trim();
  var nodes = document.getElementsByClassName('jobTarget');

  var MatchedNodesJobs = 0;
  for (i = 0; i < nodes.length; i++) {
    if (nodes[i].innerText.toLowerCase().includes(filter)) {
      nodes[i].style.display = "block";
      MatchedNodesJobs++;
    } else {
      nodes[i].style.display = "none";
    }
  }
  var spjob = "";
  MatchedNodesJobs == 1 ? spjob = " Job" : spjob = " Jobs";
  $('.searched-show').text("Showing " + MatchedNodesJobs + spjob);
});