from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.messagebox import showerror
	
class MainFrame(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.master.title("Projekt-KI mainWindow")
		self.master.columnconfigure(5, weight = 1)
		self.master.rowconfigure(5, weight = 1)
		self.grid(sticky = (N,W,E,S))
	
		self.search = Button(self, text = "...", command = self.load_file, width = 3, height = 1)
		self.search.grid(column = 2, row = 2, sticky = W)
		
		searchEntry = StringVar()
		self.searchEntry = ttk.Entry(self, width = 30, textvariable=searchEntry)
		self.searchEntry.grid(column = 1, row = 2, sticky = W)
		
		ttk.Label(self, text = "File to analyse:").grid(column = 1, row = 1, sticky = W) 
		
	
	def load_file(self):
		fname = askopenfilename()
		
		if fname:
			try:
				print("""self.settings["template"].set(fname)""")
			except:
				showerror("Open Source File", "Failed to read file\n'%s'" % fname)
			return
			
if __name__ == "__main__":
	MainFrame().mainloop()
