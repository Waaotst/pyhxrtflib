
import os
from contextlib import suppress
import functools
from pprint import pprint
import tkinter as tk
from tkinter import font as tk_font

# Autogenerated haxe lib
from hxrtflib import hxrtflib_BaseEditor
from hxrtflib import hxrtflib_Hxrtflib as Hxrtflib
from hxrtflib import hxrtflib_Globals as Globals

from tkpyhxrtflib.util import debug_echo

IGNORE_KEYS = ('Left',
               'Down',
               'Right',
               'Up',
               'BackSpace',
               'Escape',)

IGNORE_CHARS = ('\x01', # Ctrl + a
                '',)

MOVE_KEYS = ('Left',
             'Down',
             'Right',
             'Up',
             'BackSpace',
             'Prior',
             'Next',)

MODS = ('Control',
        'Alt',
        'Shift',
        'Super')

class Pos():
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Sel():
    def __init__(self, start, end):
        self.start = start
        self.end = end


def tk_index(row: int, col: int):
    return str(row)+'.'+str(col)

def hx_index(index: str):
    pos = [int(x) for x in index.split('.')]
    return Pos(pos[0], pos[1])

def named_partial(name, func, *args):
    function = functools.partial(func, *args)
    function.__name__ = name
    return function


class EditorImplementation(tk.Text, hxrtflib_BaseEditor):
    def __init__(self, *args, **kwargs):
        self.tag_prefix = 'pyhxrtflib'
        super().__init__(*args, **kwargs)
        self._fonts = {}
        self.bind('<Key>', self._insert_char)
        self.bind('<Button-1>', self._mouse_click)

        hxrtflib_BaseEditor.__init__(self)

    def _mouse_click(self, event):
        def _():
            cursor = self._insert_cursor_get()
            self.rtflib.on_mouse_click(cursor.row, cursor.col)
        self.after_idle(_)

    def _insert_char(self, event):
        cursor = self.index('insert')
        pos = hx_index(cursor)
        self.rtflib.on_char_insert(event, pos.row, pos.col)

    def _hx_is_selected(self, row, col):
        tags = self.tag_names(tk_index(row, col))
        try:
            if tags[0] == 'sel':
                return True
        except IndexError:
            return False
        return False

    def _hx_first_selected_index(self, row, col):
        return hx_index(self.index('sel.first'))

    def _hx_char_at_index(self, row, col):
        return self.get(tk_index(row, col))

    def _hx_tag_at_index(self, row, col):
        # TODO should be tags_at_index ... send all tags..
        tags = self.tag_names(tk_index(row, col))
        try:
            return self.tk_tag_convert(tags[-1])
        except IndexError:
            return Globals.NOTHING

    def _hx_tag_add(self, tag, row, col):
        assert tag is not None
        index = tk_index(row, col)
        self.after_idle(named_partial('tag_update', self.tag_update, tag, index))

    def _hx_last_col(self, row):
        pos = hx_index(self.index('{}.end'.format(row)))
        return pos.col

    # @debug_echo
    def _hx_ignore_key(self, event):
        # pprint(event.__dict__)
        if event.char in IGNORE_CHARS or event.keysym in IGNORE_KEYS:
            return True
        for mod in MODS:
            if mod in event.keysym:
                return True
        return False

    def _hx_move_key(self, event):
        if event.keysym in MOVE_KEYS:
            return True
        return False

    def _hx_insert_cursor_get(self):
        return hx_index(self.index('insert'))

    @debug_echo
    def _hx_create_style(self, tag):
        # Get base font options
        new_font = tk_font.Font(self, self.cget("font"))
        tk_tag = self.hx_tag_convert(tag)
        self.tag_configure(tk_tag, font=new_font)
        self._fonts[tag] = new_font

    @debug_echo
    def _hx_modify_style(self, tag, change_type, change):
        # configure font attributes
        tk_tag = self.hx_tag_convert(tag)
        font = self._fonts[tag]
        try:
            font.configure(**self.option_list[change])
        except KeyError:
            if change_type == 'size':
                if os.name == 'posix':
                    font.configure(size=int(change)-2)
                else:
                    font.configure(size=change)
            elif change_type == 'family':
                font.configure(family=change)
            elif change_type == 'background':
                self.tag_configure(tk_tag, background=change)
            elif change_type == 'foreground':
                self.tag_configure(tk_tag, foreground=change)
            else:
                raise Exception('bad change type?')

    @debug_echo
    def _hx_sel_index_get(self, row, col):
        assert self._is_selected(row, col)
        start = hx_index(self.index('sel.first'))
        end = hx_index(self.index('sel.last'))
        return Sel(start, end)

    def hx_tag_convert(self, tag):
        '''Convert a Pyhxrtflib tag to be suitable for tkinter'''
        return self.tag_prefix + str(tag)

    def tk_tag_convert(self, tk_tag):
        ''' Convert a tk tag back to Pyhxrtflib format'''
        return int(tk_tag.split(self.tag_prefix)[-1])

    # @debug_echo
    def tag_update(self, tag, index):
        '''
        We need to allow the char to be insert before adding tags,
        This should be called using widget.after
        '''
        tk_tag = self.hx_tag_convert(tag)
        self.tag_add(tk_tag, index)
        with suppress(IndexError):
            # Fails on 1.0
            # TODO this should be handled by the hxrtflib
            all_tags = self.tag_names(index)
            for x in all_tags:
                if x != tk_tag:
                    self.tag_remove(x, index)


class PyTextRtf(EditorImplementation):
    option_list = {'bold':{'weight':'bold'},
                   'solid':{'underline':1},
                   'italic':{'slant':'italic'},
                   'overstrike':{'overstrike':1}}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rtflib = Hxrtflib(self)

        def tk_breaker(func):
            ''' stop propergation of tkinter events '''
            def _(*args, **kwargs):
                func(*args, **kwargs)
                return 'break'
            return _

        self.rtflib.style_change = tk_breaker(self.rtflib.style_change)


if __name__ == '__main__':
    import demo
    demo.start()

