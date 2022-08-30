$('#search').keypress(function (e) {
    if (e.which == 13) {
        $('#search').submit();
        return false;    //<---- Add this line
    }
});
