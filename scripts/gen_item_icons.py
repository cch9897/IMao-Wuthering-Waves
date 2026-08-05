#!/usr/bin/env python3
"""同步缺失的点位图标到 IMao-Core 资源, 并注册到 .rc / resource.h。

用法:
    python3 scripts/gen_item_icons.py                 # 全流程: 对比 -> 下载 -> 注册
    python3 scripts/gen_item_icons.py --offline-dir DIR  # 只注册, 图标从 DIR 取(跳过下载)

图标 URL 规则(库街区官方互动地图):
    itemsData 中 icon 字段为相对路径(如 adminConfig/52/props_namephoto/xxx.png),
    完整地址 = https://web-static.kurobbs.com/ + 相对路径

注意:
    - IMao-Core.rc 为 UTF-16LE 编码, 特殊字符 typeId(+、·)使用引号资源名
    - resource.h 只追加合法 C++ 标识符条目(特殊字符 typeId 无法表示, 仅注册 .rc)
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(ROOT, "IMao-Core", "src", "Resource")
IMG_DIR = os.path.join(RES_DIR, "itemImages")
RC_PATH = os.path.join(ROOT, "IMao-Core", "src", "IMao-Core.rc")
RESH_PATH = os.path.join(ROOT, "IMao-Core", "src", "resource.h")
ICON_BASE = "https://web-static.kurobbs.com/"

DATA_FILES = [
    "itemsData_World.json",
    "itemsData_Tethys.json",
    "itemsData_Avinoleum.json",
    "itemsData_Fabricatorium.json",
    "itemsData_Lahai.json",
]

IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")


def load_type_icons():
    """typeId -> icon 相对路径"""
    out = {}
    for fname in DATA_FILES:
        with open(os.path.join(RES_DIR, fname), encoding="utf-8-sig") as f:
            for item in json.load(f):
                icon = item.get("icon", "")
                if icon:
                    out[item["id"]] = icon
    return out


def rc_registered():
    with open(RC_PATH, encoding="utf-16") as f:
        text = f.read()
    return set(re.findall(r'"?IDB_PNG_([^\s"]+)"?\s+PNG', text))


def download(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def main():
    offline_dir = None
    if "--offline-dir" in sys.argv:
        offline_dir = sys.argv[sys.argv.index("--offline-dir") + 1]

    icons = load_type_icons()
    registered = rc_registered()
    missing = sorted(set(icons) - registered)
    if not missing:
        print("没有缺失图标, 无需处理")
        return

    print(f"缺失 {len(missing)} 个图标资源")

    os.makedirs(IMG_DIR, exist_ok=True)
    ok_ids = []
    for tid in missing:
        rel = icons[tid]
        target = os.path.join(IMG_DIR, tid + ".png")
        if not os.path.exists(target):
            if offline_dir:
                src = os.path.join(offline_dir, tid + ".png")
                if not os.path.exists(src):
                    print(f"  SKIP {tid}: offline 目录无 {tid}.png")
                    continue
                with open(src, "rb") as fin, open(target, "wb") as fout:
                    fout.write(fin.read())
                print(f"  COPY {tid}")
            else:
                try:
                    data = download(ICON_BASE + rel)
                    if data[:8] != b"\x89PNG\r\n\x1a\n":
                        print(f"  SKIP {tid}: 下载内容不是 PNG ({len(data)}B)")
                        continue
                    with open(target, "wb") as fout:
                        fout.write(data)
                    print(f"  DOWNLOAD {tid}")
                except Exception as e:
                    print(f"  SKIP {tid}: {e}")
                    continue
        ok_ids.append(tid)

    if not ok_ids:
        print("没有可注册的图标")
        return

    # ---- 注册 .rc(UTF-16LE; 特殊字符 typeId 用引号资源名) ----
    with open(RC_PATH, encoding="utf-16") as f:
        rc = f.read()
    lines = rc.split("\n")
    last_png = max(i for i, l in enumerate(lines) if re.search(r"PNG\s+\"Resource", l))
    new_entries = []
    for tid in ok_ids:
        if IDENT_RE.match(tid):
            name = f"IDB_PNG_{tid}".ljust(30)
        else:
            name = f'"IDB_PNG_{tid}"'.ljust(31)
        new_entries.append(f"{name} PNG  \"Resource\\\\itemImages\\\\{tid}.png\"")
    lines[last_png + 1:last_png + 1] = new_entries
    with open(RC_PATH, "w", encoding="utf-16", newline="\n") as f:
        f.write("\n".join(lines))
    print(f".rc 追加 {len(new_entries)} 条")

    # ---- 注册 resource.h(只追加合法标识符; 编号顺延) ----
    with open(RESH_PATH, encoding="utf-8-sig") as f:
        resh = f.read()
    ids = [int(m) for m in re.findall(r"constexpr auto IDB_PNG_\S+\s*=\s*(\d+);", resh)]
    next_id = max(ids) + 1 if ids else 533
    add = []
    for tid in ok_ids:
        if IDENT_RE.match(tid):
            add.append(f"constexpr auto IDB_PNG_{tid} = {next_id};")
            next_id += 1
    if add:
        if not resh.endswith("\n"):
            resh += "\n"
        resh += "\n".join(add) + "\n"
        with open(RESH_PATH, "w", encoding="utf-8-sig", newline="\n") as f:
            f.write(resh)
        print(f"resource.h 追加 {len(add)} 条")


if __name__ == "__main__":
    main()
