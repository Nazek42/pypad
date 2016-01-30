Pypad menu configuration

This XML file contains the specification for Pypad's overhead menu. It is
composed of `menu`, `item`, and `sep` tags.

The `menu` tag represents a drop-down menu or sub-menu. The root element should
be an unlabeled `menu` tag. The `label` attribute is the text that will be
displayed to the user.

The `item` tag represents a single menu entry, with an associated action. The
`label` attribute is the text that will be displayed to the user. The `action`
attribute is the virtual event that will be raised when the entry is selected.

Note: Tkinter virtual events are surrounded by double angle brackets (<<>>). Due
to the severe annoyance of having to write `&lt;&lt;` and `&gt;&gt;` for every
action, the angle brackets may be left off; the code that parses this file
intelligently decides whether to add them back.

The `sep` tag represents a separator inside a menu.
