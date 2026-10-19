---
name: mobile-testflight-release
description: 在 spec-manager L3.4 中构建并上传移动端 Release 包到 TestFlight/Google Play 内测，完成真机新装与升级冒烟、设备矩阵记录、verification evidence 和提测交接。Use when the user says 打 TF 包、TestFlight、上传测试包、release 构建、真机验证、提测、fastlane、EAS build、内测分发，or asks to ship a build to testers.
---

# 打包上传、真机验证与提测

目标：产出干净、可安装、可回滚的 Release 包，上传到 TestFlight/内测渠道，用真机验证后提交测试。任何一步没有证据，都不算完成。

## 输入

- 通过 G5 的代码与构建配置
- `06-store/listing.md`、`release-notes.md`
- 目标平台（由用户提供的单端链接决定；iOS 就只做 TestFlight）
- **阶段 7 才收集**：签名证书、Provisioning Profile、App Store Connect API Key、Android keystore
- 测试账号（若 P0 有登录）、mock 数据/本地环境、功能开关状态
- 上一版可用包（用于升级验证与回滚；首次发布可跳过）

## OpenCode + spec-manager 模式

本阶段默认由 OpenCode 执行，写入 L3.4（Release & TestFlight）。

```bash
spec-manager spec new L3 --topic <topic> --parent <L2> --title "Release & TestFlight" --desc release
spec-manager template L3 --title "Release & TestFlight" --output .spec-manager/drafts/<topic>-L3-release.md
# 前置依赖写 L3.3 implemented + G5 passed
spec-manager spec update <L3.4> --content .spec-manager/drafts/<topic>-L3-release.md   --ai-summary "<summary>" --change-summary "initial release"
spec-manager spec validate <L3.4>
# 人工确认后
spec-manager approve <L3.4>
spec-manager task create <L3.4> --plan tasks/<topic>-L3-release-plan.json --start
```

构建/上传/真机验证用 `spec-manager task step` 记录；完成后用 `spec-manager task verify` 记录 smoke 证据，再 `task complete`。

## 流程

### 第 1 步：发布前检查

**先收集凭证**：开发者账号、签名、App Store Connect / Play Console、TestFlight 权限只在此阶段向用户索取；前面阶段不因缺少凭证阻塞。

写入 `07-release/checklist.md`：

**通用**

- [ ] 目标平台已确认（单端即可；iOS 只做 TestFlight，Android 只做 Play/Firebase）
- [ ] 版本号与 Build 号正确，Build 号单调递增
- [ ] 若使用 mock：确认无 localhost/测试域名泄漏，mock 数据不包含真实用户信息
- [ ] 若 P0 有后端：环境地址指向生产/预发，接口兼容
- [ ] 无调试菜单、测试后门、硬编码测试账号
- [ ] 无密钥、证书、token 进入仓库或包内明文
- [ ] 崩溃上报、性能监控、埋点已启用
- [ ] 功能开关与 kill switch 可用（本地/远程按 P0）
- [ ] 隐私政策、服务条款 URL 可访问

**iOS（仅当目标平台为 iOS）**

- [ ] Bundle ID、Team、签名证书、Provisioning Profile 正确
- [ ] App icon 1024 不透明，AppIcon.appiconset 各尺寸完整
- [ ] 启动屏 / Launch Screen 使用 design/splash 资产，无拉伸/裁切
- [ ] 权限文案与功能一致（相机、相册、定位、通知、通讯录等）
- [ ] `PrivacyInfo.xcprivacy` 与实际使用的 required reason API 一致
- [ ] 若使用追踪，ATT 文案与实现一致
- [ ] 出口合规/加密声明已确认（不确定时问负责人，不猜）
- [ ] 深链 Associated Domains、推送 entitlement 正确
- [ ] 内购商品已在 App Store Connect 配置并处于可测试状态

**Android（仅当目标平台为 Android）**

- [ ] applicationId、versionCode、versionName 正确
- [ ] 签名 keystore 正确，未用 debug 签名
- [ ] targetSdk/minSdk 符合商店要求
- [ ] 权限声明最小化，敏感权限有说明
- [ ] 深链、推送、ProGuard/R8 规则验证
- [ ] 内购/订阅配置与测试轨道一致

### 第 2 步：版本与构建

只构建目标平台，不要求另一平台工程存在。先发现工程结构，不猜：

```bash
# iOS
xcodebuild -list -workspace <Name>.xcworkspace
# Android
./gradlew tasks
```

**React Native / Expo**

```bash
npx eas build --platform ios --profile production
# 或 bare RN
cd ios && pod install
xcodebuild -workspace <Name>.xcworkspace -scheme <Scheme> \
  -configuration Release -archivePath build/<Name>.xcarchive archive
```

**Flutter**

```bash
flutter build ipa --release --export-method app-store
# Android
flutter build appbundle --release
```

**原生 iOS（OC / Swift / OC&Swift / SwiftUI）**

```bash
xcodebuild -workspace <Name>.xcworkspace -scheme <Scheme> \
  -configuration Release -archivePath build/<Name>.xcarchive archive
xcodebuild -exportArchive -archivePath build/<Name>.xcarchive \
  -exportOptionsPlist ExportOptions.plist -exportPath build/ipa
```

原生 iOS 补充：

- 先 `xcodebuild -list` 确认 workspace/scheme；有 `Podfile` 先 `pod install`，有 `Package.swift` 先 `swift package resolve`。
- OC/Swift 混编检查 bridging header、`@objc` 暴露、nullability 与测试 target。
- SwiftUI/UIKit 检查 AppIcon、启动屏、`NavigationStack`/`UINavigationController` 行为；Release 包不含 Preview/调试代码。
- 用 `xcodebuild -showBuildSettings` 核对 `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`。

**Android（RN / Flutter）**

```bash
# RN
cd android && ./gradlew bundleRelease
# 或 EAS
npx eas build --platform android --profile production

# Flutter
flutter build appbundle --release
```

构建日志写入 `build-log.md`：命令、时间、Commit、构建号、产物路径、校验值。

### 第 3 步：上传

**iOS**

- 推荐 `fastlane pilot upload` 或 Transporter。
- 使用 App Store Connect API Key（`.p8` + issuer id + key id）或 Keychain 中的账号，不把凭据写进仓库。
- 上传后等待处理完成，处理失败先看邮件/App Store Connect 的 ITMS 错误。

```bash
fastlane pilot upload --ipa build/ipa/<Name>.ipa
```

**Android**

```bash
# Google Play 内测轨道
fastlane supply --aab app/build/outputs/bundle/release/app-release.aab --track internal

# 或 Firebase App Distribution
firebase appdistribution:distribute app-release.apk \
  --app <FIREBASE_APP_ID> --groups testers
```

上传记录：渠道、轨道、构建号、上传时间、处理状态、测试组。

### 第 4 步：配置 TestFlight / 内测

- 填写测试信息、审核备注、测试账号
- 配置内部/外部测试组与测试员
- 确认出口合规信息
- 外部测试若需要 Beta 审核，预留时间
- 确认构建过期时间（TestFlight 构建通常 90 天）
- 通知测试员安装，提供安装步骤与问题反馈渠道

### 第 5 步：真机验证

至少 2 台真机，覆盖小屏/大屏、一个较旧系统；iPad 若支持则加测。

**安装**

- [ ] 从 TestFlight/内测渠道全新安装成功
- [ ] 从上一版覆盖升级成功，数据不丢、不崩溃
- [ ] 首次启动权限请求文案正确，拒绝后可降级使用

**功能（只测 5 图锁定的 P0）**

- [ ] 首次启动 → 首页 → 详情 → 收藏 → Watchlist
- [ ] 搜索/分类 → 详情
- [ ] 外部观看入口（mock 链接）可打开
- [ ] 离线/弱网：缓存、重试、错误提示
- [ ] 空态、图片失败、重复点击
- [ ] 设置/隐私/清数据
- [ ] 本地化、深色模式、动态字号（若 P0 支持）
- [ ] 切后台/回前台、中断后恢复

仅当 P0 包含时才加测：登录、支付、推送、深链、相册权限。P1/P2 不作为提测阻断项。

**非功能**

- [ ] 冷启动时间在预算内
- [ ] 列表滚动无明显掉帧
- [ ] 无崩溃、无 ANR/卡死
- [ ] 无调试菜单、无测试环境地址、无测试账号泄露
- [ ] 埋点与崩溃上报能在后台看到

记录到 `device-matrix.md`：设备型号、系统版本、屏幕、网络、结果、证据。

### 第 6 步：提测交接

写入 `submission.md`：

```markdown
## 提测单

- 应用/包名:
- 版本/Build:
- 平台/渠道:
- 环境:
- 测试账号:
- 提测范围:
- 回归范围:
- 已知问题:
- 验证证据:
- 回滚方案:
- 负责人/截止:
```

附：G5 测试报告、G6 文案、真机截图/录屏、构建日志。

### 第 7 步：回滚准备

- 保留上一版可用构建与构建号
- 确认本地/远程开关可关闭新功能（若 P0 使用）
- 若 P0 有后端，确认接口向后兼容
- 明确回滚触发条件与负责人
- 不删除旧构建，直到新版本稳定

## 产出

```text
artifacts/07-release/
├── checklist.md
├── build-log.md
├── device-matrix.md
└── submission.md
```

## G7 门禁

- [ ] L3.4 已 `validate` 并经人工 `approve`（frozen）
- [ ] L3.4 Agent Task 已创建并完成
- [ ] 阶段 7 才收集的账号/签名/发布权限已验证可用
- [ ] 只构建并上传目标平台；未构建平台不声称
- [ ] 发布检查表全部通过或有签核豁免
- [ ] Release 包无调试入口、测试密钥、开发环境地址
- [ ] 上传成功且处理完成
- [ ] 至少 2 台真机完成新装 + 升级冒烟
- [ ] 无崩溃、无阻断问题
- [ ] 5 图锁定的 P0 主流程通过
- [ ] 仅验证 P0 需要的权限/集成；P1/P2 不作为门槛
- [ ] 提测单信息完整，测试账号可用（若 P0 有登录）
- [ ] 回滚方案已确认
- [ ] 人工签核后提测

## 常见错误

- 在阶段 0-6 就向用户要开发者账号/签名，提前阻塞
- 只提供 iOS 链接却强行构建 Android
- 把 P1/P2 当提测阻断项
- Build 号重复或回退，导致上传被拒
- 用 debug 签名/证书打包
- 忘记切生产环境地址（若 P0 有后端）
- 权限文案与实际功能不符，审核被拒
- 未验证覆盖升级，老用户数据丢失
- 只在模拟器验证，真机问题漏掉
- 把 App Store Connect API Key、keystore 密码写进脚本或仓库
- 没留上一版构建，出问题无法回滚
- 提测单没有测试账号（若 P0 有登录）和已知问题，QA 无法开始
