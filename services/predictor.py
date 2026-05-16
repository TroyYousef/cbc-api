import joblib
import numpy as np
import pandas as pd

CBC_FEATURES = [
    'WBC', 'LYMp', 'NEUTp', 'LYMn', 'NEUTn',
    'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT', 'PDW', 'PCT'
]

xgb_model     = joblib.load("ml/xgb_model.pkl")
label_encoder = joblib.load("ml/label_encoder.pkl")


def _clean_value(val):
    if val is None:
        return np.nan
    if isinstance(val, str):
        val = val.replace('%', '').replace(',', '.').strip()
        try:
            return float(val)
        except ValueError:
            return np.nan
    return float(val)


def predict_cbc(lab_values: dict) -> tuple:
    row = {f: _clean_value(lab_values.get(f)) for f in CBC_FEATURES}
    df  = pd.DataFrame([row]).astype(float)

    pred       = xgb_model.predict(df)[0]
    proba      = xgb_model.predict_proba(df)[0]
    confidence = round(float(np.max(proba)) * 100, 1)
    diagnosis  = label_encoder.inverse_transform([pred])[0]

    return diagnosis, confidence
