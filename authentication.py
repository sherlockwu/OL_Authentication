# this is for generating lambda application
import traceback
import rethinkdb as r

DB = 'authentication'  # authentication database
TB = 'user'            # account table
AC = 'account'         # column
PW = 'password'        # column
ID = 'fbid'            # column

def cal_fbid(usr_object):
    # cal fbid algorithm   TODO
    fbid = usr_object[AC] + usr_object[PW]
    return fbid

# first log-in


def login(conn, event):
    # get the account and the input_pw
    usr_accounts = event['account']
    input_pw = event['passwd']
    # check the accounts
    # filter out the guest through account (how to realize this)
    cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)
    #account not exist
    #if cursor == None:
    #    return 'Non-exist Account'

    for row in cursor:
        if (row[PW] == input_pw ):
            # cal fbid
            fbid = cal_fbid(row)
            return fbid
        else:
            return 'wrong password'
    return 'Non-exist Account'
def add(conn, event):
    # get the account
    usr_accounts = event['account']
    usr_pw = event['passwd']
    # store into the rethinkdb
    r.db(DB).table(TB).insert({AC: usr_accounts, PW: usr_pw}).run(conn)
    return 'sucessfully added!!!'
# check log-in status (using fbid?) TODO
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
          'add'  :  add,
          'check':  check,
          'exit' :  exit_login}.get(event['op'], None)

    print (fn)
    if fn!=None:
        try:
            result = fn(conn, event)
            return {'result': result}
        except Exception:
            return {'error': traceback.format_exc()}
    else:
        # bad option
        return {'error': 'bad opt'}

