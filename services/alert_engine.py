# Severity rules

from config.settings import SEVERITY_THRESHOLDS

def get_alert(pred, confidence):
    """
    Generate professional alert messages based on prediction and confidence.
    
    Args:
        pred: Predicted event label (0=Normal, 1=Mild, 2=Severe, 3=Shift)
        confidence: Model confidence score (0.0 to 1.0)
    
    Returns:
        str: Professional alert message
    """
    if confidence > SEVERITY_THRESHOLDS["warning"] and pred == 2:
        return "🚨 SEVERE CRASH DETECTED"
    elif pred == 2:
        return "⚠️ Severe Crash Detected (Low Confidence)"
    elif confidence > SEVERITY_THRESHOLDS["normal"] and pred == 1:
        return "⚠️ Mild Impact Warning"
    elif pred == 1:
        return "⚠️ Mild Impact Detected (Low Confidence)"
    elif pred == 3:
        return "📦 Container Shift Detected"
    return "✅ Normal Operation"
