from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine


def make_palette_gif_with_transparent_background():
    img = Image.new("P", (16, 16), 0)
    palette = [255, 0, 0, 0, 0, 255] + [0, 0, 0] * 254
    img.putpalette(palette)
    img.paste(1, (4, 4, 12, 12))
    buffer = BytesIO()
    img.save(buffer, "GIF", transparency=0)
    return buffer.getvalue()


def test_resized_palette_gif_keeps_transparent_background():
    engine = Engine(Context(config=Config()))
    engine.load(make_palette_gif_with_transparent_background(), ".gif")
    engine.resize(32, 32)

    result = Image.open(BytesIO(engine.read(".gif")))
    rgba = result.convert("RGBA")

    assert "transparency" in result.info, "GIF lost its transparency index"
    assert rgba.getpixel((0, 0))[3] == 0, "corner is no longer transparent"
