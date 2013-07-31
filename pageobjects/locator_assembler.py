from selenium_wrapper import SE

def locator_assembler(locator_name, locator_parameter):
    '''assembles a locator function out of its spec by formating'''
    return lambda *args, **kvargs: getattr(SE, locator_name)(locator_parameter.format(*args, **kvargs))
