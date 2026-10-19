---
name: mobile-app-implementation
description: 由 OpenCode 读取 confirmed L2 与 specs/DESIGN.md，写 L3.1 并冻结，创建 spec-manager Agent Task，只实现 5 图锁定的 P0 垂直切片，使用本地 mock 数据，支持 React Native、Flutter、Kotlin、Java。Use when the user says 搭框架、填充功能、实现 PRD、开发 App、RN/Flutter/Kotlin/Java 实现、vertical slice、build the app skeleton，or asks to turn approved screens and requirements into working code.
---

# 框架搭建与功能填充

目标：先搭一个能跑、能扩展的骨架，再只实现 5 图锁定的 P0 垂直切片。每个切片都包含 UI、业务逻辑、状态处理、埋点和测试；MVP 数据全部本地 mock。

## 输入

- confirmed L1/L2（spec-manager）
- `specs/DESIGN.md`（design tokens / do / don't）
- `design/`（5 图、app-icon、splash、screen-map、asset-manifest、P0 锁定表）
- `artifacts/04-build/architecture.md`（已有则先读）
- 现有代码仓库、技术栈、CI 约束
- 目标平台：由用户提供的单端链接决定；另一平台可选后补
- 数据策略：本地 mock + Repository 接口，不接真实 API

## OpenCode + spec-manager 模式（默认）

本阶段由 **OpenCode** 执行：先写 L3.1 并冻结，再创建 Agent Task，最后写代码。

开始前：

```bash
spec-manager brief "实现 P0" --topic <topic>
spec-manager spec show <L2> --include-content
spec-manager spec show <L1> --include-content
```

创建 L3.1：

```bash
spec-manager spec new L3 --topic <topic> --parent <L2> --title "P0 Implementation" --desc impl
spec-manager template L3 --title "P0 Implementation" --output .spec-manager/drafts/<topic>-L3-impl.md
# 填写文件级步骤、验收标准、验证命令、回滚方案、AC 映射
spec-manager spec update <L3.1> --content .spec-manager/drafts/<topic>-L3-impl.md   --ai-summary "<一句话摘要>" --change-summary "initial L3 implementation"
spec-manager spec validate <L3.1>
spec-manager spec validate-plan tasks/<topic>-L3-impl-plan.json
```

硬规则：

- L3.1 未 `approve`（frozen）不得写代码。
- 人工确认后执行 `spec-manager approve <L3.1>`。
- 创建 Task：`spec-manager task create <L3.1> --plan ... --start`。
- 每步用 `spec-manager task step` 记录；完成前用 `spec-manager task verify` 记录证据。
- 只实现 5 图内的 P0；P1/P2 不进入首版。
- 不使用 `--skip-verification` / `--skip-verify` 绕过验证。

## 流程

### 第 1 步：识别仓库与技术栈

先看，不猜：

```bash
ls -la
cat package.json 2>/dev/null
cat pubspec.yaml 2>/dev/null
cat build.gradle.kts 2>/dev/null || cat build.gradle 2>/dev/null
cat settings.gradle.kts 2>/dev/null || cat settings.gradle 2>/dev/null
```

iOS 工程先列 workspace/scheme，不硬编码：

```bash
xcodebuild -list -workspace <Name>.xcworkspace
```

Android 先列任务：

```bash
./gradlew tasks
```

记录：

- 目标平台：iOS 链接就按 iOS 构建，不要求 Android 工程；Android 链接就按 Android，`both` 才双端。
- 框架与版本（RN/Expo、Flutter、Kotlin/Compose、Java/Views）
- 导航、状态、数据层、存储、主题、测试现有方案
- 是否已有设计系统、组件库、CI、发布脚本
- 不要引入第二套导航/状态/网络库；必须引入时写 ADR

### 第 2 步：写架构决策

在 `04-build/architecture.md` 记录：

- 模块划分：feature-first，按业务域分，不按技术层堆
- 导航图：页面 ID 与 5 屏一一对应
- 状态管理：全局/页面/本地状态边界
- 数据层：`Repository` 接口 + 本地 mock 数据源（JSON/assets），禁止把真实 API 作为 P0 依赖
- 本地存储：Watchlist、搜索历史、缓存、迁移
- 主题：tokens 单一来源，禁止散落硬编码色值
- 错误与空态：统一组件与文案规范
- 埋点：事件命名、参数、上报时机
- 特性开关：本地开关即可；远程 kill switch 可作为 P2
- 环境：MVP 只需 dev / release；真实环境后置

栈适配建议（沿用已有优先）：

| 栈 | 导航 | 状态 | 网络 | 存储 | 测试 |
| --- | --- | --- | --- | --- | --- |
| RN | React Navigation / Expo Router | Zustand / Redux Toolkit | TanStack Query + fetch/axios | MMKV / AsyncStorage | RNTL + Maestro/Detox |
| Flutter | go_router | Riverpod / Bloc | Dio | Drift / Hive | integration_test / Patrol |
| Kotlin | Navigation Compose | ViewModel + Flow | Retrofit/OkHttp | Room | Compose Test + Espresso |
| Java | Navigation Component | ViewModel + LiveData | Retrofit/OkHttp | Room | JUnit + Espresso |

### 第 3 步：搭骨架

骨架必须包含：

1. App 壳：启动、根导航、主题、字体、深色模式（若支持）
2. design tokens 映射：颜色、字体、间距、圆角、阴影
3. 共享组件：按钮、输入框、卡片、列表、空态、加载、错误、Toast/Dialog
3.1 App icon / splash：把 `design/app-icon/` 与 `design/splash/` 接入 iOS/Android；iOS 更新 `Assets.xcassets/AppIcon.appiconset` 与 LaunchScreen；Android 更新 mipmap/adaptive icon 与 splash 主题
4. 导航骨架：5 屏对应页面可进入，Tab/返回行为正确
5. 数据层：`Repository` 接口 + 本地 mock 数据源；UI 不直接读 JSON，不把假数据散落在页面里
6. 开发菜单：只在 debug 构建可见，可重置数据、切换空/错/离线模拟
7. 基础测试：至少 1 个启动/导航冒烟测试

骨架验收：目标单端能构建、能启动、5 屏可导航、主题一致、mock 数据可通过 Repository 替换。

### 第 4 步：按垂直切片实现

顺序：P0 主路径 → P0 异常/空态 → P0 需要的系统能力 → 打磨。**不实现 P1/P2**，除非用户明确批准变更。

每个切片必须同时完成：

- UI：对照 5 图与 tokens，不临时发明样式
- 领域逻辑：校验、状态转换、边界条件
- 数据：本地 mock Repository，覆盖成功/空/错误/离线；接口可替换
- 状态：加载、空、错误、离线、无权限、成功
- 埋点：按 PRD 事件表上报
- 测试：至少覆盖验收标准的自动化或可重复手工步骤
- 可访问性：语义标签、焦点顺序、动态字号、对比度
- 范围：只做 5 图里出现的 P0，不新增第 6 屏功能

切片完成定义：

```text
R-012 保存草稿
- UI: 编辑页返回/切后台触发
- 数据: 本地存储写入，失败提示
- 状态: 成功静默、失败 Toast、恢复草稿
- 埋点: draft_save_success / draft_save_failed
- 测试: 单元测试 + 1 条 E2E 草稿恢复流程
- 证据: 截图/录屏路径
```

### 第 5 步：视觉与交互对齐

- 用 `screen-map.md` 对照每个页面与 S1-S5。
- 每个页面完成后截屏对比原型：间距、字号、颜色、层级、圆角。
- 差异分三类：实现错误（修）、设计未定义（补 tokens/规范）、平台差异（记录理由）。
- 建立组件预览/Storybook（若栈支持），避免只在一个页面验证组件。

### 第 6 步：关键集成

只接入 P0 需要的系统能力，逐项验证：

- 深链/推送（仅当 P0 包含）
- 支付/订阅（仅当 P0 包含，且用沙盒）
- 相机/相册/定位/通知权限与拒绝降级（仅当 P0 包含）
- 离线缓存与重试（P0 基础能力）
- 国际化（en-US 起，结构预留）
- 崩溃上报与性能监控
- 本地特性开关；远程配置后置

如需逆向已有实现，可在用户授权且环境提供时加载 `rea` skill；否则按公开行为与 PRD 实现，不猜测内部代码。

### 第 7 步：清理与加固

Release 前必须：

- 删除 P0 假实现、TODO 桩、硬编码测试数据
- 调试菜单、日志、测试后门仅在 debug 可用
- 密钥、token、证书不入库；用环境变量/Keychain/Keystore
- 日志不打印 PII、token、完整请求体
- 权限文案与隐私清单匹配实际使用
- 确认包体积、启动时间、内存无明显回归

## 产出

```text
artifacts/04-build/
├── architecture.md
├── feature-status.md
└── implementation-log.md
```

`feature-status.md` 列：

| 需求 ID | 页面/屏幕 | 状态 | 测试 | 埋点 | 备注 |
| --- | --- | --- | --- | --- | --- |
| R-001 | S1 | done | pass | done | - |
| R-012 | S3 | in_progress | partial | todo | 草稿冲突待定 |

`implementation-log.md` 记录偏差：原型与实现不一致、第三方限制、需求变更、技术债。

## G4 门禁

- [ ] L3.1 已 `validate` 并经人工 `approve`（frozen）
- [ ] L3.1 Agent Task 已创建并完成
- [ ] Task steps 与 verification evidence 可追溯
- [ ] 目标单端可构建、可启动；另一平台未构建不阻塞
- [ ] 5 屏对应页面可导航，视觉与 tokens 一致
- [ ] app-icon 与 splash-screen 已接入目标端并在真机/模拟器显示正确
- [ ] 全部 P0 功能通过验收标准，且与 5 图一一对应
- [ ] 不存在 5 图之外的 P0 功能
- [ ] 数据层为本地 mock，Repository 接口可替换；无真实 API 作为 P0 依赖
- [ ] 无 P0 假实现、TODO 桩、硬编码测试数据
- [ ] lint、typecheck、单元测试通过
- [ ] 加载/空/错误/离线/无权限状态可用
- [ ] P0 需要的系统能力已验证；未列入 P0 的能力未强行接入
- [ ] 无密钥、调试菜单、测试后门进入 Release 配置
- [ ] 性能与包体积在预算内或有记录
- [ ] `feature-status.md` 与实际一致

## 常见错误

- 5 图之外偷偷加 P0：首版永远做不完
- 把 P1/P2 当 P0 实现：范围膨胀
- 依赖真实 API：没有后端就无法构建/演示
- 把 mock 数据散落在 UI：无法替换、无法测试
- 因缺少另一平台链接而停住：单端即可交付
- 先堆页面再补逻辑：每个页面都「差不多」，没有一条完整闭环
- 每个页面自己写按钮/颜色：设计系统失效
- 只做 happy path：空态和错误态上线后暴露
- 引入第二套状态/导航库：维护成本翻倍
- 开发菜单和测试后门带进 Release
- 视觉「大致像」就算完成：间距、层级、触控区全部漂移
