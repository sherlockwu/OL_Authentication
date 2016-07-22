# this is for generating lambda application
import traceback
import rethinkdb as r

DB = 'authentication'  # authentication database
TB = 'log_in'          # account table
AC = 'account'         # column
PW = 'password'        # column
ID = 'fbid'            # column

def cal_fbid(usr_object):
    # cal fbid algorithm   ????
    fbid = usr_object[AC] + usr_object[PW]
    return fbid

# first log-in
def login(conn, event):
    # get the account and the input_pw
    usr_accounts = event['account']
    input_pw = event['passwd']
# check the accounts
    # connect to the database? conn: RethinkDB
    # filter out the guest through account (how to realize this)
    cursor = r.table(TB).filter({AC: usr_accounts}).run(conn)
    #account not exist
    if cursor == None:
        return {'error': 'Non-exist Account'}

    for row in cursor:
        if (row[PW] == input_pw ):
            # cal fbid
            fbid = cal_fbid(row)
            return {'result': fbid}
        else:
            return {'error': 'wrong password'}

# check log-in status (using fbid?)
def check(conn, event):
    # get fbid

    # check fbid    database?

    # return status
    return ''

# exit log-in
def exit_login(conn, event):
    # invalidate fbid
    return ''


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

