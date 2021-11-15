/*====================== Dark Mode =====================*/
// check for saved 'darkMode' in localStorage
let darkMode = localStorage.getItem('darkMode'); 
const darkModeToggle = document.querySelector('#dark-mode-toggle');
const themeToggle = document.querySelector('#theme');

const enableDarkMode = () => {
// 1. Add the class to the body
document.body.classList.add('darkmode');
// 2. Add the class to the body
themeToggle.classList.add('darkmode-active');
themeToggle.classList.remove('lightmode-active');
// 3. Update darkMode in localStorage
localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
// 1. Remove the class from the body
document.body.classList.remove('darkmode');
// 2. Remove the class from the body
themeToggle.classList.remove('darkmode-active');
themeToggle.classList.add('lightmode-active');
// 3. Update darkMode in localStorage 
localStorage.setItem('darkMode', null);
}

// If the user already visited and enabled darkMode
// start things off with it on
if (darkMode === 'enabled') {
  enableDarkMode();
}
else {
  disableDarkMode();
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