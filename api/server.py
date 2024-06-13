import duckdb as db
import polars as pl
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime as dt
#import uvicorn

app = FastAPI(title="Soldier API", default_response_class=Response)
soldiers_df=pl.read_csv("./soldiers.csv")
con = db.connect(database = ":memory:")
con.execute("CREATE TABLE soldier AS SELECT * FROM soldiers_df")
print("ETL completed from CSV!")

## Routes
@app.get("/api/soldier")
async def getDetails():
    print(f">> API call api/solldier @{dt.datetime.now()}")
    query = """
        SELECT rank, sex, race, mpc, dmos,age, yrsOfSvc
        FROM soldier
        ORDER BY race DESC
    """
    data = con.execute(query).df()
    print(f"nRows: {len(data)}")
    return JSONResponse( jsonable_encoder(data.to_dict(orient="records")) )


@app.get("/api/soldier/aggregate")
async def getDetails():
    print(f">> API call api/solldier @{dt.datetime.now()}")
    query = """
        SELECT rank, sex, race, count(*) population, mean(age) avgAge, mean(yrsOfSvc) avgYrsOfSvc
        FROM soldier
        GROUP BY rank, sex, race
        ORDER BY population DESC
    """
    data = con.execute(query).df()
    print(f"nRows: {len(data)}")
    return JSONResponse( jsonable_encoder(data.to_dict(orient="records")) )


## Coment out for Docker deployment
#if __name__ == "__main__":
#    PORT = 8010
#    uvicorn.run("server:app", host="localhost", port=PORT, log_level="info") #, workers=5, limit_concurrency=50)
