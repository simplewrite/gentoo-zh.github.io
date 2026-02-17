---
title: "映象列表"
---

Gentoo 的套件管理體系由 Portage 樹和 Distfiles 兩部分組成：

- **Portage 樹**：套件資料庫，包含所有軟體套件的 ebuild 檔案和後設資料
  - 傳統透過 rsync 同步
  - 現代推薦使用 Git 同步（速度更快，支援增量更新）
- **Distfiles**：原始碼下載檔案，透過 HTTP/HTTPS 提供

Gentoo 在全球有大量映象。本頁面列出亞洲地區對中國使用者有速度優勢的主要映象。

**官方完整映象列表：**
- Distfiles 映象：<https://www.gentoo.org/downloads/mirrors/#CN>
- rsync 映象：<https://www.gentoo.org/support/rsync-mirrors/#CN>

**配置參考檔案：**
- 倉庫配置：<https://wiki.gentoo.org/wiki//etc/portage/repos.conf/zh-tw>
- Distfiles 映象配置：<https://wiki.gentoo.org/wiki/GENTOO_MIRRORS/zh-tw>

## Portage 樹同步方式

由於 rsync 是 CPU 與 IO 密集型操作，伺服器負擔較重且容易遭受 DoS 攻擊，因此絕大多數映象不再提供 rsync 服務。
**推薦使用 Git 方式同步 Portage 樹**，具有以下優勢：
- 增量更新，節省頻寬
- 更好的網路穩定性
- 支援多種映象源選擇

如果你無法找到合適的 rsync 映象，或防火牆禁止 rsync，可以使用以下替代方案：

1. **使用 emerge-webrsync**：Portage 會從 Distfiles 下載每日歸檔的 Portage 壓縮套件進行同步。
2. **使用 Git 同步**：在 `/etc/portage/repos.conf/gentoo.conf` 中配置：
   ```ini
   [DEFAULT]
   main-repo = gentoo

   [gentoo]
   location = /var/db/repos/gentoo
   sync-type = git
   sync-uri = https://mirrors.bfsu.edu.cn/git/gentoo-portage.git
   auto-sync = yes
   ```

   **可用的 Git 映象源：**
   - 北京外國語大學：`https://mirrors.bfsu.edu.cn/git/gentoo-portage.git`
   - 清華大學：`https://mirrors.tuna.tsinghua.edu.cn/git/gentoo-portage.git`
   - GitHub（國外）：`https://github.com/gentoo-mirror/gentoo.git`

   配置後執行 `emerge --sync` 即可透過 Git 同步 Portage 樹。

## Distfiles 映象配置

配置 Distfiles 映象可以加速軟體套件原始碼的下載。有兩種配置方式：

### 方法一：使用 make.conf 配置

在 `/etc/portage/make.conf` 檔案中新增 `GENTOO_MIRRORS` 變數：

```bash
GENTOO_MIRRORS="https://mirrors.bfsu.edu.cn/gentoo/ https://mirrors.tuna.tsinghua.edu.cn/gentoo/ https://mirrors.ustc.edu.cn/gentoo/"
```

建議配置多個映象源，Portage 會按順序嘗試下載，提高成功率。

### 方法二：使用 mirrorselect 工具

```bash
# 安裝 mirrorselect
emerge --ask app-portage/mirrorselect

# 自動選擇最快的映象（測試連線速度）
mirrorselect -i -o >> /etc/portage/make.conf

# 或手動從列表中選擇
mirrorselect -i -o >> /etc/portage/make.conf
```

# 中國大陸映象

* 清華大學開源映象站
  - Portage: 不提供
  - Distfiles: https://mirrors.tuna.tsinghua.edu.cn/gentoo
* 中國科學技術大學（USTC）
  - Portage: rsync://rsync.mirrors.ustc.edu.cn/gentoo/
  - Distfiles: https://mirrors.ustc.edu.cn/gentoo/
* 浙江大學
  - Portage: rsync://mirrors.zju.edu.cn/gentoo/
  - Distfiles: https://mirrors.zju.edu.cn/gentoo/
* 南京大學 eScience Center
  - Portage: 不提供
  - Distfiles: https://mirrors.nju.edu.cn/gentoo/
* 蘭州大學開源社群
  - Portage: 不提供
  - Distfiles: https://mirror.lzu.edu.cn/gentoo
* 網易
  - Portage: 不提供
  - Distfiles: https://mirrors.163.com/gentoo/
* 阿里雲
  - Portage: 不提供
  - Distfiles: https://mirrors.aliyun.com/gentoo/

# 香港映象

* CICKU
  - Portage: 不提供
  - Distfiles: https://hk.mirrors.cicku.me/gentoo/
* PlanetUnix Networks
  - Portage: rsync://hippocamp.cn.ext.planetunix.net/gentoo/
  - Distfiles: https://hippocamp.cn.ext.planetunix.net/pub/gentoo/

# 臺灣映象

* 國家高速網路與計算中心（NCHC）
  - Portage: 不提供
  - Distfiles: http://ftp.twaren.net/Linux/Gentoo/
* CICKU
  - Portage: 不提供
  - Distfiles: https://tw.mirrors.cicku.me/gentoo/

# 新加坡映象

* Freedif
  - Portage: rsync://mirror.freedif.org/gentoo
  - Distfiles: https://mirror.freedif.org/gentoo
* CICKU
  - Portage: 不提供
  - Distfiles: https://sg.mirrors.cicku.me/gentoo/
* PlanetUnix Networks
  - Portage: rsync://enceladus.sg.ext.planetunix.net/gentoo/
  - Distfiles: https://enceladus.sg.ext.planetunix.net/pub/gentoo/

# 日本映象

* 北陸尖端科學技術大學院大學（JAIST）
  - Portage: 不提供
  - Distfiles: https://ftp.iij.ad.jp/pub/linux/gentoo/
