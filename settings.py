# Pypad settings
#
# This file consists of several Python variable declarations which control the
# operation of Pypad. Lines starting with # are ignored.

# Key bindings
# The keys in this dictionary represent actions within the editor. The values
# represent the keys or other inputs bound to them. Note that capitalizing a key
# within the binding will make it require Shift, e.g. `<Control-c>` is Ctrl-C,
# but `<Control-C>` is Ctrl-Shift-C. For more information on the names of input
# events, see the Tkinter documentation.
KEYMAP = {
'<<basics.save>>': [
    '<Control-s>',
],
'<<basics.open>>': [
    '<Control-o>',
],
'<<basics.new>>': [
    '<Control-n>',
],
'<<basics.pgrt>>': [
    '<Control-Right>',
],
'<<basics.pglt>>': [
    '<Control-Left>',
],
'<<basics.quit>>': [
    '<Control-q>',
],
'<<color.fgcolor>>': [
    '<Control-C>',
],
'<<color.bgcolor>>': [
    '<Control-H>',
],
'<<basics.close>>': [
    '<Control-w>',
],
'<<underline.uon>>': [
    '<Control-u>',
],
'<<underline.uoff>>': [
    '<Control-U>',
],
}

# The text displayed in the titlebar.
TITLE = "{file} in {path} - Pypad"

# The default name for a new file.
UNTITLED = "untitled_{number}"

# The text displayed in each tab.
TAB = "{file}"
