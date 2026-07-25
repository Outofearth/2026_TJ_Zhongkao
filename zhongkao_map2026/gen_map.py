# -*- coding: utf-8 -*-
import json, csv

# 字段: (校名, 行政区, 纬度WGS84, 经度WGS84, 属性[市属/区属/民办], 2023, 2024, 2025)
# 录取分数线来源(公开网络汇总, 仅供参考):
#   2023: 网易/乐居好房《2023年天津市高中最低录取分数线》(经 Sohu 2023 官方文章核验一致)
#   2024: 天津本地宝《2024年天津市中考各批次最低分数线汇总》(用户供图提取)
#   2025: 天津本地宝/搜狐"小希"《2023-2025录取分数线汇总》(同源镜像提取, 含市九所+宝坻/武清等)
# 缺失以 None 表示(显示为 —)
# 注: 2025市五所存在两套公开数据(本表采用天津本地宝/搜狐源), 以招考资讯网(zhaokao.net)官方为准
# 坐标说明: 市内六区学校用 Nominatim(OpenStreetMap) WGS-84 地理编码校准;
# 2026-07 扩充为市内六区"全部高中"名单(约78所, 含2025-2026新建校);
# 多数公办/老校坐标来自 OSM 精确标注; 部分新建/民办校 OSM 无独立标注,
# 用其所在街道中心点坐标近似(误差约数百米, 以高德底图显示为参考, 建议实地核对)。
# 渲染时由 wgs84togcj02 转 GCJ-02 与高德底图对齐。
SCHOOLS = [
    # 和平区
    ("天津一中","和平区",39.1127941,117.1883652,"市属",769.5,772.25,768.9),
    ("耀华中学","和平区",39.1180772,117.1940022,"市属",764.25,768.25,762.8),
    ("第二十中学","和平区",39.1135415,117.2072324,"区属",755.0,760.75,753.0),
    ("第二南开中学","和平区",39.1267514,117.1764800,"区属",747.45,754.75,746.7),
    ("第五十五中学","和平区",39.1132831,117.1754310,"区属",736.25,747.5,737.5),
    ("双菱中学","和平区",39.1201783,117.2012284,"民办",729.45,743.25,730.8),
    ("第二十一中学","和平区",39.1031973,117.1863043,"区属",722.0,736.25,726.15),
    ("汇文中学","和平区",39.1210806,117.1833546,"区属",718.0,730.6,722.25),
    ("益中学校","和平区",39.1028954,117.1771040,"民办",716.4,729.5,716.05),
    ("建华中学","和平区",39.1219124,117.1796862,"民办",698.15,711.45,707.65),
    ("嘉诚中学","和平区",39.1466855,117.2107218,"民办",694.75,704.75,695.73),
    # 河西区
    ("新华中学","河西区",39.1097957,117.2057589,"市属",760.0,764.55,758.25),
    ("实验中学","河西区",39.0973701,117.1846561,"市属",757.0,762.5,755.15),
    ("第四中学","河西区",39.0787207,117.2236638,"区属",751.5,758.0,747.9),
    ("第四十一中学","河西区",39.1033680,117.1941674,"区属",710.5,721.25,708.5),
    ("海河中学","河西区",39.1108490,117.2181663,"区属",738.4,748.5,735.75),
    ("北师大天津附中","河西区",39.0703765,117.2629592,"区属",714.5,723.5,714.25),
    ("微山路中学","河西区",39.0592451,117.2568084,"区属",693.25,706.25,695.15),
    ("梅江中学","河西区",39.0692718,117.2001941,"区属",678.25,692.75,683.0),
    ("梧桐中学","河西区",39.0570934,117.2134216,"区属",710.7,721.8,711.7),
    ("第二新华中学","河西区",39.0383240,117.2480789,"区属",748.25,754.74,746.5),
    ("第四十二中学","河西区",39.0938690,117.2199361,"区属",745.0,752.5,742.0),
    ("觉民中学","河西区",39.0947681,117.2128466,"区属",706.75,733.75,724.9),
    ("卓越中学","河西区",39.0800651,117.2209909,"区属",698.0,716.31,706.35),
    ("景海道中学","河西区",39.0632760,117.2371120,"区属",None,None,None),
    ("培杰中学","河西区",39.0731968,117.2648101,"民办",667.25,672.3,649.25),
    ("自立中学","河西区",39.0952925,117.2132824,"民办",666.85,644.05,642.6),
    ("南开翔宇学校","河西区",39.0431075,117.2241882,"民办",703.0,710.75,704.25),
    ("天明高级中学","河西区",39.0520,117.2480,"民办",None,None,666.65),
    ("华兰萨顿高级中学","河西区",39.0775429,117.2109589,"民办",None,None,472.8),
    ("明德致远高级中学","河西区",39.0921080,117.2204416,"民办",None,None,519.9),
    # 南开区
    ("南开中学","南开区",39.1305977,117.1649425,"市属",767.65,770.75,766.09),
    ("天津中学","南开区",39.0830430,117.1243620,"市属",731.65,739.95,730.25),
    ("南大附中","南开区",39.1116288,117.1477168,"区属",735.25,745.35,729.0),
    ("天大附中","南开区",39.1035523,117.1665262,"区属",707.8,718.81,707.2),
    ("崇化中学","南开区",39.1425332,117.1721059,"区属",718.3,730.73,718.05),
    ("第二十五中学","南开区",39.1237285,117.1573625,"区属",714.7,726.0,715.25),
    ("育红中学","南开区",39.1250000,117.1710000,"区属",673.15,686.9,673.05),
    ("津英中学","南开区",39.1372952,117.1299026,"民办",630.5,645.9,651.9),
    ("第四十三中学","南开区",39.1377368,117.1332137,"区属",699.25,707.65,695.5),
    ("第九中学","南开区",39.0728670,117.1559714,"区属",684.0,696.1,679.7),
    ("第六十三中学","南开区",39.1032160,117.1301027,"区属",None,None,None),
    ("天津师范大学南开附属中学","南开区",39.1215,117.1245,"区属",None,None,None),
    ("南开翔宇学校","南开区",39.1330,117.1377,"民办",700.5,709.0,703.0),
    ("南开日新学校","南开区",39.0856,117.1431,"民办",None,759.8,760.75),
    ("美达菲学校","南开区",39.1253593,117.1154405,"民办",661.69,695.8,692.8),
    # 河东区
    ("第七中学","河东区",39.1276573,117.2322320,"区属",734.25,741.2,734.15),
    ("第四十五中学","河东区",39.1028566,117.2643649,"区属",719.5,732.31,720.05),
    ("第一〇二中学","河东区",39.1360207,117.2390220,"区属",706.5,719.0,709.7),
    ("第五十四中学","河东区",39.1131772,117.2274031,"区属",686.55,697.0,686.75),
    ("第三十二中学","河东区",39.1416718,117.1993958,"区属",661.2,676.0,660.75),
    ("第八十二中学","河东区",39.1068395,117.2422806,"区属",645.6,662.25,648.4),
    ("第八中学","河东区",39.1484083,117.2787262,"区属",630.25,650.2,641.25),
    ("第九十八中学","河东区",39.1108839,117.2535205,"区属",614.15,632.75,626.65),
    ("华英中学","河东区",39.1073,117.2519,"民办",None,None,669.8),
    ("求真中学","河东区",39.1471162,117.2264332,"民办",595.25,601.8,599.35),
    # 河北区
    ("第二中学","河北区",39.1525676,117.2038422,"区属",727.6,738.1,730.5),
    ("第十四中学","河北区",39.1642369,117.2144959,"区属",694.25,707.65,698.75),
    ("第五十七中学","河北区",39.1586625,117.1989072,"区属",672.45,689.25,677.5),
    ("木斋中学","河北区",39.1509977,117.1910495,"区属",626.35,644.65,638.75),
    ("教育科学研究院附属河北中学","河北区",39.1574,117.2224,"区属",652.22,669.39,655.05),
    ("美术中学","河北区",39.1576123,117.1837738,"区属",None,None,None),
    ("外国语大学附属河北外国语中学","河北区",39.1520,117.1880,"区属",None,710.9,738.75),
    ("扶轮中学","河北区",39.1580,117.1900,"区属",659.25,678.15,668.6),
    ("红光中学","河北区",39.1699222,117.2166730,"区属",None,None,711.65),
    ("博文中学","河北区",39.1584210,117.2466391,"民办",592.05,570.5,593.95),
    ("意斯特艺术高级中学","河北区",39.1541,117.2070,"民办",None,None,None),
    # 红桥区
    ("第三中学","红桥区",39.1829342,117.1504713,"区属",716.0,725.25,713.2),
    ("第五中学","红桥区",39.1573900,117.1258746,"区属",703.75,715.45,702.75),
    ("民族中学","红桥区",39.1522743,117.1426440,"区属",689.75,700.35,690.5),
    ("第五十一中学","红桥区",39.1456631,117.1528069,"区属",658.85,None,660.8),
    ("新华中学和苑学校","红桥区",39.1553,117.1033,"区属",None,None,707.85),
    ("耀华中学红桥学校","红桥区",39.1433436,117.1417815,"区属",733.7,744.75,728.1),
    ("河北工业大学附属实验学校","红桥区",39.1761,117.1684,"区属",627.25,643.45,639.0),
    ("铃铛阁外国语中学","红桥区",39.1488520,117.1538453,"区属",None,None,None),
    ("河北工业大学附属红桥中学","红桥区",39.1699713,117.1652959,"区属",658.85,674.8,None),
    ("复兴中学","红桥区",39.1486,117.1582,"区属",667.8,684.95,671.15),
    ("天骄高级中学","红桥区",39.1533661,117.1151999,"民办",584.77,576.75,537.6),
    # 海河教育园区（海教园）——面向市内六区+海教园招生
    ("海教园南开学校","海教园",39.0076697,117.3324601,"区属",666.6,677.0,662.6),
    # 东丽区
    ("第一百中学","东丽区",39.090,117.330,"区属",714.25,739.5,None),
    ("四合庄中学","东丽区",39.070,117.320,"区属",689.34,708.5,None),
    # 西青区
    ("杨柳青第一中学","西青区",39.150,117.000,"区属",714.25,750.0,None),
    ("张家窝中学","西青区",39.070,117.000,"区属",689.34,715.0,None),
    ("杨柳青第四中学","西青区",39.145,117.010,"区属",None,700.5,713.35),
    # 津南区
    ("咸水沽第一中学","津南区",38.980,117.350,"区属",722.0,743.5,None),
    ("咸水沽第二中学","津南区",38.970,117.355,"区属",704.5,721.0,None),
    ("双港中学","津南区",39.030,117.300,"区属",655.2,689.5,None),
    # 北辰区
    ("第四十七中学","北辰区",39.230,117.135,"区属",724.25,745.0,None),
    ("青光中学","北辰区",39.250,117.050,"区属",626.5,698.5,None),
    ("华辰学校","北辰区",39.220,117.140,"区属",715.0,730.5,None),
    # 武清区
    ("杨村第一中学","武清区",39.390,117.050,"区属",749.25,758.5,740.6),
    ("杨村第三中学","武清区",39.385,117.060,"区属",730.15,738.0,720.57),
    ("杨村第四中学","武清区",39.380,117.055,"区属",686.0,715.5,669.95),
    ("天和城实验中学","武清区",39.370,117.040,"区属",706.25,726.5,688),
    # 宝坻区
    ("宝坻第一中学","宝坻区",39.720,117.310,"区属",725.51,746.5,717.85),
    ("宝坻第四中学","宝坻区",39.715,117.300,"区属",626.2,705.5,631.4),
    ("宝坻九中","宝坻区",39.725,117.320,"区属",616.25,696.0,629.5),
    # 滨海新区
    ("塘沽一中","滨海新区",39.020,117.700,"区属",734.25,760.5,None),
    ("大港一中","滨海新区",38.850,117.480,"区属",720.0,754.0,None),
    ("汉沽一中","滨海新区",39.230,117.780,"区属",663.75,710.0,None),
    ("油田实验中学","滨海新区",38.800,117.450,"区属",691.2,734.5,None),
    ("开发区一中","滨海新区",39.030,117.720,"区属",714.85,738.5,None),
    ("紫云中学","滨海新区",39.010,117.690,"区属",705.5,650.0,None),
    # 宁河区
    ("芦台第一中学","宁河区",39.330,117.820,"区属",726.0,730.0,None),
    ("芦台第二中学","宁河区",39.335,117.830,"区属",621.25,688.5,None),
    # 静海区
    ("静海第一中学","静海区",38.940,116.920,"区属",715.75,744.5,None),
    ("静海第六中学","静海区",38.930,116.930,"区属",677.25,712.0,None),
    ("静海第四中学","静海区",38.945,116.915,"区属",653.0,686.5,None),
    # 蓟州区
    ("蓟州第一中学","蓟州区",40.050,117.410,"区属",729.45,748.5,None),
    ("蓟州第二中学","蓟州区",40.045,117.420,"区属",656.3,710.5,None),
    ("蓟州第四中学","蓟州区",40.040,117.400,"区属",698.95,722.0,None),
    ("杨家楼中学","蓟州区",40.030,117.390,"区属",684.35,708.5,None),
]

# 只保留市内六区 + 海河教育园区(海教园)的学校
INNER = {"和平区","河西区","南开区","河东区","河北区","红桥区","海教园","海河教育园区"}
SCHOOLS = [s for s in SCHOOLS if s[1] in INNER]

# ---------------- 一分一段表（用于计算“位次”） ----------------
import bisect, json as _json
def _load_year(path, has_year_key=False):
    raw = _json.load(open(path, encoding="utf-8"))
    if has_year_key:
        raw = raw["data"]
    city = {}; dist = {}
    for r in raw:
        sc = int(r[0]); city[sc] = int(r[1]); dist[sc] = int(r[2])
    scores = sorted(city.keys())
    return scores, city, dist

s23, c23, d23 = _load_year("data_2023_built.json")
s24, c24, d24 = _load_year("data_2024.json", has_year_key=True)
s25, c25, d25 = _load_year("data_2025_built.json")

# 2025 实际分数/位次来自用户上传《26天津中考成绩预估导航表（市内六区）》的"25年分数/25年排位"列。
# 覆盖市内六区 32 所；育红中学、津英中学、第五十一中学 未收录，保持 None。
EXCEL_2025 = {
    "天津一中": (768.9, 1088), "耀华中学": (762.8, 1982), "第二十中学": (753.0, 3962),
    "第二南开中学": (746.7, 5472), "第五十五中学": (737.5, 7732), "双菱中学": (730.8, 9513),
    "新华中学": (758.25, 2884), "实验中学": (755.15, 3491), "第四中学": (747.9, 5186),
    "第四十一中学": (708.5, 15296), "海河中学": (735.75, 8181), "北师大天津附中": (714.25, 13853),
    "微山路中学": (695.15, 18407), "梅江中学": (683.0, 20892), "梧桐中学": (711.7, 14482),
    "第二新华中学": (746.5, 5521),
    "南开中学": (766.09, 1460), "天津中学": (730.25, 9675), "南大附中": (729.0, 9973),
    "天大附中": (707.2, 15614), "崇化中学": (718.05, 12877), "第二十五中学": (715.25, 13598),
    "第七中学": (734.15, 8601), "第四十五中学": (720.05, 12322), "第一〇二中学": (709.7, 14991),
    "第五十四中学": (686.75, 20192), "第二中学": (730.5, 9601), "第十四中学": (698.75, 17613),
    "第五十七中学": (677.5, 21919), "木斋中学": (638.75, 27726), "第三中学": (713.2, 14121),
    "第五中学": (702.75, 16696), "民族中学": (690.5, 19431),
}

def rank_for(score, scores, city):
    """位次 = 全市累计人数（分数 >= 录取分 的最小档）。"""
    if score is None:
        return None
    i = bisect.bisect_left(scores, score)
    if i >= len(scores):
        return None
    return city[scores[i]]

DISTRICTS = ["和平区","河西区","南开区","河东区","河北区","红桥区","海教园","东丽区","西青区",
             "津南区","北辰区","武清区","宝坻区","滨海新区","宁河区","静海区","蓟州区"]
COLORS = ["#e6194B","#3cb44b","#f58231","#4363d8","#911eb4","#d63384","#20b2aa","#f032e6","#469990",
          "#9A6324","#800000","#000075","#808000","#6f42c1","#42d4f4","#2e8b57","#fd9e02"]
COLOR_MAP = dict(zip(DISTRICTS, COLORS))

# ---------------- 导出 CSV (utf-8-sig, Excel 友好) ----------------
csv_path = r"C:\Users\ALTC\WorkBuddy\2026-07-09-11-29-25\天津高中录取分数线_2023-2025.csv"
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["学校","行政区","属性","纬度WGS84","经度WGS84","2023录取分","2023位次","2024录取分","2024位次","2025录取分","2025位次"])
    for name, dist, lat, lng, level, sc23, sc24, sc25 in SCHOOLS:
        r23 = rank_for(sc23, s23, c23)
        r24 = rank_for(sc24, s24, c24)
        sc25x, r25x = (EXCEL_2025[name] if name in EXCEL_2025 else (sc25, None))
        r25 = r25x if r25x is not None else rank_for(sc25x, s25, c25)
        w.writerow([name, dist, level, lat, lng,
                    "" if sc23 is None else sc23, "" if r23 is None else r23,
                    "" if sc24 is None else sc24, "" if r24 is None else r24,
                    "" if sc25x is None else sc25x, "" if r25 is None else r25])
print("CSV 已写出:", csv_path)

data = []
for name, dist, lat, lng, level, sc23, sc24, sc25 in SCHOOLS:
    r23 = rank_for(sc23, s23, c23)
    r24 = rank_for(sc24, s24, c24)
    sc25x, r25x = (EXCEL_2025[name] if name in EXCEL_2025 else (sc25, None))
    r25 = r25x if r25x is not None else rank_for(sc25x, s25, c25)
    data.append({"name":name,"dist":dist,"lat":lat,"lng":lng,"level":level,
                 "color":COLOR_MAP[dist],
                 "s2023":sc23,"s2024":sc24,"s2025":sc25x,
                 "r2023":r23,"r2024":r24,"r2025":r25})

payload = {"schools":data,"districts":DISTRICTS,"colors":COLORS}
html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>天津市高中地图（高德底图·精简版）</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  html,body{margin:0;height:100%;font-family:-apple-system,"Microsoft YaHei",sans-serif;background:#1e1e1e;}
  #map{height:100%;width:100%;background:#0b0b0b;}
  .panel{position:absolute;z-index:1000;background:rgba(28,28,30,.93);color:#e6e6e6;
         border:1px solid #444;border-radius:10px;padding:12px 14px;box-shadow:0 2px 12px rgba(0,0,0,.55);}
  #ctrl{top:12px;right:12px;width:208px;max-height:84vh;overflow:auto;font-size:13px;}
  #ctrl h3{margin:0 0 8px;font-size:14px;color:#fff;}
  #ctrl .row{display:flex;align-items:center;gap:6px;margin:3px 0;cursor:pointer;}
  #ctrl input[type=text]{width:100%;box-sizing:border-box;padding:6px 8px;border-radius:6px;
        border:1px solid #555;background:#2a2a2a;color:#eee;margin-bottom:8px;font-size:13px;}
  .toggle{padding:7px 8px;margin:4px 0 8px;background:#0e639c;border:none;color:#fff;
        border-radius:6px;cursor:pointer;font-size:12px;width:100%;}
  .toggle:hover{background:#1177bb;}
  .sec{margin:10px 0 4px;font-size:12px;color:#9cdcfe;border-top:1px solid #3a3a3a;padding-top:8px;}
  .swatch{width:12px;height:12px;border-radius:50%;flex:0 0 auto;}
  .star{color:#ff3b30;font-size:14px;line-height:12px;}
  #about{bottom:10px;left:10px;font-size:11px;max-width:280px;transition:max-height .3s ease;overflow:hidden;
        max-height:28px;border-radius:8px;}
  #about.open{max-height:320px;overflow:auto;}
  #about .ab-head{display:flex;align-items:center;gap:4px;cursor:pointer;padding:5px 10px;
        user-select:none;color:#9a9a9a;font-size:11px;line-height:1.3;}
  #about .ab-head:hover{color:#ccc;}
  #about .ab-body{padding:0 10px 8px;display:none;border-top:1px solid #3a3a3a;margin-top:0;padding-top:6px;}
  #about.open .ab-body{display:block;}
  #about .ab-body p{margin:3px 0;color:#999;line-height:1.45;}
  #about .ab-body b{color:#ddd;}
  #about .lg{display:flex;flex-wrap:wrap;gap:3px 10px;margin:4px 0;}
  #about .li{display:flex;align-items:center;gap:4px;font-size:11px;color:#bbb;}
  #table{top:70px;left:12px;width:340px;max-height:78vh;overflow:auto;font-size:12px;display:none;}
  #table table{width:100%;border-collapse:collapse;}
  #table th,#table td{border:1px solid #3a3a3a;padding:4px 6px;text-align:center;}
  #table th{background:#333;position:sticky;top:0;color:#fff;cursor:pointer;}
  #table tr:hover{background:#2c2c2c;cursor:pointer;}
  #table .nm{text-align:left;}
  .badge{display:inline-block;padding:1px 6px;border-radius:8px;font-size:10px;font-weight:bold;}
  .b-city{background:#ff3b30;color:#fff;}
  .b-dist{background:#ff8c00;color:#fff;}
  .b-pri{background:#888;color:#fff;}
  .leaflet-popup-content{font-size:13px;}
  .school-label{background:transparent;border:none;color:#111;font-size:11px;font-weight:bold;
        text-shadow:0 0 3px #fff,0 0 3px #fff,0 0 3px #fff;white-space:nowrap;
        pointer-events:auto;cursor:context-menu;}
  .score-tbl{border-collapse:collapse;margin-top:6px;}
  .score-tbl td{border:1px solid #ddd;padding:2px 10px;}
  #links{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:500;}
  .card{position:fixed;z-index:620;width:300px;background:rgba(28,28,30,.97);color:#e6e6e6;
        border:1px solid #555;border-radius:10px;box-shadow:0 4px 18px rgba(0,0,0,.6);font-size:12px;display:none;}
  .card.show{display:block;}
  .card .bar{display:flex;align-items:center;gap:8px;padding:7px 10px;cursor:move;
        background:rgba(255,255,255,.06);border-bottom:1px solid #444;border-radius:10px 10px 0 0;user-select:none;}
  .card .bar .nm{font-weight:bold;color:#fff;flex:1;font-size:13px;}
  .card .bar .pin{cursor:pointer;font-size:16px;line-height:1;filter:grayscale(1);opacity:.55;
        border-radius:50%;padding:2px 3px;transition:all .15s;}
  .card .bar .pin:hover{opacity:1;filter:grayscale(.4);}
  .card .bar .pin.on{filter:none;opacity:1;color:#2ecc71;background:rgba(46,204,113,.22);
        box-shadow:0 0 0 1px rgba(46,204,113,.6);}
  .card .bar .x{cursor:pointer;color:#bbb;font-size:15px;line-height:1;padding:0 2px;}
  .card .body{padding:8px 10px;}
  .card table{width:100%;border-collapse:collapse;margin-top:4px;}
  .card td{border:1px solid #3a3a3a;padding:3px 6px;text-align:center;}
  .card .yr{color:#9cdcfe;text-align:left;}
</style>
</head>
<body>
<div id="map"></div>
<svg id="links"></svg>

<div id="about" class="panel">
  <div class="ab-head" onclick="this.parentNode.classList.toggle('open')">
    <span style="font-size:13px;">ℹ️</span> 天津市区高中分布地图 · <b id="cnt">0</b> 所 · 点击展开
  </div>
  <div class="ab-body">
    <p><b>范围</b>：市内六区 + 海河教育园区</p>
    <p><b>属性</b>：★ 市属 &nbsp; ● 区属 &nbsp; ○ 民办</p>
    <div class="lg">
      <span class="li"><span class="star">★</span> 市属</span>
      <span class="li"><span class="swatch" style="background:#ff8c00;border:2px solid #fff;"></span> 区属</span>
      <span class="li"><span class="swatch" style="background:#fff;border:2px solid #999;"></span> 民办</span>
    </div>
    <p style="margin-top:6px;"><b>数据来源</b>：zhaokao.net 官方录取分数线 PDF（2023-2025）。</p>
    <p style="color:#777;">位次 = 全市累计人数（一分一段表）。数据仅供参考，以官方公布为准。右键学校图标可收藏。</p>
  </div>
</div>

<div id="ctrl" class="panel">
  <h3>筛选</h3>
  <input id="search" type="text" placeholder="搜索学校名称…">
  <div class="sec">按属性</div>
  <div id="levelChecks"></div>
  <div class="sec">收藏</div>
  <label class="row"><input type="checkbox" id="favOnly"> <span style="color:#2ecc71;font-weight:bold;">✓</span> 只看收藏（<span id="favCnt">0</span>）</label>
  <div style="font-size:11px;color:#9a9a9a;margin:2px 0 6px;">提示：在地图上<b style="color:#ccc;">右键点击学校</b>可收藏/取消，收藏后图标带 <span style="color:#2ecc71;">✓</span> 角标。</div>
  <button class="toggle" id="lblBtn">显示全部学校名称</button>
  <button class="toggle" id="tblBtn" style="background:#5a3e8c;">查看分数线数据表</button>
</div>

<div id="table" class="panel">
  <h3 style="margin:0 0 8px;font-size:14px;color:#fff;">录取分数线（历年）</h3>
  <table id="scoreTable">
    <thead><tr><th data-k="name">学校</th><th data-k="level">属性</th><th data-k="s2023">2023<br>分数/位次</th><th data-k="s2024">2024<br>分数/位次</th><th data-k="s2025">2025<br>分数/位次</th></tr></thead>
    <tbody></tbody>
  </table>
</div>

<script>
const D = __DATA__;

// WGS-84 -> GCJ-02（高德坐标系）
function wgs84togcj02(lng, lat){
  const a=6378245.0, ee=0.00669342162296594323;
  const tLat = (x,y)=>{ let r=-100+2*x+3*y+0.2*y*y+0.1*x*y+0.2*Math.sqrt(Math.abs(x))
    +(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3
    +(20*Math.sin(y*Math.PI)+40*Math.sin(y/3*Math.PI))*2/3
    +(160*Math.sin(y/12*Math.PI)+320*Math.sin(y*Math.PI/30))*2/3; return r; };
  const tLng = (x,y)=>{ let r=300+x+2*y+0.1*x*x+0.1*x*y+0.1*Math.sqrt(Math.abs(x))
    +(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3
    +(20*Math.sin(x*Math.PI)+40*Math.sin(x/3*Math.PI))*2/3
    +(150*Math.sin(x/12*Math.PI)+300*Math.sin(x/30*Math.PI))*2/3; return r; };
  let dLat=tLat(lng-105.0,lat-35.0), dLng=tLng(lng-105.0,lat-35.0);
  const radLat=lat/180*Math.PI, magic=Math.sin(radLat);
  let mm=1-ee*magic*magic, sq=Math.sqrt(mm);
  dLat=(dLat*180)/((a*(1-ee))/(mm*sq)*Math.PI);
  dLng=(dLng*180)/(a/sq*Math.cos(radLat)*Math.PI);
  return [lng+dLng, lat+dLat];
}

// 高德路网底图（中文标注，主要道路为主，POI干扰少）
const map = L.map('map',{zoomControl:true}).setView([39.3,117.3],9);
L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
  {subdomains:'1234', maxZoom:18, attribution:'© 高德地图 GS(2023)1234号'}).addTo(map);

const LEVELS=["市属","区属","民办"];

// ---------- 收藏功能（localStorage 持久化）----------
function safeParse(key){ try{ return JSON.parse(localStorage.getItem(key)||'[]'); }catch(_){ return []; } }
let favs = new Set(safeParse('tj_fav_schools'));
function saveFavs(){ localStorage.setItem('tj_fav_schools', JSON.stringify([...favs])); }
function toggleFav(s, marker){
  if(favs.has(s.name)) favs.delete(s.name); else favs.add(s.name);
  saveFavs();
  marker.setIcon(iconFor(s));
  updateFavCount();
  buildTable();
}
function updateFavCount(){
  const el=document.getElementById('favCnt'); if(el) el.textContent=favs.size;
}

// 收藏对勾角标
function checkBadge(){
  return '<div style="position:absolute;top:-7px;right:-7px;width:15px;height:15px;border-radius:50%;'+
    'background:#2ecc71;border:1.5px solid #fff;color:#fff;font-size:11px;line-height:14px;'+
    'text-align:center;font-weight:bold;box-shadow:0 0 4px rgba(0,0,0,.7);z-index:2;">✓</div>';
}
function iconFor(s){
  const fav = favs.has(s.name);
  const badge = fav ? checkBadge() : '';
  if(s.level==="市属"){
    return L.divIcon({className:'', html:'<div style="position:relative;font-size:34px;line-height:24px;color:#ff3b30;'+
      'text-shadow:0 0 4px #000,0 0 4px #000,0 0 8px rgba(255,59,48,.8);">★'+badge+'</div>',
      iconSize:[34,34], iconAnchor:[17,17]});
  }
  if(s.level==="民办"){
    return L.divIcon({className:'', html:'<div style="position:relative;width:16px;height:16px;border-radius:50%;'+
      'background:#fff;border:3px solid #999;box-shadow:0 0 6px rgba(0,0,0,.7);">'+badge+'</div>',
      iconSize:[16,16], iconAnchor:[8,8]});
  }
  return L.divIcon({className:'', html:'<div style="position:relative;width:20px;height:20px;border-radius:50%;background:#ff8c00;'+
    'border:3px solid #fff;box-shadow:0 0 8px rgba(255,140,0,.9),0 0 3px rgba(0,0,0,.8);">'+badge+'</div>',
    iconSize:[20,20], iconAnchor:[10,10]});
}
function fmt(v){ return (v===null||v===undefined) ? '—' : v; }
function badge(level){
  if(level==="市属") return '<span class="badge b-city">市属</span>';
  if(level==="区属") return '<span class="badge b-dist">区属</span>';
  return '<span class="badge b-pri">民办</span>';
}

// ---------- 学校标记 ----------
const showLabels={val:false};
const markers=[];
D.schools.forEach(s=>{
  const [glng,glat]=wgs84togcj02(s.lng,s.lat);
  const marker=L.marker([glat,glng],{icon:iconFor(s)});
  marker.bindTooltip(s.name,{direction:'top',offset:[0,-6]});
  marker.on('click',()=>openCard(m));
  marker.on('contextmenu',e=>{ L.DomEvent.preventDefault(e); toggleFav(s,marker); });
  marker.addTo(map);
  const label=L.marker([glat,glng],{icon:L.divIcon({className:'school-label',html:s.name,iconSize:[0,0],iconAnchor:[0,0]}),interactive:true,zIndexOffset:1000});
  label.on('contextmenu',e=>{ L.DomEvent.preventDefault(e); toggleFav(s,marker); });
  label.on('click',()=>openCard(m));
  label.addTo(map);
  const m={marker,label,s,glat,glng};
  markers.push(m);
});

// ---------- 学校详情浮窗（钉住 + 拖动 + 连线）----------
const linksSvg=document.getElementById('links');
const SVGNS='http://www.w3.org/2000/svg';
let cards=[];
const pinnedCardNames=new Set(safeParse('tj_pin_cards'));
function scoreRow(y,sc,rk){ return '<tr><td class="yr">'+y+'</td><td>'+fmt(sc)+'</td><td>位次</td><td>'+fmt(rk)+'</td></tr>'; }
function openCard(m){
  const s=m.s;
  let c=cards.find(c=>c.name===s.name);
  if(c){ c.el.classList.add('show'); bringFront(c); return; }
  cards.filter(c=>!c.pinned).forEach(closeCard);
  createCard(m);
}
function createCard(m){
  const s=m.s;
  const el=document.createElement('div'); el.className='card';
  const on=pinnedCardNames.has(s.name);
  const pinTitle=on?'已钉住（点击取消钉住并关闭）':'钉住/取消钉住（固定显示此学校）';
  el.innerHTML='<div class="bar"><span class="pin'+(on?' on':'')+'" title="'+pinTitle+'">📌</span>'+
    '<span class="nm">'+s.name+'</span><span class="x" title="关闭">✕</span></div>'+
    '<div class="body">'+badge(s.level)+' &nbsp;'+s.dist+
    '<table>'+scoreRow('2023',s.s2023,s.r2023)+scoreRow('2024',s.s2024,s.r2024)+scoreRow('2025',s.s2025,s.r2025)+'</table></div>';
  document.body.appendChild(el);
  const pt=map.latLngToContainerPoint([m.glat,m.glng]);
  let x=pt.x+24, y=pt.y-24;
  x=Math.max(8,Math.min(x,window.innerWidth-318));
  y=Math.max(8,Math.min(y,window.innerHeight-230));
  el.style.left=x+'px'; el.style.top=y+'px';
  const c={name:s.name,s,m,el,pinned:on,x,y};
  el.querySelector('.pin').onclick=()=>togglePin(c);
  el.querySelector('.x').onclick=()=>closeCard(c);
  enableDrag(c);
  cards.push(c); el.classList.add('show');
  drawLinks(); bringFront(c);
  return c;
}
function togglePin(c){
  c.pinned=!c.pinned;
  if(c.pinned){
    pinnedCardNames.add(c.name);
    c.el.querySelector('.pin').classList.add('on');
    c.el.querySelector('.pin').title='已钉住（点击取消钉住并关闭）';
  }else{
    pinnedCardNames.delete(c.name);
    c.el.querySelector('.pin').classList.remove('on');
    c.el.querySelector('.pin').title='钉住/取消钉住（固定显示此学校）';
  }
  localStorage.setItem('tj_pin_cards',JSON.stringify([...pinnedCardNames]));
  drawLinks();
  if(!c.pinned) closeCard(c);
}
function closeCard(c){
  if(c.el&&c.el.parentNode) c.el.parentNode.removeChild(c.el);
  cards=cards.filter(x=>x!==c);
  drawLinks();
}
function bringFront(c){ cards.forEach(x=>x.el.style.zIndex=620); c.el.style.zIndex=630; }
function enableDrag(c){
  const bar=c.el.querySelector('.bar');
  let drag=false,sx=0,sy=0,ox=0,oy=0;
  bar.addEventListener('pointerdown',e=>{
    if(e.target.closest('.pin')||e.target.closest('.x')) return; // 图钉/关闭按钮独立响应点击，不触发拖动
    drag=true; sx=e.clientX; sy=e.clientY; ox=c.x; oy=c.y; bar.setPointerCapture(e.pointerId); e.preventDefault();
  });
  bar.addEventListener('pointermove',e=>{ if(!drag) return; c.x=ox+(e.clientX-sx); c.y=oy+(e.clientY-sy);
    c.x=Math.max(4,Math.min(c.x,window.innerWidth-c.el.offsetWidth-4));
    c.y=Math.max(4,Math.min(c.y,window.innerHeight-c.el.offsetHeight-4));
    c.el.style.left=c.x+'px'; c.el.style.top=c.y+'px'; drawLinks(); });
  bar.addEventListener('pointerup',e=>{ drag=false; try{bar.releasePointerCapture(e.pointerId);}catch(_){} });
  bar.addEventListener('pointercancel',e=>{ drag=false; });
}
function drawLinks(){
  while(linksSvg.firstChild) linksSvg.removeChild(linksSvg.firstChild);
  cards.forEach(c=>{
    const pt=map.latLngToContainerPoint([c.m.glat,c.m.glng]);
    const ln=document.createElementNS(SVGNS,'line');
    ln.setAttribute('x1',pt.x); ln.setAttribute('y1',pt.y);
    ln.setAttribute('x2',c.x); ln.setAttribute('y2',c.y+c.el.offsetHeight/2);
    ln.setAttribute('stroke',c.pinned?'#2ecc71':'#ffd479');
    ln.setAttribute('stroke-width',c.pinned?2.5:1.8);
    if(!c.pinned) ln.setAttribute('stroke-dasharray','6,4');
    linksSvg.appendChild(ln);
    const dot=document.createElementNS(SVGNS,'circle');
    dot.setAttribute('cx',pt.x); dot.setAttribute('cy',pt.y); dot.setAttribute('r',3.5);
    dot.setAttribute('fill',c.pinned?'#2ecc71':'#ffd479');
    linksSvg.appendChild(dot);
  });
}
map.on('move zoom zoomend movestart',drawLinks);
window.addEventListener('resize',drawLinks);

// ---------- 控件 ----------
const lc=document.getElementById('levelChecks');
LEVELS.forEach(l=>{
  const row=document.createElement('label'); row.className='row';
  const sym = l==="市属"?'<span class="star">★</span>':(l==="民办"?'<span class="swatch" style="background:#fff;border:2px solid #999;"></span>':'<span class="swatch" style="background:#ff8c00;"></span>');
  row.innerHTML = sym+'<input type="checkbox" data-l="'+l+'" checked> '+l;
  lc.appendChild(row);
});
function applyFilter(){
  const q=document.getElementById('search').value.trim();
  const favOnly=document.getElementById('favOnly').checked;
  const actL={}; document.querySelectorAll('#levelChecks input').forEach(c=>actL[c.dataset.l]=c.checked);
  let shown=0;
  markers.forEach(m=>{
    const okL=actL[m.s.level];
    const okQ=!q||m.s.name.includes(q);
    const okF=!favOnly||favs.has(m.s.name);
    const vis=okL&&okQ&&okF;
    if(vis){
      shown++;
      if(!map.hasLayer(m.marker)) m.marker.addTo(map);
      if(m.label&&!map.hasLayer(m.label)) m.label.addTo(map);
    }else{
      if(map.hasLayer(m.marker)) m.marker.removeFrom(map);
      if(m.label&&map.hasLayer(m.label)) m.label.removeFrom(map);
    }
  });
  document.getElementById('cnt').textContent=shown;
  buildTable();
}
let tableOrder=null;
function buildTable(){
  const q=document.getElementById('search').value.trim();
  const favOnly=document.getElementById('favOnly').checked;
  const actL={}; document.querySelectorAll('#levelChecks input').forEach(c=>actL[c.dataset.l]=c.checked);
  const src=tableOrder||markers;
  const tb=document.querySelector('#scoreTable tbody'); tb.innerHTML='';
  src.filter(m=>actL[m.s.level]&&(!q||m.s.name.includes(q))&&(!favOnly||favs.has(m.s.name)))
    .forEach(m=>{
      const s=m.s;
      const tr=document.createElement('tr');
      const favMark=favs.has(s.name)?'<span style="color:#2ecc71;font-weight:bold;" title="已收藏">✓</span> ':'';
      tr.innerHTML='<td class="nm">'+favMark+s.name+'</td><td>'+badge(s.level)+'</td>'+
        '<td style="text-align:center">'+fmt(s.s2023)+'<br><small>（'+fmt(s.r2023)+'）</small></td>'+
        '<td style="text-align:center">'+fmt(s.s2024)+'<br><small>（'+fmt(s.r2024)+'）</small></td>'+
        '<td style="text-align:center">'+fmt(s.s2025)+'<br><small>（'+fmt(s.r2025)+'）</small></td>';
      tr.onclick=()=>{ openCard(m); };
      tb.appendChild(tr);
    });
}

document.querySelectorAll('#levelChecks input').forEach(c=>c.addEventListener('change',applyFilter));
document.getElementById('search').addEventListener('input',applyFilter);
document.getElementById('favOnly').addEventListener('change',applyFilter);
document.getElementById('lblBtn').addEventListener('click',e=>{
  showLabels.val=!showLabels.val;
  e.target.textContent=showLabels.val?'隐藏全部学校名称':'显示全部学校名称';
  applyFilter();
});
document.getElementById('tblBtn').addEventListener('click',e=>{
  const t=document.getElementById('table');
  const open=t.style.display!=='block';
  t.style.display=open?'block':'none';
  e.target.textContent=open?'关闭分数线数据表':'查看分数线数据表';
  if(open) buildTable();
});
let sortKey='name', sortAsc=true;
document.querySelectorAll('#scoreTable th').forEach(th=>{
  th.onclick=()=>{
    const k=th.dataset.k; if(k===sortKey) sortAsc=!sortAsc; else {sortKey=k;sortAsc=true;}
    tableOrder=markers.slice().sort((A,B)=>{
      let va=A.s[k],vb=B.s[k];
      if(k==='name'||k==='level'){va=''+(va||'');vb=''+(vb||'');return sortAsc?va.localeCompare(vb):vb.localeCompare(va);}
      if(va===null)va=-1; if(vb===null)vb=-1;
      return sortAsc?va-vb:vb-va;
    });
    buildTable();
  };
});

const all=L.featureGroup(markers.map(m=>m.marker));
map.fitBounds(all.getBounds().pad(0.08));
updateFavCount();
applyFilter();
pinnedCardNames.forEach(nm=>{ const m=markers.find(x=>x.s.name===nm); if(m) createCard(m); });
</script>
</body>
</html>"""

html = html.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
with open(r"C:\Users\ALTC\WorkBuddy\2026-07-09-11-29-25\天津市高中地图.html", "w", encoding="utf-8") as f:
    f.write(html)

n_city = sum(1 for s in SCHOOLS if s[4]=="市属")
n_dist = sum(1 for s in SCHOOLS if s[4]=="区属")
n_pri  = sum(1 for s in SCHOOLS if s[4]=="民办")
n25 = sum(1 for s in SCHOOLS if s[7] is not None or s[0] in EXCEL_2025)
print("学校:", len(SCHOOLS), "| 市属:", n_city, "区属:", n_dist, "民办:", n_pri, "| 2025有数据:", n25, "(含Excel覆盖)")
