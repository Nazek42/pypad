from core import wmevent, editor, root, Buffer, register
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno

@register
def save(event=None):
    buf = editor.buffer()
    if buf.is_untitled:
        path = asksaveasfilename()
        # If the user clicked 'Cancel', return without changing anything.
        if not path:
            return
        buf.path = path

    buf.flush()
    editor.update_titlebar()
    editor.update_tabs()

@register
def open_(event):
    path = askopenfilename()
    # If the user clicked 'Cancel', return without changing anything
    if not path:
        return

    with open(path, 'r+t') as infile:
        editor.add(Buffer(file=infile, text=infile.read()))
        editor.select('end')

@register
def new(event):
    editor.add(Buffer())
    editor.select('end')

@register
def pgrt(event):
    old = editor.select()
    if old == len(editor.buffers()) - 1:
        new = 0
    else:
        new = old + 1
    editor.select(new)

@register
def pglt(event):
    old = editor.select()
    if old == 0:
        new = len(editor.buffers()) - 1
    else:
        new = old - 1
    editor.select(new)

@register
@wmevent('WM_DELETE_WINDOW')
def quit():
    for i in editor.tabs():
        editor.select(i)
        buf = editor.buffer()
        #print("DEBUG: buf.path => |%s|" % buf.path)
        if buf.is_untitled and buf.text not in '\n' and _asksavep():
            save()
    root.destroy()

@register
def close(event):
    if len(editor.buffers()) == 1:
        quit()
    else:
        for buf in editor.buffers():
            if buf.is_untitled and buf.text not in '\n' and _asksavep():
                save()
            editor.forget(buf)
    editor.update_titlebar()

def _asksavep():
    return askyesno("Save?", "Save %s?" % editor.buffer().path)
