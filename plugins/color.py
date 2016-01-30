from core import event, editor
from tkinter.colorchooser import askcolor

@event('<<color.fgcolor>>')
def fgcolor(event):
    color_code = askcolor()[1] # Ex. '#00cc00'
    if not color_code: return
    tagname = 'color.fgcolor-%s' % color_code# Ex: 'color.fgcolor-#00cc00'
    editor.buffer().tag_config(tagname, foreground=color_code)
    editor.buffer().tag_add(tagname, 'sel.first', 'sel.last')

@event('<<color.bgcolor>>')
def bgcolor(event):
    color_code = askcolor()[1]
    if not color_code: return
    tagname = 'color.bgcolor-%s' % color_code
    editor.buffer().tag_config(tagname, background=color_code)
    editor.buffer().tag_add(tagname, 'sel.first', 'sel.last')
