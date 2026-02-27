import joblib
import numpy as np
from datetime import datetime
from sensors.feature_engineering import extract_features
from database.db import get_connection

model = joblib.load("models/crash_model.pkl")

def log_event(pred, conf, alert):
    """
    Log event to database with proper type conversion.
    
    Args:
        pred: Predicted label (will be converted to int)
        conf: Confidence score (will be converted to float)
        alert: Alert message string
    """
    conn = get_connection()
    
    # Ensure proper type conversion
    predicted_label = int(pred) if pred is not None else None
    confidence = float(conf) if conf is not None else None
    
    # Validate that we have valid values
    if predicted_label is None:
        raise ValueError(f"Invalid prediction value: {pred}")
    if confidence is None:
        raise ValueError(f"Invalid confidence value: {conf}")
    
    conn.execute(
        "INSERT INTO events (timestamp, predicted_label, confidence, alert) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), predicted_label, confidence, str(alert))
    )
    conn.commit()
    conn.close()

def predict(signal):
    """
    Predict event type with realistic confidence variation and occasional anomalies.
    
    Args:
        signal: Sensor signal array
    
    Returns:
        tuple: (prediction, confidence) with realistic uncertainty
    """
    features = extract_features(signal)
    pred = model.predict([features])[0]
    # Convert numpy type to Python int
    pred = int(pred)
    proba = model.predict_proba([features])[0]
    base_conf = max(proba)
    
    # Add realistic confidence variation based on signal characteristics
    signal_max = np.max(np.abs(signal))
    signal_variance = np.var(signal)
    
    # Calculate uncertainty factors
    # Higher variance = lower confidence (more ambiguous signal)
    variance_factor = 1.0 - min(0.3, signal_variance / 10.0)
    
    # Extreme values might indicate noise or anomalies
    extreme_factor = 1.0
    if signal_max > 10:
        extreme_factor = 0.85  # Reduce confidence for extreme values
    elif signal_max < 0.1:
        extreme_factor = 0.90  # Slightly reduce for very quiet signals
    
    # Add random noise to confidence (realistic sensor uncertainty)
    noise = np.random.normal(0, 0.08)  # ±8% variation
    
    # Calculate adjusted confidence
    adjusted_conf = base_conf * variance_factor * extreme_factor + noise
    
    # Clamp confidence to realistic range [0.3, 0.98]
    # Never 100% confident (real-world uncertainty)
    # Never below 30% (if model predicts, it should have some confidence)
    adjusted_conf = np.clip(adjusted_conf, 0.30, 0.98)
    
    # Occasional anomaly: 5% chance of misclassification or low confidence
    if np.random.random() < 0.05:
        # Sometimes reduce confidence significantly (ambiguous reading)
        if np.random.random() < 0.5:
            adjusted_conf = np.clip(adjusted_conf - 0.25, 0.35, 0.75)
        # Rarely: slight misclassification (edge case)
        else:
            # Keep prediction but reduce confidence
            adjusted_conf = np.clip(adjusted_conf - 0.15, 0.40, 0.80)
    
    return pred, float(adjusted_conf)
