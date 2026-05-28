---
title: "更新記錄"
date: 2026-05-28
description: "Gentoo 中文社群網站更新記錄"
slug: "changelog"
showDate: false
showAuthor: false
showReadingTime: false
showEdit: false
layoutBackgroundHeaderSpace: false
---

本頁面記錄網站內容的主要更新，便於讀者追蹤變更。

---

## 2026 年 5 月

### 2026-05-28

**內容精簡**
- 移除三篇仍在草稿狀態的「Gentoo 安裝指南」系列（base / advanced / desktop），未來如要重寫會以獨立條目重新整理
- 重寫「在 Apple Silicon Mac 上安裝 Gentoo」一文：去除 AI 風格、移除全部 emoji、統一標題層級，並根據 [Asahi 官方 Feature Support](https://asahilinux.org/docs/platform/feature-support/overview/) 校正硬體支援表（M1/M2 可日常桌面使用；M3 GPU WIP，Wi-Fi/音訊仍 TBA；M4 多為 TBA；M5 未啟動）
- 重寫「Jekyll 遷移至 Hugo」公告，精簡到核心資訊

**翻譯品質**
- 修正 `sync_to_tw.sh` 多處過度替換 bug：移除 `s/包/套件/g`（導致「包含 → 套件含」、「打包 → 打套件」）、`s/文件/檔案/g`（導致文件「文档 → 檔案」）等危險規則；加入事後 cleanup pass 修正 OpenCC phrase-dict 殘留
- 全站清理殘留 OpenCC 誤譯：套件含、字地化、使用者名稱稱、打套件、檔案翻譯 等
- 繁體內文「映象 / 映像」統一為「鏡像」，與選單一致

**自動化穩定性**
- 工作流：用 `git status --porcelain` 取代 `git diff --quiet`，修正**新貢獻者目錄未提交**的 bug；加入 `concurrency:` 防併發推送、`timeout-minutes: 30`、`git pull --rebase` 3 次重試；移除未用的 `pull-requests: write` 權限
- 腳本：所有 `gh api` / `curl` 加入指數退避重試、`curl --max-time 30`、原子寫入（temp + fsync + rename）、unique temp 檔名、JSON 解析錯誤帶上下文；Twitter URL 改為 `x.com`

**基礎設施**
- Hugo 升級到 `0.161.1`（與 Blowfish v2.103.0 宣告的相容範圍對齊）
- Blowfish 主題升級到 v2.103.0
- 修正 Hugo 0.158 起的 deprecation：`languageCode` → `locale`、`languageName` → `label`
- 修正所有 `gentoo-zh.github.com` 指向為 `.io`（7 個檔案）

**Layouts**
- 修正 contributor 卡片的 X (Twitter) 圖示比對，支援新的 `x.com` 網域
- 移除 `extend-head.html` 中引用不存在檔的 cloudflare-stats 佔位、未使用的 fonts/jsdelivr preconnect
- 刪除未引用的 `assets/img/background-{light,dark}.webp`

**貢獻者資料**
- 修正 `update-contributors.py` 預設 tag：zh-cn 用「Overlay 贡献者」、zh-tw 用「Overlay 貢獻者」
- 索引頁時間戳「每周一自动更新」/「每週一自動更新」按語言分別本地化
- 修正 85 個 zh-cn 貢獻者頁中殘留繁體的 tag 值

---

## 2025 年 12 月

### 2025-12-30

**網站基礎設施**
- GitHub Actions 部署工作流調整 Hugo 版本為 `0.153.2`（與當時 Blowfish 主題宣告的相容範圍對齊）

### 2025-12-29

**網站語言與術語**
- 語言選擇器顯示名稱從「繁體中文」改為「傳統中文」，從「簡體中文」改為「簡化中文」
- 首頁「新聞」標題改為「文章」
- 使用 opencc s2twp 轉換傳統中文版文章，確保字形正確

**關於頁面**
- 更新群組規則，強調中華文化跨越地理邊界
- 新增「語言哲學」章節，說明選擇「傳統中文」命名的理由

**貢獻指南**
- 新增 `content/changelog/` 目錄說明

**Jekyll 遷移至 Hugo 公告**
- 更新 Hugo 版本資訊至 v0.148+
- 補充貢獻者自動更新功能說明
- 新增更新記錄和貢獻指南頁面說明

**網站基礎設施**
- 修正貢獻者自動更新後網站未重新部署的問題（移除提交資訊中的 `[skip ci]` 標記）
- 更新 Blowfish 主題至當時最新版本
- 新增本更新記錄頁面
- 修正 sync_to_tw.sh 轉換規則

---

## 更新說明

- 本頁面記錄網站**內容**的主要更新，不包括純技術性修改
- 貢獻者資訊每週一自動更新，不在此處記錄
- 如有問題或建議，請聯絡 [admin@zakk.au](mailto:admin@zakk.au) 或在 [Telegram 群組](https://t.me/gentoo_zh) 討論
