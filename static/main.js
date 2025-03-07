var config;
var fbid = "0";
var msg_account;

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
    var msg_passwd;
    //try to not store the passwd in script
    // get the data
    msg_account = $("#account").val();
    msg_passwd = $("#passwd").val();
    // post the data
    alert("We are using your account: " + msg_account + " passwd: " + msg_passwd + " to log in.");

    lambda_post(
        {"op" : "login", "account" : msg_account, "passwd" : msg_passwd},
        function(data){
            //alert the log-in status
            status = data['status'];
            alert(status);
            if (status == "login successfully"){
                // reset all info
                    // status
                    $("#login_status").html("");
                    // gender
                    $("#gender").html("");
                    // habit
                    $("#habit").html("");

                // store the fbid
                fbid = data['fbid'];
                alert(fbid);
                // show log-in status
                $("#login_status").html("Logged in as "+msg_account);
                $("#log_out").attr("style", "display: block;");

                // show get_habit button
                $("#get_habit").attr("style", "display: block;");

                // show gender
                gender = data['gender'];
                $("#gender").html(gender);

            }
            $("#account").val("");
            $("#passwd").val("");
            // status changed and present a log-out button
        }
    );

}

function get_habit(){
    // send post
    lambda_post(
        {"op": "get_habit", "account": msg_account, "fbid": fbid},
        function(data){
            // show the habit
            alert(data['habit']);
            $("#habit").html('habit: ' + data['habit']);
        }
    );

}

function logout(){
    //send logout info (just for invalidate the fbid)
    lambda_post(
        {"op": "logout", "account" : msg_account, "fbid" : fbid},
        function(data){

            // log-out successfully
            if (data['status'] == 'logout successfully'){

                // change log-in status
                $("#login_status").html("Log out");
                //reset fbid
                fbid = "";
                //hide things
                $("#log_out").attr("style", "display: none;");
                $("#get_habit").attr("style", "display: none;");
                // reset gender and habit
                $("#habit").html("");
                $("#gender").html("");
            } else{
            // log-out failed
            alert(data['status']);
            }
            /* TODO logic wrong
            //change the log-in status
            $("#login_status").html("logged out");

            //reset the fbid
            fbid = "";

            //hide the log-out and get_habit button
            $("#log_out").attr("style", "display: none;");
            $("#get_habit").attr("style", "display: none;");
            */
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

            // habit "enter"
            /*
            $("#habit").keypress(function(e){
                //  1. check the login status 2. insert habits to the database then
                if (e.keyCode == 13){
                    // check login status
                    if (fbid == "0"){
                        alert("Please Log-in first!");
                    } else{
                        store_habit();
                    }
                }
            });
            */
            // log-out & get habits
            $("#log_out").click(logout)
            $("#get_habit").click(get_habit)
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
