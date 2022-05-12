document.getElementById("id_submit").addEventListener("click", encryptPassKey);

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function convertASCIItoHex(asciiString) {
    let hex = '';
    let tempASCII, tempHex;
    asciiString.split('').map( i => {
        tempASCII = i.charCodeAt(0)
        tempHex = tempASCII.toString(16);
        hex = hex + tempHex + '';
    });
    hex = hex.trim();
    return hex;
}

function encryptPassKey() {
    let username = document.getElementById("id_username").value;
    let password = document.getElementById("id_password").value;
    let request_token = getCookie('request_token');

    // Convert the request_token from string into hexadecimal and store it in a variable
    // let hex_request_token = convertASCIItoHex(request_token);
    // console.log(hex_request_token);

    // ASCII Values of Username
    var ASCII_Username = new Array();
    for (let i = 0; i < username.length; i++) {
        ASCII_Username[i]=username.charCodeAt(i);
    }

    // Sum value of ASCII Values of Username
    var ASCII_Username_Sum = ASCII_Username.reduce(function(a, b){
        return a + b;
    }, 0);

    // Converting ASCII_Username_Sum to Array
    const arrayOfASCII_Username_Sum = Array.from(String(ASCII_Username_Sum), Number);

    // If arrayOfASCII_Username_Sum array contains any element zero, then replace those zero with 1
    for (let i = 0; i < arrayOfASCII_Username_Sum.length; i++) {
        if (arrayOfASCII_Username_Sum[i] == 0) {
            arrayOfASCII_Username_Sum[i] = 1;
        }
    }

    // First Largest Number in arrayOfASCII_Username_Sum
    var FirLarAUS = Math.max(...arrayOfASCII_Username_Sum);

    // Second Largest Number in arrayOfASCII_Username_Sum
    var SecLarAUS = Math.max(...arrayOfASCII_Username_Sum.filter(x => x !== FirLarAUS));

    // If SecLarAUS is zero or not finite then replace it with FirLarAUS + 1
    if (SecLarAUS == 0 || !isFinite(SecLarAUS) || SecLarAUS == FirLarAUS) {
        SecLarAUS = FirLarAUS + 1;
    }

    var SaltText = "";
    var alphaNumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < password.length*username.length*10; i++) {
        SaltText += alphaNumeric.charAt(Math.floor(Math.random() * alphaNumeric.length));
    }

    var saltTextSepUL10 = SaltText.match(new RegExp('.{1,' + username.length*10 + '}', 'g'))

    // Create a random digit of length of password
    function generate(n) {
        var add = 1, max = 12 - add;
        if ( n > max ) {
            return generate(max) + generate(n - max);
        }
        max        = Math.pow(10, n+add);
        var min    = max/10; // Math.pow(10, n) basically
        var number = Math.floor( Math.random() * (max - min + 1) ) + min;
        return ("" + number).substring(add);
    }
    var random_digit = generate(password.length)

    var randomNumberArray = Array.from(String(random_digit), Number);

    // First Largest Number in randomNumberArray
    var FirLarRNA = Math.max(...randomNumberArray);

    let AlteredText = "";
    for (let i = 0; i < password.length; i++) {
        AlteredText += String.fromCharCode(password.charCodeAt(i) + FirLarAUS + FirLarRNA);
    }

    let AlteredTextHex = convertASCIItoHex(AlteredText);

    // Replace the two characters in each element of saltTextSepUL10 at the index of randomNumberArray with the two characters in AlteredTextHex
    var saltArrayAT = saltTextSepUL10.map(function(item, index) {
        return item.substring(0, randomNumberArray[index]) + AlteredTextHex.substring(index*2,(index*2)+2) + item.substring(randomNumberArray[index] + 2);
    });

    // Replace the characters in each element of saltArrayAT using SecLarAUS value as Index from the end with characters of random_digit
    var FinalArray = saltArrayAT.map(function(item, index) {
        return item.substring(0, item.length - SecLarAUS) + random_digit.charAt(index) + item.substring(item.length - SecLarAUS + 1);
    });

    // Merge all elements of FinalArray into one string
    var mergingFinalArray = FinalArray.join("");
    
    // display password in the id="plain-text"
    document.getElementById("id_password").value = mergingFinalArray;
}