---
name: mobile-workflow
description: 编排移动端全栈开发工作流：支持从目标 App 功能分析或已有 PRD 起点，Codex 通过 spec-manager 产出 L1 PRD/L2 设计+5 图，OpenCode 基于冻结 L3 创建 Task 实现、测试、商店文案到 TestFlight/归档；支持单端、自动排期与多 Agent 并行。Use when the user says 移动端全流程、Codex 写 PRD、spec-manager、从功能分析到提测、App 二创/复刻/重构、5 图定 P0、跑完整工作流、PRD 到 TestFlight、mobile app workflow，or asks to coordinate these stages.
---

# 移动端全栈工作流编排

你是这条工作流的编排者。你的职责不是替每个阶段写全部内容，而是：确认输入、按顺序加载阶段 skill、检查门禁、维护状态、在人工签核点停下来。

## 何时使用

使用：

- 用户要从一个已上架 App 出发，走到可提测的移动应用
- 用户要串起功能分析、PRD、原型、开发、测试、商店文案、TestFlight
- 用户说「按流程走」「从功能分析到提测」「复刻这个 App」「跑移动端全流程」

不使用：

- 只做其中一个阶段：直接加载对应阶段 skill
- 纯 Web / 后端 / 桌面端
- 要求绕过付费、登录、DRM 或抓取非公开数据

## 不可协商的规则

1. 严格按阶段 0 → 8 执行，不跳阶段。
2. 每个阶段结束必须读取并执行该阶段 skill 的门禁清单。
3. 门禁未通过，不进入下一阶段；把失败项写入状态文件。
4. 缺信息时只问缺失项，不编造 App 功能、竞品数据、用户评价、下载量。
5. G2（L1）、G3（L2）、G4 入口（L3 冻结）、G7、G8 必须获得人工明确确认，不能自己签核。
6. 所有产物写入 `artifacts/`，固定路径见 `WORKFLOW.md`。
7. 不复制竞品代码、图片、文案、商标；只做行为分析与原创设计。
8. 密钥、签名、测试账号只通过环境变量或 Keychain 使用，不写入仓库和工件。
9. **目标一致性**：主题必须基于用户提供的目标 App 做二创/优化，保持同品类与核心闭环；偏离品类的方案直接淘汰。
10. **5 图定 P0**：P0 以 5 图最终展示内容为准；5 图之外默认 P1/P2，不进入首版。
11. **Mock 优先**：MVP 数据全部本地 mock；Repository 接口隔离，真实 API 不作为 P0 依赖。
12. **单端足够**：一个平台链接/安装包即可启动；另一平台可选后补，不阻塞。
13. **凭证后置**：开发者账号、签名、TestFlight 权限在阶段 7 才收集，前期不阻断。
14. **排期自适应**：按范围、估算与并行度自动修正截止日期；不可行时给缩范围或延期方案。
15. **逆向可选**：需要更深逆向时，若环境提供 `rea` skill 且用户授权，可加载；否则回退公开行为分析。
16. **spec-manager 是共享真相**：L1/L2/L3、decisions、tasks、verification evidence 以 spec-manager 为准；`artifacts/` 只做证据与阅读副本。
17. **Agent 路由**：阶段 2/3 由 Codex 写 L1/L2；阶段 4/5 由 OpenCode 写 L3/Task 并写代码；阶段 6 优先 `app-store-prd-metadata`（fallback `app-store-listing`）；阶段 7/8 由 OpenCode 执行。
18. **顺序硬约束**：L1 未 confirmed 不写 L2；L2 未 confirmed 不写 L3；L3 未 frozen 不写代码。
19. **审批**：L1/L2/L3 的 `spec-manager approve` 只能在人明确确认后执行；禁止用 `--auto-confirm` 代替人工门禁。
20. **任务证据**：每个 Task 必须有 steps 与 verification evidence；禁止 `--skip-verification` / `--skip-verify` 掩盖失败。
21. **PRD 起点**：`--prd` 时阶段 1 可 skipped，阶段 2 进入 L1 intake；保留原始 PRD、SHA256、gap 分析，不擅自改写范围。
22. **PRD-spec 起点**：`--prd-spec` 已 confirmed 时直接进阶段 3；draft 时先做 L1 review。

## 启动流程

### 第 0 步：解析命令参数

若从 `/mobile-flow` 进入，先按 `.opencode/command/mobile-flow.md` 的参数表解析：

- 优先级：命令行参数 > `workflow-state.md` / `00-intake.md` > 交互提问。
- `--help` / `-h`：只输出参数与使用示例，不执行工作流。
- `--dry-run`：只输出计划与缺失项，不创建目录、不写产物、不改状态。
- `--from-stage` / `--only-stage`：可以指定起点或单阶段，但不能绕过前置门禁。
- `--non-interactive`：不主动提问，缺必填项直接报错；G2/G3/G7 仍要暂停等签核。
- `--platform auto`：从 `--app` 链接推断；只提供一个平台即可，`both` 不要求两个链接。
- `--deadline auto`：由 `schedule.md` 自动排期；固定日期不可行时给缩范围/延期方案。
- `--parallel auto|<n>`：并行 Agent 数；默认自动，识别可并行工作流。
- `--reverse auto|rea|off`：是否尝试 `rea` skill；默认自动，缺少时回退公开分析。
- `--topic <slug>`：spec-manager topic；L1/L2/L3 共用，默认由 App 名 + P0 推导。
- `--spec-manager on|off`：默认 on；off 时回退 artifacts，不伪造 specs/tasks。
- `--app-name <name>`：新产品/品牌名；用于 L1/L2、icon/splash、商店文案、archive；不是 `--app`。
- `--prd <path|url>`：从已有 PRD 开始；默认从阶段 2 intake，阶段 1 可跳过。
- `--prd-spec <L1-code>`：使用现有 spec-manager L1；confirmed 则从阶段 3 开始。
- `--prd` 起点：阶段 1 可 skipped，阶段 2 做 L1 intake；原始 PRD 复制/哈希/缺口分析必须落盘。
- 不接受 `--skip-gates`、`--auto-approve`、`--yes`，也不接受命令行传密钥/密码；只从环境变量或 Keychain 读取。
- 未知参数或冲突参数：列出有效参数并停止，不要猜测。

### 第 0.5 步：Agent 路由与 spec-manager

| 阶段 | 执行 Agent | spec-manager |
| --- | --- | --- |
| 0-1 | OpenCode | project init + topic + handoff packet |
| 2 主题/竞品/PRD | **Codex** | L1（标题用 app_name） |
| 3 设计系统/5 图/icon/splash/P0 | **Codex** | L2 + `specs/DESIGN.md`（含 app_name） + `design/` |
| 4 实现 | **OpenCode** | L3.1 + Task |
| 5 自动化测试 | **OpenCode** | L3.2 + Task |
| 6 App Store 元数据 | OpenCode（Codex 可选） | L3.3 + Task（App Name 用 app_name；优先 `app-store-prd-metadata`，fallback `app-store-listing`） |
| 7 发布/TestFlight | **OpenCode** | L3.4 + Task |
| 8 归档/交接 | **OpenCode** | L3.5 + Task |

初始化：

```bash
spec-manager project init --name <project>
spec-manager project agents --provider all
# 或
spec-manager codex install
spec-manager opencode install
spec-manager project doctor
```

Codex 可用性检测（阶段 0）：

```bash
command -v codex >/dev/null 2>&1 && codex --version
```

- 可用：`stage_2_3=codex`，阶段 1 后 `awaiting_codex`。
- 未安装：**自动降级** `stage_2_3=opencode`、`codex_fallback=true`；跳过 handoff，OpenCode 直接按 L1/L2 模板执行阶段 2/3。

每个阶段开始前：

```bash
spec-manager brief "<request>" --topic <topic>
spec-manager flow status --topic <topic>
spec-manager spec list --topic <topic>
spec-manager decision list --topic <topic>
```

Handoff 规则：

1. 阶段 1 结束，OpenCode 生成 `artifacts/01-feature-spec/codex-handoff.md`，状态改 `awaiting_codex`。
2. Codex 用 `spec-manager spec new L1` 写 L1，`validate` 后停止；人确认后 `spec-manager approve <L1>`。
3. Codex 仅在 L1 confirmed 后创建 L2（`--parent <L1>`），产出 `specs/DESIGN.md` 与 `design/` 5 图；`validate` 后停止；人确认后 `spec-manager approve <L2>`。
4. OpenCode 状态改 `awaiting_opencode`，读 confirmed L1/L2，创建 L3.1/L3.2（`--parent <L2>`），人确认后 `approve` 冻结，再 `task create ... --start`。
5. 阶段 6 优先加载 `app-store-prd-metadata`，不可用自动降级 `app-store-listing` 并标记 `skill_fallback`；阶段 6/7 创建 L3.3/L3.4，Task 完成后用 `task verify` 记录证据；阶段 8 创建 L3.5 归档。
6. 任何 Agent 都不得替另一个 Agent 签核；Codex 不写实现代码，OpenCode 不改 L1/L2。

### 第 1 步：读取现状

先检查项目根目录：

- `WORKFLOW.md` 是否存在
- `artifacts/workflow-state.md` 是否存在
- `prd_source` / `prd_mode` / `feature_analysis`（PRD 起点）
- `artifacts/02-prd/source-prd.md`、`prd-intake.md`（如有）
- `.spec-manager/config.yaml` 是否存在
- `specs/<topic>/` 下有哪些 L1/L2/L3
- `artifacts/` 下已有哪些阶段产物

存在状态文件时，从 `current_stage` 和 `next_action` 继续，不重头再来。校验上游门禁是否真的通过；只相信产物与 spec-manager 状态，不相信状态文件里的口头结论。

```bash
spec-manager flow status --topic <topic>
spec-manager spec list --topic <topic>
spec-manager task list --topic <topic>
```

### 第 2 步：补齐建档信息

按 `templates/` 或 `00-intake.md` 收集：

| 字段 | 说明 |
| --- | --- |
| 目标 App 名称/链接/安装包 | 被分析对象；一个平台即可；有 PRD 时可选 |
| 新产品 App 名称 | `--app-name`；未提供则从 PRD/L1/主题推导，歧义时询问 |
| 已有 PRD | `--prd` 路径/URL 或 `--prd-spec` L1 code |
| 目标平台 | 由链接推断；iOS / Android；`both` 可选但不强制双链接 |
| 技术栈 | RN / Flutter / oc / swift / oc-swift / swift-swiftui / 待定 |
| 现有仓库 | 路径、分支、是否可运行 |
| 目标市场与语言 | 决定竞品、ASO、文案 |
| spec topic | 小写 slug，L1/L2/L3 共用 |
| Codex/OpenCode 可用性 | 默认 Codex 阶段 2/3、OpenCode 阶段 4-7 |
| 截止日期与范围 | `auto` 或日期；范围决定 P0 |
| 账号与权限 | **阶段 7 才收集**，前期缺失不阻塞 |
| 合规边界 | 是否仅分析公开行为；未授权逆向禁止 |

一次性列出**真正阻塞当前阶段**的缺失项，批量提问。第二平台、发布凭证、真实数据 API 不算前期阻塞。

### 第 3 步：初始化工件

创建 `artifacts/` 目录结构、`schedule.md` 与 `workflow-state.md`。状态模板：

```yaml
current_stage: 0
status: in_progress
platform: auto
app_name: null              # 新产品名称，不是目标 App
prd_source: none
prd_hash: null
prd_mode: generate
feature_analysis: pending
spec_manager:
  project: <project>
  topic: <topic>
  l1: null
  l2: null
  l3_impl: null
  l3_e2e: null
  l3_store: null
  l3_release: null
  active_task: null
agent_routing:
  stage_2_3: codex
  stage_4_5: opencode
gates: {}
p0_lock: pending
schedule:
  deadline: auto
  critical_path_days: 0
  parallel_agents: auto
  buffer_days: 1
handoff:
  next_agent: opencode
  packet: artifacts/01-feature-spec/codex-handoff.md
open_questions: []
decisions: []
next_action: 完成项目建档、spec-manager 初始化与排期
```

排期规则：

- 按阶段估算人日：分析 1、PRD 1、5 图 1、P0 开发 2-4、测试 1、文案 0.5、发布 1。
- 可并行：竞品研究与功能分析、设计与 PRD 打磨、测试脚本与开发、商店文案与测试。
- 关键路径通常是 1 → 2 → 3 → 4 → 5 → 7；阶段 6 可与 4/5 并行。
- 截止日期不可行时，自动给出「缩范围 / 延期 / 增并行」三选一，不直接卡住。

### 第 4 步：逐阶段执行

对每个阶段：

1. 宣布阶段编号、目标、执行 Agent、输入、预计产出。
2. 用 skill 工具加载对应阶段 skill。
3. 阶段 2/3：Codex 可用则生成 handoff packet、状态 `awaiting_codex`、暂停；PRD 起点时 handoff 里写 `prd_mode=intake`；Codex 不可用则自动 `codex_fallback`，由 OpenCode 直接执行 L1/L2。
4. 阶段 4/5：读取 confirmed L1/L2，创建/冻结 L3，创建 Task，再写代码/测试。
5. 阶段 6/7：阶段 6 优先 `app-store-prd-metadata`（fallback `app-store-listing`）；创建 L3.3/L3.4，完成 App Store 元数据与 Release/TestFlight。
6. 阶段 8：创建 L3.5，归档 specs/design/store/release，生成 manifest/checksums/release summary。
7. 执行该 skill 的流程，产物写入固定路径。
8. 运行门禁自检，把「通过/失败/缺证据」逐项写清楚；同时检查 `spec-manager flow status`。
9. 更新 `workflow-state.md`（spec codes、active task、next agent）。
10. 需要人工确认时停下来，给出确认清单。

阶段与 skill 对照：

| 阶段 | 执行 Agent | Skill | spec-manager |
| --- | --- | --- | --- |
| 0 启动 | OpenCode | 本 skill | project init + topic |
| 1 功能分析（可选） | OpenCode | `mobile-feature-analysis` | handoff packet；有 PRD 时可 skipped |
| 2 主题 + 竞品 + PRD | **Codex** | `mobile-prd-authoring` | L1 |
| 3 素材 + 5 图 + icon/splash | **Codex** | `mobile-ui-prototype` | L2 + DESIGN.md |
| 4 框架 + 功能填充 | **OpenCode** | `mobile-app-implementation` | L3.1 + Task |
| 5 自动化测试 | **OpenCode** | `mobile-e2e-testing` | L3.2 + Task |
| 6 App Store 元数据 | OpenCode（Codex 可选） | `app-store-prd-metadata`（fallback `app-store-listing`） | L3.3 + Task |
| 7 打包上传 + 真机 + 提测 | **OpenCode** | `mobile-testflight-release` | L3.4 + Task |
| 8 归档 | **OpenCode** | `mobile-release-archive` | L3.5 + Task |

## 排期与并行

默认 3 条工作流：

| 工作流 | 执行 Agent | 负责 | 可并行阶段 |
| --- | --- | --- | --- |
| W1 分析 | OpenCode | 功能分析、知识库、handoff | 1 |
| W2 产品/设计 | **Codex** | L1 PRD、竞品、L2 设计、5 图 | 2-3 |
| W3 工程/质量 | **OpenCode** | L3.1 实现、L3.2 测试 | 4-5 |
| W4 文案/发布 | OpenCode | L3.3 文案、L3.4 发布、L3.5 归档 | 6 可与 4/5 并行；7 依赖 G5；8 依赖 G7 |

调度规则：

- 先算关键路径（通常 1 → 2 → 3 → 4 → 5 → 7），再决定并行。
- 只有无数据依赖的任务才并行；共享 P0 锁定表与设计 tokens。
- 截止日期不可行时，优先缩 P1/P2、再增并行、最后延期；不牺牲 P0 质量。
- 每个并行 Agent 只写自己的工件，编排器负责合并与门禁。

## 阶段交接格式

每次进入下一阶段，输出一个简短交接块：

```text
阶段: 2 -> 3
已通过门禁: G2
spec:
- topic: <topic>
- L1: <L1-code> confirmed
- L2: <L2-code> pending
关键输入:
- design/screen-map.md（P0 5 屏分配草案）
- artifacts/02-prd/theme.md（基于目标 App 的二创主题）
- artifacts/schedule.md（关键路径与并行度）
未决问题:
- 第 4 屏放收藏列表还是结果页
下一步: 交给 Codex 写 L2；产出 specs/DESIGN.md 与 5 图，并在 G3 锁定 P0
```

不要复制整份文档到对话里，给路径和 3-5 条摘要。

## Codex Handoff Packet

阶段 1 结束时生成 `artifacts/01-feature-spec/codex-handoff.md`，供 Codex 直接执行阶段 2/3：

```markdown
# Codex Handoff — Stage 2/3

## Context
- Project:
- Target App:
- Platform / stack / market:
- spec topic:
- PRD source (optional):
- PRD mode: generate | intake
- Feature KB:
- Constraints: 二创/同品类（PRD 起点以 PRD 为准）、5 图定 P0、本地 mock、单端、不写代码

## Stage 2 — L1 PRD
- 先运行: spec-manager brief / spec list / decision list
- 创建 L1: spec-manager spec new L1 --topic <topic> --title "<title>"
- generate: 写主题候选、评分、竞品矩阵、PRD、P0 5 屏草案、mock、验收标准
- intake: 保存 source-prd.md + SHA256，写 prd-intake.md（章节/缺口/ID 映射），把 PRD 填入 L1，不改写范围
- spec-manager spec validate <L1>
- 停止等待人工确认；不要写 L2 或代码

## Stage 3 — L2 Design + 5 图
- 仅当 L1 confirmed 后开始
- 创建 L2: spec-manager spec new L2 --topic <topic> --parent <L1> --title "Design System + 5 Screens"
- 写 design tokens、组件、5 屏、screen-map、asset-manifest、P0 锁定
- 写 specs/DESIGN.md
- 生成 design/screens/S1..S5.png；Stitch 不可用按 fallback
- spec-manager spec validate <L2>
- 停止等待人工确认；不要写 L3 或代码

## Output
- L1 code / L2 code
- specs/DESIGN.md
- design/
- 需要人工确认的清单
```

## OpenCode Handoff

L2 confirmed 后，OpenCode 接手：

1. `spec-manager brief "implement P0" --topic <topic>`
2. `spec-manager spec show <L1/L2> --include-content`
3. 读 `specs/DESIGN.md`、`design/screens/`、`design/screen-map.md`
4. 创建 L3.1（`--parent <L2>`），人确认后 `approve` 冻结
5. `task create <L3.1> --plan ... --start`
6. 实现、`task step`、`task verify`、`task complete`

## 阶段 6 执行要点

- 优先加载 `app-store-prd-metadata`；不可用自动回退 `app-store-listing`，标记 `skill_fallback`。
- 商店截图 5 图是编辑约定；App Store Connect 接受 3–10 张/设备尺寸。
- 母版 1320x2868，另出 1206x2622（iPhone Dynamic Island medium tier）；iPad 如支持补 13-inch。
- PNG/JPEG、RGB、无 alpha；提交前复核当前 App Store Connect 规格。
- 保存 `06-store/gallery.json`，用 `check_gallery.py --check-files --assets-dir ... --size 1320x2868` 校验（需 Pillow）。
- G6 签核时检查截图尺寸/透明度/字幕/PRD metadata 一致性。

## 人工签核点

### G2：主题 + PRD

向用户展示：

- 推荐主题及理由、备选主题，明确「基于目标 App 的二创/优化」
- 竞品差异与风险
- P0 5 屏分配草案、明确不做的事
- PRD 起点：原始 PRD/hash、gap 分析、未改写范围
- 数据源为本地 mock，Repository 接口
- 关键假设与未决问题

请用户回复「通过」或指出修改项。未通过则回到阶段 2。  
通过后只执行 `spec-manager approve <L1>`；Codex 不得自行确认。

### G3：5 图与 P0 锁定

展示：

- 5 屏各自覆盖的功能
- **P0 锁定表**：每个 P0 需求落在哪一屏；5 图外是否还有 P0
- 设计 tokens 与视觉方向
- 与 PRD 的偏差
- 素材版权/来源风险
- 数据为本地 mock

请用户确认视觉方向与 5 屏范围。  
通过后执行 `spec-manager approve <L2>`；G3 通过后 `p0_lock: locked`，阶段 4 不再新增 P0。

### G4 入口：L3 冻结

展示：

- L3.1 实施步骤、文件级计划、验收标准、验证命令、回滚方案
- 是否只覆盖 5 图内的 P0
- 依赖的 L1/L2 code

请用户确认后执行 `spec-manager approve <L3.1>`；L3 未 frozen 不得写代码。

### G7：提测

展示：

- 包版本与 Build 号
- 真机验证结果
- 已知问题与非阻断项
- 提测范围与测试账号获取方式

请用户确认后提交测试。

### G8：归档

展示：

- L3.5 Archive & Handoff 的 manifest、checksums、release summary
- 归档范围与排除项（无密钥/证书/大二进制）
- `spec-manager flow status` 全链路 implemented

请用户确认归档位置与可交付性后结束工作流。

## 工具使用

- **spec-manager**：共享规格/任务/决策/证据。阶段 2/3 写 L1/L2，阶段 4/5 写 L3/Task。
- **Codex CLI**：执行阶段 2/3（L1/L2）。默认 handoff 暂停等待，用户同意时可用 `codex exec` 跑 handoff packet。
- **app-store-prd-metadata**：阶段 6 首选，更新 PRD 的 App Store 元数据/Review Notes/五图/Privacy-Terms；不可用时回退 `app-store-listing`。
- **Stitch MCP**：阶段 3 创建项目、设计系统、生成/编辑/变体屏幕。工具名以 `stitch_` 开头。
- **Figma MCP**：有现成设计稿时读取 tokens、组件、间距，减少重复设计。
- **Lark MCP**：需要跨团队评审时，把 PRD、素材清单、缺陷单同步为文档/表格；本地仍保留 `artifacts/` 为唯一真相。
- **图片生成（doubao / GPT）**：生成插画、背景、占位图；提示词写入 `design/prompts.md`。
- **awwwards.com**：只做风格参考，提取构图/排版/配色思路，不复制页面和资产。
- **OpenSpec**：项目已采用时按 `WORKFLOW.md` 的映射落盘；未安装时不要伪造命令。
- **rea skill（可选）**：需要更深的功能/实现逆向且用户授权时，先检查环境是否有 `rea` skill；有则加载，没有则回退公开行为分析。禁止用其绕过付费/登录/DRM。

## 失败与回退

| 情况 | 处理 |
| --- | --- |
| 缺当前阶段必需输入 | 状态 `blocked`，列缺失项，等用户 |
| PRD 文件不存在/无法读取 | 状态 `blocked`；PDF/DOCX 要求导出 Markdown，不猜测内容 |
| PRD 缺章节/自相矛盾 | 写入 `prd-intake.md` gap/冲突；向用户确认，不擅自补写范围 |
| 未提供 `--app-name` 且名称歧义 | 先问用户；PRD/L1 有明确名称则沿用，不擅自改名 |
| 缺第二平台链接/安装包 | 不阻塞；按已有平台继续，另一平台标记可选后补 |
| 缺开发者账号/签名/TF 权限 | 不阻塞阶段 0-6；阶段 7 再收集 |
| 缺真实数据 API | 不阻塞；使用本地 mock，Repository 接口预留 |
| 截止日期不可行 | 更新 `schedule.md`，给出缩范围/延期/增并行方案 |
| 门禁失败 | 状态 `in_progress`，记录失败项，回本阶段修复 |
| 需求变更 | 冻结后走 `spec-manager change`；同时写入 `02-prd/decisions.md`，做影响分析，回跑受影响门禁 |
| L3 未 frozen | 停止实现；先完成 L3、人工 approve |
| Task 缺 evidence | 不允许 `task complete`；补 verification 或记录真实失败 |
| spec-manager 不可用 | 回退 artifacts 工件流，状态标记 `spec-manager fallback`，不伪造 specs/tasks |
| Codex 不可用 | 自动降级：`stage_2_3=opencode`、`codex_fallback=true`；OpenCode 按 L1/L2 模板执行，仍要人工确认与 L3 冻结 |
| `app-store-prd-metadata` 不可用 | 自动降级 `app-store-listing`，标记 `skill_fallback=app-store-listing`；不伪造 PRD metadata |
| 工具不可用 | 按 WORKFLOW.md §9 降级：L1 换工具/模型 → L2 本地 fallback → L3 手工；标记 `fallback`/`unverified`，记录并复核 |
| `rea` skill 不可用 | 回退公开行为分析，不伪造逆向结果 |
| 测试发现阻断问题 | 回阶段 4 修复，重跑失败用例 + P0 冒烟 + 全量门禁 |
| 发布失败 | 保留上一个可用包，记录日志，修复后重新走 G7 |

## 输出风格

- 用中文，技术名词保留英文。
- 结论先行，再给证据路径。
- 每个阶段结束时给：已完成、spec code / task id、门禁结果、风险、下一步。
- Codex/OpenCode 交接必须给 spec topic、L1/L2/L3 code、handoff packet 路径，不要只给聊天摘要。
- 不写空泛总结；不把「计划」说成「已完成」。
