from flask import Flask, render_template, url_for, request
import sqlite3
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS admin(email TEXT, password TEXT)"""
cursor.execute(command)

cursor.execute("INSERT INTO admin VALUES ('admin@gmail.com', 'admin123')")
connection.commit()