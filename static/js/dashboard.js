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

const enableDarkMode = () => {
// 1. Add the class to the body
document.body.classList.add('darkmode');
// 2. Update darkMode in localStorage
localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
// 1. Remove the class from the body
document.body.classList.remove('darkmode');
// 2. Update darkMode in localStorage 
localStorage.setItem('darkMode', null);
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