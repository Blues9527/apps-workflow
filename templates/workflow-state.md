# Workflow State

> 版本: v0.2
> 更新: YYYY-MM-DD
> 维护: mobile-workflow

```yaml
current_stage: 0
status: in_progress   # pending | in_progress | awaiting_codex | awaiting_opencode | awaiting_human | blocked | done
platform: auto
spec_manager:
  project: <project>
  topic: <topic>
  l1: null
  l2: null
  l3_impl: null
  l3_e2e: null
  l3_store: null
  l3_release: null
  l3_archive: null
  active_task: null
agent_routing:
  stage_2_3: codex           # codex | opencode (fallback)
  stage_4_5: opencode
  codex_available: true
  codex_fallback: false
p0_lock: pending      # pending | locked（G3 锁定）
schedule:
  deadline: auto
  critical_path_days: 0
  parallel_agents: auto
  buffer_days: 1
gates:
  G0: pending
  G1: pending
  G2: pending
  G3: pending
  G4: pending
  G5: pending
  G6: pending
  G7: pending
  G8: pending
artifacts: []
open_questions: []
decisions: []
handoff:
  next_agent: opencode
  packet: artifacts/01-feature-spec/codex-handoff.md
next_action: 完成项目建档、spec-manager 初始化与排期
```

## Gate Log

| 门禁 | 结果 | 日期 | 证据 | 签核 |
| --- | --- | --- | --- | --- |
| G0 | pending | - | - | - |

## Spec-manager Snapshot

| Spec | Code | Status | Owner |
| --- | --- | --- | --- |
| L1 PRD | - | - | Codex |
| L2 Design | - | - | Codex |
| L3.1 Impl | - | - | OpenCode |
| L3.2 E2E | - | - | OpenCode |
| L3.3 Store | - | - | OpenCode |
| L3.4 Release | - | - | OpenCode |
| L3.5 Archive | - | - | OpenCode |

## Open Questions

| ID | 问题 | 影响阶段 | 负责人 | 状态 |
| --- | --- | --- | --- | --- |
| Q-001 | - | - | - | open |

## Decisions

| ID | 决策 | 理由 | 日期 |
| --- | --- | --- | --- |
| D-001 | - | - | - |

## Handoff

```text
阶段:
spec:
- topic:
- L1:
- L2:
- active_task:
已完成:
门禁:
风险:
下一步:
```
