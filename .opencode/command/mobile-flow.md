---
description: 启动移动端全栈工作流：支持从目标 App 或已有 PRD 开始，Codex 通过 spec-manager 写 L1 PRD/L2 设计+5图，OpenCode 写 L3/Task 实现、测试、商店文案、TestFlight 与归档；支持 --app/--prd/--prd-spec/--topic 等参数与 --help 指引
agent: build
---

使用 skill 工具加载 `mobile-workflow`，然后严格按 `WORKFLOW.md` 的阶段 0 → 8 执行。

用户输入：

$ARGUMENTS

## 参数解析规则

1. 同时支持 `--key value` 和 `--key=value`；带空格的值用引号包起来。
2. 参数大小写敏感，重复参数以最后一次为准。
3. 优先级：命令行参数 > `artifacts/workflow-state.md` / `00-intake.md` > 交互提问。
4. 未知参数不要猜测：列出本文档的有效参数并停止。
5. 冲突参数直接报错：`--only-stage` 与 `--from-stage` 互斥；`--resume` 与 `--restart` 互斥；`--prd` 与 `--prd-spec` 互斥。
5.1 `--prd` 起点：默认从阶段 2 开始；只允许 `--from-stage 2` 或 `--only-stage 2`，其他阶段需先导入 L1 后用 `--prd-spec`。
5.2 `--prd-spec`：L1 confirmed 自动从阶段 3 开始；draft 先进入阶段 2 review。
6. 用户输入 `--help` 或 `-h` 时，只输出本文档的「参数」和「使用指引」，不执行工作流。
7. 参数里不要传密钥、密码、Token、keystore 密码；这些只从环境变量或 Keychain 读取。

## 可选参数

### 项目信息

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--app` | 商店 URL / APK/IPA 路径 / App 名 | 无；无 PRD 时阶段 1 前必填 | 分析对象；有 `--prd`/`--prd-spec` 时可选 |
| `--prd` | 文件路径 / URL | 无 | 从已有 PRD 开始；复制为 source-prd.md，阶段 1 可跳过，默认从阶段 2 intake |
| `--prd-spec` | 现有 L1 code，如 `myapp-L1` | 无 | 已有 spec-manager L1；confirmed 则默认从阶段 3 开始 |
| `--platform` | `auto` / `ios` / `android` / `both` | `auto` | 从 `--app` 链接自动推断；**一个平台链接即可**；`both` 是交付目标，缺少另一端时按已有平台继续 |
| `--stack` | `auto` / `rn` / `flutter` / `kotlin` / `java` | `auto` | 有仓库时自动识别；无仓库时询问 |
| `--market` | `cn` / `us` / `jp` / `zh-CN` / `en-US` 等 | 询问 | 目标市场与语言，影响竞品、ASO、文案 |
| `--repo` | 目录路径 | 当前目录 | 现有代码仓库；没有则写 `none` |
| `--scope` | 自由文本 | 询问 | 首版范围；P0 最终由 5 图锁定 |
| `--deadline` | `YYYY-MM-DD` / `auto` | `auto` | 截止日期；`auto` 时由排期自动修正 |
| `--lang` | `zh` / `en` | `zh` | 工作流产物语言（不是 App 语言） |
| `--topic` | 小写 slug，如 `pinedrama-p0` | 由 App 名 + P0 推导 | spec-manager topic；L1/L2/L3 共用 |

### 执行控制

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--from-stage` | `0`-`8` | 有状态续跑；`--prd` 时默认 `2` | 从指定阶段开始；前置门禁必须已通过，不能跳过 |
| `--only-stage` | `0`-`8` | 无 | 只执行一个阶段，适合重跑某阶段；仍需满足该阶段输入与门禁 |
| `--resume` | 开关 | 有状态时默认 | 从 `workflow-state.md` 断点续跑 |
| `--restart` | 开关 | 无 | 把旧 `artifacts/` 归档到 `artifacts-archive/<时间戳>/` 后从 0 开始；执行前需人工确认 |
| `--dry-run` | 开关 | 无 | 只输出执行计划、缺失参数与将生成的工件，不写产物、不改状态 |
| `--non-interactive` | 开关 | 无 | 不主动提问；缺必填项直接报错并列出缺项；G2/G3/G7 仍会停下来等签核 |
| `--artifacts` | 目录路径 | `artifacts` | 产物根目录；内部结构不变，`WORKFLOW.md` 与各 skill 中的 `artifacts/` 都按该根目录解析 |
| `--parallel` | `auto` / `1`-`5` | `auto` | 并行 Agent 数；自动识别可并行工作流并写入 `schedule.md` |
| `--reverse` | `auto` / `rea` / `off` | `auto` | 需要更深逆向时是否尝试 `rea` skill；不可用则回退公开分析 |
| `--spec-manager` | `on` / `off` | `on` | 使用 spec-manager 协作；off 时回退 artifacts，不伪造 specs/tasks |
| `--codex` | `auto` / `on` / `off` | `auto` | auto 检测 Codex；未安装自动降级 OpenCode；off 强制 OpenCode；on 要求 Codex |

### 设计与发布

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--design` | `stitch` / `figma` / `both` / `none` | `stitch` | 5 图原型工具；`both` 表示 Stitch 生成、Figma 校对 |
| `--image` | `doubao` / `gpt` / `none` | 询问或自动 | 插画/背景等素材生成工具 |
| `--channel` | `testflight` / `play-internal` / `firebase` / `both` | iOS→`testflight`，Android→`play-internal` | 内测分发渠道；`both` 只在双端都已构建时使用 |

### 帮助

| 参数 | 说明 |
| --- | --- |
| `--help` / `-h` | 输出参数表与使用示例，然后停止 |

### 不支持的参数

以下参数不会接受，避免绕过质量门禁或泄露密钥：

- `--skip-gates`、`--auto-approve`、`--yes`：G2/G3/G4/G7/G8 必须人工签核。
- `spec-manager task create --auto-confirm`：不得用于 L1/L2/L3 人工门禁。
- `--token`、`--password`、`--api-key`、`--keystore-password`：改用环境变量或 Keychain。
- `--force`：门禁失败请修复，或用 `--restart` 重新开始。

## Agent 路由

| 阶段 | 执行 | 产物 |
| --- | --- | --- |
| 0-1 | OpenCode | 建档、排期、功能知识库、Codex handoff |
| 2 主题/竞品/PRD | **Codex** | spec-manager L1 |
| 3 设计系统/5 图/icon/splash/P0 | **Codex** | spec-manager L2 + `specs/DESIGN.md` + `design/` |
| 4 实现 | **OpenCode** | L3.1 + Agent Task + 代码 |
| 5 自动化测试 | **OpenCode** | L3.2 + Agent Task + 测试证据 |
| 6 商店文案 | OpenCode（Codex 可选） | L3.3 + Task |
| 7 发布/TestFlight | **OpenCode** | L3.4 + Task |
| 8 归档/交接 | **OpenCode** | L3.5 + Task |

默认行为：

1. 阶段 0 初始化 spec-manager（`project init` + `agents install` + `doctor`）。
2. 阶段 1 结束生成 `artifacts/01-feature-spec/codex-handoff.md`，状态改 `awaiting_codex`，暂停。
3. 用户在 Codex 中执行 handoff，写 L1/L2；人确认后 `spec-manager approve`。
4. 回到 OpenCode 继续：读 L1/L2，写 L3、冻结、Task、编码。
5. 不要自动替 Codex 签核，也不要在 L3 frozen 前写代码。
6. Codex 未安装或 `--codex off`：自动降级 OpenCode 执行阶段 2/3，标记 `codex_fallback`，不阻塞。
7. G8 归档：L3.5 完成后生成 manifest/checksums/release summary，工作流才算结束。

## 工作流默认规则

1. **主题**：基于用户提供的目标 App 做二创/优化，保持同品类与核心闭环，不转向无关产品。
2. **P0**：P0 范围 = 5 图展示的内容；5 图外默认 P1/P2，不进入首版。
3. **数据**：MVP 全部使用本地 mock 数据；Repository 接口预留，真实 API 不作为 P0 依赖。
4. **排期**：`--deadline auto` 时自动排期；不可行时给出缩范围/延期/增并行方案，不硬卡。
5. **并行**：默认可并行分析/设计/开发/测试/文案工作流，结果写入 `schedule.md`。
6. **平台**：一个平台链接即可；iOS 链接就按 iOS 执行，不要求 Android Play 链接。
7. **逆向**：需要更深逆向且环境有 `rea` skill 时可使用；没有则回退公开行为分析。
8. **凭证**：开发者账号、签名、TestFlight 权限在阶段 7 才收集，前期不阻塞。
9. **图标/启动图**：阶段 3 同时产出 app-icon 与 splash；阶段 4 接入，阶段 7 验证。
10. **归档**：阶段 8 生成 manifest/checksums/release summary，G8 通过才算结束。

## 使用指引

### 1. 全流程，参数尽量给全

```text
/mobile-flow \
  --app "https://apps.apple.com/..." \
  --platform auto \
  --stack flutter \
  --market us \
  --scope "基于目标 App 的核心闭环做优化" \
  --deadline auto \
  --parallel 3
```

`--platform auto` 会从链接推断 iOS/Android；只给一个平台即可。P0 会在阶段 3 由 5 图锁定，数据默认本地 mock。  
阶段 2/3 默认交给 Codex；命令会生成 handoff packet 并暂停，等 Codex 写完 L1/L2 后回到 OpenCode。

### 2. 最简启动，缺什么问什么

```text
/mobile-flow --app "https://apps.apple.com/..."
```

Agent 只会询问当前阶段真正缺失的信息；平台从链接推断，发布账号/签名/TestFlight 权限等到阶段 7 才需要。

### 3. 断点续跑

```text
/mobile-flow --resume
```

读取 `artifacts/workflow-state.md`，校验已完成门禁后从 `next_action` 继续。

### 4. 从第 3 阶段开始（已有功能文档和 PRD）

```text
/mobile-flow --from-stage 3
```

如果 G1/G2 未通过或产物缺失，会停下来要求先补齐，不会硬跳。

### 5. 只重跑自动化测试

```text
/mobile-flow --only-stage 5
```

适合修完缺陷后重跑，不重复执行 PRD、设计和开发阶段。

### 6. 先看计划，不写文件

```text
/mobile-flow --dry-run --app "..." --platform ios --stack rn --market us
```

输出：将执行的阶段、缺失参数、预计产物、需要人工签核的节点。

### 7. CI / 脚本式调用

```text
/mobile-flow --non-interactive \
  --app "/path/to/app.apk" \
  --platform android \
  --stack kotlin \
  --market cn \
  --repo . \
  --scope "P0 闭环" \
  --channel play-internal \
  --parallel 2 \
  --deadline auto
```

缺少必填项时直接失败并列出缺项；到 G2/G3/G7 仍会暂停等人工确认。

### 8. 从已有 PRD 开始

```text
/mobile-flow --prd "./docs/prd.md" --platform ios --stack flutter --market us --topic myapp-p0
```

行为：

- 原始 PRD 复制到 `artifacts/02-prd/source-prd.md`，记录 SHA256。
- 阶段 1 可跳过（无 `--app` 时自动跳过）。
- 阶段 2 进入 L1 intake：生成 `prd-intake.md`，保留原始范围/需求 ID，缺章节标 gap，不擅自补写。
- 人工确认 L1 后进入阶段 3。

已有 spec-manager L1：

```text
/mobile-flow --prd-spec myapp-L1 --from-stage 3
```

### 9. 指定 spec-manager topic

```text
/mobile-flow --app "..." --topic pinedrama-p0 --spec-manager on
```

阶段 2/3 的 L1/L2 与阶段 4/5 的 L3/Task 都使用同一 topic；`spec-manager flow status --topic pinedrama-p0` 查看依赖。

### 10. 强制 OpenCode / Codex fallback

```text
/mobile-flow --app "..." --codex off
```

未安装 Codex 或使用 `--codex off` 时，阶段 2/3 自动由 OpenCode 执行，标记 `codex_fallback`，不阻塞流程。

### 11. 只执行归档

```text
/mobile-flow --only-stage 8 --topic pinedrama-p0
```

创建 L3.5 Archive & Handoff，归档 specs/design/store/release，生成 manifest/checksums。

### 12. 查看帮助

```text
/mobile-flow --help
```

### 13. 自然语言也可以

```text
/mobile-flow 基于这个 iOS App 做优化，用 Flutter，目标美国市场，P0 按 5 图展示内容，数据先用本地 mock，最后提测 TestFlight
```

自然语言中的信息按同样规则解析；缺失项再问。

## 执行要求

- 先解析参数，再检查 `artifacts/workflow-state.md`；有状态且未指定 `--restart` 时断点续跑。
- `--dry-run` 只读，不创建目录、不写工件、不改状态。
- 每个阶段加载对应 skill，产物写入 `--artifacts` 指定目录（默认 `artifacts/`）。
- 每个阶段结束检查门禁，未通过不进入下一阶段。
- G2、G3、G7 停下来等人工确认，不要自己签核。
- 主题必须基于目标 App 二创/优化；有 PRD 时以 PRD 为准，不擅自改写范围。P0 以 5 图为最终边界。
- `--prd` 起点：保存原始 PRD/hash，阶段 2 做 L1 intake；无 `--app` 时阶段 1 跳过，不伪造功能清单。
- `--prd-spec` 已 confirmed 时直接进阶段 3；draft 时先 review L1。
- 阶段 2/3 默认交给 Codex；先准备 handoff packet 并暂停，不要自己写 L1/L2。
- 未安装 Codex 或 `--codex off` 时，自动降级 OpenCode 执行 L1/L2，标记 `codex_fallback`。
- 阶段 4/5 由 OpenCode 执行；先写 L3 并冻结，再创建 Task 写代码。
- spec-manager 是 L1/L2/L3/Task/evidence 的共享真相；不伪造 specs/tasks/evidence。
- `--spec-manager on` 时先 `project init`/`agents install`/`doctor`；`off` 时回退 artifacts 并标记 `spec-manager fallback`。
- `--topic` 会贯穿 L1/L2/L3/Task；未指定时由 App 名 + P0 推导。
- L1/L2 未 confirmed、L3 未 frozen 时，不进入下一阶段/不写代码。
- 数据默认本地 mock；真实 API 不作为 P0 依赖。
- 只做一个平台；缺少另一端不阻塞。
- 开发者账号、签名、TestFlight 权限在阶段 7 才收集；前期不阻塞。
- `--deadline auto` 时自动排期，必要时给缩范围/延期/增并行方案。
- 可用多 Agent 并行分析、设计、开发、测试、文案；结果写入 `schedule.md`。
- 需要用 `rea` 时先检查 skill 是否可用；不可用则回退公开分析。
- 缺信息只问缺失项，不编造功能、竞品数据、下载量、评价。
- 不复制竞品代码、图片、文案、商标；不绕过登录/付费/DRM。
- 所有密钥、签名、测试账号只用环境变量或 Keychain，不写入仓库或工件。
- 阶段 8：创建 L3.5 Archive & Handoff，归档 specs/design/store/release，生成 manifest/checksums/release summary。
- `--non-interactive` 下缺必填项时，输出「缺项 + 示例命令」后停止，不要自行假设。
