import pkgutil

# List of modules to exclude
excludeModules = ['threadingtests']

# Build list of all modules in package
__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    if module_name not in excludeModules:
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
