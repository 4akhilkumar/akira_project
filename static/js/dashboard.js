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

// ====================== Skeleton CSS ====================== //
const allSkeleton = document.querySelectorAll('.skeleton')
window.addEventListener('load', function() {
  allSkeleton.forEach(item=> {
    item.classList.remove('skeleton')
  })
})
// ====================== Skeleton CSS ====================== //

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
    console.log("entered fullscreen mode.");
  } else {
    localStorage.setItem('fullscreen', 'false');
    setFS();
    console.log('Leaving fullscreen mode.');
  }
});

window.addEventListener('DOMContentLoaded', () => {
  if(localStorage.getItem('fullscreen') === 'true'){
    setFS();
    localStorage.setItem('fullscreen', 'false');
  }
});
// ====================== End Full Screen ====================== //