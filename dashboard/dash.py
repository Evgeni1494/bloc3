import streamlit as st
import sqlite3
import pandas as pd

def fetch_data(query):
    """
    Fetch data from the SQLite database based on the provided SQL query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        DataFrame: The result of the SQL query as a pandas DataFrame.
    """
    conn = sqlite3.connect('../BDD/model_logs.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    """
    Main function to run the Streamlit app.
    
    Displays training and prediction logs from the SQLite database.
    """
    st.title('Model Monitoring Dashboard')

    st.header('Training Logs')
    train_data = fetch_data("SELECT * FROM training_logs")
    st.write(train_data)

    st.header('Prediction Logs')
    prediction_data = fetch_data("SELECT * FROM prediction_logs")
    st.write(prediction_data)

if __name__ == '__main__':
    main()
