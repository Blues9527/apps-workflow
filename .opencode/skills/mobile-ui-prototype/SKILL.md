---
name: mobile-ui-prototype
description: 由 Codex 从 confirmed L1 产出素材需求清单、design tokens 与 5 屏核心原型，用 Stitch MCP 创建设计系统和屏幕，写入 spec-manager L2 与 specs/DESIGN.md，并在 G3 用 5 图锁定 P0；数据与素材使用本地 mock。Use when the user says 素材清单、5 图、5 屏原型、5 图定 P0、Stitch 设计、UI 主题、设计系统、app prototype、asset manifest，or asks to turn a PRD into screens before development.
---

# 素材清单与 5 图原型

目标：把 PRD 变成可开发的设计资产：一套 tokens、一份素材清单、5 屏高保真原型，并用这 5 屏**锁定 P0 边界**。

## 输入

- confirmed L1（spec-manager，源；含新产品 `app_name`）
- `artifacts/02-prd/prd.md`（P0 草案与验收标准，L1 阅读副本）
- `artifacts/02-prd/theme.md`（基于目标 App 的二创主题、视觉关键词）
- `artifacts/01-feature-spec/screens.md`（目标 App 的页面与状态）
- 目标 App 的公开截图（保持信息架构与核心闭环相似）
- 品牌资产（logo、色值、字体），没有则明确「待定」
- 参考站点（awwwards 等），只提取风格思路
- 数据策略：本地 mock 数据与 mock 资产

若 L1 来自已有 PRD 且没有目标 App：以 PRD、用户提供的截图/品牌资产为设计参考；不要假装分析过原 App。

## Codex + spec-manager 模式（默认）

本阶段由 **Codex** 执行，产出写入 spec-manager **L2**；人类确认后 OpenCode 才能写 L3/代码。

开始前：

```bash
spec-manager brief "设计系统 + 5 图 + P0 锁定" --topic <topic>
spec-manager spec show <L1> --include-content
```

创建 L2：

```bash
spec-manager spec new L2 --topic <topic> --parent <L1> --title "Design System + 5 Screens"
spec-manager template L2 --title "Design System + 5 Screens" --output .spec-manager/drafts/<topic>-L2.md
# 填写设计方向、tokens、组件、5 屏、P0 锁定、状态、素材策略
spec-manager spec update <L2> --content .spec-manager/drafts/<topic>-L2.md   --ai-summary "<一句话摘要>" --change-summary "initial L2 design"
spec-manager spec validate <L2>
```

`specs/DESIGN.md` 可用 `spec-manager assist design-template` 生成骨架，再填入本项目的 tokens/do/don't。

硬规则：

- L2 保持 `draft`，Codex 不得自己 `approve`。
- L2 未 confirmed 不写 L3；Codex 不写实现代码。
- 人类确认后执行 `spec-manager approve <L2>`。
- 若 Codex 不可用，自动由 OpenCode 按同一流程创建 L2，并标记 `codex fallback`。

## 流程

### 第 1 步：确定 5 屏并锁定 P0

**5 屏就是 P0 的边界**：不多不少正好 5 屏。5 图展示的内容 = 首版 P0；放不进 5 屏的功能降为 P1/P2。

默认结构（按目标 App 的核心闭环调整）：

| 屏 | 作用 | 必须覆盖 |
| --- | --- | --- |
| S1 首页/主入口 | 信息架构、主 CTA、导航 | 核心入口、空态 |
| S2 探索/搜索 | 分类、搜索、筛选 | 发现路径 |
| S3 核心详情/任务 | 用户做决策的主界面 | P0 主路径、关键操作 |
| S4 结果/收藏 | 收藏、待看、结果确认 | 成功/失败/下一步 |
| S5 设置/我的 | 设置、隐私、关于 | 上架必需项 |

按目标 App 类型调整：

- 内容/资料：S1 首页，S2 搜索/分类，S3 详情，S4 收藏/待看，S5 设置
- 电商：S1 首页，S2 搜索，S3 商品详情，S4 结算，S5 订单/我的
- 工具：S1 首页，S2 模板/历史，S3 编辑器，S4 导出/结果，S5 设置
- 社交：S1 信息流，S2 搜索/发现，S3 发布，S4 动态详情，S5 我的

在 `screen-map.md` 建立「屏幕 → P0 需求 ID → 关键状态」矩阵，并写一个 **P0 锁定表**：

| P0 需求 | 落在屏幕 | 关键状态 |
| --- | --- | --- |
| R-001 | S1 | 加载/空/错误/离线 |

规则：

- 每条 P0 必须落在某一屏；没有落点的 P0 要么改成 P1/P2，要么替换 5 屏中的某一屏。
- 不新增第 6 屏。需要第 6 屏说明 P0 范围失控，回阶段 2 收敛。
- 5 图只承诺 P0；P1/P2 可以出现在设计说明里，但不能算首版交付。
- 5 图的信息架构要与目标 App 相似：保留核心入口与核心路径，不另起一套产品。

### 第 2 步：定义 design tokens

写入 `design-system.md`：

**颜色角色**（light / dark 各一套）：

- background、surface、surface-elevated
- primary、on-primary、primary-container
- secondary、accent
- success、warning、danger、info
- text-primary、text-secondary、text-disabled
- border、divider、overlay

用十六进制写具体值，不写「品牌蓝」这类模糊描述。说明主色种子与生成方式。

**字体**：

| 层级 | 字号 | 行高 | 字重 | 用途 |
| --- | --- | --- | --- | --- |
| Display | 32-40 | 1.1-1.2 | 700 | 启动/空态 |
| H1 | 24-28 | 1.2 | 700 | 页面标题 |
| H2 | 20 | 1.3 | 600 | 分区标题 |
| Body | 16 | 1.5 | 400 | 正文 |
| Label | 14 | 1.4 | 500 | 按钮/标签 |
| Caption | 12 | 1.4 | 400 | 辅助信息 |

**其他**：

- 间距：4/8 基准（4, 8, 12, 16, 24, 32, 48）
- 圆角：小 8 / 中 12 / 大 20 / 全圆
- 阴影/描边：定义 2-3 级，不滥用
- 图标：24 线性/面性统一，触控区 ≥ 44pt / 48dp
- 动效：150-300ms，标准 easing，支持减少动态效果
- 栅格：屏幕边距 16/20，内容最大宽度

### 第 3 步：素材需求清单

写入 `asset-manifest.md`：

| 字段 | 说明 |
| --- | --- |
| 素材 ID | A-001 |
| 类型 | icon / illustration / photo / texture / logo / font / motion / copy |
| 使用位置 | S2 首页空态 |
| 尺寸/比例 | 1024x1024 / 16:9 / 24pt |
| 格式 | SVG / PNG / WebP / Lottie / 字体文件 |
| 倍率 | @1x/@2x/@3x 或矢量 |
| 来源 | Stitch 导出 / doubao / GPT / SF Symbols / Material Icons / 授权图库 |
| 生成提示词 | 可复现的 prompt |
| 版权/状态 | 原创 / 已授权 / 待确认 / 不可用 |
| 负责人 | 人/Agent |
| 截止 | 日期 |

规则：

- 图标优先用 SF Symbols / Material Icons 或原创 SVG；不直接扒竞品图标。
- 插画/背景用 doubao 或 GPT 生成，提示词写入 `prompts.md`，保留 seed/参数（若工具支持）。
- 照片必须可商用授权；没有就先用占位图并标注。
- 不把竞品截图、logo、品牌色、插画放进原型或最终产品。
- 文案用真实目标语言，不用 Lorem Ipsum。
- MVP 素材与数据全部本地 mock：可以用占位图/生成图/本地 JSON，不接真实 API。
- 目标 App 截图只做结构参考，不直接复制其图片、文案、图标、品牌资产。

### 第 3.5 步：app-icon 与 splash-screen

除 5 图外，L2 必须交付：

**App Icon**

- `design/app-icon/AppIcon-1024.png`：1024x1024，不透明，无圆角（系统会裁切），品牌 mark 居中，四周留安全边距。
- `design/app-icon/ios/`：AppIcon.appiconset 所需尺寸（20/29/40/60/76/83.5/1024 等 @2x/@3x）。
- `design/app-icon/android/`：adaptive icon foreground/background（API 26+）与 legacy mipmap。
- 小尺寸可读：不要放复杂文字；不要使用竞品 logo/角色/品牌色组合。

**Splash Screen**

- `design/splash/splash-ios-1290x2796.png`：iOS 竖屏启动图；如有深色模式，补 `splash-ios-dark-1290x2796.png`。
- `design/splash/splash-android-1080x1920.png`：Android 启动图；Android 12+ 另出 splash icon/background。
- 品牌 mark + 产品名；背景与 design tokens 一致；避免复杂动画（MVP 静态）。
- 不使用竞品截图/角色/品牌资产。

把 icon/splash 的尺寸、格式、来源、版权写入 `asset-manifest.md`。  
若用户没有提供品牌资产，用原创几何 mark/文字标；不要直接使用目标 App 的 logo。

### 第 4 步：用 Stitch 建设计系统

用 Stitch MCP 工具，按顺序：

1. `stitch_create_project`：项目名包含 App 名与阶段（如 `AppName - Core Prototype`）。
2. `stitch_create_design_system`：传入 `projectId` 与 theme：
   - `colorMode`: LIGHT 或 DARK
   - `headlineFont` / `bodyFont`：与 tokens 一致
   - `roundness`：ROUND_FOUR / EIGHT / TWELVE / FULL
   - `customColor`：品牌主色种子
   - `designMd`：补充间距、组件、禁止项、平台规范
   - 可选 `typography`、`spacing`、`overridePrimaryColor` 等
3. 按工具返回结果调用 `stitch_update_design_system` 应用到项目并展示。
4. `stitch_list_design_systems` 确认设计系统 ID，后续生成屏幕复用同一 ID。

设计系统提示词要具体，不要只写「现代简约」。示例：

```text
移动端应用，目标用户为一线城市 25-35 岁效率工具用户。
风格：克制、清晰、留白充足；主色深青，辅助色暖橙；避免渐变滥用和大圆角堆叠。
字体：标题用无衬线中黑，正文用系统字体；字号层级明确。
组件：16px 边距、12px 卡片圆角、1px 描边、底部导航 5 项以内。
禁止：竞品 logo、玻璃拟态、过度阴影、花哨插画。
```

### 第 5 步：生成 5 屏

逐屏调用 `stitch_generate_screen_from_text`，每屏使用同一 design system ID，提示词包含：

```text
产品: <一句话定位>
用户: <目标用户>
屏幕: S2 首页
目标: <用户在此屏要完成什么>
布局: <从上到下/左右分栏/卡片流/列表>
组件: <导航、搜索、卡片、CTA、筛选、空态>
内容: <目标语言示例文案；使用本地 mock 数据>
状态: 默认态；同时说明空态/加载/错误如何呈现
风格: <design tokens 摘要；主题视觉关键词>
平台: <iOS/Android>，遵守安全区、44pt/48dp 触控、系统导航习惯
约束: 不使用竞品资产；不出现 lorem ipsum；文本不溢出；对比度达标；不依赖真实 API
```

生成顺序建议 S2 → S3 → S4 → S1 → S5：先定主框架，再补首尾。

需要风格选择时：

- 用 `stitch_generate_variants` 对 S2 或 S3 生成 2-3 版，比较后收敛。
- 用 `stitch_edit_screens` 做一致性修正，例如「统一所有屏幕的底部导航、标题字号、按钮层级和卡片间距」。

用 `stitch_list_screens` / `stitch_get_screen` 取回屏幕信息与图片，记录 screen ID 到 `screen-map.md`。

### 第 6 步：一致性检查

对 5 屏逐项检查：

- 同一角色颜色是否一致；有没有多出未定义的色值
- 标题/正文/按钮字号层级是否统一
- 卡片圆角、间距、描边是否统一
- 主 CTA 每屏最多一个，视觉优先级清晰
- 底部导航/Tab 是否一致，选中态明确
- 空态、加载、错误是否有说明或设计
- 文本是否溢出，长文案是否截断/换行
- 触控目标是否 ≥ 44pt / 48dp
- 安全区、刘海/灵动岛、底部 Home Indicator 是否避让
- 对比度：正文 ≥ 4.5:1，大字/UI ≥ 3:1
- 深色模式是否可用（若首版支持）

### 第 7 步：导出与交接

- 5 屏图片放 `design/screens/`，按实际屏幕命名（如 `S1-home.png`）。
- `screen-map.md` 记录：屏幕、对应 P0 需求、Stitch screen ID、关键状态、开发备注，以及 **P0 锁定表**。
- `prompts.md` 保存所有生成提示词，便于复现和调整。
- 素材清单标注哪些已产出、哪些待生成、哪些有版权风险。
- 明确写入：`p0_lock: locked`，阶段 4 只能实现这 5 屏内的 P0。

## 产出

```text
specs/<topic>/<topic>-L2.md     # 源（spec-manager）
specs/DESIGN.md                 # 设计上下文（tokens / do / don't）
design/
├── asset-manifest.md
├── design-system.md
├── screen-map.md
├── prompts.md
├── screens/
│   ├── S1-home.png
│   ├── S2-explore.png
│   ├── S3-detail.png
│   ├── S4-watchlist.png
│   └── S5-settings.png
├── app-icon/
│   ├── AppIcon-1024.png
│   ├── ios/
│   └── android/
└── splash/
    ├── splash-ios-1290x2796.png
    └── splash-android-1080x1920.png
```

`L2` 是源；`design/` 是设计交付与截图证据。OpenCode 必须读取 `specs/DESIGN.md`。

## Stitch 降级策略

Stitch 可能超时或不可用，不能因此停摆，也不能伪造 screen ID。

1. 记录工具名、调用、错误码、时间，写入 `prompts.md`。
2. 同一屏最多重试 2 次：优先换 `GEMINI_3_5_FLASH_LITE`，逐屏串行，不并发。
3. 仍失败则启用 L2 fallback：
   - 用 HTML/CSS 按 design tokens 搭建 5 屏高保真原型。
   - 用 Chrome headless 截图（393x852 @2x），保存到 `screens/`。
   - 源文件放 `prototype/`，保证可复现。
   - 在 `screen-map.md` 标记 `fallback`，不写 Stitch screen ID。
4. 人工 G3 接受 fallback 后，可以锁定 P0 并进入开发；状态记 `fallback accepted`。
5. 商店截图/最终视觉不得使用 fallback，必须在 G6 前重生成或由设计师替换。
6. 工具恢复后重跑，与 fallback 做差异对比，记录在 `implementation-log.md`。

## G3 门禁

- [ ] L2 已创建并通过 `spec-manager spec validate`
- [ ] `specs/DESIGN.md` 已写入
- [ ] app-icon 1024 不透明，iOS/Android 导出完整
- [ ] splash-screen iOS/Android 已生成，深色模式 variant 按需提供
- [ ] 正好 5 屏，没有第 6 屏
- [ ] 5 屏覆盖并锁定全部 P0，P0 锁定表完整
- [ ] 不存在 5 图外的 P0
- [ ] 5 屏信息架构与目标 App 的品类/核心闭环相似
- [ ] design tokens 完整，全屏一致
- [ ] 每屏标注默认/空/加载/错误态处理方式
- [ ] 主 CTA 清晰，导航一致
- [ ] 触控目标、安全区、文本溢出检查通过
- [ ] 对比度达标，颜色不是唯一信息载体
- [ ] 素材来源与版权状态清晰，无竞品资产（含 icon/splash）
- [ ] 数据与素材为本地 mock，不依赖真实 API
- [ ] Stitch screen ID 与导出文件可追溯
- [ ] 人工确认视觉方向与 5 屏范围

## 常见错误

- 5 图外还有 P0：开发阶段必然失控
- 为了塞功能新增第 6 屏：说明范围没收敛
- 5 屏只是「好看」，没有覆盖 P0 闭环
- 5 屏偏离目标 App 的信息架构，变成另一个产品
- 每屏风格不一致：字体、圆角、按钮高度各不相同
- 只做默认态：开发到空态/错误态时临时发挥
- 用竞品截图做参考图直接生成，导致视觉侵权
- 文案全是 Lorem Ipsum，无法判断信息层级
- 设计系统只写形容词，没有具体色值/字号/间距
- MVP 依赖真实 API/后端数据，无法独立演示
- 忽略 Android 与 iOS 的导航、返回、安全区差异
