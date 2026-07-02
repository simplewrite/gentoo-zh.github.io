---
title: "gentoo-zh 倉庫遷移公告與執行方案"
description: "gentoo-zh overlay 的正式維護倉庫遷移到 GitHub 組織倉庫"
date: 2026-07-02
featured: true
tags: ["announcement", "overlay"]
authors:
  - name: Locez
    image: /authors/locez.webp
    link: https://github.com/locez
  - name: Clover（審校）
    image: /contributors/simplewrite/feature.webp
    link: https://github.com/simpleWrite
  - name: Mame（審校）
    image: /contributors/yangmame/feature.webp
    link: https://github.com/YangMame
  - name: Zakk（排版）
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/Zakkaus
---

gentoo-zh overlay 的正式維護倉庫遷移到 GitHub 組織倉庫：

- 新倉庫：https://github.com/gentoo-zh/gentoo-zh
- 原倉庫：https://github.com/microcai/gentoo-zh

本次遷移由原倉庫 owner 發起 GitHub repository transfer 完成。遷移完成後，`gentoo-zh/gentoo-zh` 作為 gentoo-zh overlay 的 canonical repository。

## 遷移背景

gentoo-zh overlay 遷移到 GitHub 組織倉庫，是為了讓維護權限、CI 配置、issue/PR 管理和釋出流程統一由社群維護團隊管理，降低單一帳號對長期維護的影響。

本次遷移採用 GitHub 官方 repository transfer。遷移結果如下：

- 保留完整 Git commit 歷史
- 保留 branches 和 tags
- 保留 releases
- 保留 GitHub issues
- 保留 GitHub pull requests
- 保留 GitHub stars 和 watchers
- 保留 fork network
- 保留原倉庫 Git URL 的 redirect
- 保留原有 commit SHA

遷移完成後，訪問 `microcai/gentoo-zh` 會跳轉到 `gentoo-zh/gentoo-zh`。舊的 Git remote URL 繼續可用；建議使用者和貢獻者在方便時更新到新 URL。

為避免破壞使用者現有配置，遷移完成後舊路徑 `microcai/gentoo-zh` 保持空置。GitHub 的舊地址跳轉依賴舊路徑未被重新佔用；如果該路徑被同名倉庫或同名 fork 佔用，舊 URL 將不再跳轉到新倉庫，仍在使用舊 URL 的使用者會受到影響。原 owner 不在 `microcai` 帳號下重新建立或 fork 名為 `gentoo-zh` 的倉庫；如需保留個人 fork，應避免使用會佔用舊路徑的同名倉庫。

## 使用者切換操作

舊地址會由 GitHub redirect 到新倉庫。手動配置過 remote 的使用者，建議在方便時更新到新 URL。

重新增 overlay：

```bash
sudo eselect repository remove gentoo-zh
sudo eselect repository add gentoo-zh git https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

直接修改現有 remote：

```bash
cd /var/db/repos/gentoo-zh
sudo git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

## 貢獻者切換操作

新的 issue、pull request 和維護討論統一提交到：

```text
https://github.com/gentoo-zh/gentoo-zh
```

已有本地工作副本的貢獻者更新 upstream：

```bash
git remote set-url upstream https://github.com/gentoo-zh/gentoo-zh.git
git fetch upstream
```

新的工作分支從新倉庫預設分支建立：

```bash
git checkout master
git pull upstream master
git checkout -b topic/name
```

## 遷移執行步驟

### 1. 遷移前準備

`gentoo-zh/gentoo-zh` 當前作為 `microcai/gentoo-zh` 的 fork 存在。執行 repository transfer 前釋放目標倉庫名稱。

執行操作：

1. 刪除現有 `gentoo-zh/gentoo-zh`
2. 確認 `gentoo-zh/gentoo-zh` 名稱已釋放
3. 確認 `gentoo-zh` 組織 owner 已準備接受 transfer
4. 確認原 owner 知悉遷移完成後不再佔用 `microcai/gentoo-zh` 舊路徑，不在 `microcai` 帳號下重新建立或 fork 名為 `gentoo-zh` 的倉庫，以免破壞舊 URL 到新倉庫的跳轉

### 2. 原 owner 發起 repository transfer

由 `microcai/gentoo-zh` 的 owner 在 GitHub 倉庫設定中發起 transfer：

```text
Settings -> General -> Danger Zone -> Transfer ownership
```

目標 owner 填寫：

```text
gentoo-zh
```

目標倉庫名保持：

```text
gentoo-zh
```

### 3. gentoo-zh 組織接受遷移

`gentoo-zh` 組織 owner 接受 GitHub transfer 邀請。

接受完成後，倉庫地址變為：

```text
https://github.com/gentoo-zh/gentoo-zh
```

### 4. 驗證 transfer 結果

遷移完成後確認以下內容：

- 倉庫位於 `gentoo-zh/gentoo-zh`
- 預設分支為 `master`
- issues 已遷移
- pull requests 已遷移
- stars 和 watchers 已保留
- fork network 已保留
- 舊地址 `https://github.com/microcai/gentoo-zh` 跳轉到新地址
- `git clone https://github.com/microcai/gentoo-zh.git` 跳轉到新倉庫
- `git clone https://github.com/gentoo-zh/gentoo-zh.git` 正常工作
- `microcai/gentoo-zh` 舊路徑未被重新建立為倉庫或同名 fork

### 5. 更新倉庫內維護入口

遷移完成後修改以下檔案：

- `repo.xml`
- `README.md`
- `sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild`
- `.github/workflows/nvchecker.yml`
- `MIGRATION.md`

`repo.xml` 中的 source 更新為：

```xml
<source type="git">https://github.com/gentoo-zh/gentoo-zh.git</source>
```

`README.md` 中的 dependencies table 連結更新為：

```text
https://github.com/gentoo-zh/gentoo-zh/blob/deps-table/relation.md
```

`sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild` 中的支援入口更新為：

```text
https://github.com/gentoo-zh/gentoo-zh
```

ebuild 註釋中指向原倉庫 issue 的歷史連結保留不變。repository transfer 會保留舊 issue 連結跳轉，不需要批次替換歷史 issue URL。

### 6. 新增 `MIGRATION.md`

在新倉庫根目錄新增 `MIGRATION.md`：

````md
# gentoo-zh repository migration / gentoo-zh 倉庫遷移說明

## 中文

gentoo-zh overlay 已透過 GitHub repository transfer 從個人倉庫遷移到社群組織倉庫：

- 原倉庫：https://github.com/microcai/gentoo-zh
- 當前倉庫：https://github.com/gentoo-zh/gentoo-zh

遷移完成後，`gentoo-zh/gentoo-zh` 是 gentoo-zh overlay 的正式維護入口。GitHub 會將舊倉庫地址自動跳轉到新倉庫；舊的 Git remote URL 也會繼續跳轉。

過去所有維護者和使用者對 gentoo-zh 的貢獻會隨倉庫遷移一併保留。後續維護在 `gentoo-zh/gentoo-zh` 繼續進行。

為了讓倉庫地址與當前維護入口保持一致，建議在方便時將本地 remote 更新為：

```bash
git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
```

後續 issue、pull request 和維護討論請使用當前倉庫。

## English

The gentoo-zh overlay has been transferred from the personal repository to the community organization through GitHub repository transfer:

- Previous repository: https://github.com/microcai/gentoo-zh
- Current repository: https://github.com/gentoo-zh/gentoo-zh

After the transfer, `gentoo-zh/gentoo-zh` is the canonical maintenance repository for the gentoo-zh overlay. GitHub redirects the old repository URL to the new one, and old Git remote URLs continue to work through GitHub redirects.

Contributions from past maintainers and users are preserved as part of this repository transfer. Future maintenance continues at `gentoo-zh/gentoo-zh`.

To keep local remotes aligned with the current maintenance location, update them when convenient:

```bash
git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
```

Please use the current repository for future issues, pull requests, and maintenance discussions.
````

### 7. 更新 README

在 `README.md` 中新增一個簡短遷移小節，放在安裝說明前：

````md
> [!NOTE]
> gentoo-zh overlay has moved to https://github.com/gentoo-zh/gentoo-zh. Old GitHub URLs continue to redirect. If you manually configured a remote, update it when convenient.

## Repository migration

This repository was transferred from `microcai/gentoo-zh` to the `gentoo-zh` organization through GitHub repository transfer.

The current canonical repository is:

https://github.com/gentoo-zh/gentoo-zh

See [MIGRATION.md](./MIGRATION.md) for details.
````

### 8. 新增 Gentoo repository news

在 `metadata/news/` 中新增一個符合 GLEP 42 的 repository news item。該 news item 使用單個 `.en.txt` 檔案；英文為 authoritative 正文，中文為補充說明，最後統一給出遷移指令。使用者同步 overlay 後可透過 `eselect news read` 讀取。

新增 news item 目錄：

```text
metadata/news/2026-07-02-gentoo-zh-transfer/
```

news 檔案：

```text
metadata/news/2026-07-02-gentoo-zh-transfer/2026-07-02-gentoo-zh-transfer.en.txt
```

內容：

```text
Title: Action required: gentoo-zh repository moved
Author: gentoo-zh maintainers <overlay@gentoozh.org>
Content-Type: text/plain
Posted: 2026-07-02
Revision: 1
News-Item-Format: 1.0

ACTION REQUIRED: Update manually configured gentoo-zh overlay remotes.

The gentoo-zh overlay has been transferred through GitHub repository transfer
from:

https://github.com/microcai/gentoo-zh

to the community organization repository:

https://github.com/gentoo-zh/gentoo-zh

GitHub redirects old repository URLs and old Git remote URLs to the new
repository. The new repository is the canonical maintenance location for the
gentoo-zh overlay.

Please use the new repository for future issues, pull requests, and
maintenance discussions.

gentoo-zh overlay 已透過 GitHub repository transfer 從以下倉庫遷移：

https://github.com/microcai/gentoo-zh

到新的社群組織倉庫：

https://github.com/gentoo-zh/gentoo-zh

GitHub 會將舊倉庫地址和舊 Git remote URL 自動跳轉到新倉庫。新倉庫
是 gentoo-zh overlay 後續維護的正式入口。

後續 issue、pull request 和維護討論請使用新倉庫。

Users who configured the gentoo-zh overlay remote manually should update it
as soon as possible.

手動配置過 gentoo-zh overlay remote 的使用者請儘快更新為新地址：

cd /var/db/repos/gentoo-zh
sudo git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

### 9. 更新 CI 與自動化配置

遷移後更新 GitHub Actions 和自動化任務中的倉庫歸屬配置。

`.github/workflows/nvchecker.yml` 中的倉庫名判斷更新為：

```yaml
if: github.repository == 'gentoo-zh/gentoo-zh'
```

新倉庫確認以下 Actions secrets：

- `GENTOO_ZH_NVCHECKER_PAT`

新倉庫啟用以下 Actions 權限：

- `Read and write permissions`
- `Allow GitHub Actions to create and approve pull requests`

`deps-table` 分支由 dependencies table workflow 自動更新。倉庫 ruleset 對 `deps-table` 的 force push 權限單獨放行給 GitHub Actions。

pull request CI 繼續由 GitHub Actions 的 `pull_request` 事件觸發。

### 10. 驗證並提交遷移後倉庫修改

倉庫內遷移修改全部完成後統一驗證並提交一次，避免把 README、metadata 和 news 拆成重複提交。

驗證 news 可被讀取：

```bash
eselect news list
eselect news read
```

提交本倉庫內全部遷移修改：

```bash
git add metadata/news/2026-07-02-gentoo-zh-transfer README.md repo.xml sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild .github/workflows/nvchecker.yml MIGRATION.md
git commit -m "Update repository metadata after transfer"
git push origin master
```

### 11. 配置組織維護規則

在 `gentoo-zh/gentoo-zh` 倉庫設定中完成以下配置：

- 預設分支設定為 `master`
- 禁止刪除預設分支
- 禁止 force push 到預設分支
- 開啟 branch protection 或 ruleset
- 預設分支合併必須經過 pull request
- 維護者透過 GitHub team 管理權限
- 倉庫 description 設定為 `Gentoo Linux overlay for Chinese users`
- 倉庫 homepage 設定為 gentoo-zh 社群主頁

### 12. 更新 Gentoo overlay registry

同步更新 `gentoo/api-gentoo-org` 中的 overlay registry，讓 `gentoo-zh` 指向新的組織倉庫。

目標倉庫：

```text
https://github.com/gentoo/api-gentoo-org
```

修改檔案：

```text
files/overlays/repositories.xml
```

修改 `gentoo-zh` 條目中的以下欄位：

```xml
<repo quality="experimental" status="unofficial">
  <name>gentoo-zh</name>
  <description>To provide programs useful to Chinese speaking users (merged
    from gentoo-china and gentoo-taiwan).</description>
  <homepage>https://github.com/gentoo-zh/gentoo-zh</homepage>
  <owner type="project">
    <email>overlay@gentoozh.org</email>
    <name>gentoozh</name>
  </owner>
  <source type="git">https://github.com/gentoo-zh/gentoo-zh.git</source>
  <source type="git">git+ssh://git@github.com/gentoo-zh/gentoo-zh.git</source>
  <feed>https://github.com/gentoo-zh/gentoo-zh/commits/master.atom</feed>
</repo>
```

本次 registry PR 更新以下欄位：

- `homepage`
- `owner type`
- `owner/email`
- `owner/name`
- HTTPS `source`
- SSH `source`
- Atom `feed`

執行步驟：

```bash
git clone https://github.com/gentoo/api-gentoo-org.git
cd api-gentoo-org
git checkout -b update-gentoo-zh-overlay-metadata
```

編輯：

```text
files/overlays/repositories.xml
```

提交：

```bash
git add files/overlays/repositories.xml
git commit -m "Update gentoo-zh overlay metadata"
```

驗證：

```bash
python bin/repositories-checker.py - files/overlays/repositories.xml
```

向 `gentoo/api-gentoo-org` 提交 pull request：

```text
Title: Update gentoo-zh overlay metadata

The gentoo-zh overlay repository has been transferred from microcai/gentoo-zh to gentoo-zh/gentoo-zh via GitHub repository transfer.

This updates the overlay registry homepage, Git sources, Atom feed URL, and owner metadata to the new canonical repository and maintainer organization.
```

## 後續維護事項

遷移完成後執行以下維護事項：

1. 更新 gentoo-zh overlay 內部後設資料
2. 更新 README 和安裝文件
3. 跟進 `gentoo/api-gentoo-org` 中 gentoo-zh registry PR 合併
4. 檢查 GitHub Actions secrets 和 permissions
5. 配置 branch protection 和維護者 team
6. 確認 `eselect news read` 可讀到遷移 news
7. 將後續貢獻入口統一收斂到 `gentoo-zh/gentoo-zh`

## 補記：官網側進度（zakkaus）

官網[貢獻者牆](/contributors/)的自動統計（`update-contributors.py`）與相關頁面說明已提前指向 `Gentoo-zh/gentoo-zh`——它每月 1 日自動更新，下次執行時遷移已完成。[Overlay 頁](/overlay/)與[貢獻指南](/contributing/)裡 fork、issue 等教學連結仍指向 `microcai/gentoo-zh`，等遷移完成後再統一更新。
