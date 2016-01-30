from tkinter import Tk, BOTH, END
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook
import os
from settings import TITLE, TAB, UNTITLED, KEYMAP
import menu

_loop_functions = []
_startup_functions = []
_DEFAULT_PACK_OPT = {'fill': BOTH, 'expand': True}

def start():
    for action, bindings in KEYMAP.items():
        root.event_add(action, *bindings)
    menu.init_menu(root)
    for func in _startup_functions:
        func()
    for timeout, func in _loop_functions:
        root.after(timeout, func)
    root.mainloop()

# Very strange decorator for running a function in the Tkinter event loop.
class loop:
    """
This decorator takes one argument, timeout, and sets up the decorated function
so that it will run every timeout milliseconds.
    """
    def __init__(self, timeout=0):
        self.timeout = timeout
    def __call__(self, func):
        def func_with_loop(*args, **kwargs):
            func(*args, **kwargs)
            root.after(self.timeout, func_with_loop)
        _loop_functions.append((self.timeout, func_with_loop))
        return func

# Slightly less strange decorator for callbacks.
# This is a total abuse of decorators.
# Call 666-867-5309 now and give just $100%/month to stop decorator abuse.
class event:
    """
    This decorator takes one argument, the name of a Tkinter event, which the
    decorated function will be bound to.

    Arguments:
        event_name => A Tkinter event (e.g. <Control-c>, <Configure>)

    Returns:
        None

    """
    def __init__(self, event_name):
        self.event_name = event_name
    def __call__(self, func):
        root.bind(self.event_name, func)
        return func

# Decorator for functions called on startup.
def startup(func):
    _startup_functions.append(func)
    return func

# Decorator for window manager interfaces.
class wmevent:
    def __init__(self, event_name):
        self.event_name = event_name
    def __call__(self, func):
        root.wm_protocol(self.event_name, func)
        return func

# Main class of the editor.
class _Editor(Notebook):
    """
    The main class of the editor.

    Inherits from: `ttk.Notebook`

    Attributes:

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
