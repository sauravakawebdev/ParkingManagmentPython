from winsound import SND_ASYNC
import mysql.connector
import time
import datetime


global conn,cursor
conn = mysql.connector.connect(
    host='localhost', database='parking_system', user='root', password='root',port='3308')
cursor = conn.cursor()


def clear():
  for _ in range(65):
     print()


def display_parking_type_records():
    cursor.execute('select * from parking_type;')
    records = cursor.fetchall()
    for row in records:
        print(row)

def login():
    while True:
        clear()
        uname = input('Enter your id :')
        upass = input('Enter your Password :')
        cursor.execute('select * from login where name="{}" and pwd ="{}"'.format(uname,upass))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows!=1:
            print('Invalid Login details..... Try again')
        else:
            print('You are eligible for operating this system............')
            print('\n\n\n')
            print('Press any key to continue...............')
            break

def add_new_vehicle():
    clear()
    print('Vehicle Login Screen ')
    print('-'*100)
    vehicle_type = input('Enter Vehicle Type :' ) 
    model_name=input('Enter Vehical Model : ')
    parking_id = input('Enter Parking Id 1. Car - 2 Bike: ')
    manufature_name=input('Enter Maufacture Name :')
    vehicle_number=input('Enter Vehical Number :')
    customer_name=input('Enter Customer Name: ')
    customer_mobile_number=input('Enter Customer Number: ')
    cutomer_balance=input('Enter Customer Balance ')
    entry_time = datetime.datetime.now().replace(microsecond=0)
    
    print(entry_time)
    sql = 'insert into transaction_table(type_vehical,model_name,manufacture_name,vehical_number,customer_name,mobile_number,balance,entry_time) values \
            ("{}","{}","{}","{}","{}","{}","{}","{}");'.format(vehicle_type,model_name,manufature_name,vehicle_number,customer_name,customer_mobile_number,cutomer_balance,entry_time)
    cursor.execute(sql)
    if parking_id == "1":
        cursor.execute('update parking_space set status ="full",type_id = "car" where id ={}'.format(parking_id))
        print('\n\n\n Record added successfully.................')
        conn.commit()
        wait= input('\n\n\nPress any key to continue.....')

    if parking_id == "2":
        cursor.execute('update parking_space set status ="full",type_id = "bike" where id ={}'.format(parking_id))
        print('\n\n\n Record added successfully.................')
        conn.commit()
        wait= input('\n\n\nPress any key to continue.....')


def remove_vehicle():
    clear()
    print('Vehicle Logout Screen')
    print('-'*100)
    vehicle_id = input('Enter vehicle No :')
    '''exit_time = datetime.datetime.now().replace(microsecond=0)'''
    sql = 'select type_vehical tv,model_name mn,manufacture_name mn,vehical_number vn,customer_name cn,mobile_number mob,balance bal,entry_time et from transaction_table  \
           where vehical_number ="'+vehicle_id+'"\
           and exit_time is NULL;'
    cursor.execute(sql)
    record = cursor.fetchone()
    
    clear()
    print('Logout Details ')
    print('-'*100)
    print('Vehical Type : {}'.format(record[0]))
    print('Model Name : {}'.format(record[1]))
    print('Manufacture Name : {}'.format(record[2]))
    print('Vehical Number : {}'.format(record[3]))
    print('Customer Name : {}'.format(record[4]))
    print('Customer Mobile Number : {}'.format(record[5]))
    print('Customer Balance : {}'.format(record[6]))

    '''print(record)'''


    entry_time  = datetime.datetime.fromisoformat(record[7])
    exit_time =  datetime.datetime.now().replace(microsecond=0)
    diffhours = exit_time - entry_time
    hours = int(str(diffhours)[0])
    type_vehical = format(record[0])
    if type_vehical.upper() == "BIKE":
        print("Amount to be Collected ",get_bike_trasaction(hours))
    else:
        get_car_trasaction(hours)
        print("Amount to be Collected ",get_car_trasaction(hours))
    wait = input('press any key to continue......')
    # update transaction and parking space tables
    

def parking_status(status):
    clear()
    print('Parking Status :',status)
    print('-'*100)
    sql ="select * from parking_space where status ='{}'".format(status)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait =input('\n\n\nPress any key to continue.....')

def vehicle_status_report():
    clear()
    print('Vehicle Status - Currently Parked')
    print('-'*100)
    sql='select * from transaction where exit_date is NULL;'
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    wait =input('\n\n\nPress any key to continue.....')

'''def money_collected():
    clear()
    start_date = input('Enter start Date(yyyy-mm-dd): ')
    end_date = input('Enter End Date(yyyy-mm-dd): ')
    sql = "select sum(amount) from transaction where \
          entry_date ='{}' and exit_date ='{}'".format(start_date,end_date)
    cursor.execute(sql)
    result = cursor.fetchone()
    clear()
    print('Total money Collected from {} to {}'.format(start_date,end_date))
    print('-'*100)
    print(result[0])
    wait =input('\n\n\nPress any key to continue.....')
'''

def get_bike_trasaction(a):
    a = int(a)
    sum = 0
    if a > 1:
        if a>1 and a<12:
            if a>1 and a<=3:
                sum=sum+a*20
            if a>3 and a<=8:
                j = a-3
                sum = sum + 3*20+j*35
            if a>9 and a<=12:
                k= a-8
                sum = sum + 3*20+5*35+k*50
            if a>12 :
                t= a-12
                sum = (sum + 3*20+5*35+12*50+t*70)*1.15
                print("Surcharge of Addition 15% ",sum)
    return sum            
            

def get_car_trasaction(a):
    a = int(a)
    sum = 0
    if a > 1:
        if a>1 and a<12:
            if a>1 and a<=3:
                sum=sum+a*50
            if a>3 and a<=8:
                j = a-3
                sum = sum + 3*50+j*75
            if a>9 and a<=12:
                k= a-8
                sum = sum + 3*50+5*75+k*100
            if a>12 :
                t= a-12
                sum = sum + 3*50+5*75+12*100+t*120
                print("Surcharge of Addition 30% ",sum*1.30)
    return sum 
     

        

def report_menu():
    while True:
        clear()
        print(' P A R K I N G    R E P O R T S  ')
        print('-'*100)
        print('1.  Parking Types \n')
        print('2.  Free Space  \n')
        print('3.  Ocupied Space  \n')
        print('4.  Vehicle Status  \n')
        print('5.  Money Collected  \n')
        print('6.  Exit  \n')
        choice = int(input('Enter your choice :'))
        field = ''
        if choice == 1:
            display_parking_type_records()
        if choice == 2:
            parking_status("open")
        if choice == 3:
            parking_status("full")
        if choice == 4:
            vehicle_status_report()
        if choice == 5:
            '''money_collected()'''
        if choice ==6: 
            break
        



def main_menu():
    clear()
    login()
    clear()
    
    
    while True:
      clear()
      print(' P A R K I N G   M A N A G E M E N T    S Y S T E M')
      print('*'*100)
      print('\n1.  Vehicle Login ')
      print('\n2.  Vehicle Logout')
      print('\n3.  Close application')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))

      if choice == 1:
        add_new_vehicle()
      
      if choice == 2:
        remove_vehicle()
            
      if choice == 3:
        break
    

if __name__ == "__main__":
    main_menu()