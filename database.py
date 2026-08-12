import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('diet_data.db')
    c = conn.cursor()
    # Table pour les repas
    c.execute('''CREATE TABLE IF NOT EXISTS meals 
                 (date TEXT, food TEXT, kcal REAL, protein REAL, carbs REAL, fat REAL)''')
    # Table pour les dépenses (exercice)
    c.execute('''CREATE TABLE IF NOT EXISTS exercise 
                 (date TEXT, activity TEXT, kcal_burned REAL)''')
    conn.commit()
    conn.close()

def log_meal(food, nutrition):
    conn = sqlite3.connect('diet_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO meals VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d"), food, nutrition['calories'], 
               nutrition['protein_g'], nutrition['carbohydrates_total_g'], nutrition['fat_total_g']))
    conn.commit()
    conn.close()

def log_exercise(activity, kcal):
    conn = sqlite3.connect('diet_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO exercise VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d"), activity, kcal))
    conn.commit()
    conn.close()

def get_weekly_data():
    conn = sqlite3.connect('diet_data.db')
    df_meals = pd.read_sql_query("SELECT * FROM meals", conn)
    df_exercise = pd.read_sql_query("SELECT * FROM exercise", conn)
    conn.close()
    return df_meals, df_exercise
