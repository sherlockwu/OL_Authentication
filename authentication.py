# this is for generating lambda application
import traceback
import datetime
import rethinkdb as r

DB = 'authentication'  # authentication database
TB = 'user'            # account table
AC = 'account'         # column
PW = 'password'        # column
ID = 'fbid'            # column

def cal_fbid(usr_object):
    # cal fbid algorithm   TODO
    fbid = usr_object[AC] + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    return fbid

# first log-in


def login(conn, event):
    # get the account and the input_pw and the habbits

    usr_accounts = event['account']
    input_pw = event['passwd']
    # check the accounts
    # filter out the guest through account (how to realize this)
    cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)
    #account not exist

    for row in cursor:
        if (row[PW] == input_pw):
            # cal fbid
            fbid = cal_fbid(row)

            # insert the fbid into database
            r.db(DB).table(TB).filter({AC: usr_accounts}).update({ID: fbid}).run(conn)

            # fetch the gender
            gender = row['gender']
            return {'status': 'login successfully', 'fbid': fbid, 'gender': gender}
        else:
            return {'status': 'wrong password'}
    return {'status': 'Non-exist Account'}

# add an account from admin.html
def add(conn, event):
    # get the account
    usr_accounts = event['account']
    usr_pw = event['passwd']
    usr_gender = event['gender']
    usr_habbit = event['habbit']

    # store into the rethinkdb
    r.db(DB).table(TB).insert({AC: usr_accounts, PW: usr_pw, 'gender': usr_gender, 'habbit': usr_habbit}).run(conn)
    return {'status': 'sucessfully added!'}

# check log-in status (using fbid?) TODO
def check(conn, event):
    # get fbid

    # check fbid    database?

    # return status
    return {'status': 'cannot check right now'}

# exit log-in
def logout(conn, event):
    # invalidate fbid
    usr_accounts = event['account']
    input_fbid = event['fbid']

    # find the account
    cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)
    # check the fbid
    for row in cursor:
        if (row[ID] == input_fbid):
            fbid = cal_fbid(row)
            # TODO renew the fbid of this row
            r.db(DB).table(TB).filter({AC: usr_accounts}).update({ID: fbid}).run(conn)
            return {'status': 'logout successfully'}
    # renew the fbid

    return {'status': 'cannot exit right now'}


# handler
def handler(conn,event):
    fn = {'login':  login,
          'add'  :  add,
          'check':  check,
          'logout' : logout}.get(event['op'], None)

# TODO get habbits


    print (fn)
    if fn!=None:
        try:
            result = fn(conn, event)
            # return {'result': result}
            return result
        except Exception:
            return {'error': traceback.format_exc()}
    else:
        # bad option
        return {'error': 'bad opt'}

