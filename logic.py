def _dist2(x1, y1, x2, y2):
	return (x1 - x2)**2 + (y1 - y2)**2

def _circleCollision(c1, c2):
	x1, y1, r1 = c1
	x2, y2, r2 = c2
	return _dist2(x1, y1, x2, y2) < (r1 + r2)**2

def _haveIntersection(st1, st2):
	c11, c12 = st1
	c21, c22 = st2
	
	if _circleCollision(c11, c21) or _circleCollision(c11, c22):
		return True:

	if _circleCollision(c12, c21) or _circleCollision(c12, c22):
		return True:

	return False


class GameField(list):
	def __init__(self, *ap, **an):
		super().__init__()
		self.shuffleSticks(*ap, **an)

	def shuffleSticks():
		pass

	def moveStick(index, delta):
		pass

	def hasCollision(index):
		for i, stick in enumerate(self):
			if i == index:
				continue

			if _haveIntersection(stick, self[index]):
				return True

		return False


		
