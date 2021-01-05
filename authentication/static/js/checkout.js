
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});

function create_post() {
    console.log("create post is working!") // sanity check
    let username = $("#id_username");
    let email = $("#id_email");
    let password = $("#id_password");
    console.log(username.val())
    //process cookie
    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
    console.log(csrftoken)
    console.log(username.val())
    console.log(email.val())
    console.log(password.val())
    $.ajax({
        url : ".", // the endpoint
        type : "POST", // http method
        data :  {username: username.val(),
                email: email.val(),
                password: password.val(),
            },
        dataType: "json",
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },// data sent with the post request

        // handle a successful response
        success : function(json) {
            // console.log(response.json);
            $('#username').val(''); // remove the value from the input
            $('#email').val(''); // remove the value from the input
            $('#password').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

}