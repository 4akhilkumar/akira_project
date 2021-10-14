/*==================== SHOW NAVBAR ====================*/ 
const showMenu = (headerToggle, navbarId) =>{
  const toggleBtn = document.getElementById(headerToggle),
  nav = document.getElementById(navbarId)
  
  // Validate that variables exist
  if(headerToggle && navbarId){
      toggleBtn.addEventListener('click', ()=>{
          // We add the show-menu class to the div tag with the nav__menu class
          nav.classList.toggle('show-menu')
          // change icon
          toggleBtn.classList.toggle('fa-times')
      })
  }
}
showMenu('header-toggle','navbar')

/*==================== LINK ACTIVE ====================*/
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
  linkColor.forEach(l => l.classList.remove('active'))
  this.classList.add('active')
}

linkColor.forEach(l => l.addEventListener('click', colorLink))

/*====================== Dark Mode =====================*/
// check for saved 'darkMode' in localStorage
let darkMode = localStorage.getItem('darkMode'); 
const darkModeToggle = document.querySelector('#dark-mode-toggle');

// check for saved 'dark_mode' in localStorage
let dark_mode = localStorage.getItem('darkMode'); 
const themeToggle = document.querySelector('#theme');

const enableDarkMode = () => {
// 1. Add the class to the body
document.body.classList.add('darkmode');
// 2. Update darkMode in localStorage
localStorage.setItem('darkMode', 'enabled');
// 3. Update dark_mode in localStorage
localStorage.setItem('dark_mode', 'enabled');
}

const disableDarkMode = () => {
// 1. Remove the class from the body
document.body.classList.remove('darkmode');
// 2. Update darkMode in localStorage 
localStorage.setItem('darkMode', null);
// 3. Update dark_mode in localStorage
localStorage.setItem('dark_mode', null);
}

const enableDarkText = () => {
  themeToggle.classList.add('darkmode-active');
  themeToggle.classList.remove('lightmode-active');
}

const disableDarkText = () => {
  themeToggle.classList.remove('darkmode-active');
  themeToggle.classList.add('lightmode-active');
}

// If the user already visited and enabled darkMode
// start things off with it on
if (darkMode === 'enabled') {
enableDarkMode();
}

// When someone clicks the button
darkModeToggle.addEventListener('click', () => {
// get their darkMode setting
darkMode = localStorage.getItem('darkMode'); 

// if it not current enabled, enable it
if (darkMode !== 'enabled') {
    enableDarkMode();
// if it has been enabled, turn it off  
} else {  
    disableDarkMode(); 
}
});

if (dark_mode === 'enabled') {
  enableDarkText();
}
else {
  disableDarkText();
}

// When someone clicks the button
themeToggle.addEventListener('click', () => {
  // get their dark_mode setting
  dark_mode = localStorage.getItem('dark_mode'); 
  
  // if it not current enabled, enable it
  if (dark_mode !== 'enabled') {
    enableDarkText();
  // if it has been enabled, turn it off  
  } else {  
    disableDarkText(); 
  }
});

/* ======= checkSemesterStatus ======= */
function checkSemesterStatus() {
  var checkBox = document.getElementById("id_semester_status");
  let str = document.getElementById("semesterStatus").innerHTML; 
  if (checkBox.checked == true){
    document.getElementById("semesterStatus").innerHTML = str.replace("Disabled", "Active");
  } else {
    document.getElementById("semesterStatus").innerHTML = str.replace("Active", "Disabled");
  }
}