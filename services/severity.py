from config.settings import SEVERITY_LEVELS

def get_severity(confidence):
    for level, (low, high, color) in SEVERITY_LEVELS.items():
        if low <= confidence < high:
            return level, color
    return "Unknown", "gray"
