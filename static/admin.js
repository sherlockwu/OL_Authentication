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

function add(){
    // get the data
    var msg_account;
    var msg_passwd;
    var msg_habbit;
    var msg_gender;

    msg_account = $("#account").val();
    msg_passwd = $("#passwd").val();
    msg_gender = $("#gender").val();
    msg_habbit = $("#habbit").val();

    // post the data

    lambda_post(
        {"op" : "add", "account" : msg_account, "passwd" : msg_passwd, "gender": msg_gender, "habbit": msg_habbit},
        function(data){
            alert(JSON.stringify(data));
            // alert("added");
            $("#account").val("");
            $("#passwd").val("");
            $("#gender").val("");
            $("#habbit").val("");
        }
    );

}


function main(){
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
            $("#submit").click(add)
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
