from tkinter import *
import utils
from logic import GameField
import gettext
import sys
import os.path

GAME_SIZE = 512
RAD_SCALE = 0.015

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

	def create(self):
		self.top = Toplevel()
		self.top.title("Menu")

		self.field = GameCanvas(self)
		self.field.grid(row=0, column=0, sticky="NESW", pady=3)

		self.stats = StatFrame(self.top, self.field.scoreVar)
		self.stats.grid(row=0, column=0, sticky="NEW", pady=3)

		self.controls = ControlFrame(self.top, self.field)
		self.controls.grid(row=1, column=0, sticky="NEW", pady=3)
		utils.grid_weight_configure(self, col_val=[1, 0], row_val=[0,1])


class GameCanvas(Canvas, GameField):
	def __init__(self, master):
		self.scoreVar = StringVar()

		Canvas.__init__(self, master, width=GAME_SIZE, height=GAME_SIZE)
		GameField.__init__(self)

		self.bind("<Button-1>", self.mouseDown)
		self.bind("<B1-Motion>", self.mouseMove)
		self.bind("<ButtonRelease-1>", self.mouseUp)
		self._tag = None

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
		self.create_rectangle(self.border, self.border, GAME_SIZE - self.border,
			GAME_SIZE - self.border, fill='misty rose', outline='misty rose')
		if self.victory:
			self['bg'] = 'pale green'
		else:
			self['bg'] = 'gray90'

		for key, stick in self.sticks.items():
			if key in self.collided:
				col = 'red'
			elif self._tag == key:
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
		self.scoreVar.set('Score: ' + str(self.score))
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

class StickSettings(Frame):	
	event = '<<Changed>>'
	del_event = '<<Deleted>>'

	def __init__(self, master, id):
		self.id = id
		self.root = master
		super().__init__(master)
		self['bd'] = 2
		self['relief'] ='ridge'
		self.create()

	def get(self):
		return (self.num, self.rad)

	def setNum(self, event):
		self.num = self.numScale.get()
		self.root.event_generate(self.event)
		
	def setRad(self, event):
		self.rad = self.radScale.get()
		self.root.event_generate(self.event)

	def delete(self):
		self.root.event_generate(self.del_event, state=self.id)

	def create(self):
		self.delBtn = Button(self, text='X', command=self.delete)
		self.delBtn.grid(row=0, column=0, sticky='w', padx=5, pady=3)

		self.numScale = Scale(self, from_=10, to=100, orient=HORIZONTAL)
		self.numScale.grid(row=0, column=1, sticky='swe', padx=5, pady=3)
		self.numScale.bind("<ButtonRelease-1>", self.setNum)

		self.radScale = Scale(self, from_=1, to=4, orient=HORIZONTAL, resolution=0.25)
		self.radScale.grid(row=0, column=2, sticky='swe', padx=5, pady=3)
		self.radScale.bind("<B1-Motion>", self.setRad)

class StickList(Frame):
	def __init__(self, master):
		super().__init__(master)
		self['bd'] = 2
		self['relief'] = 'ridge'

		self.stickList = []
		self.create()

		self.bind(StickSettings.del_event, self.elemDelete)
		self.add()		

	def elemDelete(self, event):
		elem = self.stickList.pop(event.state)
		elem.destroy()
		self.replace()

	def replace(self):
		for elem in self.stickList:
			elem.grid_forget()

		for i, elem in enumerate(self.stickList):
			elem.grid(row=i+1, column=0, columnspan=2, sticky='we', pady=3)
			elem.id = i # compensate the shift from deleted items

	def add(self):
		newid = len(self.stickList)
		elem = StickSettings(self, newid)
		self.stickList.append(elem)
		self.replace()

	def clear(self):
		while self.stickList:
			elem = self.stickList.pop()
			elem.destroy()

	def create(self):
		self.addBtn = Button(self, text='Add', command=self.add)
		self.addBtn.grid(row=0, column=0, sticky='w', padx=5, pady=3)

		self.clrBtn = Button(self, text='Clear', command=self.clear)
		self.clrBtn.grid(row=0, column=1, sticky='e', padx=5, pady=3)

		# self.stickFrame = Frame(self)
		# self.stickFrame.grid(row=1, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)


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

	def create(self):
		self.Quit = Button(self, highlightthickness=0, command=self.quit)
		self.Quit.grid(row=0, column=0, sticky="SWE", padx=5, pady=3)

		self.NewGame = Button(self, highlightthickness=0, command=self.newGame)
		self.NewGame.grid(row=0, column=1, sticky="SWE", padx=5, pady=3)

		self.test = StickList(self)
		self.test.grid(row=1, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)

		utils.grid_weight_configure(self, row_val=[0, 0, 0, 0], col_val=1)


App()
