# 已有项目迁移到 Codex + spec-manager

> 适用: 已经用 artifacts 跑过阶段 1-3，想切换到 Codex/OpenCode + spec-manager  
> 注意: 如果已有完整 PRD，优先使用 `/mobile-flow --prd <path>`；本文档用于没有现成 PRD、需要从 artifacts 回填的情况。

## 1. 初始化

```bash
cd <code-repo>
spec-manager project init --name <project>
spec-manager project agents --provider all
spec-manager project doctor
```

## 2. 建 topic

```bash
# 例：pinedrama-p0
spec-manager brief "迁移现有 PRD/5图 到 spec-manager" --topic <topic>
```

## 3. 回填 L1（现有 PRD）

```bash
spec-manager spec new L1 --topic <topic> --title "<产品名> PRD"
spec-manager template L1 --title "<产品名> PRD" --output .spec-manager/drafts/<topic>-L1.md
# 把 artifacts/02-prd 的 theme/competitors/prd 合并进 L1
spec-manager spec update <L1> --content .spec-manager/drafts/<topic>-L1.md \
  --ai-summary "migrated from artifacts/02-prd" --change-summary "backfill L1"
spec-manager spec validate <L1>
# 人确认后
spec-manager approve <L1>
```

## 4. 回填 L2（现有 5 图）

```bash
spec-manager spec new L2 --topic <topic> --parent <L1> --title "Design System + 5 Screens"
spec-manager template L2 --title "Design System + 5 Screens" --output .spec-manager/drafts/<topic>-L2.md
# 把 artifacts/03-design 的设计系统/5图/screen-map/asset-manifest 合并进 L2
# 把 design tokens 写入 specs/DESIGN.md
spec-manager spec update <L2> --content .spec-manager/drafts/<topic>-L2.md \
  --ai-summary "migrated from design artifacts" --change-summary "backfill L2"
spec-manager spec validate <L2>
# 人确认后
spec-manager approve <L2>
```

## 5. 回填 L3.1（现有实现）

```bash
spec-manager spec new L3 --topic <topic> --parent <L2> --title "P0 Implementation" --desc impl
spec-manager template L3 --title "P0 Implementation" --output .spec-manager/drafts/<topic>-L3-impl.md
# 用现有代码与 04-build/architecture.md 填文件级步骤、验证命令、回滚方案
spec-manager spec update <L3.1> --content .spec-manager/drafts/<topic>-L3-impl.md \
  --ai-summary "backfill current implementation" --change-summary "backfill L3.1"
spec-manager spec validate <L3.1>
# 人确认后
spec-manager approve <L3.1>
spec-manager task create <L3.1> --plan tasks/<topic>-L3-impl-plan.json --start
# 对现有功能补 task step / verification evidence
spec-manager task complete <taskId>
```

## 6. 继续

- 阶段 5：创建 L3.2 E2E。
- 阶段 6：创建 L3.3 Store Copy。
- 阶段 7：创建 L3.4 Release & TestFlight。
- 阶段 8：创建 L3.5 Archive & Handoff，归档 specs/design/store/release。

## 7. 原则

- 已有 artifacts 只作为回填来源，不重写历史结论。
- 回填内容必须与现有代码/设计一致；不一致时先记录 decision，再补实现。
- L1/L2/L3 的确认仍由人完成。
