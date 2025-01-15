import tkinter as tk

root = tk.Tk()

v = tk.IntVar()
v.set(1)  # initializing the choice, i.e. Python

languages = [("Python", 101),
   	     ("Perl", 102),
    	     ("Java", 103),
             ("C++", 104),
             ("C", 105)]

def ShowChoice():
    print(v.get())

tk.Label(root, 
         text="""Choose your favourite 
programming language:""",
         justify = tk.LEFT,
         padx = 20).pack()

for language, val in languages:
    tk.Radiobutton(root, 
                   text=language,
                   padx = 20, 
                   variable=v, 
                   command=ShowChoice,
                   value=val).pack(anchor=tk.W)


root.mainloop()