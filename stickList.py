from tkinter import *


class StickSettings(Frame):
	del_event = '<<Deleted>>'

	def __init__(self, master, id):
		self.id = id
		self.root = master
		super().__init__(master)
		self['bd'] = 2
		self['relief'] = 'ridge'
		self.create()

	def get(self):
		return (self.numScale.get(), self.radScale.get())

	def delete(self):
		self.root.event_generate(self.del_event, state=self.id)

	def create(self):
		self.delBtn = Button(self, text='X', command=self.delete)
		self.delBtn.grid(row=0, column=0, sticky='w', padx=5, pady=3)

		self.numScale = Scale(self, from_=1, to=300, orient=HORIZONTAL, label=_("Number"), length=200)
		self.numScale.grid(row=0, column=1, sticky='swe', padx=5, pady=3)
		self.numScale.set(24)

		self.radScale = Scale(self, from_=1, to=4, orient=HORIZONTAL, resolution=0.25, label=_("Radius"), digits=3)

		self.radScale.grid(row=0, column=2, sticky='swe', padx=5, pady=3)
		self.radScale.set(2)


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

	def get(self):
		sticks_types = []
		for elem in self.stickList:
			stype = elem.get()
			sticks_types.append(stype)

		return sticks_types

	def replace(self):
		for elem in self.stickList:
			elem.grid_forget()

		for i, elem in enumerate(self.stickList):
			elem.grid(row=i + 1, column=0, columnspan=2, sticky='we', pady=3)
			elem.id = i  # compensate the shift from deleted items

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
		self.addBtn = Button(self, text=_('Add'), command=self.add)
		self.addBtn.grid(row=0, column=0, sticky='w', padx=5, pady=3)

		self.clrBtn = Button(self, text=_('Clear'), command=self.clear)
		self.clrBtn.grid(row=0, column=1, sticky='e', padx=5, pady=3)

		# self.stickFrame = Frame(self)
		# self.stickFrame.grid(row=1, column=0, columnspan=2, sticky="SWE", padx=5, pady=3)
