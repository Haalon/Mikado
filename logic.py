import random as rnd

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
	def __init__(self, size, sticksnum = 24, rad_percent=0.02, line_percent = 0.2):

		self.__size = size
		self.__baserad = rad_percent * size
		self.__baselen = line_percent * size
		self.shuffleSticks(sticksnum)

	def shuffleSticks(self, num):
		for _ in range(num):
			pass

	def moveStick(self, index, delta):
		pass

	def hasCicrleCollision(self, circle):
		for stick in self.sticks:
			if _mixedCollision(circle, stick):
				return True

		return False

	def hasStickCollision(self, index):
		for i, stick in enumerate(self.sticks):
			if i == index:
				continue

			if _stickCollision(stick, self.sticks[index]):
				return True

		return False


def _randomDot(minx=0, miny=0, maxx=1, maxy=1):
	return (rnd.uniform(minx, maxx), rnd.uniform(miny, maxy))