#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Controller for Website Todo List with Form"""

import re
import sqlite3 as lite
from flask import Flask, render_template, request, redirect
from datetime import datetime

con = None
app = Flask(__name__)
todolist = {}

def lsload():
    with lite.connect('todo.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM TASKS2")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                todolist[row[0]] = [row[1], row[2], row[3]]
    return

@app.route('/')
def todoshow():
    return render_template('index.html', todolist = todolist)
                           
@app.route('/anotherdo', methods = ['POST'])
def signup():
    taskName = request.form['NewTaskName']
    taskEmail = request.form['Email']
    if not re.search('[^@]+@[^@]+\.[^@]+', taskEmail):
        return redirect('/')
    taskPrio = request.form['Priority']
    if not (taskPrio == 'Low' or taskPrio == 'Medium' or taskPrio == 'High'):
        return redirect('/')
    taskTime = datetime.now()
    todolist[taskName] = [taskEmail, taskPrio, taskTime]
    return redirect('/')

@app.route('/cleardo', methods = ['Post'])
def clearform():
    return redirect('/')

@app.route('/clearALLdo', methods = ['Post'])
def clearALLform():
    todolist.clear()
    return redirect('/')

@app.route('/SaveAll', methods = ['Post'])
def SaveAll():
    with lite.connect('todo.db') as con1:
        cur = con1.cursor()
        for key, value in todolist.items():
            temp = value
            temp.insert(0, key)
            print temp
            #cur.executemany("INSERT INTO TASKS2 VALUES(?, ?, ?, ?);", key, value)
    return redirect('/')

if __name__ == '__main__':
    lsload()
    app.run()
