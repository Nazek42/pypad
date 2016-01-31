from tkinter import Tk, BOTH, END
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook
import os
from functools import partial
from settings import TITLE, TAB, UNTITLED, KEYMAP
import menu

_loop_functions = []
_startup_functions = []
_registered_functions = {}
_DEFAULT_PACK_OPT = {'fill': BOTH, 'expand': True}

def start():
    for action, bindings in KEYMAP.items():
        root.event_add(action, *bindings)
    for event, callback in _registered_functions.items():
        root.bind(event, callback)
    menu.init_menu(root)
    for func in _startup_functions:
        func()
    for timeout, func in _loop_functions:
        root.after(timeout, func)
    root.mainloop()

# Very strange decorator for running a function in the Tkinter event loop.
class loop:
    """
Decorator which sets the function to be run every `timeout` milliseconds. If
`timeout` is set to 0, the function will be run as often as possible.
    """
    def __init__(self, timeout=0):
        self.timeout = timeout
    def __call__(self, func):
        def func_with_loop(*args, **kwargs):
            func(*args, **kwargs)
            root.after(self.timeout, func_with_loop)
        _loop_functions.append((self.timeout, func_with_loop))
        return func

def register(func):
    """
Decorator which sets the function to be registered as an event. When `start()`
is called, a virtual event named '<<{plugin}.{func}>>' will be bound to the
function. This event is the one raised when its corresponding menu entry is
selected, or when any of the bindings defined in settings.py are pressed.
    """
    # This will result in an event_name like 'basics.new'
    event_name = '<<'+'.'.join(func.__module__.split('.')[1:]+[func.__name__])+'>>'
    #print("Registering %s" % event_name)
    _registered_functions[event_name] = func
    return func

# Decorator for functions called on startup.
def startup(func):
    """
Decorator which sets the function to be called once with no arguments on
startup.
    """
    _startup_functions.append(func)
    return func

# Decorator for window manager interfaces.
class wmevent:
    """
Decorator which sets the function to be called whenever a certain window manager
protocol happens. The name argument is typically either WM_DELETE_WINDOW
(the window is about to be deleted), WM_SAVE_YOURSELF (called by X window
managers when the application should save a snapshot of its working set) or
WM_TAKE_FOCUS (called by X window managers when the application receives
focus).
    """
    def __init__(self, name):
        self.name = name
    def __call__(self, func):
        root.wm_protocol(self.name, func)
        return func

# Main class of the editor.
class _Editor(Notebook):
    """
    The main class of the editor.

    Inherits from: `ttk.Notebook`
    """
    def __init__(self, parent=None):
        Notebook.__init__(self, parent)
        self.parent = parent
        self._untitled_index = 0
        self.pack(**_DEFAULT_PACK_OPT)
        self._buffers = []
        self.add(Buffer(self.new_untitled(), "", parent=self, is_untitled=True))
        self.select(0)
        self.enable_traversal()
        self.bind('<<NotebookTabChanged>>', self.update_titlebar)

    def select(self, tabid=None):
        """
        If called with a tab identifier: switch to that tab. If called with no
        arguments: return the window name of the active buffer.
        """
        if tabid is None:
            i = super().select() or 0
            #print("DEBUG: super().select() => |%s|" % str(i))
            return self.index(i)
        if tabid == 'end': tabid = self.index('end') - 1
        return super().select(tabid)

    def buffer(self, tabid=None):
        """
        If called with a tab identifier: return the corresponding buffer object.
        If called with no arguments: return the active buffer.
        """
        if tabid is None:
            return self._buffers[self.select()]
        return self._buffers[self.index(tabid)]

    def add(self, buf, **kw):
        """Add a buffer to the editor."""
        self._buffers.append(buf)
        p, f = os.path.split(buf.path)
        kw['text'] = TAB.format(path=p, file=f)
        if 'image' in kw:
            kw.pop('image')
        super().add(buf, **kw)

    def forget(self, tabid):
        """Completely remove a buffer from the editor."""
        super().forget(tabid)
        return self._buffers.pop(self.index(tabid))

    def update_titlebar(self, event=None):
        """Change the titlebar to reflect the current buffer."""
        buf = self.buffer()
        #print("DEBUG: self.buffer() => |%s|" % repr(buf))
        p, f = os.path.split(buf.path)
        self.parent.title(TITLE.format(path=p, file=f))

    def update_tabs(self):
        """Change the tabs' text to reflect their buffers."""
        for i in range(self.index('end')):
            buf = self.buffer(i)
            p, f = os.path.split(buf.path)
            self.tab(i, text=TAB.format(path=p, file=f))

    def new_untitled(self):
        """Generate a new unique name for an untitled file."""
        path = UNTITLED.format(number=self._untitled_index)
        self._untitled_index += 1
        return path

    def buffers(self):
        """
        Return a list of all current buffers.

        Note: This is a list of Buffer objects. For a list of window names, use
        tabs().
        """
        return self._buffers[:]


class Buffer(ScrolledText):
    """
    Class representing a single file for editing.

    Inherits from: `ScrolledText`

    Attributes:

    `path`
      A valid full path to the file associated with the buffer. If `is_untitled`
      is True, the value of `path` is not guaranteed to be readable, i.e. it may
      be something like `/home/bob/untitled_1`.

    `text`
      The contents of the buffer. Ideally, this is also the content of the file
      pointed to by `path`.

    `parent`
      The parent widget.

    `is_untitled`
      A Boolean value indicating whether or not the buffer is associated with a
      real file on disk or is just text which has not yet been saved.

    `Buffer` inherits from `ttk.ScrolledText`, meaning it also has all the
    attributes and methods of a Tkinter `Text` widget.
    """
    def __init__(self, path, text, parent=None, is_untitled=False, **kw):
        if parent is None:
            parent = editor
        ScrolledText.__init__(self, parent, **kw)
        if is_untitled:
            #print("DEBUG: os.getcwd() => |%s|" % os.getcwd())
            #print("DEBUG: path => |%s|" % path)
            self.path = os.path.join(os.getcwd(), path)
        else:
            self.path = path
        self.insert('1.0', text)
        self.is_untitled = is_untitled

    @property
    def text(self):
        return self.get('1.0', END)

    @text.setter
    def text(self, new):
        self.delete('1,0', END)
        self.insert('1.0', new)

root = Tk()
editor = _Editor(root)

if __name__ == '__main__':
    start()
