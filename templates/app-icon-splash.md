# App Icon & Splash Screen

> 版本: v0.1
> 日期: YYYY-MM-DD
> 输出: `design/app-icon/`、`design/splash/`
> 状态: draft

## 1. App Icon

| 资产 | 尺寸 | 格式 | 要求 |
| --- | --- | --- | --- |
| AppIcon-1024 | 1024x1024 | PNG | 不透明、无圆角、无透明通道；品牌 mark 居中；安全边距 ≥ 8% |
| iOS 20pt @2x/@3x | 40/60 | PNG | 无透明 |
| iOS 29pt @2x/@3x | 58/87 | PNG | 无透明 |
| iOS 40pt @2x/@3x | 80/120 | PNG | 无透明 |
| iOS 60pt @2x/@3x | 120/180 | PNG | 无透明 |
| iOS 76pt @1x/@2x | 76/152 | PNG | iPad 如支持 |
| iOS 83.5pt @2x | 167 | PNG | iPad Pro 如支持 |
| Android adaptive foreground | 108x108dp 安全区 | PNG/SVG | 前景留 66dp 安全区 |
| Android adaptive background | 108x108dp | PNG/颜色 | 纯色/渐变 |
| Android legacy mipmap | 48/72/96/144/192 | PNG | 各密度 |

规则：

- 不使用竞品 logo/角色/品牌色组合。
- 小尺寸不放复杂文字；品牌 mark 要可识别。
- 图标背景与 design tokens 一致。

## 2. Splash Screen

| 资产 | 尺寸 | 格式 | 要求 |
| --- | --- | --- | --- |
| iOS splash | 1290x2796 | PNG | 竖屏；品牌 mark + 产品名；背景与 tokens 一致 |
| iOS splash dark | 1290x2796 | PNG | 可选；深色模式 |
| Android splash | 1080x1920 | PNG | 竖屏 |
| Android 12 splash icon | 288x288dp | PNG | 系统 splash 图标 |
| Android 12 background | - | color | 与 tokens 一致 |

规则：

- MVP 用静态图，不做复杂动画。
- 不使用竞品截图/角色/品牌资产。
- 文案不承诺未上线功能。

## 3. 接入

### iOS

- 更新 `Assets.xcassets/AppIcon.appiconset`。
- 更新 LaunchScreen storyboard / 启动图。
- 真机/模拟器检查圆角裁切、深色模式、不同屏幕尺寸。

### Android

- 更新 `mipmap-*`、`mipmap-anydpi-v26` adaptive icon。
- 更新 splash theme（Android 12+ 使用 SplashScreen API）。
- 检查不同密度与深色模式。

## 4. 验收

- [ ] 1024 icon 无透明通道
- [ ] iOS/Android 各尺寸导出完整
- [ ] splash 在目标端显示正确，无拉伸/裁切
- [ ] 无竞品资产
- [ ] 已写入 `asset-manifest.md`
