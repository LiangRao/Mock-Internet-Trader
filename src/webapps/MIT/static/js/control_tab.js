function getJoinInfo() {
    var gameid = $("#gameID").val()
    // validation check
    if ($.isNumeric(gameid) == false) {
        return
    }

    $.get("/get-join-info/" + gameid)
        .done(function(data) {
            var join = data.join
            console.log(join)
            if (join) {
                $("#portfolio-tab").attr("style","color: #373739")
                console.log("unjoin")
                $("#portfolio-tab").attr("href", "javascript:void(0);")

            } else {
                $("#portfolio-tab").attr("style","")
                var gameid = $("#gameID").val()
                var playerid = $("#playerID").val()
                $("#portfolio-tab").attr("href", "/portfolio/" + gameid + "/" + playerid)

            }
        });
}
$(document).ready(function() {
    // Initialize the plugin
    getJoinInfo()

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

});
