# this is for generating lambda application
import traceback
import rethinkdb as r



# first log-in
def login(conn, event):
    # get the account and the input_pw
    usr_accounts = ???
    input_pw = ???
    # check the accounts
        # connect to the database?   RethinkDB

        # Select
        true_pw = select ... usr_accounts  # ???
            #account not exist
            if true_pw == None:
                return "Non-exist Account"
        if (true_pw == input_pw ):
            # cal fbid
            fbid = cal_fbid()
            return ["Successfully log-in", fbid]
        else:
            return "false password"

# check log-in status (using fbid?)
def check(conn, event):
    # get fbid

    # check fbid    database?

    # return status


# exit log-in
def exit_login(conn, event):
    # invalidate fbid



# handler
def handler(conn,event):
    fn = {'login':  login,
          'check':  check,
          'exit' :  exit_login}.get(event['op'], None)

    if fn!=None:
        try:
            result = fn(conn, event)
            return {'result': result}
        except Exception:
            return {'error': traceback.format_exc()}
    else:
        # bad option
        return {'error': 'bad opt'}

