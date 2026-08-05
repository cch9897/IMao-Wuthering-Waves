[简中](README.md) | [EN](README.en.md) 

> ## ⚠️ 本仓库为 Fork 增强版（LLM 辅助修改）
>
> 本仓库 fork 自 [Yepin2022/IMao-Wuthering-Waves](https://github.com/Yepin2022/IMao-Wuthering-Waves)（上游最后更新于 2026-02，v1.0.2），
> 在原作者基础上由 **LLM（AI 助手）辅助分析、修改与构建**，主要增强：
>
> | 类别 | 内容 |
> |---|---|
> | 点位数据 | 全量更新至 **3.5 版本**（梦州·玄方地界等），官方库街区数据源自动生成 |
> | 地图支持 | 扩展地图覆盖 **梦州/黯原/时隙废都**，重新生成 SURF 特征（含新区域） |
> | 大地图定位 | 修复 v2 地图下多区域锚点匹配失败的问题（多锚点搜索） |
> | OCR 修复 | 放宽坐标解析（对应上游 issue #10，4K/缩放场景） |
> | 过滤器 | 按官方数据全量重建分类（525 类型），星声奖励/收集物/敌人/其他 分组可折叠 |
> | 打包交付 | GitHub Actions 自动构建，**.NET 自包含**（无需安装运行环境）、WinUI 3 自包含、Paddle 推理内置 |
> | 更新通道 | 指向本 fork（不再误报上游旧版更新） |
>
> 使用 **本仓库 Releases**（上游 1.0.2 为旧版）：https://github.com/cch9897/IMao-Wuthering-Waves/releases

### 介绍
一款叠加在游戏窗口上的交互地图，借助图像匹配技术，实时同步玩家位置，减少玩家在探索过程中来回切换游戏与地图工具的操作次数。

### 功能演示
<details>
  <summary>小地图导航</summary>
  <img src="https://github.com/user-attachments/assets/058fec38-70c2-4fb9-9be5-4594970c7dce"/>
</details>

<details>
  <summary>交互式大地图</summary>
  <img src="https://github.com/user-attachments/assets/22ba7107-3640-4fc3-9a25-f030ab5106ef"/>
</details>

<details>
  <summary>路线指引</summary>
  <img src="https://github.com/user-attachments/assets/765c7e9b-bb05-46a7-8ece-64e5ba67ce27"/>
  <img src="https://github.com/user-attachments/assets/b49999de-c616-4c09-921b-7658eed0085a"/>
</details>

### 使用方法
1.  运行环境准备 [NET 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) 和 [Microsoft Visual C++ 2015-2022 Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
2.  前往[Releases](https://github.com/cch9897/IMao-Wuthering-Waves/releases)下载最新版 解压后运行IMao-WinUI.exe
3.  打开游戏，并将其分辨率调成16:9
4.  在确保游戏左下角坐标清晰显示后单击启动按钮，等待右下角信息消失后，即成功识别到正确的坐标后，在功能页开启需要的功能即可

### 项目依赖（包括但不限于）
* [OpenCV](https://github.com/opencv/opencv)
* [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
* [Win32CaptureSample](https://github.com/robmikh/Win32CaptureSample)
* [ImGui](https://github.com/ocornut/imgui)
* [nlohmann/json](https://github.com/nlohmann/json)
* [CommunityToolkit/Windows](https://github.com/CommunityToolkit/Windows)
* [microsoft-ui-xaml](https://github.com/microsoft/microsoft-ui-xaml)

### 开发
[如何编译项目](Docs/Compile_zh-Hans.md)

### 点位数据更新（2026-08 快照）
点位数据来自库街区《鸣潮》官方互动地图（kurobbs.com/mc/map/），已更新至 3.5 版本：

| 数据文件 | 区域 | 条目数 | 点位总数 | 状态 |
|---|---|---|---|---|
| itemsData_World.json | 瑝珑/黑海岸/黎那汐塔/罗伊冰原 + 黯原 + 时隙废都 + 梦州·玄方地界 | 451 | 19912 | ✅ 可直接使用 |
| itemsData_Tethys.json | 泰缇斯之底 | 40 | 415 | ✅ |
| itemsData_UnderVault.json | 下层金库 | 37 | 238 | ⚠️ 地下独立坐标系，暂无法定位 |
| itemsData_Avinoleum.json | 阿维纽林 | 31 | 462 | ✅ |
| itemsData_Fabricatorium.json | 隐海试验场 | 35 | 236 | ✅ |
| itemsData_Lahai.json | 罗伊冰原 | 74 | 2535 | ✅ |
| itemsData_DarkPlain.json | 黯原（已并入 World） | 43 | 673 | ✅ 并入 World |
| itemsData_TimeRift.json | 时隙废都（已并入 World） | 9 | 59 | ✅ 并入 World |

- 重新拉取最新数据：`python3 scripts/gen_itemsdata.py`（依赖库街区互动地图的静态资源，脚本内有数据源说明）
- **黯原（909）/ 时隙废都（910）**：经验证其点位为世界坐标（`Map.png` 中对应区域地形与特征均已存在），已并入 `itemsData_World.json`，可直接在地图上显示
- **梦州·玄方地界（3.5 新地图）**：点位已在 `itemsData_World.json`（state 8 全量包含 1521 个点位），但原版 `NEW MAP.png`（2025-12）不覆盖梦州区域（世界坐标 x < -205000 落在图外）。本 fork 已：
  1. 生成 **NEW_MAP_v2.png**（29696×19460）：左侧扩展 10 列瓦片拼入梦州（官方瓦片 8_-10..-1）
  2. 更新全部 `*OriginCoordinates`（x 偏移 +8786）——`CoordinateStruct.h` 已改
  3. 验证：梦州点位投影命中地形 94.0%，旧区域 100% 无损
  4. 重新生成 **Map_features_v2.yml**（含梦州特征的 SURF 特征文件）
  5. 地图与特征文件通过 GitHub Releases 分发（仓库体积限制无法放入源码树）
- **下层金库（902）**：官方将其作为地下独立坐标系管理（`countryId=3` 黎那汐塔地下，非世界坐标），`Map.png` 无对应地形，暂无法定位显示。数据文件保留（sceneId 6 已注册，origin 为 0 占位），待作者将地下瓦片拼入地图并标定后启用
- 特征文件（`Map_features.yml`）：作者 2026-01 版已覆盖黯原/时隙废都区域，但**不含梦州**；使用梦州必须替换为 release 中的 `Map_features_v2.yml`
- **安装步骤**（release: `v2-map`）：
  1. 用本 fork 源码编译（`CoordinateStruct.h` 已含 origin 偏移，`e948316` 之后）
  2. 下载 `imao_v2_map.7z`，解压后把 `Map_features_v2.yml` 重命名为 `Map_features.yml`，替换程序 `Assets/FeaturesDatas/` 下的同名文件（IMao 运行时只加载特征文件；`NEW_MAP_v2.png` 是特征生成源图，留档备用）

### 修复记录
- OCR 坐标解析放宽：允许 OCR 多文本块、置信度阈值 0.85→0.70、兼容 1~2 个分隔符（对应 #10 Win11 双屏/4K 下坐标识别失败场景）
- OCR 失败时输出诊断日志（Debug 模式）：`[IMao] OCR coords failed. blocks=N | 'text'(score=...)`
- 修正 `DrawItemBase::ClearItemData` 遗漏 Fabricatorium 区域清理的缺陷
- 补齐新区域缺失的 33 个点位图标（来自官方 CDN），资源名与文件均已在 `.rc`/`resource.h` 注册
- **大地图定位增强**（对应"大地图不显示"问题）：
  - 新增 **空间网格索引**（500px 单元格，Init 时一次性构建），锚点搜索不再每次全量扫描约 200 万特征点
  - 锚点列表加入**小地图跟踪的玩家位置**（打开大地图时地图中心即玩家位置），大幅提升首开命中率
  - 固定锚点全部失败时，按 **4200px 网格轮询全图兜底**（半径 3000 ≥ 网格半对角，任意位置必被覆盖），并在成功后复位；窄搜索失败自动降级，不再因拖动/传送永久失配
  - 窄搜索半径 400→1000，覆盖打开地图时的中心偏移；兜底匹配按响应质量截断至 4096 个特征控制 FLANN 开销
  - 修复 `mapNotMoving` 未初始化（UB，可能导致大地图首帧起不绘制）；大地图打开期间不再被小地图分支缩小覆盖窗口；定位失败提示从每 80ms 刷屏改为首次 + 每约 5 秒一次
- **点位图标全覆盖**:补齐全部 192 个缺失 typeId 的图标（含 12 个含 `+`/`·` 特殊字符 typeId 的引号资源名注册），修复 `Play_04_1` 悬挂注册；新增 `scripts/gen_item_icons.py` 一键同步（对比 → 下载 → 注册 .rc/resource.h）
