from paddle import Paddle
from constants import BLACK
from constants import PAD_WIDTH, PAD_HEIGHT, WIDTH


def test_move_left():
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_left(1000)
    assert paddle.rect.x >= 0


def test_move_right():
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_right(WIDTH+500)
    assert paddle.rect.x <= WIDTH - PAD_WIDTH
    assert paddle.rect.x >= 0


def test_move_by_mouse_left():
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_by_mouse(-5)
    assert paddle.rect.x >= 0


def test_move_by_mouse_right():
    paddle = Paddle(BLACK, PAD_WIDTH, PAD_HEIGHT)
    paddle.move_by_mouse(WIDTH+500)
    assert paddle.rect.x <= WIDTH - PAD_WIDTH
    assert paddle.rect.x >= 0
