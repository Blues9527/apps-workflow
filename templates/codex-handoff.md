# Codex Handoff — Stage 2/3

> 生成者: OpenCode
> 日期: YYYY-MM-DD
> spec topic: <topic>
> 状态: waiting_for_codex

## 1. Context

| 项目 | 内容 |
| --- | --- |
| 目标 App |  |
| 平台 / 技术栈 |  |
| 目标市场 |  |
| 功能知识库 | `artifacts/01-feature-spec/`（可选） |
| PRD 来源 | `artifacts/02-prd/source-prd.md`（intake 时） |
| PRD 模式 | generate / intake |
| 关键功能 ID |  |
| 目标 App 品类/核心闭环 |  |
| 约束 | 二创/同品类、5 图定 P0、本地 mock、单端、不写实现代码 |

## 2. Stage 2 — L1 PRD（Codex）

开始前：

```bash
spec-manager brief "<二创主题 + 竞品 + PRD>" --topic <topic>
spec-manager spec list --topic <topic>
spec-manager decision list --topic <topic>
```

创建并填写：

```bash
spec-manager spec new L1 --topic <topic> --title "<产品名> PRD"
spec-manager template L1 --title "<产品名> PRD" --output .spec-manager/drafts/<topic>-L1.md
# 填写主题候选/评分、竞品矩阵、PRD、P0 5 屏草案、mock 数据、验收标准
spec-manager spec update <L1> --content .spec-manager/drafts/<topic>-L1.md \
  --ai-summary "<summary>" --change-summary "initial L1 PRD"
spec-manager spec validate <L1>
```

L1 必须包含：

- generate：3-5 个基于目标 App 的二创/优化主题（含目标一致性评分）
- intake：保留原始 PRD 范围/ID；生成 `prd-intake.md`；缺章节标 gap，不擅自补写
- 5-8 个竞品（来源 + 日期；不编造数据）
- PRD：用户、范围、需求 ID、验收标准、非功能、埋点、权限、异常、发布标准
- P0 5 屏分配草案
- 本地 mock 数据策略
- 范围外/不做清单

停止条件：

- L1 保持 `draft`；不要 `approve`；不要创建 L2；不要写代码。
- 输出 L1 code 与需要人工确认的清单。

## 3. Stage 3 — L2 Design + 5 图（Codex）

仅当 L1 confirmed 后开始：

```bash
spec-manager brief "设计系统 + 5 图 + P0 锁定" --topic <topic>
spec-manager spec show <L1> --include-content
spec-manager spec new L2 --topic <topic> --parent <L1> --title "Design System + 5 Screens"
spec-manager template L2 --title "Design System + 5 Screens" --output .spec-manager/drafts/<topic>-L2.md
# 填写设计 tokens、组件、5 屏、screen-map、asset-manifest、P0 锁定
spec-manager spec update <L2> --content .spec-manager/drafts/<topic>-L2.md \
  --ai-summary "<summary>" --change-summary "initial L2 design"
spec-manager spec validate <L2>
```

同时产出：

- `specs/DESIGN.md`：颜色、字体、间距、圆角、组件、do/don't
- `design/screens/S1-...png` ~ `S5-...png`
- `design/app-icon/AppIcon-1024.png` + iOS/Android 导出
- `design/splash/splash-ios-*.png` + Android 启动图
- `design/screen-map.md`
- `design/asset-manifest.md`
- `design/prompts.md`
- Stitch 不可用时：HTML/CSS fallback + Chrome 截图，L2 标记 fallback

停止条件：

- L2 保持 `draft`；不要 `approve`；不要创建 L3；不要写代码。
- 输出 L2 code、`specs/DESIGN.md`、`design/` 路径与人工确认清单。

## 4. 人工确认

- L1：人确认后 `spec-manager approve <L1>`
- L2：人确认后 `spec-manager approve <L2>`
- 未确认前，OpenCode 不得进入阶段 4。

## 5. 回到 OpenCode

```bash
spec-manager brief "实现 P0" --topic <topic>
spec-manager flow status --topic <topic>
spec-manager spec show <L2> --include-content
```

OpenCode 读取 `specs/DESIGN.md` 与 `design/`，创建 L3.1 并冻结后再写代码。
