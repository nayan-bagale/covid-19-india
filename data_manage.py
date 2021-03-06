import sqlite3
import logging
from datetime import datetime, timedelta

#previous mouths data storing on database
def previous_data(confirmed,recovered,deaths,bad_date):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    cur = conn.cursor()

    x = bad_date.split()
    if x[1] == 'January':
        date = x[0] + '-' + '01' + '-' + '20'
    elif x[1] == 'February':
        date = x[0] + '-' + '02' + '-' + '20'
    elif x[1] == 'March':
        date = x[0] + '-' + '03' + '-' + '20'
    elif x[1] == 'April':
        date = x[0] + '-' + '04' + '-' + '20'
    else:
        raise Exception('Somting Happen')
    cur.execute('CREATE TABLE IF NOT EXISTS India (Id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Active INTEGER, Confirmed INTEGER, Recovered INTEGER, Deaths INTEGER)')
    cur.execute('SELECT * FROM India WHERE Date = ?', (date,))
    date_check = cur.fetchone()
    if date_check is None:
        cur.execute('INSERT OR IGNORE INTO India (Date, Confirmed, Recovered, Deaths) VALUES( ?, ?, ?, ? )', (str(date), int(confirmed), int(recovered), int(deaths)))
        print('Last Month: ', (str(date), int(confirmed), int(recovered), int(deaths)))
    conn.commit()
    cur.close()

#total world data storing on database
def total_world(t_cases,t_deaths,t_recovered,new_cases,new_deaths):
    conn = sqlite3.connect('database\covid-19-world.sqlite')
    cur = conn.cursor()

    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')

    cur.execute("CREATE TABLE IF NOT EXISTS Global (Id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Confirmed TEXT, Deaths TEXT, Recovered TEXT, New_Cases TEXT, New_Deaths TEXT)")

    #checking the date, if date is exists in database then ignore otherwise add
    cur.execute("SELECT * FROM Global WHERE Date = ?", (date,))
    date_check = cur.fetchone()
    if date_check is None:
        cur.execute('INSERT OR IGNORE INTO Global (Date, Confirmed, Deaths, Recovered, New_Cases, New_Deaths) VALUES( ?, ?, ?, ?, ?, ? )', (str(date), str(t_cases), str(t_deaths), str(t_recovered), str(new_cases), str(new_deaths)))
        print('Global: ', (str(date), str(t_cases), str(t_deaths), str(t_recovered), str(new_cases), str(new_deaths)))
    conn.commit()
    cur.close()

#worlwide data with conutry name storing on database
def worldwide_data(country,active,confirmed,critical,recovered,deaths):
    conn = sqlite3.connect('database\covid-19-world.sqlite')
    cur = conn.cursor()

    d_name = datetime.strftime(datetime.now() - timedelta(1), '%d-%b-%y')
    d_name = '"'+d_name+'"'
    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')

    cur.execute("CREATE TABLE IF NOT EXISTS " +str(d_name)+ " (Id INTEGER PRIMARY KEY AUTOINCREMENT, Country TEXT, Active TEXT, Confirmed TEXT, Critical TEXT, Recovered TEXT, Deaths TEXT, Date TEXT)")

    #checking the date, if date is exists in database then ignore otherwise add
    cur.execute("SELECT * FROM "+str(d_name)+" WHERE Country = ?", (country,))
    date_check = cur.fetchone()
    if date_check is None:
        cur.execute('INSERT OR IGNORE INTO '+str(d_name)+' (Country, Active, Confirmed, Critical, Recovered, Deaths, Date) VALUES( ?, ?, ?, ?, ?, ?, ? )', (str(country), str(active), str(confirmed), str(critical), str(recovered), str(deaths),str(date)))
        print('Worldwide: ', (str(country), str(active), str(confirmed), str(critical), str(recovered), str(deaths)))
    conn.commit()
    cur.close()

#total India data storing on database
def total_values(active,confirmed,recovered,deaths):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    cur = conn.cursor()

    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')

    cur.execute('CREATE TABLE IF NOT EXISTS India (Id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Active INTEGER, Confirmed INTEGER, Recovered INTEGER, Deaths INTEGER)')
    cur.execute('SELECT * FROM India WHERE Date = ?', (date,))
    date_check = cur.fetchone()
    if date_check is None:
        cur.execute('INSERT OR IGNORE INTO India (Date, Active, Confirmed, Recovered, Deaths) VALUES( ?, ?, ?, ?, ? )', (str(date), int(active), int(confirmed), int(recovered), int(deaths)))
        print('Total: ', (str(date), int(active), int(confirmed), int(recovered), int(deaths)))
    conn.commit()
    cur.close()

#state data storing on database
def state_data(state,active,confirmed_cases,recovered,deaths,delta):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    cur = conn.cursor()

    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')

    state = state.replace(' ','_')  #if state have any white space " " the replace with "_"

    #Creating table if not exists
    cur.execute("CREATE TABLE IF NOT EXISTS " + str(state) +" (Id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Active INTEGER, Confirmed INTEGER, Recovered INTEGER, Deaths INTEGER, Delta TEXT)")

    #checking the date, if date is exists in database then ignore otherwise add
    cur.execute("SELECT * FROM "+str(state)+" WHERE Date = ?", (date,))
    date_check = cur.fetchone()
    if date_check is None:
        insert = 'INSERT OR IGNORE INTO ' + str(state) + ' ( Date, Active, Confirmed, Recovered, Deaths, Delta) VALUES ( ?, ?, ?, ?, ?, ? )'
        cur.execute( insert , ( str(date), int(active), int(confirmed_cases), int(recovered), int(deaths), str(delta)))
        print('State: ', str(state), str(confirmed_cases), str(active), str(recovered), str(deaths), str(delta))

    conn.commit()
    cur.close()

#district data storing on database
def district_data(district,confirmed_cases,delta):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    cur = conn.cursor()

    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')

    district = district.replace(' ','_') #if district have any white space " " the replace with "_"
    district = district.replace('.','')
    district = district.replace('*','')

    try:
        #Creating table if not exists
        cur.execute("CREATE TABLE IF NOT EXISTS " + str(district) +" (Id INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, Confirmed INTEGER, Delta TEXT)")
    except:
        logging.critical(district+': '+ str(confirmed_cases) + str(delta))
        print('District: ', str(district), str(confirmed_cases), str(delta))

    #checking the date, if date is exists in database then ignore otherwise add
    cur.execute("SELECT * FROM "+str(district)+" WHERE Date = ?", (date,))
    date_check = cur.fetchone()
    if date_check is None:
        insert = 'INSERT OR IGNORE INTO ' + str(district) + ' ( Date, Confirmed, Delta) VALUES ( ?, ?, ? )'
        cur.execute( insert , ( str(date), int(confirmed_cases), str(delta)))
        print(district+': '+ str(confirmed_cases) + str(delta))
    conn.commit()
    cur.close()

''' Above functions is frontend pupose only '''
def india_data():
    conn = sqlite3.connect('database\covid-19-world.sqlite')
    cur = conn.cursor()
    d_name = datetime.strftime(datetime.now() - timedelta(1), '%d-%b-%y')
    d_name = '"'+d_name+'"'
    cur.execute("SELECT * FROM "+ str(d_name) + "WHERE Country = 'India'")
    recently = cur.fetchone()
    conn.commit()
    cur.close()
    return recently

def search(name):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    conn1 = sqlite3.connect('database\covid-19-world.sqlite')
    cur = conn.cursor()
    cur1 = conn1.cursor()

    name = name.replace(' ','_')
    if name == 'sqlite_sequence' or name == '': name = '  '

    d_name = datetime.strftime(datetime.now() - timedelta(1), '%d-%b-%y')
    d_name = '"'+d_name+'"'
    try:
        if name == 'india': raise NameError('India')
        cur.execute("SELECT * FROM "+ str(name))
        row = cur.fetchall()
    except:
        try:
            name = name.capitalize()
            print(name)
            query = "SELECT * FROM "+ str(d_name)+"WHERE Country = ?"
            cur1.execute(query,(name,))
            row = cur1.fetchall()
            if len(row) is 0:
                name = name.upper()
                query = "SELECT * FROM "+ str(d_name)+"WHERE Country = ?"
                cur1.execute(query,(name,))
                row = cur1.fetchall()
                if name == '  ':
                    cur1.execute("SELECT * FROM "+ str(d_name))
                    row = cur1.fetchall()
                if len(row) is 0: row = '~'
        except Exception as e:
            print(e)
            row = None
    conn.commit()
    cur.close()
    return row

def world_f():
    conn = sqlite3.connect('database\covid-19-world.sqlite')
    cur = conn.cursor()
    date = datetime.strftime(datetime.now() - timedelta(1), '%d-%m-%y')
    cur.execute("SELECT * FROM Global WHERE Date = ?", (date,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    return row

def secretkey(key):
    conn = sqlite3.connect('database\covid-19-India.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Secret ("X-Rapidapi-Key" TEXT)')
    cur.execute('SELECT * FROM Secret')
    check = cur.fetchall()
    if check is None or len(check) >= 0:
        ke = '"' + key + '"'
        cur.execute('INSERT OR IGNORE INTO Secret ("X-Rapidapi-Key") VALUES( ? )',(str(ke)))
    else:
        print(len(check))

    conn.commit()
    cur.close()

if __name__ == "__main__":
    #secretkey()
    print("Run the api.py file")
