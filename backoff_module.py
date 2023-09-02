# backoff_module.py

import backoff

def giveup(exc):
    """Function to determine if we should give up a retry attempt."""
    # You can customize this to determine when to give up.
    # For example, you might want to give up on specific exception types.
    return False

# Custom backoff decorator
custom_backoff = backoff.on_exception(backoff.expo,
                                      Exception,  # This can be more specific if needed
                                      max_tries=4,  # 3 retries: 10s, 30s, 60s, then it gives up
                                      max_value=60,  # Maximum backoff time
                                      giveup=giveup,
                                      jitter=None)  # No jitter for simplicity, but can be added if needed
