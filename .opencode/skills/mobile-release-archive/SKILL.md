---
name: mobile-release-archive
description: 在 TestFlight/内测提测完成后归档本次交付：创建 spec-manager L3.5 Archive & Handoff，打包 specs/design/store/release 证据，生成 manifest、checksums 与 release summary，排除密钥与构建缓存。Use when the user says 归档、archive、交付归档、release archive、收尾、交接包，or asks to close out a release.
---

# Release Archive 归档与交接

目标：把一次交付变成可复现、可审计、可交接的 release archive；归档完成后工作流才真正结束。

## 输入

- G7 通过：Release 包/上传记录、真机验证、提测单
- L1-L3.4 specs、decisions、tasks
- `design/`（5 图、app-icon、splash、screen-map、asset-manifest、prompts）
- `artifacts/01-feature-spec` ~ `07-release`
- 版本号、Build 号、Commit、构建时间

## 流程

### 第 1 步：创建 L3.5

```bash
spec-manager flow status --topic <topic>
spec-manager spec new L3 --topic <topic> --parent <L2> --title "Archive & Handoff" --desc archive
spec-manager template L3 --title "Archive & Handoff" --output .spec-manager/drafts/<topic>-L3-archive.md
# 前置依赖写 L3.4 implemented + G7 passed
spec-manager spec update <L3.5> --content .spec-manager/drafts/<topic>-L3-archive.md \
  --ai-summary "<summary>" --change-summary "initial archive"
spec-manager spec validate <L3.5>
# 人工确认后
spec-manager approve <L3.5>
spec-manager task create <L3.5> --plan tasks/<topic>-L3-archive-plan.json --start
```

### 第 2 步：确定归档范围

归档到 `artifacts/08-archive/`：

```text
artifacts/08-archive/
├── archive-manifest.md
├── release-summary.md
├── checksums.txt
├── snapshots/
│   ├── specs/          # L1-L3.5、decisions、tasks
│   ├── design/         # screens/app-icon/splash/元数据
│   ├── store/          # listing/release notes/screenshots/pages
│   └── release/        # build log/device matrix/submission
└── <version>-archive.zip   # 可选
```

包含：

- `specs/` 快照与 `.spec-manager/config.yaml`（去掉密钥）
- `design/` 的 5 图、app-icon、splash 与设计说明
- `06-store/` 文案、截图、法律页面
- `07-release/` 构建日志、设备矩阵、提测单
- 版本/Build/Commit/构建时间/checksums

排除：

- `.env`、`.p8`、证书、keystore、密码、Token
- `node_modules/`、`.dart_tool/`、构建缓存、DerivedData
- IPA/APK 二进制（记录路径与 SHA256，不复制大文件）

### 第 3 步：生成 manifest 与 checksums

`archive-manifest.md` 至少包含：

- 产品名/版本/Build/Commit
- spec topic、L1-L3.5 code
- Task IDs 与状态
- 归档文件列表与 SHA256
- 构建/上传记录路径
- 已知问题/回滚方案链接

```bash
find artifacts/08-archive -type f -not -name checksums.txt -print0 \
  | xargs -0 shasum -a 256 > artifacts/08-archive/checksums.txt
shasum -a 256 -c artifacts/08-archive/checksums.txt
```

### 第 4 步：release summary

`release-summary.md` 写：

- 本次交付的 P0 功能
- 测试/真机结果
- 已知问题与非阻断项
- 回滚方案
- 后续 P1/P2 建议
- 交接入口：spec codes、design tokens、build log

### 第 5 步：安全与完整性检查

- [ ] 归档中无密钥/证书/密码/Token
- [ ] checksums 可复算通过
- [ ] manifest 与实际 spec/task/build 一致
- [ ] `spec-manager flow status` 显示 L1-L3.5 已 implemented
- [ ] 大文件只记录路径/哈希，不复制

### 第 6 步：完成 Task

```bash
spec-manager task verify <taskId> --command "shasum -a 256 -c artifacts/08-archive/checksums.txt" \
  --exit-code 0 --summary "archive verified; no secrets" \
  --artifacts "artifacts/08-archive/" --layer smoke
spec-manager task complete <taskId>
```

## G8 门禁

- [ ] L3.5 已 `validate` 并经人工 `approve`（frozen）
- [ ] L3.5 Agent Task 已创建并完成
- [ ] `archive-manifest.md` 含版本/Build/Commit/spec codes/task IDs
- [ ] `checksums.txt` 可复算
- [ ] 归档中无密钥、证书、密码、Token
- [ ] `release-summary.md` 含功能、已知问题、回滚方案
- [ ] `spec-manager flow status` 显示 L1-L3.5 implemented
- [ ] 人工确认归档位置与可交付性

## 常见错误

- 把 `.env`/证书/keystore 打进归档
- 只复制文档，不记录 spec/task/build 对应关系
- 归档后 checksum 变了却没更新
- 归档 IPA/APK 大文件导致仓库膨胀
- 没有 release summary，后续接手只能翻聊天记录
- G8 未通过就宣布交付完成
