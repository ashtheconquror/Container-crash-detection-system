import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
from pathlib import Path

def generate_data(n_samples=5000):
    np.random.seed(42)
    
    data = {
        'wave_height_max': np.random.uniform(0, 10, n_samples),
        'wind_speed_max': np.random.uniform(0, 100, n_samples),
        'voyage_duration_days': np.random.uniform(1, 30, n_samples),
        'cargo_fragility': np.random.uniform(0.1, 1.0, n_samples),
        'container_count_teu': np.random.randint(10, 20001, n_samples),
        'alignment_score': np.random.uniform(0.5, 1.0, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate crash probability based on the features
    # Higher waves, wind, fragility, and lower alignment scores increase probability
    
    # Normalized components (0 to 1 scale)
    wave_norm = df['wave_height_max'] / 10.0
    wind_norm = df['wind_speed_max'] / 100.0
    fragility_norm = (df['cargo_fragility'] - 0.1) / 0.9
    alignment_norm = (1.0 - df['alignment_score']) / 0.5 # 0.5 -> 1.0, 1.0 -> 0.0
    
    # Base probability calculation
    # Significant weights for requested features
    prob = (
        0.30 * wave_norm + 
        0.30 * wind_norm + 
        0.15 * fragility_norm + 
        0.15 * alignment_norm +
        0.05 * (df['voyage_duration_days'] / 30.0) +
        0.05 * (df['container_count_teu'] / 20000.0)
    )
    
    # Add some noise
    noise = np.random.normal(0, 0.05, n_samples)
    prob = prob + noise
    
    # Clip probabilities to [0, 1]
    df['crash_probability'] = np.clip(prob, 0, 1)
    
    return df

def train_model():
    print("🔄 Generating synthetic dataset (5,000 samples)...")
    df = generate_data(5000)
    
    X = df.drop('crash_probability', axis=1)
    y = df['crash_probability']
    
    print("🔄 Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    model_path = Path(__file__).parent / "risk_model.pkl"
    print(f"🔄 Saving model to {model_path}...")
    joblib.dump(model, model_path)
    
    print("✅ Container Risk Assessment model training complete!")
    print(f"✅ Model saved to: {model_path}")

if __name__ == "__main__":
    train_model()
