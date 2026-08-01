# 新区域支持状态

## 已可直接使用（2026-08 数据验证）

| 区域 | stateId | 状态 |
|---|---|---|
| 黯原 | 909 | ✅ 点位为世界坐标，已并入 itemsData_World.json；Map.png 地形 + 特征均已存在 |
| 时隙废都 | 910 | ✅ 同上 |
| 下层金库 | 902 | ⚠️ 地下独立坐标系，暂无法在地图显示（见下） |

验证方法：对 909/910 的官方点位用世界映射 `x/100×1.205+WorldOrigin` 投影到
`NEW MAP.png`，点位落在有内容区域的比例分别为 82.7% / 100%，远高于其他候选映射。

## 下层金库（902）接入步骤

下层金库是黎那汐塔地下的独立场景（countryId=3），坐标不是世界坐标，
`NEW MAP.png` 中也没有对应地形。要支持它需要：

1. **确认官方地下瓦片**：`mcmap/tiles/<hash>/902/` 目录当前 404，需确认地下层瓦片的真实路径
   （可能是分楼层资源，参考 `area.json` 中的 `layeredMapId`/`floorId` 字段）
2. **拼图**：把下层金库瓦片拼入 `NEW MAP.png` 空白区域，记录 (0,0) 位置
3. **特征**：用 `scripts/gen_features.cpp` 从更新后的地图重新生成 `Map_features.yml`
   （注意：全图提取会 OOM，脚本已分块处理；生成约 27 万特征点 / 128 维描述子）
4. **标定**：游戏内站到下层金库 (0,0)，把地图位置写入
   `CoordinateStruct.h::UnderVaultOriginCoordinates`（当前 0 占位）

## 编译特征生成器（Linux）

```bash
# 需要 OpenCV with NONFREE（SURF）
# 1. 编译 OpenCV 4.10: cmake -DOPENCV_ENABLE_NONFREE=ON -DBUILD_LIST=core,imgproc,imgcodecs,features2d,flann,calib3d,xfeatures2d
# 2. 编译:
g++ -O2 scripts/gen_features.cpp -o gen_features \
  -I<opencv>/build -I<opencv>/include -I<opencv>/modules/core/include -I<opencv>/modules/imgproc/include \
  -I<opencv>/modules/imgcodecs/include -I<opencv>/modules/features2d/include -I<opencv>/modules/flann/include -I<opencv>/modules/calib3d/include \
  -I<opencv_contrib>/modules/xfeatures2d/include \
  -L<opencv>/build/lib -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lopencv_features2d -lopencv_xfeatures2d -lopencv_flann -lopencv_calib3d \
  -Wl,-rpath,<opencv>/build/lib
./gen_features "NEW MAP.png" Map_features.yml 2048
```
