import streamlit as st
import sqlite3
import pandas as pd

def fetch_data(query):
    conn = sqlite3.connect('../BDD/model_logs.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.title('Dashboard de suivi des modèles')

    st.header('Logs d\'entraînement')
    train_data = fetch_data("SELECT * FROM training_logs")
    st.write(train_data)

    st.header('Logs de prédiction')
    prediction_data = fetch_data("SELECT * FROM prediction_logs")
    st.write(prediction_data)

if __name__ == '__main__':
    main()
