# 新区域接入指南（下层金库 / 黯原 / 时隙废都）

本 fork 已完成的数据与代码工作：

| 项 | 状态 |
|---|---|
| 点位数据（官方 3.5 快照） | ✅ itemsData_UnderVault / DarkPlain / TimeRift.json |
| scene 注册（sceneId 6/7/8） | ✅ Scene / DrawItemBase / MapCoordinate / RelativeCoordinates / 资源 |
| 缺失图标 | ✅ 33 个来自官方 CDN，已挂载 .rc |
| 地图地形（NEW MAP.png） | ❌ 作者 2025-12 版不含这 3 个区域 |
| 特征文件（Map_features.yml） | ❌ 作者 2026-01 版只覆盖旧区域 |
| 原点标定（OriginCoordinates） | ❌ 当前为 0 占位，必须游戏内标定 |

原因：这三个区域在官方地图是**独立瓦片集 + 局部坐标系**（`mcmap/tiles/<hash>/909/909_{x}_{y}.png` 等），
不在地表综合地图（`8_{x}_{y}`）上。IMao 的定位依赖单张 `NEW MAP.png` 的特征匹配，
所以新区域要能定位必须把瓦片拼进地图并标定原点（作者对泰缇斯/阿维纽林也是这么做的）。

## 三步接入

### 1. 拼图（把新区域瓦片拼入 NEW MAP.png）

新区域瓦片源（1024×1024，官方 CDN，hash 从 getMapResource 拿最新值）：

```
https://web-static.kurobbs.com/mcmap/tiles/<hash>/909/909_{x}_{y}.png   # 黯原
https://web-static.kurobbs.com/mcmap/tiles/<hash>/910/910_{x}_{y}.png   # 时隙废都
https://web-static.kurobbs.com/mcmap/tiles/<hash>/902/902_{x}_{y}.png   # 下层金库（目录名待确认）
```

流程（参照作者 Test/main.cpp 的做法）：
1. 下载新区域全部瓦片（黯原约 3×3 张即可覆盖，从 position 坐标范围换算）
2. 在 `NEW MAP.png` 的空白区域（如右下角）按网格贴入
3. 记录新区域瓦片 (0,0) 在整图中的像素位置 P0

### 2. 重新生成特征

```bash
# conda-forge opencv 4.x（含 SURF）
conda create -n wuwa -c conda-forge python=3.11 opencv=4.10.0
python scripts/gen_map_features.py "NEW MAP.png" Map_features.yml
```

替换 `Assets/FeaturesDatas/Map_features.yml`（注意：文件 ~500MB，运行时加载较慢属正常）。

### 3. 游戏内标定原点

1. 在游戏里传送到新区域（如黯原），把角色移动到坐标 (0, 0) 附近
   （左下角坐标显示接近 0,0；新区域坐标是局部坐标，直接看游戏内显示即可）
2. 打开 IMao，让小地图定位成功（右下角提示消失、地图上有叠加）
3. 把此时 IMao 界面里你所在位置的地图坐标，写入：
   `IMao-Core/src/Coordinate/CoordinateStruct.h`
   ```cpp
   struct UnderVaultOriginCoordinates { inline static double x = <标定值>; inline static double y = <标定值>; };
   struct DarkPlainOriginCoordinates  { inline static double x = <标定值>; inline static double y = <标定值>; };
   struct TimeRiftOriginCoordinates   { inline static double x = <标定值>; inline static double y = <标定值>; };
   ```
4. 重新编译，玩家站到新区域 (0,0) 时，叠加点位应与游戏内实际位置重合（误差 ±5px 内）

## 标定原理

IMao 坐标映射：`Map.png 像素 = 局部坐标 × 1.205 + OriginCoordinates`。
现有区域的 origin（如 World=(2474,1957)、Tethys=(8593,1382)）就是作者当年在游戏内
站到 (0,0) 标出来的。新区域同理——必须先有地图地形和特征，才能标定。

## 验证清单

- [ ] 新区域瓦片已拼入 Map.png（肉眼可见地形，非空白）
- [ ] 生成的 Map_features.yml 能被程序加载（右下角无 Resource loading failed）
- [ ] 游戏内站到新区域 (0,0)，IMao 定位成功且点位叠加正确
- [ ] 旧区域（瑝珑/黎那汐塔/罗伊冰原等）定位不受影响（拼图不能移动旧区域位置）
