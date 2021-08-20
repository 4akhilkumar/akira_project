$.getJSON("https://api.ipify.org?format=json",
function(data) {
    document.getElementById("id_user_ip_address").value = data.ip;
})