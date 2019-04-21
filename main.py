from tkinter import *
import utils


class App(Frame):
	def __init__(self, master=None, Title="Mikado2D"):
		Frame.__init__(self, master)
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.master.title(Title)
		self.master['padx'] = 10
		self.master['pady'] = 10
		self.grid(sticky=N+E+S+W)
		self.create()
		utils.grid_weight_configure(self)

	def create(self):
		self.bQuit = Button(self, text='Quit', command=self.quit)
		self.bQuit.grid()
		
class Paint(Canvas):
	def __init__(self, master=None, *ap, foreground="black", **an):
		self.foreground = StringVar()
		self.foreground.set(foreground)
		Canvas.__init__(self, master, *ap, **an)


class CanvasFrame(App):
	def create(self):
		self.grid(rowspan=2)
		self.Canvas = Paint(self, foreground="midnightblue", bg='white')
		self.Canvas.grid(row=0, column=0, sticky=N+E+S+W)
	   

class StatFrame(App):
	def create(self):
		self['bg'] = 'gray70'
		self.statLabel = Label(self, text='Stats', bg='gray70')
		self.statLabel.grid(sticky=N)

		self.grid(row=0, column=1)

		
class ControlFrame(App):
	def create(self):
		self['bg'] = 'gray70'
		self.statLabel = Label(self, text='Controls', bg='gray70')
		self.statLabel.grid(sticky=N)

		self.grid(row=1, column=1)
		self.Quit = Button(self, text="Quit", highlightthickness=0, command=self.quit)
		self.Quit.grid(sticky=N+W+E, padx=5, pady=3)
		self.NewGame = Button(self, text="New Game", highlightthickness=0, command=self.quit)
		self.NewGame.grid(sticky=N+W+E, padx=5, pady=3)


app = CanvasFrame(Title="Canvas")
stat = StatFrame()
control = ControlFrame()
app.mainloop()