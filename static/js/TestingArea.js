document.getElementById("id_submit").addEventListener("click", myFunction);

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

function myFunction() {
    let username = document.getElementById("id_username").value;
    let password = document.getElementById("id_password").value;
    let request_token = getCookie('request_token');
    console.log(request_token);

    // Convert the request_token from string into hexadecimal and store it in a variable
    // let hex_request_token = convertASCIItoHex(request_token);
    // console.log(hex_request_token);

    // The Username
    console.log("Username:",username);
    // ASCII Values of Username
    var ASCII_Username = new Array();
    for (let i = 0; i < username.length; i++) {
        ASCII_Username[i]=username.charCodeAt(i);
    }
    console.log(ASCII_Username);
    // Sum value of ASCII Values of Username
    var ASCII_Username_Sum = ASCII_Username.reduce(function(a, b){
        return a + b;
    }, 0);
    console.log("Key:",ASCII_Username_Sum);

    // Converting ASCII_Username_Sum to Array
    const arrayOfASCII_Username_Sum = Array.from(String(ASCII_Username_Sum), Number);
    console.log("Key Array",arrayOfASCII_Username_Sum);

    // If arrayOfASCII_Username_Sum array contains any element zero, then replace those zero with 1
    for (let i = 0; i < arrayOfASCII_Username_Sum.length; i++) {
        if (arrayOfASCII_Username_Sum[i] == 0) {
            arrayOfASCII_Username_Sum[i] = 1;
        }
    }
    console.log("Key Array",arrayOfASCII_Username_Sum);

    // First Largest Number in arrayOfASCII_Username_Sum
    var FirLarAUS = Math.max(...arrayOfASCII_Username_Sum);
    console.log("Largest Number in arrayOfASCII_Username_Sum:",FirLarAUS);

    // Second Largest Number in arrayOfASCII_Username_Sum
    var SecLarAUS = Math.max(...arrayOfASCII_Username_Sum.filter(x => x !== FirLarAUS));
    console.log("Second Largest Number in arrayOfASCII_Username_Sum:",SecLarAUS);

    // If SecLarAUS is zero or not finite then replace it with FirLarAUS + 1
    if (SecLarAUS == 0 || !isFinite(SecLarAUS) || SecLarAUS == FirLarAUS) {
        SecLarAUS = FirLarAUS + 1;
    }
    console.log("Second Largest Number in arrayOfASCII_Username_Sum:",SecLarAUS);

    // The Password
    console.log("Password:",password);

    var SaltText = "";
    var alphaNumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < password.length*username.length*10; i++) {
        SaltText += alphaNumeric.charAt(Math.floor(Math.random() * alphaNumeric.length));
    }
    console.log("Salt Text Length:",SaltText.length);

    var saltTextSepUL10 = SaltText.match(new RegExp('.{1,' + username.length*10 + '}', 'g'))
    console.log("Salt Text Seperated",saltTextSepUL10);

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
    console.log("Random Number:",random_digit);

    var randomNumberArray = Array.from(String(random_digit), Number);
    console.log("Random Number Array:",randomNumberArray);

    // First Largest Number in randomNumberArray
    var FirLarRNA = Math.max(...randomNumberArray);
    console.log("Largest Number in randomNumberArray:",FirLarRNA);

    let AlteredText = "";
    for (let i = 0; i < password.length; i++) {
        AlteredText += String.fromCharCode(password.charCodeAt(i) + FirLarAUS + FirLarRNA);
    }
    console.log("Altered Password:",AlteredText);

    let AlteredTextHex = convertASCIItoHex(AlteredText);
    console.log("Hex Values",AlteredTextHex);

    // // Replace the two characters in each element of saltTextSepUL10 at the index of randomNumberArray with the two characters in AlteredTextHex
    // for (let i = 0; i < saltTextSepUL10.length; i++) {
    //     saltTextSepUL10[i] = saltTextSepUL10[i].substring(0,randomNumberArray[i]) + AlteredTextHex.substring(0,2) + saltTextSepUL10[i].substring(randomNumberArray[i]+2);
    // }
    // console.log("Salt Text Seperated with Altered Text:",saltTextSepUL10);

    // Replace the two characters in each element of saltTextSepUL10 at the index of randomNumberArray with the two characters in AlteredTextHex
    var saltArrayAT = saltTextSepUL10.map(function(item, index) {
        return item.substring(0, randomNumberArray[index]) + AlteredTextHex.substring(index*2,(index*2)+2) + item.substring(randomNumberArray[index] + 2);
    });
    console.log("After replacing with altered text in Salt Text",saltArrayAT);

    // Replace the characters in each element of saltArrayAT using SecLarAUS value as Index from the end with characters of random_digit
    var FinalArray = saltArrayAT.map(function(item, index) {
        return item.substring(0, item.length - SecLarAUS) + random_digit.charAt(index) + item.substring(item.length - SecLarAUS + 1);
    });
    console.log("After replacing with random digits in Salt Text",FinalArray);

    // Merge all elements of FinalArray into one string
    var mergingFinalArray = FinalArray.join("");
    console.log("After Merging all elements of FinalArray",mergingFinalArray);
    console.log("FinalArray Length",mergingFinalArray.length);

    // display the mergingFinalArray in the id="generatedCipherText"
    document.getElementById("generatedCipherText").innerHTML = mergingFinalArray;
    
    // display password in the id="plain-text"
    document.getElementById("plain-text").value = password;
}

// If user type in the username field then call the function to display the text in id="typedUsername"
document.getElementById("id_username").addEventListener("keyup", function(event) {
    event.preventDefault();
    document.getElementById("typedUsername").value = document.getElementById("id_username").value;
});

document.getElementById("id_password").addEventListener("keyup", function(event) {
    event.preventDefault();
    document.getElementById("typedPassword").value = document.getElementById("id_password").value;
});

// If user clicked on id="generateCipherText" the copy the text in the id="generatedCipherText" to clipboard
document.getElementById("copyText").addEventListener("click", function() {
  /* Get the text field */
  var copyText = document.getElementById("generatedCipherText");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.value);
});

$('.app-login-button').click(function() {
    $(this).attr('disabled', true);
    // $(this).closest('form').submit();
    setTimeout(function() {
        $('.app-login-button').removeAttr('disabled');
    }
    , 1000);
});