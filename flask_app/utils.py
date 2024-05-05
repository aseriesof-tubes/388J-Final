from datetime import datetime

# Don't need to touch
def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")
