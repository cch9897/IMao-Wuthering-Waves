[简中](README.md) | [EN](README.en.md) 

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
2.  前往[Releases](https://github.com/Yepin2022/IMao-Wuthering-Waves/releases)下载最新版 解压后运行IMao-WinUI.exe
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
| itemsData_World.json | 瑝珑/黑海岸/黎那汐塔/罗伊冰原 + 黯原 + 时隙废都 | 451 | 19912 | ✅ 可直接使用 |
| itemsData_Tethys.json | 泰缇斯之底 | 40 | 415 | ✅ |
| itemsData_UnderVault.json | 下层金库 | 37 | 238 | ⚠️ 地下独立坐标系，暂无法定位 |
| itemsData_Avinoleum.json | 阿维纽林 | 31 | 462 | ✅ |
| itemsData_Fabricatorium.json | 隐海试验场 | 35 | 236 | ✅ |
| itemsData_Lahai.json | 罗伊冰原 | 74 | 2535 | ✅ |
| itemsData_DarkPlain.json | 黯原（已并入 World） | 43 | 673 | ✅ 并入 World |
| itemsData_TimeRift.json | 时隙废都（已并入 World） | 9 | 59 | ✅ 并入 World |

- 重新拉取最新数据：`python3 scripts/gen_itemsdata.py`（依赖库街区互动地图的静态资源，脚本内有数据源说明）
- **黯原（909）/ 时隙废都（910）**：经验证其点位为世界坐标（`Map.png` 中对应区域地形与特征均已存在），已并入 `itemsData_World.json`，可直接在地图上显示
- **下层金库（902）**：官方将其作为地下独立坐标系管理（`countryId=3` 黎那汐塔地下，非世界坐标），`Map.png` 无对应地形，暂无法定位显示。数据文件保留（sceneId 6 已注册，origin 为 0 占位），待作者将地下瓦片拼入地图并标定后启用
- 特征文件（`Map_features.yml`）：作者 2026-01 版已覆盖黯原/时隙废都区域（黯原区 1094 个特征点），无需更新；如未来拼入新地图可用 `scripts/gen_features.cpp` 重新生成

### 修复记录
- OCR 坐标解析放宽：允许 OCR 多文本块、置信度阈值 0.85→0.70、兼容 1~2 个分隔符（对应 #10 Win11 双屏/4K 下坐标识别失败场景）
- OCR 失败时输出诊断日志（Debug 模式）：`[IMao] OCR coords failed. blocks=N | 'text'(score=...)`
- 修正 `DrawItemBase::ClearItemData` 遗漏 Fabricatorium 区域清理的缺陷
- 补齐新区域缺失的 33 个点位图标（来自官方 CDN），资源名与文件均已在 `.rc`/`resource.h` 注册
