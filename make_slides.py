"""デザイン担当：投稿JSONからインスタ用カルーセル画像（1080x1350）を作る。
使い方: python3 make_slides.py posts/<id>.json images/<日付>
必要: Pillow と Noto CJK フォント（/usr/share/fonts/opentype/noto/）
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
BG = (24, 30, 46)          # 深い紺
INK = (244, 238, 224)      # 生成り
GOLD = (201, 168, 106)     # くすんだ金
QUIET = (160, 164, 178)

FONT_DIR = "/usr/share/fonts/opentype/noto/"
SERIF_B = FONT_DIR + "NotoSerifCJK-Bold.ttc"
SERIF_M = FONT_DIR + "NotoSerifCJK-Medium.ttc"
SANS_M = FONT_DIR + "NotoSansCJK-Medium.ttc"
SANS_R = FONT_DIR + "NotoSansCJK-Regular.ttc"


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def frame(draw, page, total):
    # 細い金の枠とページ番号
    m = 48
    draw.rectangle([m, m, W - m, H - m], outline=GOLD, width=2)
    label = f"{page} / {total}"
    f = font(SANS_R, 26)
    tw = draw.textlength(label, font=f)
    draw.text((W - m - 24 - tw, H - m - 56), label, font=f, fill=QUIET)
    f2 = font(SANS_R, 26)
    draw.text((m + 24, H - m - 56), "偉人の言葉帳", font=f2, fill=QUIET)


def center_lines(draw, lines, f, y, fill, gap):
    for line in lines:
        if line:
            tw = draw.textlength(line, font=f)
            draw.text(((W - tw) / 2, y), line, font=f, fill=fill)
        y += f.size + gap
    return y


def block_height(lines, f, gap):
    return len(lines) * (f.size + gap) - gap


def render(slide, page, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    frame(d, page, total)
    t = slide["type"]

    if t == "cover":
        fk = font(SANS_M, 44)
        ft = font(SERIF_B, 112)
        fs = font(SANS_R, 40)
        title = slide["title"].split("\n")
        total_h = fk.size + 60 + block_height(title, ft, 28) + 80 + fs.size
        y = (H - total_h) / 2
        y = center_lines(d, [slide["kicker"]], fk, y, GOLD, 0) + 60
        y = center_lines(d, title, ft, y, INK, 28) + 52
        d.line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=GOLD, width=3)
        center_lines(d, [slide["sub"]], fs, y + 28, QUIET, 0)

    elif t == "quote":
        fq = font(SERIF_B, 64)
        fb = font(SANS_R, 36)
        lines = slide["quote"].split("\n")
        qh = block_height(lines, fq, 34)
        total_h = 120 + qh + 90 + fb.size
        y = (H - total_h) / 2
        fmark = font(SERIF_B, 160)
        center_lines(d, ["“"], fmark, y - 60, GOLD, 0)
        y = center_lines(d, lines, fq, y + 120, INK, 34) + 56
        center_lines(d, ["―― " + slide["by"]], fb, y, GOLD, 0)

    elif t == "body":
        fh = font(SANS_M, 52)
        fl = font(SANS_R, 46)
        lines = slide["lines"]
        bh = block_height(lines, fl, 26)
        total_h = fh.size + 90 + bh
        y = (H - total_h) / 2
        y = center_lines(d, [slide["head"]], fh, y, GOLD, 0) + 36
        d.line([(W / 2 - 40, y), (W / 2 + 40, y)], fill=GOLD, width=3)
        center_lines(d, lines, fl, y + 54, INK, 26)

    elif t == "end":
        ft = font(SERIF_B, 84)
        fs = font(SANS_R, 42)
        fh = font(SANS_M, 44)
        title = slide["title"].split("\n")
        total_h = block_height(title, ft, 24) + 70 + fs.size + 110 + fh.size
        y = (H - total_h) / 2
        y = center_lines(d, title, ft, y, INK, 24) + 70
        y = center_lines(d, [slide["sub"]], fs, y, QUIET, 0) + 90
        hw = d.textlength(slide["handle"], font=fh) + 64
        d.rounded_rectangle([(W - hw) / 2, y, (W + hw) / 2, y + fh.size + 40], radius=40, outline=GOLD, width=3)
        center_lines(d, [slide["handle"]], fh, y + 14, GOLD, 0)

    return img


def main():
    post = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    total = len(post["slides"])
    for i, s in enumerate(post["slides"], 1):
        # インスタはJPEGのみ受け付けるのでJPEGで保存する
        p = out / f"{post['id']}_{i}.jpg"
        render(s, i, total).save(p, "JPEG", quality=92, optimize=True)
        print(p)


if __name__ == "__main__":
    main()
