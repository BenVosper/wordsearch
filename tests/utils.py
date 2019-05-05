from numpy.random import get_state, set_state, seed as set_seed


def fix_random_seed(seed=1234):
    """Fix numpy random seed for decorated function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            initial_state = get_state()
            set_seed(seed)
            return_value = func(*args, **kwargs)
            set_state(initial_state)
            return return_value
        return wrapper
    return decorator
