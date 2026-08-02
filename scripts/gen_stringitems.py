#!/usr/bin/env python3
"""从库街区官方数据生成 StringItems.json（Filter 页面分类）。

分组规则（按玩家需求：星声奖励 > 收集物 > 敌人 > 其他）：
1. 星声奖励: 奇藏箱/潮汐之遗/声匣/终声残卷 + 副本挑战 + 地图探索(信标/挑战/藏宝地等)
2. 收集物:   采集物 + 收集道具(定风铎/隙声蝶/观景点/无主的梁鸢等)
3. 敌人/强敌: 大地图-敌人/强敌/BOSS
4. 其他:     NPC/武器/角色等

用法: python3 gen_stringitems.py <catalog.json> <out.json>
"""
import json, os, sys
from collections import OrderedDict

def main():
    catalog_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/wuwa_imao/catalog_id_map.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "StringItems.json"

    with open(catalog_path, encoding="utf-8") as f:
        catalog = json.load(f)

    # 收集 position 里实际出现的 typeId（避免把不在地图上的类型也加进来）
    pos_dir = os.path.dirname(catalog_path)
    used_ids = set()
    for st in [8, 900, 902, 903, 905, 906, 909, 910]:
        p = os.path.join(pos_dir, f"position_{st}.json")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            used_ids.add(item.get("id", ""))

    groups = OrderedDict([
        ("星声奖励", []),
        ("收集物", []),
        ("敌人/强敌", []),
        ("其他", []),
    ])

    def group_of(k):
        v = catalog.get(k, {})
        tn = v.get("tableName", "")
        # 宝箱/声匣/残卷 → 星声奖励
        if k.startswith(("qzx_", "cx_", "sx")) or k == "zscj":
            return "星声奖励"
        if tn == "大地图-地图探索" or tn == "大地图-副本挑战":
            return "星声奖励"
        if tn == "大地图-采集物" or tn == "大地图-收集道具":
            return "收集物"
        if tn in ("大地图-敌人", "大地图-强敌", "大地图-BOSS"):
            return "敌人/强敌"
        return "其他"

    for k in sorted(used_ids):
        if not k:
            continue
        v = catalog.get(k, {})
        name = v.get("name", "") or k
        g = group_of(k)
        groups[g].append((k, name))

    # 星声奖励组内排序: 宝箱(qzx/cx/sx/zscj)最前, 其余按名称
    def is_chest(k):
        return k.startswith("qzx_") or k.startswith("cx_") or k == "zscj" or k == "sx" or k.startswith("sx·")

    def sort_key(g, item):
        k, name = item
        if g == "星声奖励":
            if is_chest(k):
                return (0, name)
            return (1, name)
        return (0, name)

    result = OrderedDict()
    for g, items in groups.items():
        items.sort(key=lambda it: sort_key(g, it))
        result[g] = OrderedDict((k, {"zh-CN": name}) for k, name in items)

    with open(out_path, "w", encoding="utf-8-sig") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    for g, items in groups.items():
        print(f"{g}: {len(items)} 项")
    print(f"输出: {out_path}")

if __name__ == "__main__":
    main()
