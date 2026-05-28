---
title: "貢獻指南"
description: "如何為 Gentoo 中文社群網站做出貢獻"
---

歡迎來一起建設 Gentoo 中文社群網站！這篇指南會帶你瞭解網站的專案結構，以及想參與貢獻該從哪裡入手。

## 專案概況

本網站使用 [Hugo](https://gohugo.io/) 靜態網站生成器和 [Hextra](https://imfing.github.io/hextra/) 主題構建，託管在 GitHub Pages 上。主題透過 [Hugo Modules](https://gohugo.io/hugo-modules/) 引入（見 `go.mod`），不再使用 git submodule。

**專案倉庫**：<https://github.com/Gentoo-zh/gentoo-zh.github.io>

## 專案結構

### 內容組織

內容按語言分目錄存放，簡體中文在 `content/zh-cn/`，傳統中文在 `content/zh-tw/`，兩者目錄結構完全一致：

- `download/` — 下載頁面（鏡像源和安裝介質）
- `overlay/` — gentoo-zh Overlay 說明
- `mirrorlist/` — 鏡像列表（Portage 樹和 Distfiles 配置）
- `about/` — 關於頁面（專案歷史、社群頻道、網站語言說明）
- `contributors/` — 貢獻者頁面（**自動更新，無需手動編輯**）
- `contributing/` — 貢獻指南（本頁面）
- `changelog/` — 更新記錄
- `posts/` — 新聞文章和教學

> 同一篇內容的簡體版放在 `content/zh-cn/...`、傳統版放在對應的 `content/zh-tw/...`，檔名都是 `index.md` / `_index.md`（**不再**使用 `index.zh-cn.md` 這種語言字尾）。

### 配置檔案

主要配置位於 `config/_default/` 目錄：

- `hugo.toml` — Hugo 主配置（站點資訊、分類法、Markdown 渲染、輸出格式等）
- `languages.toml` — 語言配置（簡繁雙語，單檔案內分 `[zh-cn]` / `[zh-tw]`）
- `menus.zh-cn.toml` / `menus.zh-tw.toml` — 各語言導航選單
- `params.toml` — 主題引數（外觀、功能開關）

### 多語言支援

- 介面翻譯：`i18n/zh-cn.yaml`（簡體）、`i18n/zh-tw.yaml`（傳統）
- 預設語言為簡體中文，位於站點根路徑 `/`；傳統中文位於 `/zh-tw/`
- 簡繁轉換由倉庫內的 `sync_to_tw.sh` 指令碼完成（見下文）

### 主題與資源

- 主題 Hextra 透過 Hugo Modules 引入，版本固定在 `go.mod`，不在倉庫內儲存主題原始碼
- `layouts/` — 站點自定義模板（覆蓋主題預設，如首頁 `shortcodes/home-bento.html`、貢獻者頁等）
- `assets/css/custom.css` — 在 Hextra 樣式之上的站點樣式覆蓋
- `static/` — 靜態資源（`CNAME`、圖片等）

## 環境準備

需要 **Hugo extended** 版本；因為主題透過 Hugo Modules 引入，還需要 **Go** 工具鏈。

```bash
# Gentoo
emerge --ask www-apps/hugo dev-lang/go

# macOS
brew install hugo go
```

Fork 並 clone 倉庫（**無需** `git submodule`，模組會在構建時自動拉取）：

```bash
git clone https://github.com/你的使用者名稱/gentoo-zh.github.io.git
cd gentoo-zh.github.io
```

本地預覽：

```bash
hugo server -D
# 訪問 http://localhost:1313 預覽
```

## 如何貢獻

### 1. 提交新文章

在 `content/zh-cn/posts/` 下按 `YYYY-MM-DD-article-name` 建立目錄，寫簡體版 `index.md`：

```bash
mkdir -p content/zh-cn/posts/2026-05-29-my-article
$EDITOR content/zh-cn/posts/2026-05-29-my-article/index.md
```

front matter 範例：

```yaml
---
title: "文章標題"
date: 2026-05-29
tags: ["tutorial"]
---

文章正文……（作者署名見下方第 3 節）
```

可選的標籤（`tags`，顯示在文章列表與文章頁的 `#標籤`、連結到 `/tags/` 聚合頁，首頁文章卡片也會顯示首個標籤）：`tutorial`（教學）、`news`（新聞）、`announcement`（公告）、`website`（站務）。

寫完簡體版後，用指令碼生成傳統中文版（見下一節），傳統版放在對應的 `content/zh-tw/posts/.../index.md`。

### 2. 簡繁轉換

`sync_to_tw.sh` 封裝了 OpenCC（`s2twp`）+ 針對本站術語的修正與已知誤轉清理，**接收「原始檔 → 目標檔案」兩個路徑引數**：

```bash
# 先安裝 OpenCC
emerge --ask app-i18n/opencc   # Gentoo
brew install opencc            # macOS
sudo apt install opencc        # Debian/Ubuntu

# 簡體 → 傳統
./sync_to_tw.sh \
  content/zh-cn/posts/2026-05-29-my-article/index.md \
  content/zh-tw/posts/2026-05-29-my-article/index.md
```

轉換後建議人工檢查臺灣用語差異。

### 3. 文章署名與頭像

在文章 front matter 的 `authors` 用「對映」形式寫明作者，Hextra 會在署名處顯示頭像 + 姓名 + 連結：

```yaml
authors:
  - name: 你的名字
    image: /contributors/<你的標識>/feature.webp
    link: https://github.com/yourname
```

`image` 可指向貢獻者頁裡的頭像；省略 `image` 則只顯示姓名。

### 4. 改進現有內容 / 技術改進

錯別字、過時資訊、使用技巧、缺失的傳統中文翻譯，看到了都歡迎隨手修正。模板、樣式、效能、功能等技術層面，也歡迎提改進。

> **貢獻者列表（`content/*/contributors/`）由指令碼自動維護**，抓取 [gentoo-zh Overlay](https://github.com/microcai/gentoo-zh) 中提交 5 次以上者，顯示提交次數並按提交量排序，每月自動更新（`scripts/update-contributors.py` + GitHub Actions）。**請勿手動編輯該目錄**；首頁貢獻者展示也隨之自動更新。

## 提交 Pull Request

```bash
git checkout -b your-feature-branch
git add .
git commit -m "描述你的更改"
git push origin your-feature-branch
# 然後在 GitHub 上建立 Pull Request
```

## 寫作規範

### Markdown 格式

- 使用標準 Markdown 語法
- 程式碼塊標註語言（如 ` ```bash `）
- 圖片放在文章目錄內並使用相對路徑
- 連結使用 Markdown 格式

### 中文排版

- 中英文之間留一個空格
- 使用全形中文標點
- 數字、英文用半形
- 專有名詞保持原文（如 Gentoo、Hugo、Hextra、Portage）

## 常見問題

### 如何更新主題？

主題是 Hugo Module，用 `hugo mod` 升級，不再操作 submodule：

```bash
hugo mod get -u github.com/imfing/hextra
hugo mod tidy
git add go.mod go.sum
git commit -m "更新 Hextra 主題"
```

### 如何新增新的欄目頁面？

在 `content/zh-cn/<欄目>/` 下建 `_index.md`，用指令碼生成 `content/zh-tw/<欄目>/_index.md`；若要進入頂部導航，再到 `config/_default/menus.zh-cn.toml` 和 `menus.zh-tw.toml` 各加一條 `[[main]]`。

### 簡繁內容不一致怎麼辦？

以簡體版為源，重新執行 `sync_to_tw.sh`（用法見上）覆蓋生成傳統版，再人工校對。請勿手動維護兩份正文導致內容漂移。

## 社群交流

遇到問題或有建議？

- **Telegram 頻道**：[@gentoocn](https://t.me/gentoocn)
- **Telegram 群組**：[@gentoo_zh](https://t.me/gentoo_zh)
- **GitHub Issues**：<https://github.com/Gentoo-zh/gentoo-zh.github.io/issues>

更多頻道（IRC / Matrix / 閒聊群等）見[關於頁面](/about/)。

## 許可協議

本站內容採用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 許可協議，除非另有說明。程式碼貢獻遵循專案的 MIT 許可。

---

改一個錯字、補一句翻譯、提個 PR，都算數。Gentoo 中文社群就是這麼一點點攢起來的。
