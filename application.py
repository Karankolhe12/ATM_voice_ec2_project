from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import time
import os
from pygame import mixer

application = Flask(__name__)
application.secret_key = 'your_secret_key'

balance = 2000

def play_sound(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    time.sleep(3)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pin = request.form['pin']
        if pin == '1234':
            flash("Pin accepted")
            return redirect(url_for('menu'))
        else:
            flash("Incorrect pin")
    return render_template('index.html')

@application.route('/menu')
def menu():
    return render_template('menu.html')

@application.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    global balance
    if request.method == 'POST':
        amount = int(request.form['amount'])
        if amount <= balance:
            balance -= amount
            
            with open("history.txt", "a") as ko:
                ko.write(f"debit {amount} and current balance is {balance}  {datetime.datetime.now()}\n")
            flash(f"{amount} withdrawn. Current balance: {balance}")
        else:
            flash("Insufficient balance")
    return render_template('withdraw.html')

@application.route('/add', methods=['GET', 'POST'])
def add():
    global balance
    if request.method == 'POST':
        amount = int(request.form['amount'])
        balance += amount
        
        with open("history.txt", "a") as ko:
            ko.write(f"deposit {amount} and current balance is {balance}  {datetime.datetime.now()}\n")
        flash(f"{amount} added. Current balance: {balance}")
    return render_template('add.html')

@application.route('/balance')
def check_balance():
    return render_template('balance.html', balance=balance)

@application.route('/history')
def history():
    with open("history.txt") as kp:
        history = kp.read()
    return render_template('history.html', history=history)

@application.route('/send', methods=['GET', 'POST'])
def send():
    global balance
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        amount = int(request.form['amount'])
        if amount <= balance:
            balance -= amount
            
            with open("history.txt", "a") as ko:
                ko.write(f"money sent to {name} ({mobile}) debit {amount} and current balance is {balance}  {datetime.datetime.now()}\n")
            flash(f"Money sent to {name}. Current balance: {balance}")
        else:
            flash("Insufficient balance")
    return render_template('send.html')

if __name__ == '__main__':
    application.run(debug=True)
