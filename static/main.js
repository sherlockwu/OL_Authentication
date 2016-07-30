var config;

function lambda_post(data, callback){
    // url
    var url = config['url'];

    // post

    $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        dataType: "json",
        success: callback,
        failure: function(error){
            $("#submit").html("Error: " + error);
        }
    });



}

function login(){
    // get the data
    var msg_account;
    var msg_passwd;
    msg_account = $("#account").val();
    msg_passwd = $("#passwd").val();
    // post the data
    alert("We are using your account: " + msg_account + " passwd: " + msg_passwd + " to log in.");

    lambda_post(
        {"op" : "login", "account" : msg_account, "passwd" : msg_passwd},
        function(data){
            alert("Successfully Log-in");
            $("#account").val("");
            $("#passwd").val("");
        }
    );

}


function main(){
    // log-in
    //alert("Please Log-in first")
    $("#passwd").val("");
    $.getJSON('config.json')
        .done(function(data){
            // get config
            alert("config loaded");
            config = data;
            // normal running
            $("#passwd").keypress(function(e){
                if (e.keyCode == 13){
                    $("#submit").click();
                }
            });
            $("#submit").click(login)
        }
        ).fail(function(jqxhr, textStatus, error){
            // direct refreshing
            $("login_status").html("Error: " + error + ". Consider Refreshing.")

        }
        );

}


$(document).ready(function(){
    main();
});
