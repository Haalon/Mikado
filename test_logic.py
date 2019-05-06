from logic import *
import pytest


def test_fail_generation():
	failnum = rnd.randint(40, 200)
	field = GameField()
	with pytest.raises(MyIterError):
		field.newGame(types=[(failnum, 4)])


def test_good_generation():
	num = rnd.randint(1, 200)
	field = GameField()
	field.newGame(types=[(num, 1)])
	assert len(field.sticks) == num


def test_good_mixed_generation():
	num1 = rnd.randint(1, 200)
	num2 = rnd.randint(1, 8)
	field = GameField()
	field.newGame(types=[(num1, 1), (num2, 4)])
	assert len(field.sticks) == num1 + num2


def test_victory1():
	num = rnd.randint(1, 200)
	field = GameField()
	field.newGame(types=[(num, 1)])
	for key in field.sticks.copy():
		field.moveStick(key, (10500, 0))
	assert field.victory


def test_victory2():
	num = rnd.randint(1, 20)
	rad = rnd.uniform(1, 4)
	field = GameField()
	field.newGame(types=[(num, rad)])
	for key in field.sticks.copy():
		field.moveStick(key, (10500, 0))
	assert field.victory


def test_loss():
	rad = rnd.uniform(1, 4)
	field = GameField()

	field.newGame(types=[(2, rad)])
	c1 = field.sticks['t0'][0]
	c2 = field.sticks['t1'][0]
	delta = (c1[0] - c2[0], c1[1] - c2[1])

	field.moveStick('t1', delta)

	assert field.gameover and not field.victory
