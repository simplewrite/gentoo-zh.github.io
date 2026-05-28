---
title: "下載"
---

想裝 Gentoo，第一步是把安裝介質弄到手——官方提供了多種可選的安裝介質。下面先列官方下載源，再附一份中國內陸的快速下載源（多為鏡像站）：大陸直連官方站通常比較慢，能走鏡像就儘量走。

## 中文社群定製：KDE 桌面 Live ISO {#live-iso}

中文社群自己做的，每週自動構建，裝完就能用：中文顯示、中文輸入法（fcitx5）和 flclash 網路工具都配好了。不想一上來就跟指令列死磕，可以從這個起步。

- **下載站**：<https://iso.gig-os.org/>（中國內陸可直接訪問）
- **專案倉庫（備用）**：<https://github.com/Gig-OS/Live-ISO>
- **登入憑據**：使用者 `live` / 密碼 `live` / Root 密碼 `live`

## 官方下載頁面

**Gentoo 官方下載頁：** <https://www.gentoo.org/downloads/>

官方提供了以下安裝介質：
- **Minimal Installation CD**：最小化安裝光碟，適合有經驗的使用者
- **LiveGUI**：帶圖形介面的 Live 系統，適合新使用者
- **Stage Archives**：Stage3 壓縮包，Stage3 是一個預先編譯好的最小化 Linux 使用者空間環境，它內含了完整的編譯工具鏈（GCC）與 Portage 套件管理器，作為使用者從原始碼構建個性化 Gentoo 系統的標準起點
## 架構選擇

Gentoo 支援多種 CPU 架構：
- **amd64** - 64 位 x86 架構（最常用，支援 Intel 和 AMD 處理器）
- **x86** - 32 位 x86 架構
- **arm64** - 64 位 ARM 架構
- **arm** - 32 位 ARM 架構
- 其他架構請參考官方下載頁

{{< callout type="info" >}}
**Apple Silicon Mac 使用者注意**

本頁面列出的標準鏡像**不適用於 Apple Silicon Mac**。如果您使用 M1 / M2 系列 MacBook（M3 及以上目前驅動支援尚不完整），請參考：

**[在 Apple Silicon Mac 上安裝 Gentoo Linux](/posts/2025-10-02-gentoo-m-series-mac/)**
{{< /callout >}}

## 中中國內陸陸鏡像源

以下鏡像源提供 Gentoo 安裝介質的快速下載（推薦中中國內陸陸使用者使用）：

### 清華大學開源鏡像站
- **下載地址：** <https://mirrors.tuna.tsinghua.edu.cn/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等
- 穩定快速，推薦使用

### 中國科學技術大學（USTC）
- **下載地址：** <https://mirrors.ustc.edu.cn/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等
- 教育網和公網訪問速度都很快

### 浙江大學
- **下載地址：** <https://mirrors.zju.edu.cn/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 北京外國語大學
- **下載地址：** <https://mirrors.bfsu.edu.cn/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 網易開源鏡像
- **下載地址：** <https://mirrors.163.com/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 南京大學 eScience Center
- **下載地址：** <https://mirrors.nju.edu.cn/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

## 其他亞洲地區鏡像

### 香港地區

**CICKU 鏡像**
- **下載地址：** <https://hk.mirrors.cicku.me/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

**PlanetUnix Networks**
- **下載地址：** <https://hippocamp.cn.ext.planetunix.net/pub/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 臺灣地區

**國家高速網路與計算中心（NCHC）**
- **下載地址：** <http://ftp.twaren.net/Linux/Gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

**CICKU 臺灣鏡像**
- **下載地址：** <https://tw.mirrors.cicku.me/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 新加坡地區

**Freedif**
- **下載地址：** <https://mirror.freedif.org/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

**CICKU 新加坡鏡像**
- **下載地址：** <https://sg.mirrors.cicku.me/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

**PlanetUnix Networks**
- **下載地址：** <https://enceladus.sg.ext.planetunix.net/pub/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

### 日本地區

**北陸尖端科學技術大學院大學（JAIST）**
- **下載地址：** <https://ftp.iij.ad.jp/pub/linux/gentoo/releases/>
- 支援架構：amd64, x86, arm64 等

## 下載檔案說明

在鏡像站的 `releases/` 目錄下，選擇您的架構（如 `amd64/`），然後選擇：

### 安裝 ISO 鏡像
- 目錄：`autobuilds/current-install-amd64-minimal/`
  - `install-amd64-minimal-*.iso` - 最小化安裝 ISO
  - `install-amd64-minimal-*.iso.DIGESTS` - 校驗檔案

- 目錄：`autobuilds/current-livegui-amd64/`
  - `livegui-amd64-*.iso` - 圖形化 Live ISO

### Stage3 壓縮包
- 目錄：`autobuilds/current-stage3-amd64-*/`
  - `stage3-amd64-*.tar.xz` - Stage3 壓縮包
  - `stage3-amd64-*.tar.xz.DIGESTS` - 校驗檔案

**重要提示：** 下載後請驗證檔案完整性（使用 DIGESTS 檔案）。

## 驗證下載檔案

下載完成後，建議驗證檔案的完整性：

```bash
# 計算 SHA512 校驗和
sha512sum install-amd64-minimal-*.iso

# 與 DIGESTS 檔案中的值對比
cat install-amd64-minimal-*.iso.DIGESTS
```

## 安裝指南

下載安裝介質後，請參考：
- **Gentoo 官方手冊：** <https://wiki.gentoo.org/wiki/Handbook:AMD64/zh-cn>
- **中文社群文件：** 正在建設中