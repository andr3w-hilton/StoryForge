#!/usr/bin/env python3
"""
Generate icon-192.png and icon-512.png for StoryForge PWA.
Uses only Python stdlib: zlib, struct, math.
"""
import zlib
import struct
import math


# ── Colors ────────────────────────────────────────────────────────────────────
BG       = (14,  12,  8,   255)   # #0e0c08
TRANSP   = (0,   0,   0,   0)     # transparent corners
GOLD     = (200, 150, 30,  255)   # #c8961e
GOLD_DIM = (200, 150, 30,  100)   # page lines
PAGE     = (26,  21,  16,  255)   # #1a1510 parchment page fill
DARK     = (14,  12,  8,   255)   # spine / page-curl fill
GOLD_LO  = (200, 150, 30,  26)    # very subtle glow (~10% opacity)


# ── PNG writer ────────────────────────────────────────────────────────────────

def _chunk(tag: bytes, data: bytes) -> bytes:
    c = struct.pack(">I", len(data)) + tag + data
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return c + struct.pack(">I", crc)


def write_png(pixels, size, path):
    """pixels: list of rows, each row a list of (r,g,b,a) tuples."""
    w = h = size
    raw = bytearray()
    for row in pixels:
        raw.append(0x00)  # filter byte: None
        for (r, g, b, a) in row:
            raw.extend([r, g, b, a])

    compressed = zlib.compress(bytes(raw), 9)

    ihdr_data = struct.pack(">IIBBBBB", w, h, 8, 2 | (1 << 2), 0, 0, 0)
    # bit depth=8, color type=6 (RGBA), compression=0, filter=0, interlace=0
    ihdr_data = struct.pack(">II", w, h) + bytes([8, 6, 0, 0, 0])

    png = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr_data)
        + _chunk(b"IDAT", compressed)
        + _chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)


# ── Drawing primitives ────────────────────────────────────────────────────────

def make_canvas(size):
    return [[TRANSP] * size for _ in range(size)]


def set_pixel(buf, x, y, color, size):
    if 0 <= x < size and 0 <= y < size:
        buf[y][x] = color


def blend_pixel(buf, x, y, color, size):
    """Alpha-composite color onto existing pixel."""
    if not (0 <= x < size and 0 <= y < size):
        return
    src_r, src_g, src_b, src_a = color
    dst_r, dst_g, dst_b, dst_a = buf[y][x]
    if src_a == 0:
        return
    if src_a == 255:
        buf[y][x] = (src_r, src_g, src_b, 255)
        return
    a = src_a / 255.0
    r = int(src_r * a + dst_r * (1 - a))
    g = int(src_g * a + dst_g * (1 - a))
    b = int(src_b * a + dst_b * (1 - a))
    out_a = min(255, dst_a + src_a)
    buf[y][x] = (r, g, b, out_a)


def fill_rect(buf, x1, y1, x2, y2, color, size):
    for y in range(max(0, y1), min(size, y2 + 1)):
        for x in range(max(0, x1), min(size, x2 + 1)):
            buf[y][x] = color


def blend_rect(buf, x1, y1, x2, y2, color, size):
    for y in range(max(0, y1), min(size, y2 + 1)):
        for x in range(max(0, x1), min(size, x2 + 1)):
            blend_pixel(buf, x, y, color, size)


def draw_line_bresenham(buf, x0, y0, x1, y1, color, size, thickness=1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    pts = []
    cx, cy = x0, y0
    while True:
        pts.append((cx, cy))
        if cx == x1 and cy == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            cx += sx
        if e2 < dx:
            err += dx
            cy += sy
    t = thickness // 2
    for (px, py) in pts:
        for tx in range(-t, t + 1):
            for ty in range(-t, t + 1):
                blend_pixel(buf, px + tx, py + ty, color, size)


def apply_rounded_corners(buf, size, radius):
    """Set pixels outside rounded corners to transparent."""
    for y in range(size):
        for x in range(size):
            in_tl = (x < radius and y < radius and
                     (x - radius) ** 2 + (y - radius) ** 2 > radius ** 2)
            in_tr = (x >= size - radius and y < radius and
                     (x - (size - 1 - radius)) ** 2 + (y - radius) ** 2 > radius ** 2)
            in_bl = (x < radius and y >= size - radius and
                     (x - radius) ** 2 + (y - (size - 1 - radius)) ** 2 > radius ** 2)
            in_br = (x >= size - radius and y >= size - radius and
                     (x - (size - 1 - radius)) ** 2 + (y - (size - 1 - radius)) ** 2 > radius ** 2)
            if in_tl or in_tr or in_bl or in_br:
                buf[y][x] = TRANSP


def fill_polygon(buf, points, color, size):
    """Fill a polygon defined by list of (x,y) float points."""
    if not points:
        return
    min_y = max(0, int(min(p[1] for p in points)))
    max_y = min(size - 1, int(max(p[1] for p in points)) + 1)
    n = len(points)
    for y in range(min_y, max_y + 1):
        xs = []
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                if y1 == y0:
                    continue
                t = (y - y0) / (y1 - y0)
                xi = x0 + t * (x1 - x0)
                xs.append(xi)
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            xa = int(math.ceil(xs[k]))
            xb = int(xs[k + 1])
            for x in range(max(0, xa), min(size, xb + 1)):
                blend_pixel(buf, x, y, color, size)


def star_points(cx, cy, R, r):
    """4-pointed star: outer radius R, inner radius r, centered at (cx,cy)."""
    pts = []
    # 8 points alternating outer/inner at 45° starting from top (-90°)
    for i in range(8):
        angle = math.radians(-90 + i * 45)
        radius = R if i % 2 == 0 else r
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return pts


def draw_rect_border(buf, x1, y1, x2, y2, color, size, thickness=2):
    """Draw a rectangle outline."""
    for t in range(thickness):
        # top
        for x in range(x1 + t, x2 - t + 1):
            blend_pixel(buf, x, y1 + t, color, size)
        # bottom
        for x in range(x1 + t, x2 - t + 1):
            blend_pixel(buf, x, y2 - t, color, size)
        # left
        for y in range(y1 + t, y2 - t + 1):
            blend_pixel(buf, x1 + t, y, color, size)
        # right
        for y in range(y1 + t, y2 - t + 1):
            blend_pixel(buf, x2 - t, y, color, size)


def draw_rounded_rect_border(buf, x1, y1, x2, y2, rx, color, size, thickness=2):
    """Draw a rounded rectangle outline (approximate with quadrant arcs)."""
    # straight edges
    for t in range(thickness):
        # top and bottom horizontal segments
        for x in range(x1 + rx, x2 - rx + 1):
            blend_pixel(buf, x, y1 + t, color, size)
            blend_pixel(buf, x, y2 - t, color, size)
        # left and right vertical segments
        for y in range(y1 + rx, y2 - rx + 1):
            blend_pixel(buf, x1 + t, y, color, size)
            blend_pixel(buf, x2 - t, y, color, size)
    # corners: draw arc using angle sweep
    corners = [
        (x1 + rx, y1 + rx, math.pi, 3 * math.pi / 2),       # top-left
        (x2 - rx, y1 + rx, 3 * math.pi / 2, 2 * math.pi),   # top-right
        (x2 - rx, y2 - rx, 0, math.pi / 2),                  # bottom-right
        (x1 + rx, y2 - rx, math.pi / 2, math.pi),            # bottom-left
    ]
    steps = max(60, rx * 4)
    for (cx, cy, a_start, a_end) in corners:
        for step in range(steps + 1):
            a = a_start + (a_end - a_start) * step / steps
            for t in range(thickness):
                r = rx - t
                px = int(round(cx + r * math.cos(a)))
                py = int(round(cy + r * math.sin(a)))
                blend_pixel(buf, px, py, color, size)


def fill_quad(buf, pts, color, size):
    """Fill a quadrilateral given 4 (x,y) points (clockwise/CCW)."""
    fill_polygon(buf, pts, color, size)


# ── Build icon at given size ──────────────────────────────────────────────────

def build_icon(size):
    S = size
    sc = size / 512.0  # scale factor

    def s(v):
        return int(round(v * sc))

    buf = make_canvas(S)

    # 1. Fill background
    fill_rect(buf, 0, 0, S - 1, S - 1, BG, S)

    # 2. Rounded corners (radius ~80 at 512)
    corner_r = s(80)
    apply_rounded_corners(buf, S, corner_r)

    # 3. Outer ornamental border (double-line)
    border_r = s(64)
    GOLD_90 = (200, 150, 30, 230)
    GOLD_55 = (200, 150, 30, 140)
    draw_rounded_rect_border(buf, s(18), s(18), S - s(18), S - s(18),
                              border_r, GOLD_90, S, thickness=max(2, s(2)))
    draw_rounded_rect_border(buf, s(28), s(28), S - s(28), S - s(28),
                              s(56), GOLD_55, S, thickness=max(1, s(1)))

    # 4. Corner flourish diamonds
    GOLD_65 = (200, 150, 30, 166)
    for (cx, cy) in [(s(48), s(28)), (S - s(48), s(28)),
                     (s(48), S - s(28)), (S - s(48), S - s(28))]:
        d = s(10)
        diamond = [(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)]
        fill_polygon(buf, diamond, GOLD_65, S)

    # 5. Stars — above (cy=118) and below (cy=394) book
    star_R = s(22)
    star_r = s(9)
    for cy in [s(118), s(394)]:
        pts = star_points(S // 2, cy, star_R, star_r)
        fill_polygon(buf, pts, GOLD, S)

    # 6. Book geometry
    # Page coordinates (at 512): left page x118–246, right page x266–394, y148–370
    lx1, lx2 = s(118), s(246)   # left page
    rx1, rx2 = s(266), s(394)   # right page
    sp1, sp2 = s(246), s(266)   # spine
    by1, by2 = s(148), s(362)   # book top/bottom

    # Outer edges are slightly angled (perspective)
    # Left page: outer-left edge goes from (118,155) top to (118,370) bottom
    # Right page: outer-right edge goes from (394,155) top to (394,370) bottom
    left_page = [(s(118), s(155)), (s(246), s(148)), (s(246), s(362)), (s(118), s(370))]
    right_page = [(s(266), s(148)), (s(394), s(155)), (s(394), s(370)), (s(266), s(362))]

    fill_quad(buf, left_page, PAGE, S)
    fill_quad(buf, right_page, PAGE, S)

    # Spine fill
    spine_pts = [(sp1, by1), (sp2, by1), (sp2, s(362)), (sp1, s(362))]
    fill_quad(buf, spine_pts, DARK, S)

    # Book outlines
    stroke_t = max(2, s(2))
    # Left page outline
    lp = left_page
    for i in range(len(lp)):
        p1 = lp[i]
        p2 = lp[(i + 1) % len(lp)]
        draw_line_bresenham(buf, int(p1[0]), int(p1[1]),
                            int(p2[0]), int(p2[1]), GOLD, S, thickness=stroke_t)
    # Right page outline
    for i in range(len(right_page)):
        p1 = right_page[i]
        p2 = right_page[(i + 1) % len(right_page)]
        draw_line_bresenham(buf, int(p1[0]), int(p1[1]),
                            int(p2[0]), int(p2[1]), GOLD, S, thickness=stroke_t)
    # Spine outline
    for i in range(len(spine_pts)):
        p1 = spine_pts[i]
        p2 = spine_pts[(i + 1) % len(spine_pts)]
        draw_line_bresenham(buf, int(p1[0]), int(p1[1]),
                            int(p2[0]), int(p2[1]), GOLD, S, thickness=max(1, s(1)))
    # Centre spine highlight
    mid_x = (sp1 + sp2) // 2
    GOLD_60 = (200, 150, 30, 153)
    draw_line_bresenham(buf, mid_x, by1 + s(2), mid_x, s(360), GOLD_60, S, thickness=1)

    # 7. Page text lines — left page (9 lines in two groups)
    line_pairs_left = [
        (s(136), s(183), s(234)),
        (s(136), s(203), s(234)),
        (s(136), s(223), s(234)),
        (s(136), s(243), s(234)),
        (s(136), s(263), s(234)),
        (s(136), s(283), s(212)),
        (s(136), s(310), s(234)),
        (s(136), s(330), s(234)),
        (s(136), s(350), s(212)),
    ]
    for (lx, ly, lend) in line_pairs_left:
        draw_line_bresenham(buf, lx, ly, lend, ly, GOLD_DIM, S, thickness=max(1, s(1)))

    # Right page (mirrored)
    line_pairs_right = [
        (s(278), s(183), s(376)),
        (s(278), s(203), s(376)),
        (s(278), s(223), s(376)),
        (s(278), s(243), s(376)),
        (s(278), s(263), s(376)),
        (s(278), s(283), s(356)),
        (s(278), s(310), s(376)),
        (s(278), s(330), s(376)),
        (s(278), s(348), s(356)),
    ]
    for (lx, ly, lend) in line_pairs_right:
        draw_line_bresenham(buf, lx, ly, lend, ly, GOLD_DIM, S, thickness=max(1, s(1)))

    return buf


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for size, path in [(512, "../icon-512.png"), (192, "../icon-192.png")]:
        buf = build_icon(size)
        write_png(buf, size, path)

    print("Generated icon-192.png and icon-512.png")
