from flask import Flask, request, render_template, redirect, send_file, jsonify
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_agg import FigureCanvasAgg as figurecanva
from io import BytesIO

import read_data

app = Flask(__name__)


@app.route('/')
def index():
    order_number = read_data.get_order_number()
    customers = read_data.get_customer_list()
    products = read_data.get_product_list()
    return render_template('neworder.html', order_number=order_number[0] + 1, customers=customers, products=products)


@app.route('/list')
def list():
    orders = read_data.get_orders_list()
    return render_template('orderlist.html', orders=orders)


@app.route('/add_record', methods=['POST'])
def add_record():
    date = request.form['date']
    empId = request.form['empId']
    name = request.form['name']
    pName = request.form['pName']
    quantity = request.form['quantity']
    total = request.form['total']
    read_data.add_record(date, empId, name, pName, quantity)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_orders():
    id=request.form['id']
    read_data.delete_order(id)
    return redirect('/list')

@app.route('/total_cal/<p_id>')
def total_cal(p_id):
    unit_price = read_data.get_unit_price(p_id)
    return str(unit_price)


@app.route('/customers/<name>')
def cus_names(name):

    cus_names = read_data.search_customer(name)
    cus_names_list = []
    for row in cus_names:
        cus_names_list.append(row[0])
    print(cus_names_list)

    return jsonify({"customers": cus_names_list})


@app.route('/analytics')
def analytics():
    orders, emp = read_data.graph1()

    return render_template('analytics.html', orders=orders, emp=emp)


if __name__ == '__main__':
    app.run(debug=True)
