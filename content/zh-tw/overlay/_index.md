---
title: "Overlay"
---

Overlay 是官方 Portage 樹之外的軟體來源——疊加上去，就能裝到官方源裡沒有的包。gentoo-zh 是其中歷史悠久的一個：前身是 2003 年的 gentoo-tw 與隨後的 gentoo-china，兩岸社群合併而來，原始碼在 [GitHub](https://github.com/microcai/gentoo-zh)。

到現在 gentoo-zh 收錄了 450 多個軟體套件，大致這麼幾類：

- **中文 / CJK**：fcitx 輸入法和一大堆外掛、碼錶（rime、chinese-addons 等），搜狗 / 萌娘 / zhwiki 拼音詞庫，中文字型，以及一些軟體的 CJK 補丁
- **網路、開發工具等官方源裡還沒有的**：畢竟是 gentoo 使用者，誰手裡沒幾個自己維護的包
- **打好補丁的桌面 / 效能向核心**：cachyos-sources、xanmod、liquorix 這些
- **跟進新版本**：官方源暫時沒人管的包，這邊接著出新版
- **錯誤修復**：開發者踩到 bug，解決後第一時間把補丁推回源裡

有條立身的鐵規矩——「別弄壞別人的系統」，每個 ebuild 都得在支援的架構上測過才進源。

## 新增 gentoo-zh

用 `eselect repository` 啟用最省事（先裝好 `app-eselect/eselect-repository`）：

```bash
eselect repository enable gentoo-zh
emerge --sync gentoo-zh
```

{{% details title="手動配置（不想用 eselect）" %}}

在 `/etc/portage/repos.conf/` 下建立 `gentoo-zh.conf`：

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://github.com/microcai/gentoo-zh.git
auto-sync = yes
```

然後 `emerge --sync gentoo-zh`。

{{% /details %}}

{{< callout type="info" >}}
2025 年 10 月起官方不再為第三方倉庫提供快取鏡像，gentoo-zh 改為直接從 GitHub 上游同步。之前新增過的使用者需更新同步源，見 [這篇說明](/posts/2025-10-07-thirdparty-repo-mirror-removal/)。
{{< /callout >}}

## 中國內陸鏡像加速

直連 GitHub 或官方 distfiles 偏慢時，把 gentoo-zh 換成中國內陸鏡像。下面都已實測可用，整理自 [peeweep](/contributors/peeweep/) 的[公告](https://t.me/gentoocn/56)，感謝！

### git 同步源

把 overlay 的同步源切到中國內陸鏡像（gentoo-zh 是 [microcai/gentoo-zh](https://github.com/microcai/gentoo-zh) 的完整 ebuild 鏡像，只含 ebuild、不含原始碼）。可用地址：

- 重慶大學：`https://mirrors.cqu.edu.cn/git/gentoo-zh.git`
- 南京大學：`https://mirror.nju.edu.cn/git/gentoo-zh.git`

第一次新增（先裝好 git）：

```bash
sudo emerge -aq dev-vcs/git          # 沒裝 git 先裝
rm -rf /var/db/repos/gentoo-zh       # 同步過的話先清掉舊的
eselect repository add gentoo-zh git https://mirrors.cqu.edu.cn/git/gentoo-zh.git
emerge --sync gentoo-zh
```

已經新增過的，把 `/etc/portage/repos.conf/gentoo-zh.conf` 裡的 `sync-uri` 改成上面任一地址即可。

### distfiles 快取

加速軟體套件原始碼下載。源站 <https://distfiles.gentoocn.org/>，可用鏡像：

- 重慶大學：`https://mirrors.cqu.edu.cn/gentoo-zh/`
- 南京大學：`https://mirror.nju.edu.cn/gentoo-zh`

在 `/etc/portage/make.conf` 的 `GENTOO_MIRRORS` 裡，官方源之後追加：

```bash
GENTOO_MIRRORS="${GENTOO_MIRRORS} https://distfiles.gentoocn.org"
```

{{< callout type="info" >}}
- gentoo-zh 裡部分包需要啟用 `~amd64` 關鍵字，注重穩定性的話自行取捨。
- 不想 mirror 某些 distfiles（版權等原因）時，在對應 ebuild 里加 `RESTRICT="mirror"`。
{{< /callout >}}

## 用 overlay 裡的包

配置好後，gentoo-zh 裡的包就和官方源一樣，直接 emerge：

```bash
emerge --ask <package-name>     # 安裝
eix -RO gentoo-zh               # 看 overlay 提供了哪些包
```

## 參與貢獻

歡迎給 gentoo-zh 添磚加瓦：到 [GitHub 倉庫](https://github.com/microcai/gentoo-zh) 提 Pull Request，發現問題也歡迎提 issue。
