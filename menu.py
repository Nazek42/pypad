from tkinter import Menu
from functools import partial, reduce
from itertools import zip_longest
import xml.etree.ElementTree as ET
from os import listdir
from os.path import abspath, join, splitext

def init_menu(window):
    tree = _load()
    _prioritize(tree)
    top = Menu(window)
    window.config(menu=top)
    def populate(element, menu):
        for child in element:
            if child.tag == 'item':
                action = child.get('action')
                if not action.startswith('<<'):
                    if action.startswith('<'):
                        action = '<' + action
                    else:
                        action = '<<' + action
                if not action.endswith('>>'):
                    if action.endswith('>'):
                        action += '>'
                    else:
                        action += '>>'
                assert action.startswith('<<') and action.endswith('>>')
                gen = partial(window.event_generate, action)
                menu.add_command(label=child.get('label'),command=gen)
            elif child.tag == 'sep':
                menu.add_separator()
            elif child.tag == 'menu':
                sub = populate(child, Menu(menu))
                menu.add_cascade(label=child.get('label'), menu=sub)
        return menu
    return populate(tree, top)

def _load():
    paths = [path for path in listdir('plugins') if _ext(path) == '.xml']
    trees = [ET.parse(abspath(join('plugins', path))).getroot() for path in paths]
    return reduce(_merge, trees)

def _merge(a, b):
    final = ET.Element('menu', a.attrib)
    for x, y in zip_longest(a, b):
        if x is None:
            final.append(y)
        elif y is None:
            final.append(x)
        elif x.tag == y.tag == 'menu' and x.get('label') == y.get('label'):
            final.append(_merge(x, y))
        else:
            final.append(x)
            final.append(y)
    return final

def _prioritize(menu):
    elements = list(menu)
    i = len(elements)
    for elem in elements:
        if elem.tag == 'menu':
            _prioritize(elem)
        priority = elem.get('priority')
        if priority is None:
            elem.set('priority', 'medium')
    elements.sort(key=lambda elem: {'highest': 0,
                                    'high':    1,
                                    'medium':  2,
                                    'low':     3,
                                    'lowest':  4,
                                   }[elem.get('priority')])
    attrib = menu.attrib
    menu.clear()
    for k, v in attrib.items():
        menu.set(k, v)
    menu.extend(elements)

def _ext(path):
    return splitext(path)[1]
