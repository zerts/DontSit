/**
 * Created by zerts on 28.11.16.
 */

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {

    function updateLikes() {
        var ids = [];

        $('.post-likes').each(function () {
            ids.push($(this).data('post-id'));
        });

        $.getJSON('/post/likes/', {ids: ids.join(',')}, function (data) {
            console.log(data);
            for (var i in data) {
                $('.post-likes[data-post-id='+i+']').html(data[i]);
            }
        });
    }
    updateLikes();

    window.setInterval(updateLikes, 5000);

    $('.post-likes-form').click(function() {
        var url = $(this).data('likes-url');
        var element = $(this);
        $.post(url, function(data) {
            updateLikes();
        });
    });

    $('.b-post-edit-button').click(function () {
        var curr_id = ($(this).data('post-id'));
        console.log(curr_id);
        $('#b-post-edit-back'+curr_id).show();
        return false;
    });

    //window.setInterval(updateLikes, 5000);

});