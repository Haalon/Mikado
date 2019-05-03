import random as rnd
import math

"""
stick:
	[[x1, y1, r1],
	 [x2, y2, r2]]
"""


def _dist2(x1, y1, x2, y2):
	return (x1 - x2)**2 + (y1 - y2)**2


def _circleCollision(c1, c2):
	x1, y1, r1 = c1
	x2, y2, r2 = c2
	return _dist2(x1, y1, x2, y2) < (r1 + r2)**2


def _mixedCollision(circle, stick):
	c1, c2 = stick[0:2]

	return _circleCollision(c1, circle) or _circleCollision(c2, circle)


def _stickCollision(st1, st2):
	c1, c2 = st1[0:2]

	return _mixedCollision(c1, st2) or _mixedCollision(c2, st2)


class GameField:
	def __init__(self):
		self.newGame()		

	def newGame(self, size=512, sticksnum=24, rad_percent=0.015, line_percent=0.2, border_percent=0.2):
		self.__size = size
		self.__baserad = rad_percent * size
		self.__baselen = line_percent * size
		self.score = 0
		self.border = border_percent * size

		self.sticks = {}
		self.gameover = False
		self.collided = []
		self.victory = False

		self.sticksnum = sticksnum
		self.shuffleSticks(sticksnum)

	def createStick(self):
		x1 = rnd.uniform(self.border, self.__size - self.border)
		y1 = rnd.uniform(self.border, self.__size - self.border)

		P = rnd.random() * math.pi * 2

		x2 = self.__baselen * math.cos(P) + x1
		y2 = self.__baselen * math.sin(P) + y1
		return [[x1, y1, self.__baserad], [x2, y2, self.__baserad]]

	def shuffleSticks(self, num):
		self.sticks = {}

		i = 0
		while i < num:
			newstick = self.createStick()
			if not self.hasStickCollision(newstick):
				self.sticks['t' + str(i)] = newstick
				i += 1

	def isOutOfBorders(self, key):
		(x1, y1, _), (x2, y2, _) = self.sticks[key][0:2]
		b0 = self.border
		b1 = self.__size - self.border

		def inside(x, y):
			return b0 < x < b1 and b0 < y < b1

		return not (inside(x1, y1) or inside(x2, y2))

	def moveStick(self, key, delta):
		if self.gameover:
			return

		st = self.sticks[key]  # just an alias

		st[0][0] += delta[0]
		st[1][0] += delta[0]

		st[0][1] += delta[1]
		st[1][1] += delta[1]

		coll_flag = self.hasStickCollision(key)  # also key if collided
		out_flag = self.isOutOfBorders(key)

		if out_flag:
			self.sticks.pop(key)
			self.score += 100
			if len(self.sticks) == 0:
				self.victory = True
				self.score += 1000
				self.gameover = True

		if coll_flag:
			self.gameover = True
			self.collided = [coll_flag, key]

	def hasStickCollision(self, item):
		if isinstance(item, str):  # we assume it's a key
			for key, stick in self.sticks.items():
				if key == item:
					continue

				if _stickCollision(stick, self.sticks[item]):
					return key
		else:  # we assume it's a stick
			for stick in self.sticks.values():
				if _stickCollision(stick, item):
					return True

		return False
