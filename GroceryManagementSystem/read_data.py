# Read the database and get the data
import pyodbc

 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-DCCTUJ08;'
                      'Database=shopDB;'
                      'Trusted_Connection=yes;'
                      'MARS_Connection=Yes')

 
def get_orders_list():
    orders = []
    final_orders = []
    sql = 'SELECT * FROM orders'
    cursor = conn.cursor()
    cursor.execute(sql)
    orders = list(cursor.fetchall())

    for order in orders:
        order = list(order)

        sql = 'SELECT cus_name FROM customer WHERE cus_id = (?)'
        cursor.execute(sql, (order[4],))
        cus_name = cursor.fetchone()
        order.append(cus_name[0])

        sql = 'SELECT unit_price FROM product WHERE p_id = (?)'
        cursor.execute(sql, (order[3],))
        p_id = cursor.fetchone()
        order.append(p_id[0])

        final_orders.append(order)

    return final_orders


def get_order_number():
    cursor = conn.cursor()
    sql = 'SELECT MAX(o_id) FROM orders'
    cursor = conn.cursor()
    cursor.execute(sql)
    order_number = cursor.fetchone()
    return order_number


def get_customer_list():
    customers = []
    cursor = conn.cursor()
    sql = 'SELECT cus_name FROM customer'
    cursor = conn.cursor()
    cursor.execute(sql)
    customers_list = list(cursor.fetchall())
    for row in customers_list:
        customers.append(row[0])
    return customers


def get_product_list():
    cursor = conn.cursor()
    sql = 'SELECT * FROM product'
    cursor = conn.cursor()
    cursor.execute(sql)
    products = list(cursor.fetchall())

    return products


def add_record(date, empId, name, pName, quantity):
    cursor = conn.cursor()
    sql = 'SELECT cus_id From customer WHERE cus_name = (?)'
    cursor.execute(sql, (name,))
    cus_id = cursor.fetchone()

    sql = 'INSERT INTO orders VALUES (?,?, ?,?,?)'
    cursor.execute(sql, (date, quantity, pName, cus_id[0], empId))
    conn.commit()
    print(date, quantity, pName, cus_id[0], empId)
    print(cursor.rowcount, "was inserted.")


def get_unit_price(p_id):
    cursor = conn.cursor()
    sql = 'SELECT unit_price From product WHERE p_id = (?)'
    cursor.execute(sql, (p_id,))
    unit_price = cursor.fetchone()
    unit_price = unit_price[0]
    return unit_price


def search_customer(name):
    cursor = conn.cursor()
    name = "%" + name + "%"
    sql = "SELECT cus_name From customer WHERE cus_name LIKE ?"
    cursor.execute(sql, (name,))
    cus_names = list(cursor.fetchall())
    return cus_names

def delete_order(id):
    cursor = conn.cursor()
    sql = 'DELETE orders WHERE o_id = (?)'
    cursor.execute(sql, (id,))
    conn.commit()
    

def graph1():
    cursor = conn.cursor()
    sql = 'select e.emp_id, count(o_id) from orders o join employee e on e.emp_id = o.emp_id group by e.emp_id;'
    cursor.execute(sql)

    data = cursor.fetchall()
    orders = []
    emp = []
    for row in data:
        orders.append(row[1])
        emp.append(row[0])

    return orders, emp
