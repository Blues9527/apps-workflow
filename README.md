# 移动端全栈开发工作流 + Skills

把「已上架 App 功能分析 / 已有 PRD → Codex 写 L1 PRD/L2 设计+5 图 → OpenCode 写 L3/Task 实现 → 自动化测试 → 商店文案 → TestFlight/内测提测」固化成一套由 **spec-manager** 协作、可断点续跑、带门禁、自动排期并支持多 Agent 并行的 Agent 工作流。

## 安装

仓库地址：<https://github.com/Blues9527/apps-workflow>

### 1. 克隆

```bash
git clone https://github.com/Blues9527/apps-workflow.git
cd apps-workflow
```

### 2. 项目内使用（推荐）

把 `.opencode/` 复制到你的 App 项目根目录：

```bash
cp -R /path/to/apps-workflow/.opencode /path/to/your-app/
cd /path/to/your-app
opencode
```

opencode 会加载项目内的 `/mobile-flow` 命令与 skills。

### 3. 全局安装

```bash
mkdir -p ~/.config/opencode/skills ~/.config/opencode/command
cp -R /path/to/apps-workflow/.opencode/skills/* ~/.config/opencode/skills/
cp /path/to/apps-workflow/.opencode/command/mobile-flow.md ~/.config/opencode/command/
```

重启 opencode 后，在任意项目里都可以使用 `/mobile-flow`。

### 4. 压缩包

如果不想用 git，可以在 GitHub 页面选择 **Code → Download ZIP**，解压后按上面的项目内或全局方式安装。

## 前置条件

| 依赖 | 是否必需 | 说明 |
| --- | --- | --- |
| OpenCode | 必需 | 运行 command 与 skills |
| spec-manager | 必需（默认） | L1/L2/L3、Task、evidence；`npm install -g spec-manager` |
| Codex CLI | 可选 | 阶段 2/3 写 L1/L2；未安装自动降级 OpenCode |
| Stitch MCP | 可选 | 5 图；不可用按 fallback |
| Figma / Lark MCP | 可选 | 设计稿/协作 |
| 图片生成（doubao/GPT） | 可选 | 插画/占位图 |

首次在目标项目初始化：

```bash
cd /path/to/your-app
spec-manager project init --name <project>
spec-manager project agents --provider all
spec-manager project doctor
```

如果 Codex 未安装，工作流会自动使用 OpenCode 执行阶段 2/3，并标记 `codex_fallback`。

## 快速使用

```text
/mobile-flow --app "https://apps.apple.com/..." --platform auto --stack flutter --market us --deadline auto --topic <topic>
```

只给一个平台链接即可；P0 由 5 图锁定，数据默认本地 mock，发布凭证到阶段 7 才需要。  
阶段 2/3 默认交给 Codex；命令会生成 `codex-handoff.md` 并暂停，等 L1/L2 确认后回到 OpenCode。

也可以直接说：

```text
用 mobile-workflow 从功能分析开始，走到 TestFlight 提测
```

### 从已有 PRD 开始

```text
/mobile-flow --prd "./docs/prd.md" --platform ios --stack flutter --market us --topic myapp-p0
```

- 原始 PRD 会复制到 `artifacts/02-prd/source-prd.md`，并记录 SHA256。
- 没有 `--app` 时阶段 1 可跳过；阶段 2 进入 L1 intake。
- 生成 `prd-intake.md`，保留原始范围/需求 ID；缺失章节标 gap，不擅自补写。
- 人工确认 L1 后进入阶段 3。
- `--prd` 只用于阶段 2 intake；要从阶段 3 开始请先用 `--prd-spec` 指向 confirmed L1。

已有 spec-manager L1：

```text
/mobile-flow --prd-spec myapp-L1 --from-stage 3
```

## 包含内容

```text
work-flow/
├── WORKFLOW.md                     # 主流程、门禁、工件契约、技术栈适配
├── README.md
├── .opencode/
│   ├── command/
│   │   └── mobile-flow.md          # /mobile-flow 命令
│   └── skills/
│       ├── mobile-workflow/        # 编排器
│       ├── mobile-feature-analysis/
│       ├── mobile-prd-authoring/
│       ├── mobile-ui-prototype/
│       ├── mobile-app-implementation/
│       ├── mobile-e2e-testing/
│       ├── app-store-prd-metadata/
│       ├── app-store-listing/          # fallback
│       ├── mobile-testflight-release/
│       └── mobile-release-archive/
└── templates/                      # 可直接复制到 artifacts/ 的模板
    ├── workflow-state.md
    ├── 00-intake.md
    ├── schedule.md
    ├── feature-inventory.md
    ├── prd.md
    ├── prd-intake.md
    ├── design-system.md
    ├── app-icon-splash.md
    ├── asset-manifest.md
    ├── test-plan.md
    ├── store-listing.md
    ├── release-checklist.md
    ├── codex-handoff.md
    ├── spec-manager-setup.md
    ├── spec-manager-migration.md
    ├── archive-manifest.md
    └── agent-plan.json
```

## Agent 路由与 spec-manager

```text
OpenCode 阶段 0-1
  └── Codex Handoff Packet
        └── Codex 阶段 2-3（spec-manager L1/L2 + specs/DESIGN.md + design/5 图）
              └── OpenCode 阶段 4-5（L3.1/L3.2 + Agent Task + 代码/测试）
                    └── OpenCode 阶段 6-8（L3.3 商店文案 / L3.4 TestFlight / L3.5 Archive）
```

| 阶段 | 执行 Agent | spec-manager |
| --- | --- | --- |
| 0-1 | OpenCode | project init、topic、handoff |
| 2 主题/竞品/PRD | **Codex** | L1 |
| 3 设计系统/5 图/icon/splash/P0 | **Codex** | L2 + `specs/DESIGN.md` + `design/` |
| 4 实现 | **OpenCode** | L3.1 + Agent Task |
| 5 自动化测试 | **OpenCode** | L3.2 + Agent Task |
| 6 App Store 元数据 | OpenCode（Codex 可选） | L3.3 + Task（优先 `app-store-prd-metadata`，fallback `app-store-listing`） |
| 7 发布/TestFlight | **OpenCode** | L3.4 + Task |
| 8 归档/交接 | **OpenCode** | L3.5 + Task |

Codex 未安装或不可用时，自动降级：`stage_2_3=opencode`、`codex_fallback=true`；OpenCode 按同一 L1/L2 模板执行，不进入 `awaiting_codex`。

初始化：

```bash
cd <project>
spec-manager project init --name <project>
spec-manager project agents --provider all
# 或 spec-manager codex install && spec-manager opencode install
spec-manager project doctor
```

硬规则：

- L1 未 confirmed 不写 L2；L2 未 confirmed 不写 L3；L3 未 frozen 不写代码。
- Codex 不写实现代码；OpenCode 不替 Codex 改 L1/L2。
- 所有 Task 必须记录 steps 与 verification evidence。
- spec-manager 不可用时回退 `artifacts/` 工件流，标记 `spec-manager fallback`。

## 2026-10-19 修订

针对试跑中暴露的卡点，工作流已调整为：

1. **主题二创**：主题必须基于目标 App，保持同品类与核心闭环。
2. **5 图定 P0**：P0 范围 = 5 图展示内容，G3 锁定，5 图外不做。
3. **Mock 数据**：MVP 全部本地 mock，Repository 接口预留，不接真实 API。
4. **自动排期**：`--deadline auto` 自动估算关键路径，支持多 Agent 并行，不可行时给缩范围/延期方案。
5. **单端优先**：一个平台链接即可；iOS 链接不再要求 Android Play 链接。
6. **rea 可选**：需要更深逆向且环境提供 `rea` skill 时使用，否则回退公开分析。
7. **凭证后置**：开发者账号、签名、TestFlight 权限在阶段 7 才收集，前期不阻塞。
8. **Codex 协作**：阶段 2/3 由 Codex 写 spec-manager L1/L2；阶段 4-8 由 OpenCode 写 L3/Task 并执行。
9. **自动降级**：未安装 Codex 时自动回退 OpenCode 执行阶段 2/3，标记 `codex_fallback`。
10. **图标/启动图**：阶段 3 同时产出 app-icon 与 splash-screen，阶段 4 接入。
11. **收尾归档**：新增阶段 8 Archive & Handoff，生成 manifest/checksums/release summary，G8 通过才算结束。
12. **PRD 起点**：支持 `--prd`/`--prd-spec`；阶段 1 可跳过，阶段 2 做 L1 intake，保留原始 PRD/hash/gap。

## 命令参数与使用指引

`/mobile-flow` 支持 `--key value` 和 `--key=value` 两种写法；带空格的值用引号包住。完整参数说明在 `.opencode/command/mobile-flow.md`，也可以直接运行：

```text
/mobile-flow --help
```

### 项目信息

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--app` | 商店 URL / APK/IPA 路径 / App 名 | 无 PRD 时必填 | 分析对象；有 PRD 时可选 |
| `--prd` | 文件路径 / URL | 无 | 从已有 PRD 开始；默认从阶段 2 intake |
| `--prd-spec` | 现有 L1 code | 无 | 已有 spec-manager L1；confirmed 默认从阶段 3 |
| `--platform` | `auto` / `ios` / `android` / `both` | `auto` | 从链接推断；一个平台即可；`both` 缺少另一端时按已有平台继续 |
| `--stack` | `auto` / `rn` / `flutter` / `kotlin` / `java` | `auto` | 有仓库时自动识别 |
| `--market` | `cn` / `us` / `jp` / `zh-CN` / `en-US` 等 | 询问 | 目标市场与语言 |
| `--repo` | 目录路径 / `none` | 当前目录 | 现有仓库 |
| `--scope` | 自由文本 | 询问 | 首版范围；P0 最终由 5 图锁定 |
| `--deadline` | `YYYY-MM-DD` / `auto` | `auto` | 截止日期；`auto` 自动排期 |
| `--lang` | `zh` / `en` | `zh` | 产物语言 |

### 执行控制

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--from-stage` | `0`-`8` | 有状态续跑；`--prd` 时默认 `2` | 从指定阶段开始，前置门禁必须通过 |
| `--only-stage` | `0`-`8` | 无 | 只跑一个阶段，适合重跑 |
| `--resume` | 开关 | 有状态时默认 | 断点续跑 |
| `--restart` | 开关 | 无 | 归档旧产物后从 0 开始，需确认 |
| `--dry-run` | 开关 | 无 | 只输出计划，不写文件 |
| `--non-interactive` | 开关 | 无 | 不提问，缺项直接报错；签核点仍暂停 |
| `--artifacts` | 目录路径 | `artifacts` | 产物根目录，内部结构不变 |
| `--topic` | 小写 slug | 自动推导 | spec-manager topic，L1/L2/L3 共用 |
| `--spec-manager` | `on` / `off` | `on` | 使用 spec-manager 协作；off 回退 artifacts |
| `--codex` | `auto` / `on` / `off` | `auto` | auto 检测 Codex；未安装自动降级 OpenCode |
| `--parallel` | `auto` / `1`-`5` | `auto` | 并行 Agent 数，自动生成 `schedule.md` |
| `--reverse` | `auto` / `rea` / `off` | `auto` | 是否尝试 `rea` skill 做更深逆向 |

### 设计与发布

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `--design` | `stitch` / `figma` / `both` / `none` | `stitch` | 原型工具 |
| `--image` | `doubao` / `gpt` / `none` | 询问/自动 | 素材生成工具 |
| `--channel` | `testflight` / `play-internal` / `firebase` / `both` | 按平台 | 内测渠道 |

### 常用示例

```text
# 全流程（单端链接即可，自动排期，3 个 Agent 并行）
/mobile-flow --app "https://apps.apple.com/..." --platform auto --stack flutter --market us --scope "基于目标 App 的核心闭环做优化" --deadline auto --parallel 3

# 分别从已有 PRD / 现有 L1 开始
/mobile-flow --prd "./docs/prd.md" --platform ios --stack flutter --market us --topic myapp-p0
/mobile-flow --prd-spec myapp-L1 --from-stage 3

# 最简启动，缺什么问什么
/mobile-flow --app "https://play.google.com/store/apps/details?id=..."

# 断点续跑
/mobile-flow --resume

# 已有功能文档和 PRD，从 5 图开始
/mobile-flow --from-stage 3

# 只重跑自动化测试
/mobile-flow --only-stage 5

# 只执行归档
/mobile-flow --only-stage 8 --topic pinedrama-p0

# 先看计划，不写文件
/mobile-flow --dry-run --app "..." --platform ios --stack rn --market us

# CI / 脚本式调用
/mobile-flow --non-interactive --app "/path/to/app.apk" --platform android --stack kotlin --market cn --repo . --scope "P0 闭环" --channel play-internal --parallel 2 --deadline auto
```

不支持 `--skip-gates`、`--auto-approve`、`--yes`，也不接受在命令行传 Token、密码、API Key 或 keystore 密码；这些只从环境变量或 Keychain 读取。

## 工作流默认规则

- **二创/优化**：主题必须基于目标 App，保持同品类与核心闭环，不转向无关产品。
- **5 图定 P0**：P0 = 5 图展示的内容；5 图外默认 P1/P2，不进入首版。
- **PRD 起点**：支持 `--prd`/`--prd-spec`；保留原始 PRD/hash/gap，阶段 1 可跳过，阶段 2 做 L1 intake。
- **Mock 优先**：MVP 数据全部本地 mock，Repository 接口预留，真实 API 不作为 P0 依赖。
- **单端足够**：提供一个平台链接/安装包即可；另一平台可选后补。
- **凭证后置**：开发者账号、签名、TestFlight 权限在阶段 7 才收集。
- **自动排期**：`--deadline auto` 时自动估算关键路径，不可行则给缩范围/延期/增并行方案。
- **并行 Agent**：分析、设计、开发、测试、文案可并行；结果写入 `schedule.md`。
- **逆向可选**：需要更深逆向且环境有 `rea` skill 时使用，否则回退公开分析。
- **Codex 分工**：阶段 2/3 默认交给 Codex 写 L1/L2，写完停下等人工确认；未安装 Codex 自动降级 OpenCode。
- **OpenCode 分工**：阶段 4-8 先写 L3 并冻结，再创建 Agent Task 写代码/测试/文案/发布/归档。
- **图标/启动图**：阶段 3 同时产出 app-icon 与 splash；阶段 4 接入，阶段 7 验证。
- **商店元数据**：阶段 6 优先 `app-store-prd-metadata`；不可用自动回退 `app-store-listing`，标记 `skill_fallback`。
- **归档**：阶段 8 生成 manifest/checksums/release summary，G8 通过才算结束。
- **spec-manager 真相**：L1/L2/L3/Task/evidence 以 spec-manager 为准；不伪造、不跳过。

## 工具降级策略

工具失败不阻塞流程，但不能伪造结果：

- **L0**：首选工具（Stitch、Figma、Lark）。
- **L1**：换同类工具/模型/参数（如 Stitch lite 模型、Figma 导出截图）。
- **L2**：本地 fallback（HTML/CSS 5 图 + Chrome 截图、本地 mock 数据）。
- **L3**：手工/未验证产物，必须显式标记。

Codex 未安装时自动降级 OpenCode 执行阶段 2/3（`codex_fallback=true`），不阻塞；spec-manager 不可用时回退 artifacts 工件流。

降级必须写入 `decisions.md` 和 `prompts.md`；fallback 可让人工签核 G3 并锁定 P0，但商店截图/最终视觉必须在 G6 前替换。详见 `WORKFLOW.md` 第 9 节。

## 阶段与产出

| 阶段 | 执行 Agent | 关键产出 | 人工签核 |
| --- | --- | --- | --- |
| 0 启动 | **OpenCode** | `00-intake.md`、`schedule.md`、`workflow-state.md`、spec-manager init（skill: `mobile-workflow`） | - |
| 1 功能分析（可选） | **OpenCode** | 功能清单、页面、流程、规则、术语、Codex handoff（skill: `mobile-feature-analysis`） | G1（PRD 起点可跳过） |
| 2 二创主题/竞品/PRD | **Codex** | `L1` + `theme.md`、`competitors.md`、`prd.md` | G2 |
| 3 素材/5 图/icon/splash | **Codex** | `L2` + `specs/DESIGN.md` + `design/` | G3 |
| 4 框架/填充 | **OpenCode** | `L3.1` + Task + 可运行 App | G4 |
| 5 自动化测试 | **OpenCode** | `L3.2` + Task + 脚本/报告 | G5 |
| 6 App Store 元数据 | OpenCode（Codex 可选） | `L3.3` + PRD metadata/`listing.md`/`release-notes.md`（优先 `app-store-prd-metadata`，fallback `app-store-listing`） | G6 |
| 7 打包提测 | **OpenCode** | `L3.4` + Release 包、设备矩阵、提测单 | G7 |
| 8 归档 | **OpenCode** | `L3.5` + archive manifest/checksums/release summary | G8 |

`artifacts/` 保存证据与阅读副本；`specs/`、`.spec-manager/`、`design/` 由 spec-manager 与 Codex/OpenCode 共享。目录契约见 `WORKFLOW.md`。

## 设计原则

- **工件驱动**：结论必须落盘，下一个 Agent 只读文件就能接手。
- **门禁制**：G0-G7 逐级通过，失败回到本阶段修复。
- **证据优先**：竞品与数据标注来源和日期，推断标「假设」。
- **人工签核**：主题/PRD、5 图与 P0 锁定、提测必须由人确认。
- **目标一致**：主题基于目标 App 二创/优化，不偏离品类与核心闭环。
- **5 图定 P0**：P0 以 5 图为准，5 图外不做。
- **Mock 优先**：MVP 本地 mock，真实 API 不作为 P0 依赖。
- **单端优先**：一个平台链接即可，另一端不阻塞。
- **合规原创**：只分析公开行为，不复制竞品资产，不绕过付费/登录/DRM。
- **密钥安全**：签名、API Key、测试账号只走环境变量或 Keychain；阶段 7 才收集。

## 工具与栈

- Agent: OpenCode（实现/编排）+ Codex（L1 PRD/L2 设计）
- 协作: spec-manager（L1/L2/L3/Agent Task/Decision/Evidence）
- 模型: Claude / GPT / DeepSeek / GLM
- 商店元数据: `app-store-prd-metadata`（fallback `app-store-listing`）
- MCP: Stitch（已支持）、Figma、Lark
- UI: Stitch、GPT、doubao、awwwards（仅参考）
- 技术栈: React Native、Flutter、Kotlin、Java
- 逆向: 可选 `rea` skill（环境提供时）；不可用则回退公开分析
- 规范: 可选 OpenSpec 映射，见 `WORKFLOW.md` 第 8 节

Stitch 相关 skill 使用 `stitch_*` MCP 工具：创建项目、设计系统、生成屏幕、变体、编辑与读取。没有 Stitch MCP 时，skill 会要求产出可复现的提示词和手工步骤，不伪造结果。

## 使用注意事项

- **不要提交密钥**：`opencode.json` 里的 API Key、Stitch Key、App Store Connect API Key、证书、keystore、TestFlight 账号都不要进仓库；用环境变量或 Keychain。
- **不要提交测试产物**：`artifacts/`、`artifacts-pinedrama/`、`pinedrama_app/`、`.opencode/node_modules/`、`.DS_Store` 默认不分享；示例 demo 可单独放仓库。
- **spec-manager 按项目初始化**：每个目标 App 项目执行一次 `project init` + `agents install`；不要共用别人的 `.spec-manager/`。
- **安装后重启 opencode**：skills 与 command 在启动时加载，新复制后需要重启。
- **Codex 可选**：未安装会自动 `codex_fallback`；如果强制 `--codex on`，需要先安装并登录 Codex CLI。
- **门禁不可跳过**：L1/L2 未 confirmed、L3 未 frozen 不写代码；G2/G3/G4/G7/G8 需要人工签核。
- **5 图定 P0**：P0 = 5 图展示内容；5 图外默认 P1/P2。
- **PRD 起点**：`--prd` 时保存原始 PRD/SHA256/`prd-intake.md`，不擅自改写范围；`--prd-spec` 已 confirmed 可直接从阶段 3 开始。
- **Mock 优先**：MVP 数据本地 mock，真实 API/CDN 不作为 P0 依赖。
- **单端足够**：一个平台链接即可；另一平台可选后补。
- **归档**：阶段 8 生成 archive manifest/checksums/release summary；归档中不得含密钥或大二进制。
- **素材版权**：不复制竞品代码、图片、文案、商标；Stitch/生成图/字体要保留来源与授权记录。
- **License**：本仓库当前未附 LICENSE；公开分发前请补充你选择的许可证（如 MIT / Apache-2.0），并确认第三方依赖与素材的授权。

## License

本仓库暂未附 `LICENSE` 文件。公开分享前请添加许可证，并确认工作流中引用的第三方工具、字体、图片与示例素材的授权边界。

## 自定义

- 改阶段内容：直接编辑对应 `SKILL.md`。
- 改模板：编辑 `templates/`；skill 会按固定路径写入 `artifacts/`。
- 增删阶段：同步更新 `WORKFLOW.md` 的阶段表、`mobile-workflow` 的阶段对照和状态机。
- 改 Agent 路由：同步更新 `WORKFLOW.md` §2.5、`mobile-flow` 的 Agent 路由、各阶段 skill 的 spec-manager 命令。
- 保持 skill 目录名与 frontmatter `name` 一致，否则 opencode 不会正确加载。

## 验证

```bash
find .opencode -name SKILL.md -maxdepth 4 | sort
find templates -type f | sort
```

重启 opencode 后，用 `/mobile-flow` 或在对话里说「跑移动端全流程」验证 skill 是否被加载。
