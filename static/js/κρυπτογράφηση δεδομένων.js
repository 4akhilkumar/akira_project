document.getElementById("id_submit").addEventListener("click", myFunction);

function myFunction() {
    let username = document.getElementById("id_username").value;
    let password = document.getElementById("id_password").value;

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
    console.log(arrayOfASCII_Username_Sum);

    // First Largest Number in arrayOfASCII_Username_Sum
    var FirLarAUS = Math.max(...arrayOfASCII_Username_Sum);
    console.log("Largest Number in arrayOfASCII_Username_Sum:",FirLarAUS);

    // Second Largest Number in arrayOfASCII_Username_Sum
    var SecLarAUS = Math.max(...arrayOfASCII_Username_Sum.filter(x => x !== FirLarAUS));
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

    // Replace the characters in each element of saltTextSepUL10 at the index of randomNumberArray with the characters in AlteredText
    var saltArrayAT = saltTextSepUL10.map(function(item, index) {
        return item.substring(0, randomNumberArray[index]) + AlteredText.charAt(index) + item.substring(randomNumberArray[index] + 1);
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

    document.getElementById("id_password").value = mergingFinalArray;
}