document.getElementById("id_submit").addEventListener("click", myFunction);

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

    var EnUserKey = getShiftedString(Encrypted_text, username.length, 0);
    
    var HoneypotText = "";
    var alphaNumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < EnUserKey.length*2; i++)
        HoneypotText += alphaNumeric.charAt(Math.floor(Math.random() * alphaNumeric.length));

    var MergedText = "";
    for (var i = 0; i < EnUserKey.length; i++)
        MergedText += EnUserKey.charAt(i) + HoneypotText.charAt(i);

    document.getElementById("id_password").value = MergedText+HoneypotText;
}