def seconds_to_ms(seconds: int):
    try:
        return seconds * 1000
    except Exception:
        return seconds
