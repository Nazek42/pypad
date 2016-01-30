import os
plugins = os.listdir('plugins')
plugins.remove('__init__.py')
try:
    plugins.remove('__pycache__')
except ValueError:
    pass
plugins = [name for name, ext in map(os.path.splitext, plugins) if ext != '.pyc']
for plugin in plugins:
    exec("import plugins.{plugin}".format(plugin=plugin))
