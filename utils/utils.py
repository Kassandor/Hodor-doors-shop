import logging


def get_logger(name='', module_name='komstroy'):
    if name:
        module_name += '.{}'.format(name)
    return logging.getLogger(module_name)
