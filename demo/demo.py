import tkinter as tk
import tkinter.ttk as ttk

from pyhxrtflib import PyTextRtf

try:
    from . import button_styling
except SystemError:
    import button_styling

try:
    from . import util
except SystemError:
    import util


def print_tag(event, editor):
    def _():
        cursor = editor.index('insert')
        try:
            print(cursor, ' ',editor.tag_names(cursor))
        except IndexError:
            pass
    editor.after_idle(_)


def remove_default_bindings(text):
    '''
    silence those pesky tkinter textwidget binds!
    If you plan to use the key, you need to ensure to return "break"
    this could also be an option
    http://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding-in-python
    '''
    # Remove Default Bindings and what happens on insert etc
    def null(event):
        print('removed binding')
        return "break"
    text.bind('<Control-Key-d>', null)      # Delete
    text.bind('<Control-Key-t>', null)      # Switch chars
    text.bind('<Control-Key-h>', null)      # Backspace
    text.bind('<Control-Key-k>', null)      # Delete Rest of line
    text.bind('<Control-Key-o>', null)      # Shift line down
    text.bind('<Control-Key-o>', null)      # Shift line down
    text.bind('<Control-Key-r>', null)      # Home
    text.bind('<Control-Key-i>', null)      # Tab
    text.bind('<Control-Key-p>', null)      # Paste


class RoomEditor(PyTextRtf):
    # http://effbot.org/zone/vroom.htm  credits Fredrik Lundh
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.debug_echo =  True
        self.config(
            borderwidth=0,
            font=('Lucida Sans Typewriter', 12),
            foreground="green",
            background="black",
            insertbackground="white", # cursor
            selectforeground="green", # selection
            selectbackground="turquoise1",
            wrap=tk.WORD, # use word wrapping
            undo=True,)

        remove_default_bindings(self)

root = tk.Tk()
root.config(background="black")
editor = RoomEditor(root)
editor.pack(fill='both', expand=1, pady=10)
editor.focus_set()

# Clicking will print the tags at that char
editor.bind('<Button-1>', lambda e, editor=editor: print_tag(e, editor))

# Pdb
import pdb
def _():
    pdb.set_trace()
    return 'break'
editor.bind('<9>', lambda e: _())

# Style for ttk button styles for button state toggling
button_styling.install(root, imgdir='img')

# Setting up Keybinds
editor.bind('<Control-Key-b>', lambda e:editor.rtflib.style_change('weight', 'bold'))
editor.bind('<Control-Key-i>', lambda e:editor.rtflib.style_change('slant', 'italic'))

# Setting up buttons and callbacks
bold = ttk.Button(root,
        text='Bold',
        command = lambda: editor.rtflib.style_change('weight', 'bold'),
        style='ToggleButton')
bold.pack(side='left')
italic = ttk.Button(root,
        text='Italic',
        command = lambda: editor.rtflib.style_change('slant', 'italic'),
        style='ToggleButton')
italic.pack(side='left')
# underline = ttk.Button(root,
        # text='Underline',
        # command = lambda: editor.rtflib.style_change('', 'solid'),
        # style='ToggleButton')
# underline.pack(side='left')
# overstrike = ttk.Button(root,
        # text='Overstrike',
        # command = lambda: editor.rtflib.style_change('overstrike'),
        # style='ToggleButton')
# overstrike.pack(side='left')

class FamilyMenu(util.MakerOptionMenu):
    def start(self):
        self.initialValue = 'Font'
        self.options = ['Arial','Times New Roman','Trebuchet Ms','Comis Sans Ms','Verdana','Georgia']
        self.conPack = {'expand':0,'side':'left'}
        self.frm_style = {'width':20}
    def run_command(self,value):
        editor.rtflib.style_change(('family',value))

class SizeMenu(util.MakerOptionMenu):
    def start(self):
        self.initialValue = 'Size'
        self.options = [6,8,10,12,14,16,18]
        self.conPack = {'expand':0,'side':'left'}
        self.frm_style = {'width':20}
    def run_command(self,value):
        editor.rtflib.style_change(('size',value))

class Colour(ttk.Button):
    def __init__(self, parent, colour_type, **kwargs):
        ttk.Button.__init__(self, parent)
        self.colour_type = colour_type
        self.style = ttk.Style()
        self.config(command=lambda:self.change_colour(),
                    width=6,
                    style = colour_type +'.TButton', **kwargs)
        self.pack()
                                                                    # Colour type can be foreground or background
    def change_colour(self):
        value = askcolor()[1]
        editor.tag_manager.style_change((self.colour_type, value))
        ttk.Style().configure(self.colour_type+'.TButton', background=value)

    def set(self, value):
        ttk.Style().configure(self.colour_type+'.TButton', background=value)

# Init the buttons
family_font_menu = FamilyMenu(root)
size_menu = SizeMenu(root)
foreground = Colour(root, colour_type='foreground', text='A')
background = Colour(root, colour_type='background', text ='H')

# Setting up button references for indenting and value setting
def event_handler(key, value): # TODO move into haxe core
    print('event_handler ', key)
    if key == 'reset':
        util.button_change(bold, 0)
    if value == 'bold':
        util.button_change(bold)
    elif value == 'italic':
        util.button_change(italic)
    elif value == 'overstrike':
        util.button_change(overstrike)
    elif key == 'size':
        util.menu_change(size_menu.var, value)
    elif key == 'family':
        util.menu_change(family_font_menu.var, value)
    elif key == 'foreground':
        util.menu_change(foreground, value)
    elif key == 'background':
        util.menu_change(background, value)

editor.rtflib.register_consumer(event_handler)

def start():
	root.mainloop()

if __name__ == '__main__':
    start()

