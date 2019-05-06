from tkinter import *
import utils
from logic import *
from stickList import StickList
import gettext
import sys
import os.path
from tkinter import messagebox

GAME_SIZE = 512
RAD_SCALE = 0.015
BASE_COL = (255, 0, 0)  # light green, color of stick with value = 1
BASE_DELTA = 27  # hue shift for a stick with next value
BASE_SCALE = 0.75

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
		self.controls.newGame()
		self.update_labels()
		self.mainloop()

	def update_labels(self):
		self.master.title(_("Mikado2D"))
		self.field.scoreVar.set(_('Score: ') + str(self.field.score))
		self.controls.Quit['text'] = _("Quit")
		self.controls.NewGame['text'] = _("New Game")

	def create(self):
		self.top = Toplevel()
		self.top.title(_("Menu"))
		self.top.protocol("WM_DELETE_WINDOW", self.quit)

		self.field = GameCanvas(self)
		self.field.grid(row=1, column=0, sticky="NESW", pady=3)

		self.stats = StatFrame(self, self.field.scoreVar)
		self.stats.grid(row=0, column=0, sticky="NEW", pady=3)

		self.controls = ControlFrame(self.top, self.field)
		self.controls.grid(row=1, column=0, sticky="NEW", pady=3)
		utils.grid_weight_configure(self, col_val=[1, 0], row_val=[0, 1])


class GameCanvas(Canvas, GameField):
	def __init__(self, master):
		self.scoreVar = StringVar()

		Canvas.__init__(self, master, width=GAME_SIZE, height=GAME_SIZE)
		GameField.__init__(self)

		self.bind("<Button-1>", self.mouseDown)
		self.bind("<B1-Motion>", self.mouseMove)
		self.bind("<ButtonRelease-1>", self.mouseUp)
		self._tag = None

	def newGame(self, **an):
		try:
			super().newGame(**an)
			self.scoreVar.set(_('Score: ') + str(self.score))
			self.reDraw()
		except MyIterError:
			messagebox.showinfo(
				_("Error"),
				_("Could not create a valid game field.\n Try again, or reduce number of sticks or radius values")
			)

	def drawStick(self, stick, key, col='black'):
		x1, y1, r1 = stick[0]
		x2, y2, r2 = stick[1]

		self.create_line(x1, y1, x2, y2, tag=key, fill=col)
		self.create_oval(x1 - r1, y1 - r1, x1 + r1, y1 + r1, tag=key, fill=col)
		self.create_oval(x2 - r2, y2 - r2, x2 + r2, y2 + r2, tag=key, fill=col)

	def reDraw(self):
		self.delete("all")
		self.create_rectangle(
			self.border, self.border, GAME_SIZE - self.border,
			GAME_SIZE - self.border, fill='misty rose', outline='misty rose'
		)
		if self.victory:
			self['bg'] = 'pale green'
		else:
			self['bg'] = 'gray90'

		for key, stick in self.sticks.items():
			val = stick[2]
			stick_col_rgb = utils.shift_hue(BASE_COL, BASE_DELTA * (val - 1))

			stick_col_hex = utils.rgb_to_hex(stick_col_rgb)
			if key in self.collided:
				col = 'black'
			elif self._tag == key:
				stick_col_rgb = utils.scale_brightness(stick_col_rgb, BASE_SCALE)
				col = utils.rgb_to_hex(stick_col_rgb)
			else:
				col = stick_col_hex

			self.drawStick(stick, key, col=col)

	def mouseDown(self, event):
		self.x0, self.y0 = event.x, event.y
		index = self.find_closest(event.x, event.y)

		if index is None:
			self._tag = None
		else:
			tags = self.gettags(index)
			self._tag = tags[0] if len(tags) > 1 else None
			self.reDraw()

	def mouseMove(self, event):
		if self._tag is None:
			return

		if not self._tag in self.sticks:
			self._tag = None
			return

		delta = (event.x - self.x0, event.y - self.y0)
		self.x0, self.y0 = event.x, event.y
		self.moveStick(self._tag, delta)
		self.scoreVar.set(_('Score: ') + str(self.score))
		self.reDraw()

	def mouseUp(self, event):
		self._tag = None
		self.reDraw()


class StatFrame(Frame):
	def __init__(self, master, scoreVar):
		super().__init__(master)
		self.scoreVar = scoreVar
		self['bg'] = 'gray70'
		self.create()

	def create(self):
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
		self.field.newGame(types=self.stickTypes.get())

	def create(self):
		self.Quit = Button(self, highlightthickness=0, command=self.quit)
		self.Quit.grid(row=0, column=0, sticky="SWE", padx=5, pady=3)

		self.NewGame = Button(self, highlightthickness=0, command=self.newGame)
		self.NewGame.grid(row=0, column=1, sticky="SWE", padx=5, pady=3)

		self.stickTypes = StickList(self)
		self.stickTypes.grid(row=1, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)

		utils.grid_weight_configure(self, row_val=[0, 0, 0, 0], col_val=1)


App()
