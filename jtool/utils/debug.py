DEBUG_ENABLED = False


def enable_debug():
    global DEBUG_ENABLED
    DEBUG_ENABLED = True


def print_debug(*args):
    global DEBUG_ENABLED
    if DEBUG_ENABLED:
        print(*args)