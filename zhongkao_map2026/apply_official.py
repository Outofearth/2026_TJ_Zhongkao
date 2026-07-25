import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "gen_map.py")

# ---------- 1) 解析三个官方文件 ----------
def parse_file(fname, year):
    out = {}          # (name, dist_or_None, year) -> score(float) | None(空)
    nk = 0
    with open(BASE + r"\\" + fname, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith(">") or s.startswith("学校"):
                continue
            p = s.split(",")
            if len(p) < 2:
                continue
            name = p[0].strip()
            v = p[1].strip()
            if not name:
                continue
            if name.startswith("南开翔宇学校"):   # 命名碰撞：河西分校/南开本校（2025 文件带「（河西）」后缀）
                nk += 1
                dist = "河西区" if nk == 1 else "南开区"
            else:
                dist = None
            score = None if v == "空" else float(v)
            out[(name, dist, year)] = score
    return out

raw = {}
for fn, yr in (("official_2023.md", 2023), ("official_2024.md", 2024), ("official_2025.md", 2025)):
    raw.update(parse_file(fn, yr))

# ---------- 2) 从当前 SCHOOLS 建立 name->dist（市内学校） ----------
text = open(path, encoding="utf-8").read()
m = re.search(r"SCHOOLS = \[(.*?)\]\s*\n# 只保留市内六区", text, re.S)
block = m.group(1)
name2dist = {}
for nm, dt in re.findall(r'^\s*\("([^"]+)","([^"]+)"', block, re.M):
    name2dist.setdefault(nm, dt)

# ---------- 3) 合并成 corrections: (name,dist) -> [sc23,sc24,sc25] ----------
SKIP = {"美术中学", "意斯特艺术高级中学", "天津师范大学南开附属中学"}   # 纯艺术高中，其官方值均为艺术线
KEEP = {("育红中学", "2024"), ("华兰萨顿高级中学", "2025"), ("明德致远高级中学", "2025")}  # 子代理漏报/征询线，保留现值
DONT = {("河北工业大学附属红桥中学", "2025")}                          # 2025 为艺术高中线，不填

corr = {}
for (name, dist, year), score in raw.items():
    if name in SKIP:
        continue
    if dist is None:
        dist = name2dist.get(name)
    if dist is None:
        continue
    key = (name, dist)
    c = corr.setdefault(key, [None, None, None])
    c[{2023: 0, 2024: 1, 2025: 2}[year]] = score

# ---------- 4) 逐行替换分数（保留注释与经纬度） ----------
pat = re.compile(r'^(\s*\()"([^"]+)","([^"]+)",([^,]+),([^,]+),"([^"]+)",([^,]+),([^,]+),([^,]+)(\)),\s*$')
lines = text.split("\n")
diffs = []
for i, line in enumerate(lines):
    mo = pat.match(line)
    if not mo:
        continue
    name, dist = mo.group(2), mo.group(3)
    key = (name, dist)
    if key not in corr:
        continue
    newsc = corr[key]
    cur = [mo.group(7), mo.group(8), mo.group(9)]
    outsc = []
    changed = False
    for yi, year in enumerate((2023, 2024, 2025)):
        o = newsc[yi]
        kkey = (name, str(year))
        if o is None:
            nv = cur[yi] if kkey in KEEP else "None"
        else:
            nv = cur[yi] if kkey in DONT else ("None" if o is None else repr(o))
        if nv != cur[yi]:
            changed = True
        outsc.append(nv)
    if not changed:
        continue
    new_line = (line[:mo.start(7)] + outsc[0]
                + line[mo.end(7):mo.start(8)] + outsc[1]
                + line[mo.end(8):mo.start(9)] + outsc[2]
                + line[mo.end(9):])
    diffs.append((name, dist, cur, outsc))
    lines[i] = new_line

open(path, "w", encoding="utf-8").write("\n".join(lines))

# ---------- 5) 输出差异报告 ----------
print(f"实际变更行数: {len(diffs)}\n")
for name, dist, cur, outsc in diffs:
    def f(x):
        return "空" if x == "None" else x
    old = "/".join(f(c) for c in cur)
    new = "/".join(f(o) for o in outsc)
    print(f"  {name}({dist}): 23/24/25  {old}  ->  {new}")
