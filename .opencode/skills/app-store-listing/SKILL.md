---
name: app-store-listing
description: 基于 confirmed L2 与实现证据，在 spec-manager L3.3 中产出 App Store 的应用名称、副标题、描述、关键词、截图字幕、What's New 与对内 QA Notes；只写已构建平台。Use when the user says 商店文案、App Store 描述、Google Play 文案、ASO、关键词、release notes、更新说明、截图字幕、提审文案，or asks to write store listing copy for an app.
---

# 商店文案与 Release Notes

目标：让 AI 基于事实产出可提交的商店文案，不夸大、不侵权、可追溯，并由人审核后使用。

## 输入

- `02-prd/prd.md`：价值主张、目标用户、P0 功能
- `01-feature-spec/`：真实功能与限制
- `03-design/screens/`：5 屏截图
- 目标市场、语言、竞品关键词（可选）
- 目标平台（单端即可；iOS 链接就只写 App Store）
- 版本号、Build 号、本次变更

## OpenCode + spec-manager 模式

本阶段默认由 OpenCode 执行，写入 L3.3（Store Copy）；Codex 可代写文案，但必须由 OpenCode 记录 Task 与 evidence。

```bash
spec-manager spec new L3 --topic <topic> --parent <L2> --title "App Store Copy" --desc store
spec-manager template L3 --title "App Store Copy" --output .spec-manager/drafts/<topic>-L3-store.md
# 填写文案范围、截图、合规检查、验收命令
spec-manager spec update <L3.3> --content .spec-manager/drafts/<topic>-L3-store.md   --ai-summary "<summary>" --change-summary "initial store copy"
spec-manager spec validate <L3.3>
# 人工确认后
spec-manager approve <L3.3>
spec-manager task create <L3.3> --plan tasks/<topic>-L3-store-plan.json --start
```

完成后用 `spec-manager task verify` 记录人工审核/截图证据，再 `task complete`。

## 流程

### 第 1 步：提取事实

先列事实清单：

- 一句话价值主张
- 3 个核心收益（对应 P0 功能）
- 2-3 个差异点（有功能或体验支撑）
- 适用场景与目标用户
- 明确的限制与不适用人群（避免误导）
- 本次版本的变更

每条事实标注来源（PRD 需求 ID / 功能 ID / 截图）。无法追溯的句子不进入最终文案。

### 第 2 步：生成 3 组语气

- **克制型**：功能清楚，少形容词，适合理性工具
- **利益型**：先讲结果，再讲功能，适合效率/生活类
- **品牌型**：强调理念与调性，适合内容/社区/品牌产品

每组给出名称、副标题、描述开头 2 段。选 1 组进入正式稿，另外保留在 `listing.md` 供对比。

### 第 3 步：按字段写作

只写**已构建平台**：iOS 只填 App Store，Android 只填 Google Play；未构建的平台不写、不声称。

**iOS（App Store Connect）**

| 字段 | 限制 | 要点 |
| --- | --- | --- |
| App Name | 30 字符 | 品牌 + 核心品类，不堆关键词 |
| Subtitle | 30 字符 | 一句补充定位，不与名称重复 |
| Promotional Text | 170 字符 | 可随时更新，放当前亮点 |
| Description | 4000 字符 | 前 3 行决定转化，分段短句 |
| Keywords | 100 字符 | 逗号分隔，不重复名称，不堆竞品词 |
| What's New | 4000 字符 | 用户语言，列 3-5 条 |
| Support URL | - | 可访问 |
| Marketing URL | - | 可选 |

**Google Play**

| 字段 | 限制 | 要点 |
| --- | --- | --- |
| App name | 30 字符 | 与 iOS 可本地化不同 |
| Short description | 80 字符 | 一句话卖点 |
| Full description | 4000 字符 | 前 2 段最重要，可分段/符号 |
| What's new | 500 字符 | 简洁列变更 |

描述结构建议：

1. 一句话定位
2. 用户痛点场景
3. 3 个核心能力（用收益写，不只列功能）
4. 使用方式/适用人群
5. 差异化或信任信息（仅限可验证）
6. 温和 CTA

### 第 4 步：ASO 检查

- 关键词与产品实际功能相关，不塞无关热词
- 不使用竞品商标、品牌名、应用名
- 不承诺排名、下载量、收益
- 不使用「第一」「最好」「唯一」等无法证明的绝对化表述
- 不在名称/副标题堆砌关键词
- 不声称未构建的平台、未上线的功能、真实实时数据或流媒体播放
- 目标语言母语审校；机翻痕迹要修
- 本地化时重写而不是逐字翻译

可用的关键词来源：应用商店搜索联想、公开竞品文案、用户评论用词、客服高频问题。不要编造搜索量。

### 第 5 步：截图字幕

为 5 屏各写 1 条字幕（3-6 个词），利益导向、与画面一致：

| 屏 | 字幕 |
| --- | --- |
| S1 | 30 秒开始你的第一件事 |
| S2 | 所有任务，一屏看清 |
| S3 | 输入一次，自动整理 |
| S4 | 结果可分享，进度可追踪 |
| S5 | 你的数据，你做主 |

字幕是截图设计的一部分；确保最终截图里的文字与文案一致，不出现截图没有的功能。

### 第 6 步：Release Notes

**对外（用户）**：

- 3-5 条，用户能感知的变化
- 不写内部术语、工单号、SDK 升级
- 修复类写「修复了……问题」，不写「修复若干问题」糊弄

**对内（QA/团队）**：

- 版本号 + Build 号
- 变更范围与关联需求 ID
- 测试重点与回归范围
- 已知问题与绕过方式
- 测试账号/环境
- 后端/配置依赖

写入 `release-notes.md`，与 `07-release/submission.md` 交叉引用。

### 第 7 步：合规审核

逐项检查：

- 功能声明能在 App 中找到
- 价格/订阅/试用描述与实际一致
- 隐私说明与权限请求一致
- 医疗、金融、教育等敏感声明有依据
- 没有诱导性、歧视性、侵权内容
- 截图不含测试数据、真实用户信息、竞品界面

AI 只产出草稿；最终由产品/法务/市场负责人审核。

## 产出

```text
artifacts/06-store/
├── listing.md
└── release-notes.md
```

`listing.md` 包含：事实清单、3 组语气、最终字段、字符计数、关键词、截图字幕、本地化版本、审核记录。

## G6 门禁

- [ ] L3.3 已 `validate` 并经人工 `approve`（frozen）
- [ ] L3.3 Agent Task 已创建并完成
- [ ] 只写已构建平台；未构建平台不出现声明
- [ ] 每个字段符合对应平台字符限制
- [ ] 名称/副标题/描述/关键词无竞品商标
- [ ] 所有功能声明可追溯到 PRD 或截图
- [ ] 无编造的下载量、排名、用户数、评价
- [ ] 无无法证明的绝对化表述
- [ ] 不声称流媒体播放、真实实时数据或未上线功能
- [ ] 截图字幕与最终截图一致
- [ ] 对外 Release Notes 与对内 QA Notes 分开
- [ ] 目标语言已审校
- [ ] 人工审核通过

## 常见错误

- 只建了 iOS 却写 Google Play 文案
- 把 mock 数据描述成真实实时榜单/真实评分
- 把功能列表直接当描述：用户看不出价值
- 关键词堆砌竞品名：审核风险/下架风险
- 描述里承诺未上线功能
- 截图字幕与 App 实际界面不一致
- Release Notes 写「优化体验、修复若干问题」
- 用机翻直接提交小语种
- 用「第一」「唯一」「必装」等绝对化词
