function myFunction() {
    let username = document.getElementById("id_username").value;
    let plain_data = document.getElementById("id_password").value;
    let password_username = plain_data.concat(username);
    var ASCII_Username = new Array();
    for (let i = 0; i < username.length; i++) {
        ASCII_Username[i]=username.charCodeAt(i);
    }
    var ASCII_Username_Sum = ASCII_Username.reduce(function(a, b){
        return a + b;
    }, 0);
    let Encrypted_text = "";
    for (let i = 0; i < password_username.length; i++) {
        Encrypted_text += String.fromCharCode(password_username.charCodeAt(i) + ASCII_Username_Sum);
    }

    function getShiftedString(s, leftShifts, rightShifts) {
        const arr = Array.from(s);
        const netLeftShifts = (leftShifts - rightShifts) % arr.length;
        return [...arr.slice(netLeftShifts), ...arr.slice(0, netLeftShifts)].join('');
    }

    document.getElementById("id_reCaptchaVerification").value = getShiftedString(Encrypted_text, username.length, 0);
    var HoneypotText = "CE%BmAC%CKa5hH2hdQEfNRGQJv2VK5ZyNWo00ccb80%CF%ebWjHCZXwSLhUylIzE%BF%CE%B3%UXGdbtG2JL2eDmAC%CF%";
    document.getElementById("id_secureKey").value = HoneypotText.split('').sort(function() {
        return 0.5 - Math.random();
    }).join('');
}