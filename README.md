# README 
This is an open-lambda based application for web application's integrated log-in with "social" accounts.

## File Organization
* authentication.py         main file in Open Lambda
* setup.py                  application start file for OL
* common.py                 common functions for application setup 
* ./static
    * admin.html            admin page for adding accounts into application database
    * admin.js
    * index.html            main page for users to log-in and get user features stored in application database
    * main.js
    * sdk.js                future sdk file for authentication service 


## Demo
* Please place this application dir under `OpenLambda/application/`, then enter this application directory
* Start local cluster: `sudo ../../util/start-local-cluster.py`
* Start and setup the authentication service
    * `sudo ./setup.py`
    * open `./static/admin.html` with your browser, for instance `firefox ./static/admin.html`
    * in the admin page, add new accounts with their gender, habit and set a password
* Use our service: 
    * open `./static/index.html` wih your browser
    * log-in
        * log in your added account with corresponding password 
        * you will see alerted status and access token received 
        * you will see log-in status change in log-in status field
        * you will see the correspongind gender of this account at bottom of the page
    * get-habit
        * push the `get habit` button
        * you will see received habit of the account in both alert and bottom of the page 
    * log-out 
        * push the `log out` button 
        * you will see the change of the log-in status


## INFO
Author: Kan Wu
Contact: wukanustc@gmail.com




