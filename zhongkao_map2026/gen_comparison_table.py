# -*- coding: utf-8 -*-
"""生成官方数据对照总表"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

def parse_official(path):
    result = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(">") or line.startswith("学校"):
                continue
            m = re.match(r"^([^,]+),([^,]+)", line)
            if m:
                name = m.group(1).strip()
                val = m.group(2).strip()
                base_name = re.sub(r'[（(].*[）)]', '', name).strip()
                score = None if val == "空" else (float(val) if val.replace('.','').isdigit() else None)
                if "南开翔宇" in base_name:
                    if "河西" in name: result["南开翔宇学校##河西"] = score
                    elif "南开" in name and "河西" not in name: result["南开翔宇学校##南开"] = score
                    else: result[base_name] = score
                else:
                    result[base_name] = score
    return result

INNER = {"和平区","河西区","南开区","河东区","河北区","红桥区","海教园","海河教育园区"}
schools = []
with open(os.path.join(BASE, "gen_map.py"), "r", encoding="utf-8") as f:
    content = f.read()
pat = r'\("(.*?)"\s*,\s*"(.*?)"\s*,[\d.]+\s*,[\d.]+\s*,\s*"(.*?)"\s*,\s*(None|[\d.]+)\s*,\s*(None|[\d.]+)\s*,\s*(None|[\d.]+)\s*\)'
for m in re.finditer(pat, content):
    name, dist, level, s23, s24, s25 = m.groups()
    if level not in ("市属","区属","民办"): continue
    if dist not in INNER: continue
    schools.append((name, dist, level,
                     None if s23=="None" else float(s23),
                     None if s24=="None" else float(s24),
                     None if s25=="None" else float(s25)))

print(f"SCHOOLS 共 {len(schools)} 所")

off23 = parse_official(os.path.join(BASE, "official_2023.md"))
off24 = parse_official(os.path.join(BASE, "official_2024.md"))
off25 = parse_official(os.path.join(BASE, "official_2025.md"))

def get_off(name, dist, d):
    if name == "南开翔宇学校":
        k = f"{name}##{dist}"
        return d.get(k, d.get(name))
    return d.get(name)

def fmt(v): return "—" if v is None else str(v)
def ds(orig, off):
    if orig is None and off is not None: return f"+{off}（补）"
    if orig is not None and off is None: return f"清空(原{orig})"
    if orig is None and off is None: return ""
    if abs(orig-off) < 0.01: return "✓"
    d = off-orig
    return f"{'+'if d>0 else ''}{d:.2f}"

out_path = os.path.join(BASE, "官方数据核对对照表.md")
dc = 0
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write("# 天津市高中录取分数线 · 官方数据核对对照表\n\n")
    fh.write("> **基准来源**：天津市教育招生考试院官网 (zhaokao.net) 官方《高中阶段教育学校招生录取分数线》PDF\n")
    fh.write("> **核对时间**：2026-07-10\n\n")
    fh.write("| # | 学校 | 行政区 | 属性 | 2023原值→官方 | 偏差 | 2024原值→官方 | 偏差 | 2025原值→官方 | 偏差 |\n")
    fh.write("|---|------|--------|------|-------------|------|-------------|------|-------------|------|\n")
    for i,(name,dist,level,s23,s24,s25) in enumerate(schools,1):
        o23=get_off(name,dist,off23); o24=get_off(name,dist,off24); o25=get_off(name,dist,off25)
        d23,d24,d25=ds(s23,o23),ds(s24,o24),ds(s25,o25)
        if any(x and x!="✓" for x in [d23,d24,d25]): dc+=1
        fh.write(f"| {i} | {name} | {dist} | {level} | {fmt(s23)}→{fmt(o23)} | {d23} | {fmt(s24)}→{fmt(o24)} | {d24} | {fmt(s25)}→{fmt(o25)} | {d25} |\n")
    fh.write(f"\n**汇总**：共 {len(schools)} 所；**{dc} 所有差异**，其余 {len(schools)-dc} 所完全一致 ✓。\n")

print(f"写出完成: {out_path}, 差异={dc}")
