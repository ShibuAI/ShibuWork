from http.client import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional

import pandas as pd
import os
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

class CallCenterRequest(BaseModel):
    City: Optional[str] = None
    CustomerName: Optional[str] = None


def excel_to_json(file_name: str):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_excel(file_path)
    print(f"Reading data from {file_path}")
    if df.empty:
        print("Warning: The DataFrame is empty.")
    else:
        print(f"DataFrame shape: {df.shape}")

    df = df.replace([float("inf"), float("-inf")], None)
    df = df.fillna("")  
    df = df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)
    return JSONResponse(content=df.to_dict(orient="records"))

# @app.get("/call_center")
# def get_call_center_data():
#     return excel_to_json("Call-Center-Sentiment-Sample-Data.xlsx")
@app.post("/call_center")
def get_call_center_data(request: CallCenterRequest):
    file_path = os.path.join(DATA_DIR, "Call-Center-Sentiment-Sample-Data.xlsx")
    df = pd.read_excel(file_path)
    filtered_df = df.copy()
    print(f"Reading data from {request.City} and {request.CustomerName}")
    if request.City:
        filtered_df = filtered_df[filtered_df["City"].str.lower() == request.City.lower()]
    if request.CustomerName:
        filtered_df = filtered_df[filtered_df["CustomerName"].str.lower() == request.CustomerName.lower()]

    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="No matching records found.")

    filtered_df = filtered_df.replace([float("inf"), float("-inf")], None)
    filtered_df = filtered_df.fillna("")
    filtered_df = filtered_df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)
    return JSONResponse(content=filtered_df.to_dict(orient="records"))

@app.get("/inventory")
def get_inventory_data():
    return excel_to_json("Inventory-Records-Sample-Data.xlsx")

@app.get("/tech_product")
def get_tech_product_data():
    return excel_to_json("Technological-Products-Sample-Data.xlsx")

