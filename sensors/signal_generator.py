# Synthetic sensor logic

import numpy as np
from config.settings import SAMPLE_RATE, WINDOW_DURATION

def time_axis():
    return np.linspace(0, WINDOW_DURATION, SAMPLE_RATE * WINDOW_DURATION)

def normal_signal(t):
    base = 0.3 * np.sin(2 * np.pi * 0.5 * t)
    noise = np.random.normal(0, 0.05, len(t))
    
    # Occasional small anomalies in normal signals (10% chance)
    if np.random.random() < 0.10:
        # Add occasional spike or dip
        spike_idx = np.random.randint(0, len(t))
        noise[spike_idx] += np.random.choice([-0.3, 0.3])
    
    return base + noise

def crash_signal(t, severity=8):
    # Add variation to severity (±20%)
    severity_variation = severity * (1 + np.random.uniform(-0.2, 0.2))
    
    impact = severity_variation * np.exp(-20 * (t - 2.5)**2)
    vibration = 0.5 * np.sin(20 * t)
    
    # Variable noise level
    noise_level = np.random.uniform(0.08, 0.15)
    noise = np.random.normal(0, noise_level, len(t))
    
    # Occasional sensor glitches (5% chance)
    if np.random.random() < 0.05:
        # Add random spike or dropout
        glitch_idx = np.random.randint(0, len(t))
        if np.random.random() < 0.5:
            noise[glitch_idx] += np.random.uniform(1.0, 2.0)  # Spike
        else:
            noise[glitch_idx:glitch_idx+5] *= 0.1  # Brief dropout
    
    return impact + vibration + noise

def generate_signal(label):
    t = time_axis()
    if label == 0:
        signal = normal_signal(t)
    elif label == 1:
        # Mild impact with more variation
        severity = np.random.uniform(2.5, 3.5)
        signal = crash_signal(t, severity=severity)
    elif label == 2:
        # Severe crash with variation
        severity = np.random.uniform(7.0, 9.0)
        signal = crash_signal(t, severity=severity)
    else:
        # Container shift with variation
        severity = np.random.uniform(4.0, 6.0)
        signal = crash_signal(t, severity=severity) * np.sign(np.sin(t))
    
    # Add occasional sensor drift or calibration issues (3% chance)
    if np.random.random() < 0.03:
        drift = np.linspace(0, np.random.uniform(-0.2, 0.2), len(signal))
        signal = signal + drift
    
    return signal
