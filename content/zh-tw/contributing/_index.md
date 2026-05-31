---
title: "貢獻指南"
description: "如何為 gentoo-zh Overlay 與 Gentoo 中文社群網站做出貢獻"
---

歡迎參與 Gentoo 中文社群！貢獻分兩條線，入口和登上[貢獻者牆](/contributors/)的方式都不一樣，先看你想做哪種：

- **為 gentoo-zh Overlay 貢獻**（軟體套件 / ebuild）——社群主線，也是[貢獻者牆](/contributors/)的來源（指令碼每月抓取 [microcai/gentoo-zh](https://github.com/microcai/gentoo-zh) 提交 5 次以上者）。詳見下方「為 gentoo-zh Overlay 貢獻」。
- **為社群網站貢獻**（文章 / 翻譯 / 修正）——在 [gentoo-zh.github.io](https://github.com/Gentoo-zh/gentoo-zh.github.io) 倉庫，詳見本頁後半「為社群網站貢獻」。

## 為 gentoo-zh Overlay 貢獻

gentoo-zh 是一個 `masters = gentoo` 的 Gentoo overlay（疊加在官方 Portage 樹之上），收錄 450 多個包，原始碼在 [microcai/gentoo-zh](https://github.com/microcai/gentoo-zh)。新增或更新 ebuild、修 bug、跟進新版本，都透過 GitHub Pull Request 提交；發現問題也歡迎提 [issue](https://github.com/microcai/gentoo-zh/issues)。

{{< callout type="info" >}}
首頁[貢獻者牆](/contributors/)統計的就是這種貢獻——指令碼每月抓取本倉庫提交 5 次以上者。
{{< /callout >}}

### 準備

```bash
# 提交/QA 工具：pkgdev 生成提交資訊與 Manifest，pkgcheck 做檢查
# （二者已取代舊的 repoman，是現行官方工具）
emerge --ask dev-util/pkgdev   # 連帶裝上 pkgcheck
```

到 [GitHub](https://github.com/microcai/gentoo-zh) fork 倉庫、clone 你的 fork、新建分支；本地啟用 overlay 方便測試（見上文「新增 gentoo-zh」或 [Overlay 頁](/overlay/)）。

### 提交一個 ebuild 的標準流程

本倉庫遵循官方 Gentoo ebuild 倉庫規範，寫法權威參考是 [Devmanual](https://devmanual.gentoo.org/)：

1. **放對位置**：`<category>/<package>/<package>-<version>.ebuild`，目錄與命名按官方分類。
2. **寫 ebuild**：用本倉庫主流的 `EAPI=8` 與標準兩行版權頭（`# Copyright <年> Gentoo Authors` + GPL-2 宣告）；填好 `DESCRIPTION`、`HOMEPAGE`、`SRC_URI`、`LICENSE`、`SLOT`、依賴（`DEPEND`/`RDEPEND`/`BDEPEND`）、`IUSE` 等。
3. **KEYWORDS 只用測試關鍵字**（`~amd64`、`~arm64` 等）——**本倉庫不收 stable 關鍵字**。
4. **寫 `metadata.xml`**：每個包都要有，宣告維護者與各 USE 的用途說明（官方規範要求，`pkgcheck` 會查）。
5. **生成 Manifest**：`pkgdev manifest`。本倉庫用 thin manifest（`thin-manifests = true`），只記 distfiles 校驗，ebuild 完整性交給 git。
6. **本地測試構建**：`emerge` 或 `ebuild <檔案> install`，並在它 `KEYWORDS` 宣告的**每個架構上都實測**——沒測過就別宣告支援。
7. **QA 自查**：`pkgcheck scan --commits --net`（PR 模板要求你勾選確認已在本地跑過；CI 也會另跑 `pkgcheck`）。
8. **提交**：用 `pkgdev commit` 生成規範提交資訊（格式見下）；一個 PR 含單個貢獻的全部提交，ebuild 連它的 `Manifest` 一起提，別拆成兩個 PR。
9. **開 PR**：CI 會自動 `emerge` 該包並跑 `pkgcheck`，按 PR 模板逐項勾選後才會合併。

{{< callout type="warning" >}}
**唯一規則：別弄壞別人的系統（DO NOT BREAK PEOPLE'S SYSTEM）。**
{{< /callout >}}

### 提交資訊規範

推薦用 `pkgdev commit` 自動生成符合規範的提交資訊。

{{% details title="提交資訊格式範例" %}}

普通（非版本更新）改動：

```text
$category/$package: 一句話簡述

多行說明改動的原因；若是修 bug 且 GitHub 上有對應 issue，把連結附在這裡。
```

版本更新（bump）：

```text
$category/$package: add $new_version, drop $old_version
```

{{% /details %}}

### 跟進上游新版本（nvchecker）

倉庫用 [nvchecker](https://github.com/lilydjwg/nvchecker) 每天自動比對各包的上游版本（配置在 `.github/workflows/overlay.toml`），有新版本就自動開/更新對應的 [GitHub issue](https://github.com/microcai/gentoo-zh/issues)——**不知道從哪下手，挑一個版本更新（bump）issue 來做最省心**。新增包時，記得也在 `overlay.toml` 中加一條 nvchecker 規則（寫明上游版本來源），讓它一併納入版本追蹤。

### 官方規範與參考

- [Gentoo Devmanual](https://devmanual.gentoo.org/)——寫 ebuild 的權威手冊（EAPI、變數、依賴、`metadata.xml` 等）
- [Ebuild 倉庫格式](https://wiki.gentoo.org/wiki/Repository_format)與 [Overlay 專案](https://wiki.gentoo.org/wiki/Project:Overlays)
- `pkgdev` / `pkgcheck`（`app-portage`）——現行的提交與 QA 工具
- 本倉庫 [README](https://github.com/microcai/gentoo-zh#readme)（鐵規矩與提交規範原文）與[依賴關係表](https://github.com/microcai/gentoo-zh/blob/deps-table/relation.md)

---

以下是**為社群網站（文章 / 翻譯 / 文件）貢獻**的指南。

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

## 如何為網站貢獻

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
