---
name: mobile-e2e-testing
description: 由 OpenCode 创建 spec-manager L3.2 与 Agent Task，为移动应用编写并运行自动化主流程测试，只覆盖 5 图锁定的 P0、本地 mock 数据与目标单端，分级缺陷并循环修复到无阻断问题，记录 verification evidence。Use when the user says 自动化测试、主流程测试、E2E、跑回归、阻断性问题、Maestro、Detox、Patrol、Espresso、XCUITest，or asks to verify an app before release.
---

# 自动化主流程测试

目标：用可重复的自动化脚本证明 P0 主流程可用，并把阻断问题清零。测试不是「跑一下看看」，而是有范围、有数据、有证据、有退出条件。

## 输入

- 可运行的目标单端 App（debug / release 候选包）
- `02-prd/prd.md` 的验收标准
- `03-design/screen-map.md` 的 P0 锁定表
- `04-build/feature-status.md`
- 本地 mock 数据与固定 seed（不依赖后端/真实账号）
- 设备/模拟器清单

## OpenCode + spec-manager 模式（默认）

本阶段由 **OpenCode** 执行：创建 L3.2 测试规格并冻结，再创建 Agent Task 运行测试与修复。

```bash
spec-manager flow status --topic <topic>       # 确认 L3.1 implemented
spec-manager spec new L3 --topic <topic> --parent <L2> --title "Automated P0 E2E" --desc e2e
spec-manager template L3 --title "Automated P0 E2E" --output .spec-manager/drafts/<topic>-L3-e2e.md
# 填写测试范围、框架、用例、数据、运行命令、通过标准、证据路径
spec-manager spec update <L3.2> --content .spec-manager/drafts/<topic>-L3-e2e.md   --ai-summary "<summary>" --change-summary "initial L3 E2E"
spec-manager spec validate <L3.2>
# 人工确认后
spec-manager approve <L3.2>
spec-manager task create <L3.2> --plan tasks/<topic>-L3-e2e-plan.json --start
```

规则：

- L3.2 依赖 L3.1；L3.1 未 implemented 不执行全量 E2E。
- L3.2 未 frozen 不创建 Task。
- 每个测试轮次用 `spec-manager task step` 记录；通过标准用 `spec-manager task verify` 记录。
- 修复 Blocker/P1 后重跑失败用例 + P0 冒烟 + 全量；完成后 `spec-manager task complete <taskId>`。

## 流程

### 第 1 步：定义测试范围

只测 5 图锁定的 P0，不把 P1/P2 当发布门槛：

| 范围 | 是否自动化 |
| --- | --- |
| 5 图内的 P0 主路径（首页/搜索/详情/收藏/设置等） | 必须 |
| P0 的空/错/离线/图片失败/重复操作 | 必须 |
| P0 需要的权限（相册/通知等，仅当 P0 使用） | 必须 |
| 外部观看入口（mock 链接/占位页） | 必须 |
| P1/P2 功能 | 不测或抽测，不阻塞 |

在 `test-plan.md` 写清：测什么、不测什么、为什么、风险在哪。测试范围必须能回溯到 P0 锁定表。

### 第 2 步：选择测试框架

| 栈 | 推荐 | 说明 |
| --- | --- | --- |
| RN | Maestro / Detox | Maestro 黑盒、YAML 简单；Detox 灰盒、同步更稳 |
| Expo | Maestro + EAS | 真机/模拟器均可，注意 dev build |
| Flutter | integration_test + Patrol | Patrol 支持原生弹窗与权限 |
| Kotlin | Compose UI Test + Espresso + UIAutomator | 跨 App 系统交互用 UIAutomator |
| Java | Espresso + UIAutomator | 同上 |
| 原生 iOS | XCUITest | 系统权限/推送/深链验证 |

优先用仓库已有框架，不为了「新」引入第二套。

### 第 3 步：准备测试数据与环境

- 使用本地 mock 数据与固定 seed；每次运行前回到已知状态
- 不依赖真实账号、后端、支付；如 P0 有登录/支付，则用 mock 适配器或沙盒
- 唯一标识（时间戳/UUID）避免并发冲突
- 弱网/离线用系统网络链路工具或本地 mock 开关模拟
- 测试数据不写真实用户数据；截图/录屏脱敏

### 第 4 步：写稳定选择器

优先级：

1. `testID` / `accessibilityIdentifier`
2. 语义标签 / `contentDescription`
3. 稳定文本（仅当文案不会变）
4. 避免：索引、XPath、坐标、临时 class name

如果控件没有稳定标识，先让开发补，不要用 `tap(0.5, 0.5)` 硬点。

### 第 5 步：编写 P0 流程

按 5 图的实际 P0 覆盖，典型内容/资料类 App：

1. 首次启动 → 首页（含空/加载/错误）
2. 首页 → 详情 → 加入待看 → Watchlist
3. 搜索 → 结果 → 详情
4. Explore/分类 → 列表 → 详情
5. Watchlist 移除/撤销/空态
6. 详情 → 外部观看入口（mock 链接）
7. 设置 → 隐私/清数据
8. 离线/弱网/图片失败/重复点击

仅当 P0 包含时才加测：登录、支付、推送、深链、相册权限。不要为 P1/P2 写发布阻断用例。

用例格式：

```markdown
### TC-003 核心任务-提交成功

- 关联需求: R-012
- 优先级: P0
- 前置: 已登录；草稿为空
- 步骤:
  1. 打开 S3 编辑页
  2. 输入合法内容
  3. 点击提交
- 预期:
  - 显示成功态并返回详情
  - 列表出现新内容
  - 埋点 submit_success 上报
- 选择器: screen.s3.editor / action.submit
- 数据: test_user_01
- 证据: reports/TC-003.mp4
```

### 第 6 步：运行与分级

先跑冒烟，再跑全量 P0。每次失败必须归类：

| 级别 | 定义 | 例子 |
| --- | --- | --- |
| Blocker | 无法继续测试或核心不可用 | 启动崩溃、登录失败、支付扣款错误、数据丢失 |
| P1 | 主要功能不可用，无绕过 | 核心任务提交失败、深链全部失效 |
| P2 | 有绕过或影响局部 | 某筛选条件错误、次要页面崩溃 |
| P3 | 体验/文案/样式 | 间距、错别字、非关键动画 |

写入 `bugs.md`：复现步骤、期望/实际、设备/系统/构建号、日志、截图/录屏、关联需求。

### 第 7 步：修复循环

规则：

1. Blocker/P1 必须修复，修复后先跑失败用例，再跑 P0 冒烟。
2. 每轮修复后跑全量 P0，避免回归。
3. 同一用例连续失败 2 次仍不稳定，标记 flaky，单独排查；不要靠无限重试掩盖。
4. 阻断问题清零前，不进入商店文案与发布阶段。
5. 修不了的问题写清绕过方案、影响范围、负责人和截止时间；Blocker 不允许带病发布。

### 第 8 步：稳定性与 CI

- 禁止固定 `sleep`；用等待元素/网络空闲/动画结束。
- 每个用例独立重置状态，避免顺序依赖。
- 失败自动保存截图、录屏、日志。
- CI：PR 跑冒烟， nightly 跑全量；设备矩阵至少覆盖小屏与大屏、一个旧系统。
- 记录运行时长与 flaky 率；超过预算先修稳定性再加用例。

## 产出

```text
artifacts/05-test/
├── test-plan.md
├── cases/
│   ├── TC-001-onboarding.md
│   ├── TC-002-login.md
│   └── ...
├── reports/
│   ├── run-YYYYMMDD-HHmm.md
│   ├── screenshots/
│   └── videos/
└── bugs.md
```

报告包含：构建号、环境、设备矩阵、通过/失败/跳过、失败归因、flaky、覆盖的 P0 需求、结论（可提测/不可提测）。

## G5 门禁

- [ ] L3.1 已 implemented
- [ ] L3.2 已 `validate` 并经人工 `approve`（frozen）
- [ ] L3.2 Agent Task 已创建并完成
- [ ] 5 图锁定的全部 P0 主流程自动化通过
- [ ] P0 的空/错/离线/重复操作路径已覆盖
- [ ] 仅测试 P0 需要的权限/集成；P1/P2 不作为发布门槛
- [ ] Blocker = 0，P1 = 0（或有人签核的明确豁免）
- [ ] 无「靠重试才通过」的假绿
- [ ] 失败用例有复现步骤、日志、截图/录屏
- [ ] 使用本地 mock 数据可重复运行，不依赖后端
- [ ] 目标单端通过；另一平台未构建不阻塞
- [ ] 报告已归档，结论明确

## 常见错误

- 测试 5 图之外的 P1/P2，把范围拖垮
- 依赖真实后端/账号，测试无法重复
- 只测 happy path：上线后死在空态、权限、弱网
- 用文本/坐标做选择器：文案一改全挂
- 用例之间共享状态：单独跑过，一起跑失败
- 失败就加重试：掩盖真实缺陷
- 只在一台模拟器跑：真机/小屏/旧系统问题漏掉
- 测试数据写生产库：污染真实用户
- 把 Blocker 记成「已知问题」直接发布
