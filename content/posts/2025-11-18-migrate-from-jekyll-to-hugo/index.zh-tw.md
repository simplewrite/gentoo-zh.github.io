---
title: "網站從 Jekyll 遷移至 Hugo"
date: 2025-11-18
categories: ["announcement"]
authors: ["zakkaus"]
---

經創始人 [@biergaizi](https://github.com/biergaizi) 授權，[@Zakkaus](https://github.com/zakkaus) 於 2025 年接手本站日常維護，並將站點從 Jekyll 遷移到 Hugo。

## 為什麼換 Hugo

Jekyll 依賴 Ruby 環境，構建較慢，主題生態也不如以往活躍。Hugo 是單一 Go 二進位制檔案，構建速度快、部署簡單，原生支援多語言。主題選用 [Blowfish](https://blowfish.page/)。

## 遷移內容

- `_posts` 目錄改用 Hugo 的 Page Bundles 組織（`content/posts/<slug>/index.zh-tw.md`）
- Front matter 從 YAML 改為 TOML
- 簡繁雙語並存（zh-CN / zh-TW）
- 作者資料集中到 `data/authors/`
- 部署改走 GitHub Actions，每週自動更新貢獻者列表

## 回饋

- Telegram 群：[@gentoo_zh](https://t.me/gentoo_zh)
- Telegram 頻道：[@gentoocn](https://t.me/gentoocn)
- 提交 Issue / PR：[GitHub](https://github.com/gentoo-zh/gentoo-zh.github.io)

感謝 [@biergaizi](https://github.com/biergaizi) 與 [@zhcj](https://github.com/zhcj) 創立並長期維護 Gentoo 中文社群，也感謝 Blowfish 主題的開發者。
