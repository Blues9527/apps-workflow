# spec-manager 初始化与协作

> 用途: Codex/OpenCode 共享 specs、tasks、decisions 与证据

## 1. 初始化

```bash
cd <project>
spec-manager project init --name <project>
spec-manager project agents --provider all
# 或
spec-manager codex install
spec-manager opencode install
spec-manager project doctor
```

## 2. 选 topic

小写 slug，例如 `pinedrama-p0`。后续 L1/L2/L3 都使用同一 topic。

```bash
spec-manager next "<request>" --topic <topic>
spec-manager brief "<request>" --topic <topic>
spec-manager flow status --topic <topic>
```

## 2.1 PRD 起点

已有 PRD 时优先：

```text
/mobile-flow --prd <path|url> --topic <topic>
```

阶段 1 可跳过，阶段 2 进入 L1 intake；原始 PRD 复制到 `artifacts/02-prd/source-prd.md` 并记录 SHA256。

## 3. 规格链

```text
L1 PRD（Codex）
  └── L2 Design + 5图（Codex）
        ├── L3.1 Implementation（OpenCode）
        ├── L3.2 Automated E2E（OpenCode）
        ├── L3.3 Store Copy（OpenCode / Codex 文案）
        ├── L3.4 Release & TestFlight（OpenCode）
        └── L3.5 Archive & Handoff（OpenCode）
```

## 4. 审批

```bash
spec-manager approve <L1>     # 人确认后；draft -> confirmed
spec-manager approve <L2>     # 人确认后；draft -> confirmed
spec-manager approve <L3.x>   # 人确认后；draft -> frozen
```

禁止 `task create --auto-confirm` 代替 L1/L2/L3 人工门禁。

## 5. Task

```bash
spec-manager task create <L3> --plan tasks/<topic>-L3-plan.json --start
spec-manager task step <taskId> --no 1 --status succeeded \
  --type tool_action --name "<verb + object + file>" \
  --output-json '{"summary":"<result>"}'
spec-manager task verify <taskId> --command "<cmd>" --exit-code 0 \
  --summary "<result>" --covers-ac "<AC>" --layer functional
spec-manager task complete <taskId>
```

## 6. 变更与审计

```bash
spec-manager change propose --task <taskId> --title "<change>"
spec-manager change list
spec-manager decision create <L1> --what "<decision>" --why "<reason>"
spec-manager assist acceptance <taskId>
spec-manager audit
```

## 7. 多仓库

在代码仓库 `.spec-manager/config.yaml` 配置共享 specs：

```yaml
specStore:
  id: product-planning
  path: ../product-specs
  mode: write
contextSources:
  - id: platform-specs
    path: ../platform-specs
    mode: read
```

写入前检查 `spec-manager project context --json` 与 `spec-manager project store show`。
