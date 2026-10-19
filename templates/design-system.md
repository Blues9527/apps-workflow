# Design System

> 版本: v0.1
> 日期: YYYY-MM-DD
> 状态: draft
> 来源: artifacts/02-prd/theme.md
> spec-manager: <topic>-L2（源）；同步写入 specs/DESIGN.md

## 1. 视觉方向

- 主题: T-xx
- 关键词:
- 参考（只取思路）:
- 禁止项:

## 2. 颜色

### Light

| Token | 值 | 用途 | 对比度 |
| --- | --- | --- | --- |
| background | #FFFFFF | 页面底色 | - |
| surface | #F7F8FA | 卡片 | - |
| primary | #0F766E | 主 CTA | 4.5:1 |
| on-primary | #FFFFFF | 主 CTA 文字 | 4.5:1 |
| text-primary | #111827 | 正文 | 4.5:1 |
| text-secondary | #6B7280 | 辅助 | 4.5:1 |
| border | #E5E7EB | 分割/描边 | - |
| danger | #DC2626 | 错误 | 4.5:1 |

### Dark

| Token | 值 | 用途 | 对比度 |
| --- | --- | --- | --- |
| background | #0B0F14 | 页面底色 | - |
| surface | #151B23 | 卡片 | - |
| primary | #2DD4BF | 主 CTA | 4.5:1 |
| on-primary | #042F2E | 主 CTA 文字 | 4.5:1 |
| text-primary | #F9FAFB | 正文 | 4.5:1 |
| text-secondary | #9CA3AF | 辅助 | 4.5:1 |

## 3. 字体

| 层级 | 字号 | 行高 | 字重 | 用途 |
| --- | --- | --- | --- | --- |
| Display | 36 | 1.1 | 700 | 启动/空态 |
| H1 | 28 | 1.2 | 700 | 页面标题 |
| H2 | 20 | 1.3 | 600 | 分区标题 |
| Body | 16 | 1.5 | 400 | 正文 |
| Label | 14 | 1.4 | 500 | 按钮/标签 |
| Caption | 12 | 1.4 | 400 | 辅助 |

## 4. 间距与形状

- 间距: 4, 8, 12, 16, 24, 32, 48
- 页面边距: 16（小屏）/ 20（大屏）
- 圆角: 8 / 12 / 20 / full
- 描边: 1px
- 阴影: 0 1px 2px rgba(0,0,0,.06) / 0 8px 24px rgba(0,0,0,.12)
- 图标: 24，触控区 44pt / 48dp

## 5. 动效

| 场景 | 时长 | Easing |
| --- | --- | --- |
| 页面切换 | 250ms | ease-out |
| 按钮反馈 | 150ms | ease-out |
| 列表加载 | 200ms | ease-in-out |

支持「减少动态效果」。

## 6. 组件

- Button: primary / secondary / ghost / danger；loading/disabled
- Input: label、帮助、错误、字数
- Card: 内容/操作/空态
- List: 加载/空/错误/分页
- Dialog/Toast: 文案规范、最大宽度
- Navigation: Tab、返回、深层级

## 7. 可访问性

- [ ] 正文对比度 ≥ 4.5:1，大字/UI ≥ 3:1
- [ ] 触控目标 ≥ 44pt / 48dp
- [ ] 颜色不是唯一状态指示
- [ ] 动态字号下不截断关键操作
- [ ] 语义标签完整
- [ ] 安全区适配
