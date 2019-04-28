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
	def __init__(self, size, sticksnum=24, rad_percent=0.02, line_percent=0.2):

		self.__size = size
		self.__baserad = rad_percent * size
		self.__baselen = line_percent * size
		self.sticks = {}
		self.shuffleSticks(sticksnum)

	def createStick(self):
			x1 = rnd.randint(self.__baselen, self.__size - self.__baselen)
			y1 = rnd.randint(self.__baselen, self.__size - self.__baselen)

			P = rnd.random() * math.pi * 2

			x2 = self.__baselen * math.cos(P) + x1
			y2 = self.__baselen * math.sin(P) + y1
			return [[x1,y1, self.__baserad], [x2,y2, self.__baserad]]		

	def shuffleSticks(self, num):
		for i in range(num):
			self.sticks['t'+ str(i)] = self.createStick()

	def moveStick(self, key, delta):
		st = self.sticks[key] #just an alias

		st[0][0] += delta[0]
		st[1][0] += delta[0]

		st[0][1] += delta[1]
		st[1][1] += delta[1]

	def hasCicrleCollision(self, circle):
		for stick in self.sticks.values():
			if _mixedCollision(circle, stick):
				return True

		return False

	def hasStickCollision(self, key):
		for i, stick in self.sticks.items():
			if i == key:
				continue

			if _stickCollision(stick, self.sticks[key]):
				return True

		return False


def _randomDot(minx=0, miny=0, maxx=1, maxy=1):
	return (rnd.uniform(minx, maxx), rnd.uniform(miny, maxy))
