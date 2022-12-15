from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
from fastapi import Depends
import numpy as np
import pandas as pd

app = FastAPI(title="Credit card fraud model", description="API for fraud detection", version="1.0")

model = load('./rf_credit_card.joblib')
scaler = load('./rf_credit_card_scaler.joblib')


class Input(BaseModel):
    distance_from_home: float
    distance_from_last_transaction: float
    ratio_to_median_purchase_price: float
    repeat_retailer: float
    used_chip: float
    used_pin_number: float
    online_order: float


@app.get("/credit_card", response_model=float, operation_id="score_credit_card_transaction")
async def root(data: Input = Depends()):
    query_df = pd.DataFrame(vars(data), index=[0])
    query = scaler.transform(np.array(query_df))
    prediction = model.predict(query)
    return prediction[0]
