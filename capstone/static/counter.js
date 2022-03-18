document.addEventListener("DOMContentLoaded", function(){
    var element = document.getElementById("messageToast");
    var myToast = new bootstrap.Toast(element, {
        autohide: false
    });

    const counter = JSON.parse(document.getElementById('messageCounter').textContent);
    if (counter > 0){
        myToast.show();
    }
});
