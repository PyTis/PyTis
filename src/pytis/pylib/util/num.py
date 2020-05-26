__all__ = ['is_positive_int']
def is_positive_int(value):
    try:
        value = int(value)
    except ValueError:
        return False
    return value > 1

