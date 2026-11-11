from types import SimpleNamespace

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine
from thumbor.point import FocalPoint
from thumbor.transformer import Transformer


def test_auto_crop_keeps_a_row_for_very_wide_resize():
    with open("course/images/rainbow.png", "rb") as f:
        src = f.read()
    ctx = Context(config=Config())
    engine = Engine(ctx)
    engine.load(src, ".png")
    ctx.request = SimpleNamespace(engine=engine)

    transformer = Transformer(ctx)
    transformer.target_width = 800.0
    transformer.target_height = 20.0
    transformer.focal_points = [
        FocalPoint.from_alignment("center", "middle", 16, 16)
    ]

    transformer.auto_crop()

    width, height = engine.size
    assert width >= 1 and height >= 1, (
        f"auto_crop left an empty {width}x{height} region"
    )
