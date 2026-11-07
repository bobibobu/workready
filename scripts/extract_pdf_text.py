from pathlib import Path
import re
import sys
import zlib
import unicodedata

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def obj_streams(data):
    pattern = re.compile(rb"(\d+)\s+0\s+obj\s*(.*?)\s*endobj", re.S)
    for m in pattern.finditer(data):
        obj_id = int(m.group(1))
        body = m.group(2)
        sm = re.search(rb"<<(.*?)>>\s*stream\r?\n(.*?)\r?\nendstream", body, re.S)
        if not sm:
            continue
        header, stream = sm.group(1), sm.group(2)
        if b"FlateDecode" in header:
            try:
                stream = zlib.decompress(stream)
            except Exception:
                continue
        yield obj_id, header, stream


def parse_cmap(stream):
    text = stream.decode("latin1", "ignore")
    cmap = {}
    for block in re.finditer(r"beginbfchar(.*?)endbfchar", text, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block.group(1)):
            cmap[int(src, 16)] = chr(int(dst, 16))
    for block in re.finditer(r"beginbfrange(.*?)endbfrange", text, re.S):
        content = block.group(1)
        for start, end, arr in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]", content, re.S):
            code = int(start, 16)
            for dst in re.findall(r"<([0-9A-Fa-f]+)>", arr):
                cmap[code] = chr(int(dst, 16))
                code += 1
        for start, end, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", content):
            s, e, d = int(start, 16), int(end, 16), int(dst, 16)
            for code in range(s, e + 1):
                cmap[code] = chr(d + code - s)
    return cmap


def build_font_maps(data):
    streams = {obj: stream for obj, _header, stream in obj_streams(data)}
    font_to_obj = {}
    for m in re.finditer(rb"(\d+)\s+0\s+obj\s*<<(.*?)>>", data, re.S):
        obj_id = int(m.group(1))
        body = m.group(2)
        to_unicode = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", body)
        if to_unicode:
            font_to_obj[obj_id] = int(to_unicode.group(1))

    resource_map = {}
    for m in re.finditer(rb"/(F\d+)\s+(\d+)\s+0\s+R", data):
        name, obj_id = m.group(1).decode(), int(m.group(2))
        if obj_id in font_to_obj and font_to_obj[obj_id] in streams:
            resource_map[name] = parse_cmap(streams[font_to_obj[obj_id]])
    return resource_map


TOKEN_RE = re.compile(
    rb"(/F\d+|/Span|BDC|EMC|BT|ET|Tj|TJ|Td|Tm|Tf|<[^>]+>|\[[^\]]+\]|-?\d+(?:\.\d+)?)",
    re.S,
)


def decode_hex(hex_token, cmap):
    raw = re.sub(rb"[^0-9A-Fa-f]", b"", hex_token.strip(b"<>"))
    chars = []
    for i in range(0, len(raw), 4):
        chunk = raw[i : i + 4]
        if len(chunk) == 4:
            chars.append(cmap.get(int(chunk, 16), ""))
    return "".join(chars)


def extract_text(data):
    font_maps = build_font_maps(data)
    rows = []
    for _obj_id, header, stream in obj_streams(data):
        if b"/Type /Font" in header or b"/FontFile" in header:
            continue
        if b"BT" not in stream:
            continue
        tokens = TOKEN_RE.findall(stream)
        stack = []
        font = None
        x = y = 0.0
        in_marked = False
        for tok in tokens:
            if re.fullmatch(rb"-?\d+(?:\.\d+)?", tok):
                stack.append(float(tok))
            elif tok.startswith(b"/F"):
                font = tok[1:].decode()
                stack.append(tok)
            elif tok.startswith(b"<"):
                stack.append(tok)
            elif tok == b"Tm":
                if len(stack) >= 6:
                    x, y = float(stack[-2]), float(stack[-1])
                stack.clear()
            elif tok == b"Td":
                if len(stack) >= 2:
                    x += float(stack[-2])
                    y += float(stack[-1])
                stack.clear()
            elif tok == b"Tf":
                stack.clear()
            elif tok == b"BDC":
                in_marked = True
                stack.clear()
            elif tok == b"EMC":
                in_marked = False
                stack.clear()
            elif tok == b"Tj":
                if stack and not in_marked:
                    chars = decode_hex(stack[-1], font_maps.get(font, {}))
                    if chars:
                        rows.append((round(y, 1), round(x, 1), chars))
                stack.clear()
            else:
                stack.clear()

    by_y = {}
    for y, x, txt in rows:
        by_y.setdefault(y, []).append((x, txt))
    lines = []
    for y in sorted(by_y):
        parts = [txt for _x, txt in sorted(by_y[y])]
        line = "".join(parts).strip()
        if line and (not lines or line != lines[-1]):
            lines.append(line)
    return unicodedata.normalize("NFKC", "\n".join(lines))


if __name__ == "__main__":
    for name in sys.argv[1:] or [p.name for p in Path(".").glob("*.pdf")]:
        p = Path(name)
        print(f"===== {p.name} =====")
        try:
            print(extract_text(p.read_bytes()))
        except Exception as exc:
            print(f"[extract failed: {exc}]")
