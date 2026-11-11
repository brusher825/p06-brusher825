from thumbor.ext.filters import _round_corner

SRC = (0, 0, 255, 255)  # opaque blue, RGBA
W, H = 40, 40
RADIUS = 12


def test_transparent_round_corner_has_no_dark_opaque_edge():
    """Edge pixels must not stay opaque while darkening toward black."""
    data = bytearray(SRC * (W * H))
    out = _round_corner.apply(
        1, "RGBA", RADIUS, RADIUS, 255, 255, 255, W, H, bytes(data), 1
    )
    px = [tuple(out[i:i + 4]) for i in range(0, len(out), 4)]

    dark_opaque = [
        (i % W, i // W, p)
        for i, p in enumerate(px)
        if p[3] == 255 and p[2] < 255
    ]
    assert dark_opaque == [], (
        "opaque edge pixels darkened toward black (dark ring): "
        f"{dark_opaque[:5]}"
    )
