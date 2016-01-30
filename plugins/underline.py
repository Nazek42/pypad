from core import event, editor

_i = 0

@event('<<underline.uon>>')
def uon(event):
    global _i
    print("hi")
    buf = editor.buffer()
    tagname = 'underline.underline-%d' % _i
    _i += 1
    buf.tag_config(tagname, underline=True)
    buf.tag_add(tagname, 'sel.first', 'sel.last')

@event('<<underline.uoff>>')
def uoff(event):
    global _i
    buf = editor.buffer()
    tagname = 'underline.underline-%d' % _i
    _i += 1
    buf.tag_config(tagname, underline=False)
    buf.tag_add(tagname, 'sel.first', 'sel.last')
