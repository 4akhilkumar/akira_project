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

    document.getElementById("id_encrypted_password").value = Encrypted_text;
}