"""Small helper functions, mostly for tkinter"""
import tkinter as tk


def set_col(widg, col):
	"""
	Recursively set color to widget and all of its children

	Args:
		widg (tkinter.Widget): widget to start from
		col (str): color to set, hex or a color name string

	Returns:
		None
	"""

	if not isinstance(widg, tk.Widget):
		return

	widg['bg'] = col
	for child in widg.winfo_children():
		set_col(child, col)


def grid_weight_configure(widg, row_val=1, col_val=1):
	"""
	Set default weights to all rows and columns for a grid layout

	Args:
		widg (tkinter.Widget): widget with a grid layout
		row_val (int or list(int)): default values for rows
		col_val (int or list(int)): default values for columns

	Returns:
		None
	"""
	if not isinstance(widg, tk.Widget):
		return

	for i in range(widg.size()[0]):
		if isinstance(col_val, list):
			widg.columnconfigure(i, weight=col_val[i])
		else:
			widg.columnconfigure(i, weight=col_val)

	for i in range(widg.size()[1]):
		if isinstance(row_val, list):
			widg.rowconfigure(i, weight=row_val[i])
		else:
			widg.rowconfigure(i, weight=row_val)
