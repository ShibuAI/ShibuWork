# agents/data_fetch_agent.py
import requests
from typing import Dict

BASE_URL = "http://127.0.0.1:8080"

def fetch_call_center_data(params: Dict):
    return requests.post(f"{BASE_URL}/call_center", json=params).json()

def fetch_inventory_data():
    return requests.get(f"{BASE_URL}/inventory").json()

def fetch_tech_product_data():
    return requests.get(f"{BASE_URL}/tech_product").json()
