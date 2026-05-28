---
title: "Overlay"
---

Gentoo 的 Overlay 機制可以讓使用者使用官方 Portage 樹以外的軟體套件，作為一個軟體來源的擴充和疊加。
故名為 Overlay（意為疊加）。

gentoo-zh Overlay 是 Gentoo 社群歷史悠久的老牌 Overlay 之一，其前身是 2003 年創立的 gentoo-tw
和隨後創立的 gentoo-china。後來，臺灣和大陸社群的共同努力下，合併為了 gentoo-zh overlay。

到現在，gentoo-zh 已經收錄了 450 多個軟體套件，大致是這麼幾類：

* **中文 / CJK 相關**：fcitx 輸入法和一大堆外掛、碼錶（rime、chinese-addons 等），搜狗 / 萌娘 / zhwiki 拼音詞庫，中文字型，以及一些軟體的 CJK 補丁。
* **網路、開發工具等官方源裡還沒有的**：畢竟是 gentoo 使用者，誰手裡沒幾個自己維護的包。
* **打好補丁的桌面 / 效能向核心**：cachyos-sources、xanmod、liquorix 這些，省得自己一個個打補丁。
* **跟進新版本**：有些包官方源裡暫時沒人管、更新不及時，這邊自己接著出新版本。
* **錯誤修復**：開發者自己踩到 bug，解決後會第一時間把補丁推回源裡。

overlay 有條立身的鐵規矩——「別弄壞別人的系統」，所以每個 ebuild 都得在支援的架構上測過才進源。

## 倉庫地址

gentoo-zh overlay 的原始碼託管在 GitHub 上：

<https://github.com/microcai/gentoo-zh>

## 如何使用

{{< callout type="warning" >}}
**重要提示**（更新時間：2025-10-07）

根據 [Gentoo 官方公告](https://www.gentoo.org/support/news-items/2025-10-07-cache-enabled-mirrors-removal.html)，Gentoo 已停止為第三方倉庫提供快取鏡像支援。從 2025-10-30 起，所有第三方倉庫（包括 gentoo-zh）的鏡像配置將從官方倉庫列表中移除。

**這意味著什麼？**
- `eselect repository` 和 `layman` 等工具仍可正常使用
- 官方將不再提供快取鏡像，改為直接從上游源（GitHub）同步
- 官方倉庫（::gentoo、::guru、::kde、::science）不受影響，仍可使用鏡像

**如果您之前已新增 gentoo-zh overlay，請按下方指令更新同步 URI。**
{{< /callout >}}

```bash
# 檢視已安裝的倉庫
eselect repository list -i

# 移除舊配置
eselect repository remove gentoo-zh

# 重新啟用（將自動使用正確的上游源）
eselect repository enable gentoo-zh
```

### 手動配置

在 `/etc/portage/repos.conf/` 目錄下建立 `gentoo-zh.conf` 檔案，內容如下：

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://github.com/microcai/gentoo-zh.git
auto-sync = yes
```

然後同步：

```bash
emerge --sync gentoo-zh
```

## 鏡像加速

中國內陸直連 GitHub 或官方 distfiles 偏慢時，用下面的中國內陸鏡像加速。

### distfiles 鏡像

把 overlay 軟體套件的原始碼快取了一份，直連慢的時候從這兒拉。源站：<https://distfiles.gentoocn.org/>

**鏡像站點**：
- 重慶大學：<https://mirrors.cqu.edu.cn/gentoo-zh/>
- 南京大學：<https://mirror.nju.edu.cn/gentoo-zh>

在 `/etc/portage/make.conf` 的 `GENTOO_MIRRORS` 中，於官方源之後追加 gentoo-zh distfiles 源：

```bash
GENTOO_MIRRORS="https://mirrors.bfsu.edu.cn/gentoo"               # ::gentoo 官方 distfiles
GENTOO_MIRRORS="${GENTOO_MIRRORS} https://distfiles.gentoocn.org" # ::gentoo-zh distfiles
```

{{< callout type="info" >}}
如果因版權問題或其他原因不想 mirror 某些 distfiles，請在對應 ebuild 中加入 `RESTRICT="mirror"`。
{{< /callout >}}

### Git 倉庫鏡像

中國內陸直連 GitHub 不穩或太慢時，把 overlay 同步切到中國內陸鏡像，更穩更快。源倉庫：<https://github.com/microcai/gentoo-zh.git>

**鏡像站點**：
- 重慶大學：<https://mirrors.cqu.edu.cn/git/gentoo-zh.git>
- 南京大學：<https://mirror.nju.edu.cn/git/gentoo-zh.git>

在 `/etc/portage/repos.conf/gentoo-zh.conf` 中，把 `sync-uri` 指向鏡像即可：

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://mirrors.cqu.edu.cn/git/gentoo-zh.git
auto-sync = yes
```

配置幫助見 [cqu mirror wiki](https://mirrors.cqu.edu.cn/#/wiki/mirror-wiki/gentoo-zh.git)。

本節鏡像站彙總與配置說明整理自 [peeweep](/contributors/peeweep/) 的[公告](https://t.me/gentoocn/56)，感謝！

## 使用 overlay 中的軟體套件

配置好之後，gentoo-zh 裡的軟體套件就和官方源一樣，直接 emerge 就行：

```bash
emerge --ask <package-name>
```

如果想檢視 overlay 提供了哪些軟體套件，可以使用：

```bash
eix -RO gentoo-zh
```

## 參與貢獻

歡迎給 gentoo-zh overlay 添磚加瓦：到 GitHub 倉庫提個 Pull Request 即可，發現問題也歡迎提 issue。
