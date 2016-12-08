
import tkinter as tk
import tkinter.ttk as ttk

class MakerOptionMenu(tk.Frame):        #Used for creating Option Menus
    """
    Subclass and define a start method

    Required Options include:

    self.options                -       elements in the drop down menu

    Optional settings:

    self.butnOptions = {'width':25,'direction':'below'}         - config
    self.heading                s-      heading item for the list
    self.initialValue   -       a heading that lasts until selection change
    self.auto_list_update       - set to false to set updating list on click

    self.options can be either an iterable as well as a function

    To get results:
    use the self.var.get / set tkinter method
    or you can use:  def run_command(self, selection):
    """
    heading = None
    last_selected = ''
    auto_list_update = True
    frm_style = None
    def start(self):
        pass

    def __init__ (self, parent =None,app=None):
        tk.Frame.__init__(self,parent)
        #~ self.config(takefocus=True)
        self.app = app
        self.parent=parent
        self.start()
        if self.frm_style==None:
            self.config(**cfg_guimaker_frame)
        else:
            self.config(**self.frm_style)
        if not hasattr(self,'initialValue'):
            self.initialValue='Select a Key'
        if self.conPack==None:
            self.pack(expand=1,fill='both')
        else:
            self.pack(**self.conPack)
        self.create_entries()
        self.make_widget(self.LIST)

    def make_widget(self, options):
        self.var=tk.StringVar()
        self.var.set(self.initialValue)
        if len(options)==0:
            options=['empty']
        self.wid=ttk.Menubutton(self,textvariable=self.var)
        if hasattr(self,'butnOptions'):
            self.wid.config(**self.butnOptions)
        self.wid.menu = tk.Menu(self.wid,tearoff=0)
        self.re_populate()
        self.last_selected = self.var.get()
        self.wid.config(takefocus=True,menu=self.wid.menu)
        self.wid.pack(expand=1, fill='both')

    def create_entries(self):
        if not self.heading:
            # static list
            if type(self.options)==list:
                self.LIST=self.options
            # function that changes
            else:
                self.LIST=self.options()
        # with heading
        else:
            # static list
            if type(self.options)==list:
                self.LIST=self.options[:]
            # function that changes
            else:
                self.LIST=self.options()
            self.LIST.insert(0,self.heading)

    # redefine me lower
    def run_command(self, selection):
        pass

    def get_result(self,value):
        if self.auto_list_update:
            self.re_populate()
        self.run_command(value)
        self.var.set(value)

    def re_populate(self):
        self.create_entries()
        menu = self.wid.menu
        menu.delete(0, 'end')
        for string in self.LIST:
            menu.add_command(label=string,
                             command=lambda value=string: self.get_result(value))


def toggle(btn,tog=[0]):
    '''
    a list default argument has a fixed address
    '''
    tog[0] = not tog[0]
    if not tog[0]:
        return False
    else:
        return True


def button_change(but, state='toggle'):
    '''
    Used for setting TTK buttons as selected or unselected.

    str 'toggle' to toggle from the current state
    1 to set default to active              - Pressed state
    0 to set default state to normal

    To create the style of the selected state see below.
    Or see button_styling.py used by demo.py

    tkinter.ttk.Style().theme_create("toggle",
    "default",
    settings={
        "ToggleButton": {
            "configure": {"width": 10, "anchor": "center"},
            "layout": [
                ("ToggleButton.button", {"children":
                    [("ToggleButton.focus", {"children":
                        [("ToggleButton.padding", {"children":
                [("ToggleButton.label", {"side": "left", "expand": 1})]
                        })]
                    })]
                })
            ]
        }
        "ToggleButton.button": {"element create":
            ("image", 'button-n',
            ("pressed", 'button-p'),
            ("active","!alternate", 'button-h'),
            ("alternate", "button-s"), # THIS IS THE MAGIC tbutton-p
            {"border": [4, 10], "padding": 4, "sticky":"ewns"}
            )}
    })
    style.theme_use('toggle')
    '''
    if state == 'toggle':
        if str(but.cget('default')) == 'normal':
            but.config(default='active')
        else:
            but.config(default='normal')
    elif state:
        but.config(default='active')
    else:
        but.config(default='normal')


def menu_change(tk_var, value):
    tk_var.set(value)
