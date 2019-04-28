from tkinter import *
import utils
from logic import GameField

GAME_SIZE = 800


class App(Frame):
	def __init__(self):
		super().__init__()
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.master.title("Mikado2D")
		self.master['padx'] = 10
		self.master['pady'] = 10
		self.grid(sticky="NESW")

		self.create()
		self.mainloop()

	def create(self):
		self.field = GameCanvas(self, bg='gray90')
		self.field.grid(row=0, column=0, rowspan=2, sticky="NESW", pady=3)

		self.stats = StatFrame(self)
		self.stats.grid(row=0, column=1, sticky="NESW", pady=3)

		self.controls = ControlFrame(self)
		self.controls.grid(row=1, column=1, sticky="NESW", pady=3)
		utils.grid_weight_configure(self, col_val=[1, 0])


class GameCanvas(Canvas, GameField):
	def __init__(self, *ap, **an):
		an['width'] = GAME_SIZE
		an['height'] = GAME_SIZE
		Canvas.__init__(self, *ap, **an)
		GameField.__init__(self, size=GAME_SIZE, canvas=self)


class StatFrame(Frame):
	def __init__(self, *ap, **an):
		super().__init__(*ap, **an)
		self['bg'] = 'gray70'
		self.create()

	def create(self):
		self.statLabel = Label(self, text='Stats', bg='gray70')
		self.statLabel.grid(sticky=N)
		utils.grid_weight_configure(self)


class ControlFrame(Frame):
	def __init__(self, *ap, **an):
		super().__init__(*ap, **an)
		self['bg'] = 'gray70'
		self.create()

	def newGame(self):
		pass

	def create(self):
		self.Quit = Button(self, text="Quit", highlightthickness=0, command=self.quit)
		self.Quit.grid(row=1, column=0, sticky="SWE", padx=5, pady=3)

		self.NewGame = Button(self, text="New Game", highlightthickness=0, command=self.newGame)
		self.NewGame.grid(row=0, column=0, sticky="SWE", padx=5, pady=3)
		utils.grid_weight_configure(self, row_val=[1, 0], col_val=1)


App()
