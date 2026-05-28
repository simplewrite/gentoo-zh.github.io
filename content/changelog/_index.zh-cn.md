---
title: "更新记录"
date: 2026-05-28
description: "Gentoo 中文社区网站更新记录"
slug: "changelog"
showDate: false
showAuthor: false
showReadingTime: false
showEdit: false
layoutBackgroundHeaderSpace: false
---

本页面记录网站内容的主要更新，便于读者追踪变更。

---

## 2026 年 5 月

### 2026-05-28

**内容精简**
- 移除三篇仍在草稿状态的「Gentoo 安装指南」系列（base / advanced / desktop），未来如要重写会以独立条目重新整理
- 重写「在 Apple Silicon Mac 上安装 Gentoo」一文：去除 AI 风格、移除全部 emoji、统一标题层级，并根据 [Asahi 官方 Feature Support](https://asahilinux.org/docs/platform/feature-support/overview/) 校正硬件支持表（M1/M2 可日常桌面使用；M3 GPU WIP，Wi-Fi/音频仍 TBA；M4 多为 TBA；M5 未启动）
- 重写「Jekyll 迁移至 Hugo」公告，精简到核心信息

**翻译质量**
- 修复 `sync_to_tw.sh` 多处过度替换 bug：移除 `s/包/套件/g`（导致「包含 → 套件含」、「打包 → 打套件」）、`s/文件/檔案/g`（导致文档「文档 → 檔案」）等危险规则；加入事后 cleanup pass 修正 OpenCC phrase-dict 残留
- 全站清理残留 OpenCC 误译：套件含、字地化、使用者名稱稱、打套件、檔案翻譯 等
- 繁体内文「映象 / 映像」统一为「鏡像」，与菜单一致

**自动化稳定性**
- 工作流：用 `git status --porcelain` 取代 `git diff --quiet`，修复**新贡献者目录未提交**的 bug；加入 `concurrency:` 防并发推送、`timeout-minutes: 30`、`git pull --rebase` 3 次重试；移除未用的 `pull-requests: write` 权限
- 脚本：所有 `gh api` / `curl` 加入指数退避重试、`curl --max-time 30`、原子写入（temp + fsync + rename）、unique temp 档名、JSON 解析错误带上下文；Twitter URL 改为 `x.com`

**基础设施**
- Hugo 升级到 `0.161.1`（与 Blowfish v2.103.0 声明的相容范围对齐）
- Blowfish 主题升级到 v2.103.0
- 修正 Hugo 0.158 起的 deprecation：`languageCode` → `locale`、`languageName` → `label`
- 修正所有 `gentoo-zh.github.com` 指向为 `.io`（7 个档案）

**Layouts**
- 修正 contributor 卡片的 X (Twitter) 图标比对，支持新的 `x.com` 域名
- 移除 `extend-head.html` 中引用不存在档的 cloudflare-stats 占位、未使用的 fonts/jsdelivr preconnect
- 删除未引用的 `assets/img/background-{light,dark}.webp`

**贡献者数据**
- 修正 `update-contributors.py` 默认 tag：zh-cn 用「Overlay 贡献者」、zh-tw 用「Overlay 貢獻者」
- 索引页时间戳「每周一自动更新」/「每週一自動更新」按语言分别本地化
- 修正 85 个 zh-cn 贡献者页中残留繁体的 tag 值

---

## 2025 年 12 月

### 2025-12-30

**网站基础设施**
- GitHub Actions 部署工作流调整 Hugo 版本为 `0.153.2`（与当时 Blowfish 主题声明的兼容范围对齐）

### 2025-12-29

**网站语言与术语**
- 语言选择器显示名称从「繁体中文」改为「传统中文」，从「简体中文」改为「简化中文」
- 首页「新闻」标题改为「文章」
- 使用 opencc s2twp 转换传统中文版文章，确保字形正确

**关于页面**
- 更新群组规则，强调中华文化跨越地理边界
- 新增「语言哲学」章节，说明选择「传统中文」命名的理由

**贡献指南**
- 添加 `content/changelog/` 目录说明

**Jekyll 迁移至 Hugo 公告**
- 更新 Hugo 版本信息至 v0.148+
- 补充贡献者自动更新功能说明
- 添加更新记录和贡献指南页面说明

**网站基础设施**
- 修复贡献者自动更新后网站未重新部署的问题（移除提交信息中的 `[skip ci]` 标记）
- 更新 Blowfish 主题至当时最新版本
- 新增本更新记录页面
- 修正 sync_to_tw.sh 转换规则

---

## 更新说明

- 本页面记录网站**内容**的主要更新，不包括纯技术性修改
- 贡献者信息每周一自动更新，不在此处记录
- 如有问题或建议，请联系 [admin@zakk.au](mailto:admin@zakk.au) 或在 [Telegram 群组](https://t.me/gentoo_zh) 讨论
