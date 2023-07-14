from . import user, utils


def get_all_handlers():
    return user.get_handlers() + utils.get_handlers()