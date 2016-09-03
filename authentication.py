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
    # get the account and the input_pw and the habits

    usr_accounts = event['account']
    input_pw = event['passwd']
    # check the accounts
    # filter out the guest through account (how to realize this)
    # cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)

    #account not exist
    row = r.db(DB).table(TB).get(usr_accounts).run(conn)
    if (row[PW] == input_pw):
        # cal fbid
        fbid = cal_fbid(row)
        # insert the fbid into database
        r.db(DB).table(TB).get(usr_accounts).update({ID: fbid}).run(conn)

        # return gender
        gender = row['gender']
        return {'status': 'login successfully', 'fbid': fbid, 'gender': gender}
    else:
        return {'status': 'wrong password'}

    return {'status': 'Non-exist Account'}



    #for row in cursor:
    #    if (row[PW] == input_pw):
    #        # cal fbid
    #        fbid = cal_fbid(row)

    #        # TODO insert the fbid into database
    #        # r.db(DB).table(TB).update({ID: fbid}).run(conn)
    #        # fetch the gender
    #        gender = row['gender']
    #        return {'status': 'login successfully', 'fbid': fbid, 'gender': gender}
    #    else:
    #        return {'status': 'wrong password'}
    #return {'status': 'Non-exist Account'}

# add an account from admin.html
def add(conn, event):
    # get the account
    usr_accounts = event['account']
    usr_pw = event['passwd']
    usr_gender = event['gender']
    usr_habit = event['habit']

    # store into the rethinkdb
    r.db(DB).table(TB).insert({AC: usr_accounts, PW: usr_pw, 'gender': usr_gender, 'habit': usr_habit, ID: 'EE'}).run(conn)
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
    # cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)
    # check the fbid
    # for row in cursor:
    #    if (row[ID] == input_fbid):
    #        fbid = cal_fbid(row)
    #        # renew the fbid of this row
    #        r.db(DB).table(TB).filter({AC: usr_accounts}).update({ID: fbid}, non_atomic = True).run(conn)
    #        # r.db(DB).table(TB).filter({AC: usr_accounts}).update({ID: fbid}).run(conn)

    #        return {'status': 'logout successfully', 'fbid': row[ID]}
    # renew the fbid


    row = r.db(DB).table(TB).get(usr_accounts).run(conn)
    if (row[ID] == input_fbid):
        # recal fbid
        fbid = cal_fbid(row)
        # renew the fbid in database
        r.db(DB).table(TB).get(usr_accounts).update({ID: fbid}).run(conn)

        return {'status': 'logout successfully', 'fbid': fbid}
    else:
        return {'status': 'not matched fbid', 'fbid': row[ID]}


def get_habit(conn, event):
    # get account
    usr_accounts = event['account']
    input_fbid = event['fbid']

    # search account
    # cursor = r.db(DB).table(TB).filter({AC: usr_accounts}).run(conn)

    # for row in cursor:
    #    # check fbid
    #    if (row[ID] == input_fbid):
    #        # habit_return = row['habit']
    #        return {'habit': 'try!'}
    #        # return habit
    #    else:
    #        return {'not match': row[ID]}

    # return {'Status': 'Not Found!'}

    row = r.db(DB).table(TB).get(usr_accounts).run(conn)
    if (row[ID] == input_fbid):
        habit_return = row['habit']
        return {'habit': habit_return}
    else:
        return {'not match': row[ID]}

# handler
def handler(conn,event):
    fn = {'login':  login,
          'add'  :  add,
          'check':  check,
          'logout' : logout,
          'get_habit': get_habit}.get(event['op'], None)

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

