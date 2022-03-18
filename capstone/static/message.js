$(document).ready(function($) {
    $(".tableRow").click(function() {
        window.document.location = $(this).data("href");
    });
});