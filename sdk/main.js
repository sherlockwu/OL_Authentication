var account;
var passwd;

function login(){
    <!--create the data-->

    JSON_Account = "{";

    account = $("#account")[0];
    passwd = $("#passwd")[0];

    JSON_Account += " \"account :\" " + account + "\"passwd : \"" + passwd + "}";
    <!--JSON Style-->


    <!--send out the data-->

}
