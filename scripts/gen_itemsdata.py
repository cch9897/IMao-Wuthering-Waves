#!/usr/bin/env python3
"""从库街区官方互动地图数据生成 IMao itemsData JSON。

用法: python3 gen_itemsdata.py [--out DIR] [--report]
数据源: /tmp/wuwa_imao/position_<stateId>.json (官方 mcmap/position API)
映射:   /tmp/wuwa_imao/catalog_id_map.json (catalog.json 的 typeId -> name/icon)
"""
import json, os, sys, datetime

# stateId -> IMao 文件名
STATE_FILES = [
    (8,   "itemsData_World.json",        "瑝珑/黑海岸/黎那汐塔/罗伊冰原 综合"),
    (900, "itemsData_Tethys.json",       "泰缇斯之底"),
    (902, "itemsData_UnderVault.json",   "下层金库 (新)"),
    (903, "itemsData_Avinoleum.json",    "阿维纽林"),
    (905, "itemsData_Fabricatorium.json","隐海试验场"),
    (906, "itemsData_Lahai.json",        "罗伊冰原"),
    (909, "itemsData_DarkPlain.json",    "黯原 (新)"),
    (910, "itemsData_TimeRift.json",     "时隙废都 (新)"),
]

SRC_DIR = "/tmp/wuwa_imao"
ID_MAP_PATH = f"{SRC_DIR}/catalog_id_map.json"
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "IMao-Core", "src", "Resource")

def main():
    with open(ID_MAP_PATH, encoding="utf-8") as f:
        id_map = json.load(f)

    report = []
    for state_id, fname, label in STATE_FILES:
        src = f"{SRC_DIR}/position_{state_id}.json"
        if not os.path.exists(src):
            report.append(f"SKIP {fname}: {src} 不存在")
            continue
        with open(src, encoding="utf-8") as f:
            data = json.load(f)

        # 转换: 补 name、x/y 转 int
        items = []
        total_locs = 0
        for item in data:
            iid = item.get("id", "")
            meta = id_map.get(iid, {})
            locs = []
            for loc in item.get("location", []):
                nl = dict(loc)
                # 坐标转整数（官方 float -> int）
                nl["x"] = int(round(float(nl["x"])))
                nl["y"] = int(round(float(nl["y"])))
                locs.append(nl)
                total_locs += 1
            items.append({
                "icon": item.get("icon", ""),
                "id": iid,
                "name": meta.get("name") or item.get("name") or iid,
                "location": locs,
            })

        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8-sig") as f:
            json.dump(items, f, ensure_ascii=False, indent=1)
        report.append(f"{fname:<32} {len(items):>4} items, {total_locs:>6} locations  <- state {state_id} ({label})")

    print("\n".join(report))
    print(f"\n输出目录: {OUT_DIR}")

if __name__ == "__main__":
    main()
