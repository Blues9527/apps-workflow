# Release Archive Manifest

> 版本: v0.1
> 日期: YYYY-MM-DD
> 产品: <app-name>
> 版本/Build:
> Commit:
> spec topic:
> 状态: draft

## 1. Spec / Task

| 层级 | Code | 状态 | Task |
| --- | --- | --- | --- |
| L1 PRD |  |  | - |
| L2 Design |  |  | - |
| L3.1 Impl |  |  |  |
| L3.2 E2E |  |  |  |
| L3.3 Store |  |  |  |
| L3.4 Release |  |  |  |
| L3.5 Archive |  |  |  |

## 2. 归档文件

| 路径 | 类型 | SHA256 |
| --- | --- | --- |
| `specs/` | specs snapshot |  |
| `design/screens/` | design |  |
| `design/app-icon/` | icon |  |
| `design/splash/` | splash |  |
| `06-store/` | store |  |
| `07-release/` | release |  |
| `README.md` | summary |  |

## 3. 构建与上传

| 项目 | 内容 |
| --- | --- |
| Build 命令 |  |
| 产物路径 |  |
| 上传渠道 |  |
| 上传时间 |  |
| 构建日志 |  |
| 设备矩阵 |  |
| 提测单 |  |

## 4. 排除项

- `.env` / `.p8` / 证书 / keystore / 密码 / Token
- `node_modules/` / `.dart_tool/` / 构建缓存 / DerivedData
- IPA/APK 二进制（只记录路径与 SHA256）

## 5. 验证

- [ ] `shasum -a 256 -c checksums.txt` 通过
- [ ] 无密钥/证书/密码
- [ ] spec-manager flow status 显示 L1-L3.5 implemented
- [ ] release-summary.md 已生成

## 6. 交接

- 维护入口:
- 设计上下文: `specs/DESIGN.md`
- 回滚方案:
- 已知问题:
