from tkinter import *
import utils
from logic import GameField
import gettext
import sys
import os.path

GAME_SIZE = 512

datapath = os.path.dirname(sys.argv[0])
gettext.install('app', datapath)

class App(Frame):
	def __init__(self):
		super().__init__()
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)


		self.master['padx'] = 10
		self.master['pady'] = 10
		self.grid(sticky="NESW")

		self.create()

		self.update_labels()
		self.mainloop()

	def update_labels(self):
	    self.master.title(_("Mikado2D"))
	    self.field.scoreVar.set(_('Score: ') + str(self.field.score))
	    self.controls.Quit['text'] = _("Quit")
	    self.controls.NewGame['text'] = _("New Game")
	    self.controls.difLabel['text'] = _("Difficulty: ")

	def create(self):
		self.field = GameCanvas(self)
		self.field.grid(row=0, column=0, rowspan=2, sticky="NESW", pady=3)

		self.stats = StatFrame(self, self.field.scoreVar)
		self.stats.grid(row=0, column=1, sticky="NESW", pady=3)

		self.controls = ControlFrame(self, self.field)
		self.controls.grid(row=1, column=1, sticky="NESW", pady=3)
		utils.grid_weight_configure(self, col_val=[1, 0])


class GameCanvas(Canvas, GameField):
	def __init__(self, master):
		self.scoreVar = StringVar()

		Canvas.__init__(self, master, width=GAME_SIZE, height=GAME_SIZE)
		GameField.__init__(self)

		self.bind("<Button-1>", self.mouseDown)
		self.bind("<B1-Motion>", self.mouseMove)
		self.bind("<ButtonRelease-1>", self.mouseUp)
		
		self.reDraw()

	def newGame(self, **an):
		super().newGame(**an)
		self.scoreVar.set(_('Score: ') + str(self.score))

	def drawStick(self, stick, key, col='black'):
		x1, y1, r1 = stick[0]
		x2, y2, r2 = stick[1]

		self.create_line(x1, y1, x2, y2, tag=key, fill=col)
		self.create_oval(x1 - r1, y1 - r1, x1 + r1, y1 + r1, tag=key, fill=col)
		self.create_oval(x2 - r2, y2 - r2, x2 + r2, y2 + r2, tag=key, fill=col)

	def reDraw(self):
		self.delete("all")
		self.create_rectangle(self.border, self.border, GAME_SIZE - self.border, GAME_SIZE -self.border, fill='misty rose', outline='misty rose')
		if self.victory:
			self['bg'] = 'pale green'
		else:
			self['bg'] = 'gray90'

		for key, stick in self.sticks.items():
			if key in self.collided:
				col = 'red'
			elif key in self.solved:
				col = 'sky blue'
			else:
				col = 'black'

			self.drawStick(stick, key, col=col)

	def mouseDown(self, event):
		self.x0, self.y0 = event.x, event.y
		index = self.find_closest(event.x, event.y)

		if index is None:
			self._tag = None
		else:
			tags = self.gettags(index)
			self._tag = tags[0] if len(tags) > 1 else None
			

	def mouseMove(self, event):
		if self._tag is None:
			return

		delta = (event.x - self.x0, event.y - self.y0)
		self.x0, self.y0 = event.x, event.y
		self.moveStick(self._tag, delta)
		self.scoreVar.set('Score: ' + str(self.score))
		self.reDraw()

	def mouseUp(self, event):
		self._tag = None


class StatFrame(Frame):
	def __init__(self, master, scoreVar):
		super().__init__(master)
		self.scoreVar = scoreVar
		self['bg'] = 'gray70'
		self.create()

	def create(self):
		self.statLabel = Label(self, text=_('Stats'), bg='gray70')
		self.statLabel.grid(row=0, sticky=N)

		self.scoreLabel = Label(self, textvariable=self.scoreVar, bg='gray70')
		self.scoreLabel.grid(row=1, sticky=N)

		utils.grid_weight_configure(self, row_val=0)


class ControlFrame(Frame):
	def __init__(self, master, field):
		self.field = field
		super().__init__(master)
		self['bg'] = 'gray70'
		self.create()
		self.settings = {}

	def newGame(self):
		self.field.newGame(**self.settings)
		self.field.reDraw()

	def difficulty(self, event):
		num = self.difText.get('1.0', 'end-1c')
		if num and int(num) < 100:
			self.settings['sticksnum'] = int(self.difText.get('1.0', 'end-1c'))
			self.newGame()
		self.difText.edit_modified(False)

	def create(self):
		self.Quit = Button(self, highlightthickness=0, command=self.quit)
		self.Quit.grid(row=2, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)

		self.NewGame = Button(self, highlightthickness=0, command=self.newGame)
		self.NewGame.grid(row=0, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)

		self.difLabel = Label(self, bg='gray70')
		self.difLabel.grid(row=1, column=0, sticky="SWE", padx=5, pady=3)

		self.difText = Text(self, height=1, width=3)
		self.difText.grid(row=1, column=1, sticky='swe', padx=5, pady=3)
		self.difText.bind('<<Modified>>', self.difficulty)

		utils.grid_weight_configure(self, row_val=[0, 0, 0], col_val=1)


App()
