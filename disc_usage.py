#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the week 11 warmup task 1 that crreates and modifieds two objects."""

import os
import datetime as datetime
import Tkinter as tk
import tkFileDialog
import ttk
import csv
import pickle


class SavePath(object):
    """ This class asks as an interface for savingn and retriving the latest
        starting directory.

    Attribtues:
    get_lastpath (method): Returns current value for the last starting path.

    get_start_path (method): Retrieves the saved starting path from the pickle
                            file for this class.

    set_start_path m(ethod): Save the pickle file for this class to preserve
                            the last used starting path.
    """
    __last_path = ""

    def __init__(self, pfdir='/home/vagrant/Public/', pfname='DULpath.pkl'):
        """ The constructor for the SavePath class.

        Args:
            pfdir (string): The name of the folder / directory that does or will
                            containe the class' pickle file.

            pfname (string): The name of the pickle file to be saved or loaded.

        Atritbutes:
            pfdir (string): The name of the folder / directory that does or will
                            containe the class' pickle file.

            pfname (string): The name of the pickle file to be saved or loaded.
        """
        self.__pfdir = pfdir
        self.__pfname = pfname

    def get_lastpath(self):
        """ Returns current value for the last starting path.

        Args:
            none.

        Returns:
            string: The full path and folder name of the lattest starting
                    directory.
        """
        return self.__last_path

    def get_start_path(self):
        """ Retrieves the saved starting path from the pickle file of this class

        Args:
            none.

        Returns:
            string: The full path and folder name of the lattest starting
                    directory.
        """
        prevpath = None
        pklfile = os.path.join(self.__pfdir, self.__pfname)

        if os.path.exists(pklfile):

            try:
                pfilesys = open(pklfile, 'rb')
                prevpath = pickle.load(pfilesys)

            except IOError:
                pass

            finally:
                pfilesys.close()

        self.__last_path = prevpath.get_lastpath() if prevpath is not None \
            else os.getcwd()

        return self.get_lastpath()

    def set_start_path(self, newpath):
        """ Saves the pickle file for this class to preserve the newly set
            latest starting path.

        Args:
            newpath (string): The full path and folder name of the lattest
                                starting directory.

        Returns:
            none.
        """
        self.__last_path = newpath

        pklfile = os.path.join(self.__pfdir, self.__pfname)

        try:
            pfilesys = open(pklfile, 'wb')
            pickle.dump(self, pfilesys)

        except IOError as ioe:
            print ioe

        else:
            pfilesys.close()


class DirSel(tk.Frame):
    """ This class provides the dialog setup and interacton to propmt for the
        starting directory to begin the data collection.

    Attributes:
        get_lastpath (method): Returns the directory path selected in the dialog

        set_lastpath (method): Sets the directory path selected in the dialog.

        select_dir (method): Performs the sub-dialog for the directory selection

        dialog_exit (method): Handles the exit and closing of the dialog.
    """
    __final_path = None

    def __init__(self, master, path=""):
        """ Constructor for the Dirsel directory selection dialog class.

        Args:
            master (Tk): tkinter window to build the dialog.

            path (string): the current statring directory path.

        Attributes:
            dialog_ended (bool): indicates if the dialog was ended (Quit).

            mainwin (tk): main window for dialog.

            dirframe (tk.LabelFrame): Frame for directory field.

            pathfld (tk.Label): Label field to display selected directory.

            btnframe (tk.LabelFrame): Frame to contain action Buttons.

            brwsbtn (tk.Button): Button for directory browse command.

            strtbtn (tk.Button): Button to start directory processing.

            quitbtn (tk.Button): Button to quit (exit) the dialog.

            msgfield (tk.Label): Label field to display messages.
        """
        self.dialog_ended = True
        tk.Frame.__init__(self, master)
        self.__final_path = path            # save starting path
        self.mainwin = master
        master.title('Disc Usage Analyzer')
        master.rowconfigure(0, weight=1)     # set window row as adjustable
        master.columnconfigure(0, weight=1)  # set window column as adjustable

        self.rowconfigure(0, weight=1)      # set this frame row as adjustable
        self.columnconfigure(0, weight=1)   # set this frame column adjustable
        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)   # stick frame to window

#       create frame for the starting directory
        self.dirframe = tk.LabelFrame(self, text='Current Starting Directory')
        self.columnconfigure(0, minsize=max(len(path),
                                            len(self.dirframe.cget('text')),
                                            len(master.title())+10))
        self.dirframe.grid(column=0)
        self.pathfld = tk.Label(self, text=self.__final_path)
        self.pathfld.grid(in_=self.dirframe)

#       create frame for action buttons and the buttons
        self.btnframe = tk.Frame(self)
        self.btnframe.grid(column=0)
        self.brwsbtn = tk.Button(self, text='Browse', relief=tk.RAISED,
                                 command=self.select_dir)
        self.brwsbtn.grid(in_=self.btnframe, row=0, column=0)
        self.strtbtn = tk.Button(self, text='Start', relief=tk.RAISED,
                                 command=lambda: self.dialog_exit(False))
        self.strtbtn.grid(in_=self.btnframe, row=0, column=1)
        self.quitbtn = tk.Button(self, text='Quit', relief=tk.RAISED,
                                 command=lambda: self.dialog_exit(True))
        self.quitbtn.grid(in_=self.btnframe, row=0, column=2)

        self.msgfield = tk.Label(self, text="")     # Message field
        self.msgfield.grid(row=2)

    def get_lastpath(self):
        """ Returns current value for the last starting path.

        Args:
            none.

        Returns:
            string: The full path and folder name of the lattest starting
                    directory.
        """
        return self.__final_path

    def set_lastpath(self, path):
        """ Sets the current value for the lastest starting path.

        Args:
            path (string): The full path and folder name of the lattest starting
                            directory.

        Returns:
            none.
        """
        self.__final_path = path

    def select_dir(self):
        """ Performs the sub-dialog for the directory selection.

        Args:
            none.

        Returns:
            string: The full path and folder name of the selected starting
                    directory.
        """
        prmtwin = tk.Toplevel()                   # create dialog window
        prmtwin.title('Select Starting Directory')
        dirsel = tkFileDialog.askdirectory(parent=prmtwin,
                                           initialdir=self.get_lastpath(),
                                           mustexist=True)
        prmtwin.destroy()
        if dirsel != '':                # if directory selected, save and set
            self.set_lastpath(dirsel)
            self.pathfld['text'] = dirsel

    def dialog_exit(self, ended):
        """ Handles the exit and closing of the dialog.

        Args:
            ended (bool): Indicates if the dialog is ended (True) or exiting to
                            perform the analysis (False).

        Returns:
            none.
        """
        if not ended:
            self.msgfield['text'] = 'Processing Directory'

        self.dialog_ended = ended
        self.mainwin.quit()


class DirList(tk.Frame):
    """ Directory analysis and sub-tree list processing and display dialog class

    Attributes:
        Action_CSV, Action_Del, Action_Move (int): Dialog action indicator
                                                    values.
        process_directory (method): Processes subdirectories and files.

        tree_selected (method): Processes the selected items in the treeview to
                                record the selection.

        set_select (method): Set the selection status for the given folder or
                                file.

        selected_list (method): Returns the list of keys (tree line identifiers)
                                that were marked for selection.

        perform_action (method): Processes the selected dialog action (invoked
                                    from Process button)

        prompt_target (method): Performs dialog to prompt for the target file
                                for the CSV or directory to recieve moved files.

        generate_csv (method): Generates a CSV file with the information for the
                                selected folders and files.
    """
    Action_CSV = 1
    Action_Del = 2
    Action_Move = 3

    def __init__(self, path, treemap):
        """ Constructor for the directory list treeview dialog execution class.

        Args:
            path (string): The starting (high-level) folder path.

            treemap (dict): Dictionary for maping entries to the treeview and
                            save collected file information.

        Attributes:
            treemap (dict): Dictionary for maping entries to the treeview and
                            save collected file information.

            listwin (Tk): Identification of parent window.

            selcheck (tk.PhotoImage): The check mark image for marking selected
                                        items.

            actionvar (tk.IntVar): The integer value of the selected action
                                    radio button.

            tree (ttk.Treeview): The Treeview widget for the directory tree.

            selbtn (tk.Button): The Select command Button widget.

            rbframe (tk.Frame): The display Frame to contain the action Radio
                                Button widgets.

            csvbtn (tk.Radiobutton): The CSV file action option Radio Button.

            delbtn (tk.Radiobutton): The delete files action option Radio Button

            movbtn (tk.Radiobutton): The move files action option Radio Button.

            actbtn (tk.Button): The action invocation command Button

            quitbtn (tk.Button): The command Button to Quit the dialog

            msglabel (tk.Label): A Label widget for displaying status and error
                                    message text.
        """
        self.treemap = treemap
        self.listwin = tk.Toplevel()        # create dialog window
        tk.Frame.__init__(self, self.listwin)
        self.listwin.title('Directory and File Information')

#       Create special values
        self.selcheck = tk.PhotoImage(file='check.png')     # check mark image
        self.actionvar = tk.IntVar()                    # action value
        self.actionvar.set(self.Action_CSV)             # set default action

#       Define directory tree (Treeview) display widget
        self.tree = ttk.Treeview(self, columns=('Count, Size'))
        self.tree.grid(row=0, column=0)

#       Define virtical and horizontal scroll bars for treeview
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

#       Configure Treeview display columns and headers
        self.tree.column('#0', anchor='w', width=300)
        self.tree.heading('#0', text='Path', anchor='w')

        self.tree.heading('#1', text='Count', anchor='center')
        self.tree.column('#1', anchor='e', width=100)

        self.tree.column('#2', anchor='e', width=100)
        self.tree.heading('#2', text='Size (kb)', anchor='center')

        self.selbtn = tk.Button(self, text='Select', relief=tk.RAISED,
                                command=self.tree_selected)
        self.selbtn.grid(row=2, column=0)

#       create frame for action buttons and the buttons
        self.rbframe = tk.Frame(self)
        self.rbframe.grid(row=3, column=0)

        self.csvbtn = tk.Radiobutton(self, text='Create CSV', relief=tk.FLAT,
                                     variable=self.actionvar,
                                     value=self.Action_CSV)
        self.csvbtn.grid(in_=self.rbframe, row=0, column=0)
        self.delbtn = tk.Radiobutton(self, text='Delete', relief=tk.FLAT,
                                     variable=self.actionvar,
                                     state=tk.DISABLED,
                                     value=self.Action_Del)
        self.delbtn.grid(in_=self.rbframe, row=0, column=1)
        self.movbtn = tk.Radiobutton(self, text='Move', relief=tk.FLAT,
                                     variable=self.actionvar,
                                     state=tk.DISABLED,
                                     value=self.Action_Move)
        self.movbtn.grid(in_=self.rbframe, row=0, column=2)

#       Define comnmand button for Processing the selected action
        self.actbtn = tk.Button(self, text='Perform', relief=tk.RAISED,
                                state=tk.DISABLED,
                                command=self.perform_action)
        self.actbtn.grid(row=4, column=0)
#       Define Quit command button
        self.quitbtn = tk.Button(self, text='Quit', relief=tk.RAISED,
                                 command=self.listwin.destroy)
        self.quitbtn.grid(row=4, column=2)

        self.msglabel = tk.Label(self, text='')     # Message field
        self.msglabel.grid(row=5, column=0)
        self.grid()

        startpath = os.path.abspath(path)       # set starting directory path
#       Add starting directory to sttar of display
        root_node = self.tree.insert('', 'end', text=startpath, open=True)
        self.treemap[root_node] = {'path': startpath, 'content': [],
                                   'Folder': ''}
#       Start processing of files and sub-folders
        self.tree.item(root_node,
                       value=self.process_directory(root_node, startpath))

        self.mainloop()

    def process_directory(self, parent, path):
        """ Process the information for the given directory and its files and
            sub-folders.

        Args:
            parent (string): Treeview (and dict) entry key.

            path (string): Full path name for this folder.

        Returns:
            (tuple): A pair of integers representing the count of files and the
                        total size of files in the folder and all sub-folders.
        """
        dirsize = 0
        dircount = 0

        for fname in os.listdir(path):      # Process all flies and sub-folder

            fullname = os.path.join(path, fname)
            isdir = os.path.isdir(fullname)
            fsize = int(os.path.getsize(fullname)/1024)

            treeid = self.tree.insert(parent, 'end', text=fname, open=False)
            self.treemap[parent]['content'].append(treeid)

#           Save information for the file or sub-folders
            if isdir:
                self.treemap[treeid] = {'Path': path, 'Folder': fname,
                                        'content': []}
                dirinfo = self.process_directory(treeid, fullname)
                dircount += 1
            else:
                self.treemap[treeid] = {'Path': path, 'FileName': fname}
                dirinfo = (1, fsize)

            self.treemap[treeid]['FileSize'] = dirinfo[1]
            self.treemap[treeid]['FileCreate'] = \
                datetime.datetime.fromtimestamp(os.path.getctime(fullname))
            self.treemap[treeid]['FileModify'] = \
                datetime.datetime.fromtimestamp(os.path.getmtime(fullname))

#           Add file or sub-folder to treeview
            self.tree.item(treeid, value=('{0:12d}'.format(dirinfo[0]),
                                          '{0:12d}'.format(dirinfo[1])))
            dircount += dirinfo[0]
            dirsize += dirinfo[1]

        return (dircount, dirsize)

    def tree_selected(self):
        """ Processes the selected items in the treeview to record the selection

        Args:
            none.

        Returns:
            none.
        """
        slist = self.tree.selection()
        for item in slist:
            self.set_select(item, 'flip')

        self.tree.selection('toggle', slist)

        selcount = len(self.selected_list())
        self.msglabel['text'] = 'Items selected: {0:5d}'.format(selcount)
        progstate = tk.NORMAL if selcount > 0 else tk.DISABLED
        self.actbtn.configure(state=progstate)

    def set_select(self, item, newstate):
        """ Set the selection status for the given file or folder and all of its
            files and sub-folders.

        Args:
            item (string): Treeview (and dict) entry key.

            newstate (mixed): String of 'flip' to switch item's selection state
                                or the image to be assigned.

        Returns:
            none.
        """
        newimg = newstate

        if newstate == 'flip':
            newimg = '' if self.tree.item(item, 'image') != '' \
                     else self.selcheck

        self.tree.item(item, image=newimg)

        if 'Folder' in self.treemap[item]:

            for subitem in self.treemap[item]['content']:
                self.set_select(subitem, newimg)

    def selected_list(self):
        """ Returns the list of keys (tree line identifiers) that were marked
            for selection.

        Args:
            none.

        Returns:
            (list): List of tree and dict item keys that were selected.
        """
        return [ik for ik in self.treemap.iterkeys()
                if self.tree.item(ik, 'image') != ""]

    def perform_action(self):
        """ Processes the selected dialog action (invoked from Process button).

            *** NOTE: due to time constranits, the Move and Delete actions are
                        not yet implemented.
        Args:
            none.

        Returns:
            none.
        """
        action_list = self.selected_list()
        action_num = self.actionvar.get()
        action_name = {self.Action_CSV: 'CSV File',
                       self.Action_Del: 'Delete files',
                       self.Action_Move: 'Move files'}[action_num]

        if action_num != self.Action_Del:
            fldopt = action_num == self.Action_Move
            target_name = self.prompt_target(folder=fldopt, action=action_name)

            if target_name is None:
                return
            else:
                target_fname = os.path.abspath(target_name)

            if action_num == self.Action_CSV:
                self.generate_csv(target_fname, action_list)

            elif action_num == self.Action_Move:
                pass    # self.do_move_files(target_fname, action_list)

        else:
            pass    # self.do_delete_files(action_list)

    def prompt_target(self, folder=False, action='Unknown'):
        """ Performs dialog to prompt for the target file for the CSV or
            directory to recieve moved files.

        Args:
            folder (bool): Indicates if the prompt dialog will be for a target
                            directory (True) for file moves, or for a (CSV) file
                            (False) to recieve the CSV formatted file and folder
                            information.

            action (string): Name of the action the target is being prompted for

        Returns:
            none.
        """
        prmtwin = tk.Toplevel()         # create dialog window
        prmtwin.title('Select Target for ' + action)

        if folder:
            fselect = tkFileDialog.askdirectory(parent=prmtwin,
                                                initialdir=os.getcwd(),
                                                mustexist=True)
        else:
            filetypes = [('CSV files', '.csv'), ('all files', '.*')]
            fselect = tkFileDialog.asksaveasfilename(parent=prmtwin,
                                                     initialdir=os.getcwd(),
                                                     defaultextension='.csv',
                                                     filetypes=filetypes)
        prmtwin.destroy()

        if fselect == '':
            return None

        return fselect

    def generate_csv(self, csvfile, sellist):
        """ Generates a CSV file with the information for the selected folders
            and files.

        Args:
            csvfile (string): The full (abspath) name for the target file to
                                receive the CSV data.

            sellist (list): The list of item keys to be processed for the CSV
                            data generation.

        Returns:
            none.
        """
        try:
            csvfs = open(csvfile, 'w')
            field_order = ['Path', 'Folder', 'FileName', 'FileSize',
                           'FileCreate', 'FileModify']
            csvwtr = csv.DictWriter(csvfs, field_order, restval='',
                                    extrasaction='ignore',
                                    quoting=csv.QUOTE_NONNUMERIC)
            csvwtr.writeheader()

            for item in sellist:
                csvwtr.writerow(self.treemap[item])

        except IOError as ioerr:
            self.msglabel['text'] = 'Error writing CSV file: ' + ioerr.strerror

        finally:
            try:
                csvfs.close()
            except IOError:
                pass


#   Start of main section
LASTPATH = SavePath()               # get directory last specified
PRIMEWIN = tk.Tk()                  # create dialog interface
DSEL = DirSel(PRIMEWIN, path=LASTPATH.get_start_path())  # prompt for directory

while True:
    DSEL.msgfield['text'] = ''      # clear any previous message
    DSEL.mainloop()
    LASTPATH.set_start_path(DSEL.get_lastpath())    # Save the latest directory

    if DSEL.dialog_ended:
        break

    TREE_DICT = {}                  # clear the file info dictionary
    DIRDIALOG = DirList(LASTPATH.get_start_path(), TREE_DICT)  # start dialog

PRIMEWIN.destroy()
