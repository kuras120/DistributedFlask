
$(document).ready( function() {
    $('#like-button').click(function () {
        $.ajax({
            type: 'POST',
            url: '/add_like'
        })
        .done(function (data) {
            $('#like-button').html(" " + data);
        });
    })
});
