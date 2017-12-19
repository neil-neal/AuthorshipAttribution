#!/usr/bin/env python

'''
AuthorshipAttribution UI created by neil at 12/14/17 3:09 PM

Description:
user interface
'''

import glob
import os
import tkinter as tk

import attribute

def commandline():
    while True:
        try:
            authorA = input("first author (A): ")
            authorA = authorA.strip()
            if not len(authorA):
                authorA = 'A'

            while True:
                filenamesA = input("text files by author %s : "%(authorA))
                filesA = glob.glob(filenamesA)
                if len(filesA) > 0:
                    break
                else:
                    print('no files found by pathname %s. Try again'%filenamesA)

            authorB = input("second author (B): ")
            authorB = authorB.strip()
            if not len(authorB):
                authorB = 'B'

            while True:
                filenamesB = input("text files by author %s : "%(authorB))
                filesB = glob.glob(filenamesB)
                if len(filesB) > 0:
                    break
                else:
                    print('no files found by pathname %s. Try again'%filenamesB)

            author_files = {authorA:filesA, authorB:filesB}
            print("author files: %s"%author_files)

            print('learning about the styles of the authors...')
            aa = attribute.AuthorAttribute()
            aa.identify(author_files)

            while True:
                filenames = input("text files to be attributed among authors: ")
                files = glob.glob(filenames)
                if len(files) > 0:
                    break
                else:
                    print('no files found by pathname %s. Try again'%filenames)

            authors = aa.attribute(files)
            for file, author in authors.items():
                print("%s author by: %s" % (file, author))
            #print('author(s) identified: %s'%authors)

        except KeyboardInterrupt:
            print('Bye')
            break



class Frames(object):

    def __init__(self):
        self.aa = attribute.AuthorAttribute()
        self.relief = tk.RIDGE


    def find_texts(self, author_name, e_files, l_tx_fnd, t_files):
        filenames = e_files.get().strip()
        if not len(filenames):
            filenames = 'text/'
        if os.path.isdir(filenames):
            fl_fnd = tk.filedialog.askopenfilenames(initialdir = filenames)
            if len(fl_fnd):
                e_files.delete(0, tk.END)
                e_files.insert(tk.END, os.path.dirname(os.path.relpath(fl_fnd[0])))
        else:
            fl_fnd = glob.glob(filenames)
        l_tx_fnd['text'] = "%d text(s) by %s found:"%(len(fl_fnd), author_name)
        t_files.delete('1.0',tk.END)
        if len(fl_fnd):
            msg = '\n'.join([os.path.relpath(fl) for fl in fl_fnd])
            #msg = '\n'.join( fl_fnd)
            t_files.config(foreground='black')
        else:
            msg = "  no files found. Please change Text(s) pathname and try again"
            t_files.config(foreground='red')
        t_files.insert(tk.END, msg)
        self.change_learn_button_state()


    def change_learn_button_state(self):
        filesA = self.t_filesA.get('1.0', tk.END).strip()
        filesB = self.t_filesB.get('1.0', tk.END).strip()
        #print(len(filesA), len(filesB))
        if (filesA and filesB and 'no files found' not in filesA
                and 'no files found' not in filesB):
            self.b_learn.config(state='normal')
        else:
            self.b_learn.config(state='disabled')
            self.b_attribute.config(state='disabled')

    def learn_author_styles(self):
        #aa = attribute.AuthorAttribute() # reset aa
        fl_fndA = self.t_filesA.get('1.0', tk.END).split()
        fl_fndB = self.t_filesB.get('1.0', tk.END).split()
        author_files = {self.e_nameA.get(): fl_fndA, self.e_nameB.get(): fl_fndB}
        #print(len(fl_fndA), len(fl_fndB))
        self.aa.identify(author_files)
        self.b_attribute.config(state='normal')


    def determine_authors(self):
        filenames = self.e_files.get().strip()
        if not len(filenames):
            filenames = 'text/'
        if os.path.isdir(filenames):
            files = tk.filedialog.askopenfilenames(initialdir = filenames)
        else:
            files = glob.glob(filenames)
        if len(files):
            authors = self.aa.attribute(files)
            #out = ''
            self.t_files.delete('1.0', tk.END)
            for file, author in authors.items():
                out = "%s by: %s\n" % (os.path.basename(file), author)
                self.t_files.insert(tk.END, out)
        else:
            out = "  no files found. Please change Text(s) pathname and try again"
            self.t_files.insert(tk.END, out)


    def main_layout(self, root):
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # top level layout
        f_learn = tk.Frame(root, bd=2, relief=self.relief)
        f_learn.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        f_attribute = tk.Frame(root, bd=2, relief=self.relief)
        f_attribute.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        f_author1 = tk.Frame(f_learn, bd=1, relief=self.relief)
        f_author1.grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
        f_author2 = tk.Frame(f_learn, bd=1, relief=self.relief)
        f_author2.grid(row=1, pady=4, sticky=tk.N+tk.S+tk.E+tk.W)

        for x in range(10):
            tk.Grid.columnconfigure(f_learn, x, weight=1)
            tk.Grid.columnconfigure(f_attribute, x, weight=1)
        #    tk.Grid.columnconfigure(f_author1, x, weight=1)
        #    tk.Grid.columnconfigure(f_author2, x, weight=1)
        #    tk.Grid.columnconfigure(self.e_nameA, x, weight=1)

        for y in range(5):
            tk.Grid.rowconfigure(f_learn, y, weight=1)
            tk.Grid.columnconfigure(f_attribute, y, weight=1)
        #    tk.Grid.columnconfigure(f_author1, y, weight=1)
        #    tk.Grid.columnconfigure(f_author2, y, weight=1)
        #    tk.Grid.columnconfigure(self.e_nameB, x, weight=1)

        # author 1
        tk.Label(f_author1, text="Author A").grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
        tk.Label(f_author1, text="Name:", width=5).grid(row=1, sticky=tk.W)
        self.e_nameA = tk.Entry(f_author1, width=35)
        self.e_nameA.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.e_nameA.insert(10, "A. Hamilton")
        tk.Label(f_author1, text="Text(s):").grid(row=2, column=0, sticky=tk.W)
        e_filesA = tk.Entry(f_author1, width=35)
        e_filesA.grid(row=2, column=1)
        e_filesA.insert(10, "text/federalist_papers/*[0-9]_Hamilton")
        l_tx_fndA = tk.Label(f_author1, text="Text(s) found:")
        l_tx_fndA.grid(row=3, column=1, sticky=tk.W)
        self.t_filesA = tk.Text(f_author1, height=5, width=50)
        self.t_filesA.grid(row=4, column=0, columnspan=3)
        b_findA = tk.Button(f_author1, text='find', command=
            lambda: self.find_texts(self.e_nameA.get(), e_filesA, l_tx_fndA, self.t_filesA))
        b_findA.grid(row=3, column=0)

        # author 2
        tk.Label(f_author2, text="Author B").grid(row=0, sticky=tk.W)
        tk.Label(f_author2, text="Name:", width=5).grid(row=1, sticky=tk.W)
        self.e_nameB = tk.Entry(f_author2, width=35)
        self.e_nameB.grid(row=1, column=1)
        self.e_nameB.insert(10, "J. Madison")
        tk.Label(f_author2, text="Text(s):").grid(row=2, column=0, sticky=tk.W)
        e_filesB = tk.Entry(f_author2, width=35)
        e_filesB.grid(row=2, column=1)
        e_filesB.insert(10, "text/federalist_papers/*[0-9]_Madison")
        l_tx_fndB = tk.Label(f_author2, text="Text(s) found:")
        l_tx_fndB.grid(row=3, column=1, sticky=tk.W)
        self.t_filesB = tk.Text(f_author2, height=5, width=50)
        self.t_filesB.grid(row=4, column=0, columnspan=3)
        b_findB = tk.Button(f_author2, text='find', command=
            lambda: self.find_texts(self.e_nameB.get(), e_filesB, l_tx_fndB, self.t_filesB))
        b_findB.grid(row=3, column=0)

        self.b_learn= tk.Button(f_learn, text='Learn author styles', width=40
                           , command=self.learn_author_styles, state=tk.DISABLED)
        self.b_learn.grid(row=3, pady=4)

        # predict
        tk.Label(f_attribute, text="Text(s) of unknown author(s):").grid(row=0, sticky=tk.W)
        #tk.Label(f_attribute, text="Text(s)").grid(row=1, sticky=tk.W)
        self.e_files = tk.Entry(f_attribute, width=42)
        self.e_files.grid(row=1, column=0, padx=5)
        self.e_files.insert(10, "text/federalist_papers/*[0-9]_H_M")
        self.t_files = tk.Text(f_attribute, height=20, width=50)
        self.t_files.grid(row=3, column=0, columnspan=2,  sticky=tk.W)

        self.b_attribute = tk.Button(f_attribute, width=40 , command=self.determine_authors
                    , state=tk.DISABLED ,text='Find text(s), analyze style(s) and match with author(s)')
        self.b_attribute.grid(row=2, pady=4)



def TKUI():
    root = tk.Tk()
    root.title("Text Author Attribution")
    app = Frames()
    app.main_layout(root)
    root.mainloop()



def tester():
    authorA = 'hamilton'
    filenamesA = 'text/federalist_papers/*[0-9]_Hamilton'
    filesA = glob.glob(filenamesA)

    authorB = 'madison'
    filenamesB = 'text/federalist_papers/*[0-9]_Madison'
    filesB = glob.glob(filenamesB)

    author_files = {authorA: filesA, authorB: filesB}
    print("author files: ")
    for author, files in author_files.items():
        print("%d from %s"%(len(files), author))

    print('learning about the styles of the authors...')
    aa = attribute.AuthorAttribute()
    aa.identify(author_files)

    filenames = 'text/federalist_papers/*[0-9]_H_M'
    #filenames = 'text/federalist_papers/*[0-9]_Madison'
    files = glob.glob(filenames)

    authors = aa.attribute(files)
    for file, author in authors.items():
       print("%s authored by: %s"%(file, author))

    #print('author(s) identified: %s' % authors)
