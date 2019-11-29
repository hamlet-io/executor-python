def replace_parameters_values(kwargs, replacers=None):
    for key, value in kwargs.items():
        for target, replacer in replacers:
            if value is target or value == target:
                kwargs[key] = replacer
                break
