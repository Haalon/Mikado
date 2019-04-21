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
		self.mainloop()

	def create(self):
		self.GameCanvas = GameCanvas(self, bg = 'gray90')
		self.GameCanvas.grid(row = 0, column = 0, rowspan = 2, sticky=N+E+S+W, pady=3)

		self.stats = StatFrame(self)
		self.stats.grid(row = 0, column = 1, sticky=N+E+S+W, pady=3)
		
		self.controls = ControlFrame(self)
		self.controls.grid(row = 1, column = 1, sticky=N+E+S+W, pady=3)		
		utils.grid_weight_configure(self, col_val = [1,0])
		

class GameCanvas(Canvas):
	def __init__(self, *ap,  **an):
		super().__init__( *ap, **an)


class StatFrame(Frame):
	def __init__(self, *ap,  **an):
		super().__init__(*ap,  **an)
		self['bg'] = 'gray70'
		self.create()
		

	def create(self):
		self.statLabel = Label(self, text='Stats', bg='gray70')
		self.statLabel.grid(sticky=N)
		utils.grid_weight_configure(self)

		
class ControlFrame(Frame):
	def __init__(self,  *ap,  **an):
		super().__init__( *ap,  **an)
		self['bg'] = 'gray70'
		self.create()	


	def create(self):
		self.Quit = Button(self, text="Quit", highlightthickness=0, command=self.quit)
		self.Quit.grid(row = 0, column = 0, sticky=S+W+E, padx=5, pady=3)

		self.NewGame = Button(self, text="New Game", highlightthickness=0, command=self.quit)
		self.NewGame.grid(row = 1, column = 0, sticky=S+W+E, padx=5, pady=3)
		utils.grid_weight_configure(self, row_val = [1,0], col_val = 1)
		
App()