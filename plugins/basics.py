from core import wmevent, editor, root, Buffer, register
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno

#print("I LIVE") # (don't ask)

@register
def save(event=None):
    buf = editor.buffer()
    if buf.is_untitled:
        path = asksaveasfilename()
        # If the user clicked 'Cancel', return without changing anything.
        if not path:
            return
        buf.path = path
        buf.is_untitled = False
        editor.update_titlebar()
        editor.update_tabs()
    with open(buf.path, 'wt') as outfile:
        outfile.write(buf.text)

@register
def open_(event):
    path = askopenfilename()
    # If the user clicked 'Cancel', return without changing anything
    if not path:
        return
    with open(path, 'rt') as infile:
        editor.add(Buffer(path, infile.read(), is_untitled=False))
        editor.select('end')

@register
def new(event):
    editor.add(Buffer(editor.new_untitled(), "", is_untitled=True))
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
        buf = editor.buffer()
        if buf.is_untitled and buf.text and _asksavep():
            save()
        editor.forget(editor.select())
    editor.update_titlebar()

def _asksavep():
    return askyesno("Save?", "Save %s?" % editor.buffer().path)
