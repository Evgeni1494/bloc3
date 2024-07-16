from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite3
import pandas as pd
from typing import Optional

app = FastAPI()

DATABASE_PATH = 'data_expo_bdd/exposition_database.db'

class QueryParams(BaseModel):
    year: Optional[int] = Query(None, description="Year of the data")
    state_name: Optional[str] = Query(None, description="Name of the state")
    sector_name: Optional[str] = Query(None, description="Sector name")
    fuel_name: Optional[str] = Query(None, description="Fuel name")

def query_database(query_params: QueryParams):
    query = "SELECT * FROM emissions WHERE 1=1"
    params = []

    if query_params.year and query_params.year != 'any':
        query += " AND year = ?"
        params.append(query_params.year)
    if query_params.state_name and query_params.state_name.lower() != 'any':
        query += " AND state_name = ?"
        params.append(query_params.state_name)
    if query_params.sector_name and query_params.sector_name.lower() != 'any':
        query += " AND sector_name = ?"
        params.append(query_params.sector_name)
    if query_params.fuel_name and query_params.fuel_name.lower() != 'any':
        query += " AND fuel_name = ?"
        params.append(query_params.fuel_name)

    query += " LIMIT 100"

    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    return df.to_dict(orient='records')

@app.get("/emissions")
def get_emissions(
    year: Optional[str] = Query('any', description="Year of the data"),
    state_name: Optional[str] = Query('any', description="Name of the state"),
    sector_name: Optional[str] = Query('any', description="Sector name"),
    fuel_name: Optional[str] = Query('any', description="Fuel name")
):
    query_params = QueryParams(
        year=year,
        state_name=state_name,
        sector_name=sector_name,
        fuel_name=fuel_name
    )
    results = query_database(query_params)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Run uvicorn Api_data:app --reload

