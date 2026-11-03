#!/usr/bin/env python3
"""Cut the four speaker headshots out of their flat studio backdrops.

Writes <name>-cut.webp (transparent background) next to the originals, so the page
can put its own gradient behind the speakers.

Joanne:      pure white backdrop
Terry/Linda: flat #e0e0e0 backdrop
Summer:      warm grey studio backdrop (colour-tested, connected to the border only)
"""
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT_WIDTH = 800


def flood_from_border(cand):
    """Pixels of `cand` that are connected (4-way) to the image border."""
    h, w = cand.shape
    out = np.zeros((h, w), bool)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if cand[y, x] and not out[y, x]:
                out[y, x] = True
                dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if cand[y, x] and not out[y, x]:
                out[y, x] = True
                dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True
                dq.append((ny, nx))
    return out


def grow(mask_bool, px):
    img = Image.fromarray((mask_bool * 255).astype("uint8"))
    return np.array(img.filter(ImageFilter.MaxFilter(2 * px + 1))) > 0


def background_flat(im, value, tol, fringe_tol=16):
    """Flat-colour backdrop (white or #e0e0e0)."""
    a = np.array(im).astype(int)
    d = np.abs(a - value).max(2)
    bg = flood_from_border(d <= tol)
    spread = a.max(2) - a.min(2)
    near = grow(bg, 3)
    fringe = near & ~bg & (d <= fringe_tol) & (spread <= 7)
    return bg | fringe


def background_joanne(im):
    """White backdrop. Her curls trap pockets of white that the border flood can't reach,
    so light neutral pixels hugging the backdrop count as backdrop too. The eyes, teeth
    and necklace are protected because white is part of the photo there."""
    a = np.array(im).astype(int)
    bg = background_flat(im, 255, 9, 0)
    h, w = bg.shape
    protect = np.zeros((h, w), bool)
    protect[int(h * 0.15):int(h * 0.38), int(w * 0.35):int(w * 0.62)] = True   # eyes, mouth
    protect[int(h * 0.44):int(h * 0.56), int(w * 0.35):int(w * 0.65)] = True   # necklace
    neutral = (a.max(2) - a.min(2)) <= 14
    nearwhite = (a.min(2) >= 236) & neutral
    bg = bg | (nearwhite & ~protect)
    for _ in range(3):  # eat the light anti-aliased fringe, a couple of pixels at a time
        near = grow(bg, 2)
        bg = bg | (near & ~protect & neutral & (a.min(2) >= 200))
    return bg


def background_summer(im):
    a = np.array(im.filter(ImageFilter.GaussianBlur(0.8))).astype(int)
    mx, mn = a.max(2), a.min(2)
    r, b = a[:, :, 0], a[:, :, 2]
    cand = ((mx - mn) < 30) & ((r - b) >= 4) & (r > 185) & (r < 236)
    return flood_from_border(cand)


def clean_alpha(bg):
    subj = Image.fromarray(np.where(bg, 0, 255).astype("uint8"))
    subj = subj.filter(ImageFilter.MedianFilter(3))
    subj = subj.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    subj = subj.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    return np.array(subj) > 127


def decontaminate(rgb, solid, rings=4):
    """Repaint the edge ring with colours from just inside the subject,
    so no trace of the old backdrop survives against a dark background."""
    h, w, _ = rgb.shape
    known = solid.copy()
    out = rgb.copy()
    for _ in range(rings):
        new_known = known.copy()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            shifted = np.roll(np.roll(known, dy, 0), dx, 1)
            src = np.roll(np.roll(out, dy, 0), dx, 1)
            take = shifted & ~new_known
            out[take] = src[take]
            new_known |= take
        known = new_known
    return out


def cut(name, source, backdrop):
    im = Image.open(ROOT / source).convert("RGB")
    bg = backdrop(im)
    subject = clean_alpha(bg)
    # pull the edge in ~2px, repaint it, then feather
    solid_img = Image.fromarray((subject * 255).astype("uint8")).filter(ImageFilter.MinFilter(5))
    solid = np.array(solid_img) > 127
    rgb = decontaminate(np.array(im), solid, rings=5)
    alpha = Image.fromarray((subject * 255).astype("uint8")).filter(ImageFilter.MinFilter(3))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.9))
    rgba = Image.fromarray(np.dstack([rgb, np.array(alpha)]), "RGBA")
    if rgba.width > OUT_WIDTH:
        rgba = rgba.resize((OUT_WIDTH, round(rgba.height * OUT_WIDTH / rgba.width)), Image.LANCZOS)
    dest = ROOT / f"{name}-cut.webp"
    rgba.save(dest, "WEBP", quality=92, alpha_quality=100, method=6)
    print(dest.name, rgba.size, f"{dest.stat().st_size // 1024} KB", f"bg {bg.mean():.2f}")


if __name__ == "__main__":
    cut("joanne", "joanne-headshot.jpg", background_joanne)
    cut("summer", "summer-headshot.jpg", background_summer)
    cut("terry", "terry-headshot.jpg", lambda im: background_flat(im, 224, 3))
    cut("linda", "linda-headshot.jpg", lambda im: background_flat(im, 224, 3))
