
from flask import *  
import os 
import qrcode
import uuid
from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
import pandas as pd

con=sqlite3.connect("database.db")
cur=con.cursor()
#con.execute("create table if not exists shopdetails(name text primary key,colordouble integer,colorsingle integer,blacksingle integer,blackdouvble integer)")
cur.execute("select * from shopdetails")
data=cur.fetchall()
print(data)



