from flask import *  
import os 
import qrcode
import uuid
from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

con=sqlite3.connect("database.db")
cur=con.cursor()
cur.execute("select * from shop")
data=cur.fetchall()
print(data)
con.close()
