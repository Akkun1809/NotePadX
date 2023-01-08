import tkinter as tk
import customtkinter as cstk
from tkinter.messagebox import *
from tkinter import filedialog as fd
from configparser import ConfigParser
import os, sys, getpass

class App(cstk.CTk):
    def __init__(self):
        super().__init__()
        
        self.usrnm = getpass.getuser()
        self.pth_fldr = f"C:\\Users\\{self.usrnm}\\AppData\\Roaming\\NotePadX"
        if os.path.isdir(f"{self.pth_fldr}"):
            pass
        else:
            os.makedirs(f"{self.pth_fldr}")
            
        self.wind_width = 600
        self.wind_height = 400
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.center_x = int(self.screen_width/2 - self.wind_width/2)
        self.center_y = int(self.screen_height/2 - self.wind_height/2)
        self.title("NotePadX")
        self.geometry(f"{self.wind_width}x{self.wind_height}+{self.center_x}+{self.center_y}")
        cstk.set_appearance_mode("Dark")
        cstk.set_default_color_theme("blue")

        if len(sys.argv) == 2:
            self.fl_pssd = sys.argv[1]
        else:
            self.fl_pssd = ""

        self.mn_var = 0
        self.base = ""
        self.file = ""
        self.selected = ""
        self.config_object = None
        self.txt_fnt = None
        self.sys_fnt = None
        self.about_win = cstk.CTkToplevel(self)
        self.about_win.destroy()
        self.sttngs_win = cstk.CTkToplevel(self)
        self.sttngs_win.destroy()
        x = 0
        self.config_name = "config.ini"
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.path.dirname(__file__)
        self.config_path = os.path.join(self.pth_fldr, self.config_name)

        if os.path.isfile(os.path.join(self.application_path, "note.ico")):
            self.iconbitmap(os.path.join(self.application_path, "note.ico"))
        else:
            pass
        if os.path.isfile(f"{self.config_path}"):
            pass
        else:
            self.crt_cnfgfl()

        self.load_cnfgfl()

        # Menu Frame
        self.lft_frame = cstk.CTkFrame(self)

        # Text Frame
        self.txt_frame = cstk.CTkFrame(self)
        self.txt_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.txt_box = cstk.CTkTextbox(self.txt_frame, corner_radius=0, border_spacing=1, undo=True)
        self.txt_box.pack(expand=True, fill=tk.BOTH)
        self.txt_box.bind("<Control-o>", self.openfl)
        self.txt_box.bind("<Control-s>", self.save)
        self.txt_box.bind("<Control-S>", self.save_as)
        self.txt_box.bind("<Control-q>", self.close_fl)

        if os.path.isfile(self.fl_pssd):
            print("El Archivo Existe!")
            self.file = self.fl_pssd
            self.base = os.path.basename(self.file)
            self.title(f"{self.base} - NotePadX")
            self.txt_box.delete(1.0, tk.END)
            with open(self.fl_pssd, "r") as filehandle:
                for linea in filehandle:
                    self.txt_box.insert(tk.END, linea)
        else:
            print("El Archivo No Existe!")

        # Status Bar Frame
        self.sts_frame = cstk.CTkFrame(self.txt_frame, height=40)
        self.sts_frame.pack(fill=tk.X)

        ################################
        # Menu
        self.menu_lbl = cstk.CTkLabel(self.sts_frame, text="Menu")
        self.menu_lbl.pack(side=tk.LEFT, padx=10)
        self.menu_lbl.bind("<Button-1>", self.menu)

        #################
        # File Menu Options
        #################
        self.btn_file = cstk.CTkButton(self.lft_frame, text="File", corner_radius=0, fg_color='transparent', hover_color="red", border_color="red", command=self.mn_file) #command=self.mn_file
        self.btn_file.pack(fill=tk.BOTH, expand=True)

        self.btn_open = cstk.CTkButton(self.lft_frame, text="Open", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.openfl) #command=self.openfl
        self.btn_save = cstk.CTkButton(self.lft_frame, text="Save", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.save) #command=self.save
        self.btn_saveas = cstk.CTkButton(self.lft_frame, text="Save As", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.save_as) #command=self.save_as
        self.btn_close = cstk.CTkButton(self.lft_frame, text="Close", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.close_fl) #command=self.close_fl

        #################
        # Edit Menu Options
        #################
        self.btn_edit = cstk.CTkButton(self.lft_frame, text="Edit", corner_radius=0, fg_color='transparent', hover_color="red", border_color="red", command=self.mn_edit) #command=self.mn_edit
        self.btn_edit.pack(fill=tk.BOTH, expand=True)

        self.btn_cut = cstk.CTkButton(self.lft_frame, text="Cut", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.cut_text) #command=self.cut_text
        self.btn_copy = cstk.CTkButton(self.lft_frame, text="Copy", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.copy_text) #command=self.copy_text
        self.btn_paste = cstk.CTkButton(self.lft_frame, text="Paste", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.paste_text) #command=self.paste_text
        self.btn_undo = cstk.CTkButton(self.lft_frame, text="Undo", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.txt_box.edit_undo) #command=self.txt_box.edit_undo
        self.btn_redo = cstk.CTkButton(self.lft_frame, text="Redo", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.txt_box.edit_redo) #command=self.txt_box.edit_redo

        #################
        # Settings Menu Options
        #################
        self.btn_settings = cstk.CTkButton(self.lft_frame, text="Settings", corner_radius=0, fg_color='transparent', hover_color="red", border_color="red", command=self.mn_settings) #command=self.mn_settings
        self.btn_settings.pack(fill=tk.BOTH, expand=True)

        #################
        # About Menu Options
        #################
        self.btn_about = cstk.CTkButton(self.lft_frame, text="About", corner_radius=0, fg_color='transparent', hover_color="red", border_color="red", command=self.mn_about) #command=self.mn_about
        self.btn_about.pack(fill=tk.BOTH, expand=True)

        self.set_sysfnt(self.sys_fnt['family'], self.sys_fnt['size'], self.sys_fnt['weight'])
        self.set_txtfnt(self.txt_fnt['family'], self.txt_fnt['size'], self.txt_fnt['weight'])

    def menu(self, e=None):
        """Show and Hide the Menu Options"""
        if self.mn_var == 0:
            self.lft_frame.pack(side=tk.RIGHT, fill=tk.BOTH, ipadx=20)
            self.mn_var = 1
        elif self.mn_var == 1:
            self.menu_bck()
            self.lft_frame.pack_forget()
            self.mn_var = 0
    
    def menu_bck(self):
        """Function to show the Menu Options and get back from Options"""
        self.btn_file.pack_forget()
        self.btn_open.pack_forget()
        self.btn_save.pack_forget()
        self.btn_saveas.pack_forget()
        self.btn_close.pack_forget()
        self.btn_edit.pack_forget()
        self.btn_cut.pack_forget()
        self.btn_copy.pack_forget()
        self.btn_paste.pack_forget()
        self.btn_undo.pack_forget()
        self.btn_redo.pack_forget()
        self.btn_settings.pack_forget()
        self.btn_about.pack_forget()

        self.btn_file.pack(fill=tk.BOTH, expand=True)
        self.btn_file.configure(command=self.mn_file)

        self.btn_edit.pack(fill=tk.BOTH, expand=True)
        self.btn_edit.configure(command=self.mn_edit)

        self.btn_settings.pack(fill=tk.BOTH, expand=True)
        #self.btn_settings.configure(command=self.mn_settings)

        self.btn_about.pack(fill=tk.BOTH, expand=True)
        self.btn_about.configure(command=self.mn_about)

        self.update()

    def mn_file(self):
        """Display the File Menu Options"""
        self.btn_file.pack_forget()
        self.btn_edit.pack_forget()
        self.btn_settings.pack_forget()
        self.btn_about.pack_forget()
        self.update()
        self.btn_file.pack(side=tk.TOP, fill=tk.X)
        self.btn_file.configure(command=self.menu_bck)
        self.btn_open.pack(fill=tk.X, pady=(20,0))
        self.btn_save.pack(fill=tk.X, pady=(20,0))
        self.btn_saveas.pack(fill=tk.X, pady=(20,0))
        self.btn_close.pack(fill=tk.X, pady=(20,0))

    #################
    # File Functions

    def openfl(self, e=None):
        """Open a FileDialog to Choose the file to open\n\n
        base => BaseName of the file\n
        file => Path of the file"""
        filetypes = (
            ('Text Files', '*.txt'),
            ('All Files', '*.*')
        )

        f = fd.askopenfilename(filetypes=filetypes)
        self.file = f
        self.base = os.path.basename(f)
        self.title(f"{self.base} - NotePadX")
        if f != "":
            self.txt_box.delete(1.0, tk.END)
            with open(f, "r") as filehandle:
                for linea in filehandle:
                    self.txt_box.insert(tk.END, linea)
        self.menu()

    def save(self, e=None):
        """Save the file if exists and if don't show the FileDialog to save the file\n\n
        base => BaseName of the file\n
        file => Path of the file"""
        if self.file == "":
            f = fd.asksaveasfilename(defaultextension='.txt', filetypes=(
                            ("Text files", "*.txt"),
                            ("All files", "*.*"),
                        ))
            if f != "":
                self.file = f
                self.base = os.path.basename(f)
                self.title(f"{self.base} - NotePadX")
                txt = self.txt_box.get("0.0", "end")
                arch1 = open(f, "w")
                arch1.write(txt)
                arch1.close()
            else:
                showerror(title="Error", message="Ha Ocurrido un Error al guardar")
        else:
            self.title(f"{self.base} - NotePadX")
            txt = self.txt_box.get("0.0", "end")
            arch1 = open(self.file, "w")
            arch1.write(txt)
            arch1.close()
        self.menu()

    def save_as(self, e=None):
        """Show a FileDialog to save the file don't care if exists\n\n
        base => BaseName of the file\n
        file => Path of the file"""
        f = fd.asksaveasfilename(defaultextension='.txt', filetypes=(
                        ("Text files", "*.txt"),
                        ("All files", "*.*"),
                    ))
        if f != "":
            self.file = f
            self.base = os.path.basename(f)
            self.title(f"{self.base} - NotePadX")
            txt = self.txt_box.get("0.0", "end")
            arch1 = open(f, "w")
            arch1.write(txt)
            arch1.close()
        else:
            showerror(title="Error", message="Ha Ocurrido un Error al guardar")
        
        self.menu()

    def close_fl(self, e=None):
        """If an file is opened save's it, clear the Text Box, reset the title and if not exists just clear the Text Box and reset the title\n
        file => Path of the file"""
        if self.file != "":
            self.save()
            self.file = ""
            self.title("NotepadX")
            self.txt_box.delete(1.0, tk.END)
        else:
            self.file = ""
            self.title("NotepadX")
            self.txt_box.delete(1.0, tk.END)

    ##############################
    # Edit Functions
    def mn_edit(self):
        """Display the Edit Menu Options"""
        self.btn_file.pack_forget()
        self.btn_edit.pack_forget()
        self.btn_settings.pack_forget()
        self.btn_about.pack_forget()
        self.update()
        self.btn_edit.pack(side=tk.TOP, fill=tk.X)
        self.btn_edit.configure(command=self.menu_bck)
        self.btn_cut.pack(fill=tk.X, pady=(20,0))
        self.btn_copy.pack(fill=tk.X, pady=(20,0))
        self.btn_paste.pack(fill=tk.X, pady=(20,0))
        self.btn_undo.pack(fill=tk.X, pady=(20,0))
        self.btn_redo.pack(fill=tk.X, pady=(20,0))

    def cut_text(self, e=None):
        """Just Cut Text Function\n\n
        selected => Text from Text Box"""
        if self.txt_box.selection_get():
            # Grab selected text from text box
            self.selected = self.txt_box.selection_get()
            # Delete select text from text box
            self.txt_box.delete("sel.first", "sel.last")
            #root.clipboard_clear()
            self.clipboard_append(self.selected)
            self.update()

    def copy_text(self, e=None):
        """Just Copy Text FUnction\n\n
        selected => Text from Text Box"""
        if self.txt_box.selection_get():
            self.selected = self.txt_box.selection_get()
            self.clipboard_append(self.selected)
            self.update()

    def paste_text(self, e=None):
        """Just Paste Text Function"""
        position = self.txt_box.index(tk.INSERT)
        self.txt_box.insert(position, self.clipboard_get())

    def mn_settings(self):
        """Display the Settings in a TopLevel"""
        try:
            if tk.Toplevel.winfo_exists(self.sttngs_win) == 0:
                self.sttngs_win = cstk.CTkToplevel(self)
                self.sttngs_win.geometry("540x300")
                self.sttngs_win.resizable(False,False)
                self.sttngs_win.title("Settings")
                self.sttngs_win.iconbitmap(os.path.join(self.application_path, "note.ico"))

                # Creating the lists
                self.font_list = []
                self.font_style = ["Normal", "Bold"]
                self.font_size = []

                self.crrnt_fnt = self.txt_fnt["family"]
                self.crrnt_sze = int(self.txt_fnt["size"])
                self.crrnt_weight = self.txt_fnt["weight"]

                self.rgt_frame2 = cstk.CTkFrame(self.sttngs_win)
                self.rgt_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

                # Filling the font list
                for fnt in tk.font.families():
                    self.font_list.append(str(fnt))
                self.font_list.sort()
                # Filling the size list
                for n in range(2,81):
                    self.font_size.append(str(n))

                # Header
                self.lbl1 = cstk.CTkLabel(self.rgt_frame2, text="Text Font Settings", bg_color=self._from_rgb((43, 43, 43)))
                self.lbl1.place(x=120, y=5)

                def callback2(P):
                    global x
                    if str.isalpha(P):
                        if P in self.font_list:
                            x = self.font_list.index(P)
                            print(f"Encontrado: {P} en {x}")
                            self.update()
                        return True
                    elif P == "":
                        return True
                    else:
                        return False

                # Fonts
                self.font_list_frame1 = cstk.CTkFrame(self.rgt_frame2, height=6, bg_color=self._from_rgb((43, 43, 43)))
                self.font_list_frame1.place(x=5, y=35)
                self.lbl_fontlst = cstk.CTkLabel(self.font_list_frame1, text="Font", bg_color=self._from_rgb((43, 43, 43)))
                self.lbl_fontlst.pack(side=tk.TOP, fill=tk.X)
                self.fnt_vcmd = self.rgt_frame2.register(callback2)
                self.entry_fontlst = cstk.CTkEntry(self.font_list_frame1, corner_radius=0, border_width=0, border_color=None, bg_color="transparent", validate='key', validatecommand=(self.fnt_vcmd, '%P'))
                self.entry_fontlst.pack(side=tk.TOP, fill=tk.X)
                self.entry_fontlst.bind("<Return>", self.fnt_lst_chngslct)
                self.entry_fontlst.insert(tk.END, self.txt_fnt["family"])
                self.list_items = tk.StringVar(value=self.font_list)
                self.listbox = tk.Listbox(self.font_list_frame1, listvariable=self.list_items, height=6, bg=self._from_rgb((43, 43, 43)), fg=self._from_rgb((220, 228, 238)), border=None, borderwidth=0, selectbackground="red", selectmode=tk.SINGLE)
                self.listbox.pack(side=tk.LEFT, fill=tk.X)
                self.listbox.bind("<<ListboxSelect>>", self.fnt_lst_slct)
                self.listbox.select_set(self.font_list.index(self.txt_fnt["family"]))
                self.listbox.see(self.font_list.index(self.txt_fnt["family"]))
                self.scrlbarr = cstk.CTkScrollbar(self.font_list_frame1, command=self.listbox.yview, height=6)
                self.scrlbarr.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
                self.listbox.configure(yscrollcommand=self.scrlbarr.set)

                # Font Style
                self.font_style_frame1 = cstk.CTkFrame(self.rgt_frame2, height=6, bg_color=self._from_rgb((43, 43, 43)))
                self.font_style_frame1.place(x=200, y=35)
                self.lbl_fntstyl = cstk.CTkLabel(self.font_style_frame1, text="Font Style", bg_color=self._from_rgb((43, 43, 43)))
                self.lbl_fntstyl.pack(side=tk.TOP, fill=tk.X)
                self.font_style_cbbx = cstk.CTkOptionMenu(self.font_style_frame1, values=self.font_style, command=self.fnt_stl_slct)
                self.font_style_cbbx.pack(side=tk.TOP, fill=tk.X)
                self.font_style_cbbx.set("Normal")

                def callback(P):
                    if str.isdigit(P) or P == "":
                        return True
                    else:
                        return False

                # Font Size
                self.font_size_frame1 = cstk.CTkFrame(self.rgt_frame2, height=6, bg_color=self._from_rgb((43, 43, 43)))
                self.font_size_frame1.place(x=180, y=125)
                self.lbl_fntsze = cstk.CTkLabel(self.font_size_frame1, text="Font Size", bg_color=self._from_rgb((43, 43, 43)))
                self.lbl_fntsze.pack(side=tk.TOP, fill=tk.X)
                self.fnt_sze_frm = cstk.CTkFrame(self.font_size_frame1, height=6, bg_color=self._from_rgb((43, 43, 43)))
                self.fnt_sze_frm.pack(side=tk.TOP, fill=tk.X)
                self.vcmd = (self.rgt_frame2.register(callback))
                self.entry_fontsze = cstk.CTkEntry(self.fnt_sze_frm, corner_radius=0, border_width=0, border_color=None, bg_color="transparent", validate='all', validatecommand=(self.vcmd, '%P'))
                self.entry_fontsze.pack(side=tk.LEFT, fill=tk.BOTH)
                self.entry_fontsze.bind('<Return>', self.prvw_font)
                self.entry_fontsze.insert(tk.END, self.font_size[self.crrnt_sze-2])
                self.btns_fntsze_frm = cstk.CTkFrame(self.fnt_sze_frm, height=6, bg_color=self._from_rgb((43, 43, 43)))
                self.btns_fntsze_frm.pack(side=tk.LEFT, fill=tk.Y)
                self.btn_inc_fntsze = cstk.CTkButton(self.btns_fntsze_frm, text="+", height=8, width=8, fg_color=self._from_rgb((52, 54, 56)), hover_color="red", border_color="red", corner_radius=0, command=self.fntsze_inc)
                self.btn_inc_fntsze.pack(side=tk.LEFT, fill=tk.Y, padx=0, ipadx=2, pady=0, ipady=0)
                self.btn_dec_fntsze = cstk.CTkButton(self.btns_fntsze_frm, text="-", height=10, width=8, fg_color=self._from_rgb((52, 54, 56)), hover_color="red", border_color="red", corner_radius=0, command=self.fntsze_dec)
                self.btn_dec_fntsze.pack(side=tk.LEFT, fill=tk.Y, padx=0, ipadx=4, pady=0, ipady=0)

                # Sample
                self.lbl_smpl = cstk.CTkLabel(self.rgt_frame2, text="Sample", bg_color=self._from_rgb((43, 43, 43)))
                self.lbl_smpl.place(x=120, y=205)
                self.lbl_smpltxt = cstk.CTkLabel(self.rgt_frame2, text="AaBbYyZz", fg_color=self._from_rgb((52, 54, 56)), corner_radius=50)
                self.lbl_smpltxt.place(x=100, y=245)

                # Buttons
                self.btn_apply = cstk.CTkButton(self.rgt_frame2, text="        Apply        ", fg_color=self._from_rgb((52, 54, 56)), hover_color="red", border_color="red", corner_radius=60, width=4, height=20, command=self.chng_font)
                self.btn_apply.place(x=250, y=265)

                ######################
                # Settings Menu
                self.lft_frame1 = cstk.CTkFrame(self.sttngs_win)
                self.lft_frame1.pack(side=tk.RIGHT, fill=tk.BOTH, ipadx=0)

                self.lbl_settings = cstk.CTkLabel(self.lft_frame1, text="Settings", corner_radius=0, fg_color='transparent')
                self.lbl_settings.pack(side=tk.TOP, fill=tk.X)

                self.btn_gnrl = cstk.CTkButton(self.lft_frame1, text="General", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.gnrl_mnu, state='disabled')
                self.btn_gnrl.pack(side=tk.TOP, fill=tk.X, pady=(20,0))

                self.btn_systm = cstk.CTkButton(self.lft_frame1, text="System", corner_radius=20, fg_color='transparent', hover_color="red", border_color="red", command=self.systm_mnu)
                self.btn_systm.pack(side=tk.TOP, fill=tk.X, pady=(20,0))


                self.sttngs_win.grab_release()
        except:
            self.sttngs_win = cstk.CTkToplevel(self)
            self.sttngs_win.geometry("400x200")
            self.sttngs_win.resizable(False,False)
            self.sttngs_win.title("Settings")

                
            self.sttngs_win.grab_release()

    ####################
    # General Menu

    def fnt_lst_slct(self, e):
        """Changes the font family from the Listbox and call the preview font text function\n\n
            crrnt_fnt => Current Font Family selected"""
        if self.listbox.curselection():
            self.slct = self.listbox.curselection()[0]
            self.entry_fontlst.delete(0, tk.END)
            self.entry_fontlst.insert(0, self.font_list[self.slct])
            self.crrnt_fnt = self.font_list[self.slct]
            self.prvw_font()

    def fnt_lst_chngslct(self, e):
        """Changes the font family from the Entry and call the preview font text function\n\n
            x => index of the family font's list entered in the Entry\n
            crrnt_fnt => Current Font Family selected"""
        global x
        if self.entry_fontlst.get() in self.font_list:
            self.listbox.selection_clear(0, "end")
            self.listbox.select_set(x)
            self.listbox.see(x)
            self.crrnt_fnt = self.font_list[self.font_list.index(self.entry_fontlst.get())]
            self.prvw_font()

    def fnt_stl_slct(self, e):
        """Changes the font weight and call the preview font text function\n\n
            crrnt_weight => Current Font Weight selected"""
        self.crrnt_weight = e.lower()
        self.prvw_font()

    def fntsze_inc(self):
        """Button callback increment the font size and call the preview font text function\n\n
            crrnt_sze => Current Font Size selected"""

        if self.crrnt_sze >= 2:
            if self.crrnt_sze%2 == 0:
                self.crrnt_sze+= 2
            else:
                self.crrnt_sze+= 1
        self.entry_fontsze.delete(0, tk.END)
        self.entry_fontsze.insert(tk.END, self.crrnt_sze)
        self.update()
        self.prvw_font()

    def fntsze_dec(self):
        """Button callback decrement the font size and call the preview font text function\n\n
            crrnt_sze => Current Font Size selected"""

        if self.crrnt_sze >=3:
            if self.crrnt_sze%2 == 0:
                self.crrnt_sze-= 2
            else:
                self.crrnt_sze-= 1
        self.entry_fontsze.delete(0, tk.END)
        self.entry_fontsze.insert(tk.END, self.crrnt_sze)
        self.update()
        self.prvw_font()

    def prvw_font(self, e=None):
        """Display the preview text"""
        self.lbl_smpltxt.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.update()

    def chng_font(self):
        """Apply the changes of font text and save  it to config file"""
        print(f"Font: {self.crrnt_fnt} | Style: {self.crrnt_weight} | Size: {self.crrnt_sze}")
        self.txt_fnt["family"] = self.crrnt_fnt
        self.txt_fnt["size"] = str(self.crrnt_sze)
        self.txt_fnt["weight"] = self.crrnt_weight
        
        self.set_txtfnt(self.crrnt_fnt, self.crrnt_sze, self.crrnt_weight)
        self.update()

        with open(f"{self.config_path}", 'w') as conf:
            self.config_object.write(conf)

    def chng_font2(self):
        """Apply the changes of font settings and save  it to config file"""
        print(f"Font: {self.crrnt_fnt} | Style: {self.crrnt_weight} | Size: {self.crrnt_sze}")
        self.sys_fnt["family"] = self.crrnt_fnt
        self.sys_fnt["size"] = str(self.crrnt_sze)
        self.sys_fnt["weight"] = self.crrnt_weight
        self.lbl_settings.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.btn_gnrl.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.btn_systm.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.btn_apply.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.lbl_smpl.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.entry_fontsze.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.lbl_fntsze.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.font_style_cbbx.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.lbl_fntstyl.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.entry_fontlst.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.lbl_fontlst.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)
        self.lbl1.cget("font").configure(family=self.crrnt_fnt, size=int(self.crrnt_sze), weight=self.crrnt_weight)

        with open(f"{self.config_path}", 'w') as conf:
            self.config_object.write(conf)
        
        self.set_sysfnt(self.crrnt_fnt, self.crrnt_sze, self.crrnt_weight)
        self.update()

    #####################
    # System Menu

    def systm_mnu(self):
        self.crrnt_fnt = self.sys_fnt["family"]
        self.crrnt_sze = int(self.sys_fnt["size"])
        self.crrnt_weight = self.sys_fnt["weight"]
        self.prvw_font()
        self.lbl1.configure(text="System Font Settings")
        self.listbox.selection_clear(0, "end")
        self.listbox.select_set(self.font_list.index(self.sys_fnt["family"]))
        self.listbox.see(self.font_list.index(self.sys_fnt["family"]))
        self.entry_fontlst.delete(0, tk.END)
        self.entry_fontlst.insert(tk.END, self.sys_fnt["family"])
        self.font_style_cbbx.set(self.sys_fnt["weight"].capitalize())
        self.entry_fontsze.delete(0, tk.END)
        self.entry_fontsze.insert(tk.END, self.font_size[self.crrnt_sze-2])
        self.btn_apply.configure(command=self.chng_font2)
        self.btn_gnrl.configure(state='enabled')
        self.btn_gnrl.configure(command=self.gnrl_mnu)
        self.btn_systm.configure(state='disabled')
        self.update()

    def gnrl_mnu(self):
        self.crrnt_fnt = self.txt_fnt["family"]
        self.crrnt_sze = int(self.txt_fnt["size"])
        self.crrnt_weight = self.txt_fnt["weight"]
        self.prvw_font()
        self.lbl1.configure(text="Text Font Settings")
        self.listbox.selection_clear(0, "end")
        self.listbox.select_set(self.font_list.index(self.txt_fnt["family"]))
        self.listbox.see(self.font_list.index(self.txt_fnt["family"]))
        self.entry_fontlst.delete(0, tk.END)
        self.entry_fontlst.insert(tk.END, self.txt_fnt["family"])
        self.font_style_cbbx.set(self.txt_fnt["weight"].capitalize())
        self.entry_fontsze.delete(0, tk.END)
        self.entry_fontsze.insert(tk.END, self.font_size[self.crrnt_sze-2])
        self.btn_apply.configure(command=self.chng_font)
        self.btn_gnrl.configure(state='disabled')
        self.btn_systm.configure(state='enabled')
        self.btn_systm.configure(command=self.systm_mnu)
        self.update()

    def mn_about(self):
        """Display About Info in a TopLevel"""
        try:
            if tk.Toplevel.winfo_exists(self.about_win) == 0:
                self.about_win = cstk.CTkToplevel(self)
                self.about_win.geometry("400x200")
                self.about_win.resizable(False,False)
                self.about_win.title("About")
                self.about_win.iconbitmap(os.path.join(self.application_path, "note.ico"))

                self.lbl = cstk.CTkLabel(self.about_win, text="Product: NotePadX\nVersion: 0.9.9\nAuthor: Akkun\nDate Release: 06/01/2023\n\nThanks for using this software <3")
                self.lbl.pack(fill=tk.BOTH, expand=True)
                self.about_win.grab_release()
        except:
            self.about_win = cstk.CTkToplevel(self)
            self.about_win.geometry("400x200")
            self.about_win.resizable(False,False)
            self.about_win.title("About")

            self.lbl = cstk.CTkLabel(self.about_win, text="Product: NotePadX\nVersion: 0.9.9\nAuthor: Akkun\nDate Release: 06/01/2023\n\nThanks for using this software <3")
            self.lbl.pack(fill=tk.BOTH, expand=True)
            self.about_win.grab_release()

    ###################################
    # Other Functions
    def crt_cnfgfl(self):
        self.config_object = ConfigParser()

        self.config_object["FONT_TXTEDITOR"] = {
            "family": "Georgia",
            "size": "12",
            "weight": "normal"
        }
        self.config_object["FONT_SYS"] = {
            "family": "Georgia",
            "size": "12",
            "weight": "normal"
        }

        with open(f"{self.config_path}", 'w') as conf:
            self.config_object.write(conf)

    def load_cnfgfl(self):
        self.config_object = ConfigParser()
        self.config_object.read(f"{self.config_path}")
        self.txt_fnt = self.config_object["FONT_TXTEDITOR"]
        self.sys_fnt = self.config_object["FONT_SYS"]

    def set_sysfnt(self, font, size, weight="normal"):
        self.menu_lbl.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_file.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_open.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_save.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_saveas.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_close.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_edit.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_cut.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_copy.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_paste.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_undo.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_redo.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_settings.cget("font").configure(family=font, size=int(size), weight=weight)
        self.btn_about.cget("font").configure(family=font, size=int(size), weight=weight)

        self.update()

    def set_txtfnt(self, font, size, weight="normal"):
        self.txt_box.cget("font").configure(family=font, size=int(size), weight=weight)
        self.update()

    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'

if __name__ == "__main__":
    app = App()
    app.mainloop()
