# Training script

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports after path setup (required for module resolution)
import joblib  # noqa: E402
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
from sensors.signal_generator import generate_signal  # noqa: E402
from sensors.feature_engineering import extract_features  # noqa: E402

print("🔄 Generating training data...")
X, y = [], []

# Reduced samples for faster training (4 labels × 200 samples = 800 total)
# Increase if you need better accuracy
SAMPLES_PER_LABEL = 200

for label in range(4):
    print(f"  Generating samples for label {label}...")
    for _ in range(SAMPLES_PER_LABEL):
        signal = generate_signal(label)
        X.append(extract_features(signal))
        y.append(label)

print(f"✅ Generated {len(X)} training samples")
print("🔄 Training model...")

model = RandomForestClassifier(
    n_estimators=100,  # Reduced from 200 for faster training
    class_weight="balanced",
    random_state=42,
    n_jobs=-1  # Use all CPU cores for faster training
)

model.fit(X, y)
model_path = project_root / "models" / "crash_model.pkl"
joblib.dump(model, model_path)
print(f"✅ Model trained & saved to {model_path}")
