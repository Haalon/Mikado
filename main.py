from tkinter import *
import utils

class App(Frame):
	def __init__(self, master=None, Title="Mikado2D"):
		super().__init__(master)
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.master.title(Title)
		self.master['padx'] = 10
		self.master['pady'] = 10
		self.grid(sticky=N+E+S+W)
		self.create()
		utils.grid_weight_configure(self, col_val = [1,0])
		self.mainloop()

	def create(self):
		self.field = Field(self)
		self.field.grid(row = 0, column = 0, rowspan = 2, sticky=N+E+S+W)

		self.stats = StatFrame(self)
		self.stats.grid(row = 0, column = 1, sticky=N+E+S+W)
		
		self.controls = ControlFrame(self)
		self.controls.grid(row = 1, column = 1, sticky=N+E+S+W)		
		

class Field(Canvas):
	def __init__(self, master=None, *ap, foreground="black", **an):
		Canvas.__init__(self, master, *ap, **an)


class StatFrame(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self['bg'] = 'gray70'
		self.create()
		utils.grid_weight_configure(self)

	def create(self):
		self.statLabel = Label(self, text='Stats', bg='gray70')
		self.statLabel.grid(sticky=N)

		
class ControlFrame(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self['bg'] = 'gray70'
		self.create()
		utils.grid_weight_configure(self, row_val = 0, col_val = 0)


	def create(self):
		self.Quit = Button(self, text="Quit", highlightthickness=0, command=self.quit)
		self.Quit.grid(sticky=S+W+E, padx=5, pady=3)
		self.NewGame = Button(self, text="New Game", highlightthickness=0, command=self.quit)
		self.NewGame.grid(sticky=S+W+E, padx=5, pady=3)


App()