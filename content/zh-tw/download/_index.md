---
title: "下載"
---

裝 Gentoo 先把安裝介質準備好。新手最省事的是中文社群的 Live ISO；想用官方介質的，從下面的鏡像裡就近選一個。

## 中文社群 Live ISO

中文社群定製的 KDE 桌面 Live ISO——中文顯示、中文輸入法（fcitx5）、flclash 網路工具的安裝鏡像，適合新手入門使用。

- **下載站**：<https://mirror.gentoozh.org/>（海外伺服器，1Gbps 不限流量；境內訪問可能偏慢）
- **備用倉庫**：<https://github.com/Gig-OS/Live-ISO>
- **登入憑據**：使用者 {{< copy "live" >}} / 密碼 {{< copy "live" >}} / Root {{< copy "live" >}}
- **硬體要求**：64 位 x86 CPU，需支援 AVX2（約 2013 年後的處理器）；更老的 CPU 無法啟動本鏡像。
- **更新頻率**：每週自動重新編譯並上傳，始終是較新的系統快照；下載站只保留最近幾個版本，請以站上實際檔名（`gig-os-日期.iso`）為準。

{{< callout type="info" >}}
**Apple Silicon Mac（M1 / M2）** 不適用下面的標準鏡像，請看 [在 Apple Silicon Mac 上安裝 Gentoo Linux](/posts/2025-10-02-gentoo-m-series-mac/)。
{{< /callout >}}

## 鏡像源

下面節點都已逐項實測可用，均提供 amd64 / x86 / arm64 等架構的安裝介質。按地區就近選一般更快：

| 鏡像 | 地區 | 下載地址（releases/） |
| --- | --- | --- |
| 清華 TUNA | 華北·北京 | <https://mirrors.tuna.tsinghua.edu.cn/gentoo/releases/> |
| 北外 BFSU | 華北·北京 | <https://mirrors.bfsu.edu.cn/gentoo/releases/> |
| 中科大 USTC | 華東·合肥 | <https://mirrors.ustc.edu.cn/gentoo/releases/> |
| 浙大 ZJU | 華東·杭州 | <https://mirrors.zju.edu.cn/gentoo/releases/> |
| 南大 NJU | 華東·南京 | <https://mirrors.nju.edu.cn/gentoo/releases/> |
| 山大 SDU | 華東·青島 | <https://mirrors.sdu.edu.cn/gentoo/releases/> |
| 華科 HUST | 華中·武漢 | <https://mirrors.hust.edu.cn/gentoo/releases/> |
| 南科大 SUSTech | 華南·深圳 | <https://mirrors.sustech.edu.cn/gentoo/releases/> |
| 哈工大 HIT | 東北·哈爾濱 | <https://mirrors.hit.edu.cn/gentoo/releases/> |
| 蘭大 LZU | 西北·蘭州 | <https://mirror.lzu.edu.cn/gentoo/releases/> |
| 阿里雲 | 全國·CDN | <https://mirrors.aliyun.com/gentoo/releases/> |
| 網易 163 | 全國·CDN | <https://mirrors.163.com/gentoo/releases/> |
| CERNET | 全國·就近 | <https://mirrors.cernet.edu.cn/gentoo/releases/> |
| CICKU | 香港 | <https://hk.mirrors.cicku.me/gentoo/releases/> |
| PlanetUnix | 香港 | <https://hippocamp.cn.ext.planetunix.net/pub/gentoo/releases/> |
| xTom | 香港 | <https://mirror.xtom.com.hk/gentoo/releases/> |
| Rackspace | 香港 | <https://mirror.rackspace.com/gentoo/releases/> |
| aditsu | 香港 | <http://gentoo.aditsu.net:8000/releases/>（HTTP） |
| NCHC | 臺灣 | <http://ftp.twaren.net/Linux/Gentoo/releases/> |
| CICKU | 臺灣 | <https://tw.mirrors.cicku.me/gentoo/releases/> |
| Freedif | 新加坡 | <https://mirror.freedif.org/gentoo/releases/> |
| CICKU | 新加坡 | <https://sg.mirrors.cicku.me/gentoo/releases/> |
| PlanetUnix | 新加坡 | <https://enceladus.sg.ext.planetunix.net/pub/gentoo/releases/> |

{{% details title="官方介質與架構" %}}

**官方下載頁**：<https://www.gentoo.org/downloads/>

- **Minimal Installation CD** — 最小化安裝光碟，適合有經驗的使用者
- **LiveGUI** — 帶圖形介面的 Live 系統，適合新使用者
- **Stage3** — 預先編譯好的最小化使用者空間，含完整編譯工具鏈與 Portage，是從原始碼構建的標準起點

架構：amd64（最常用）、x86、arm64、arm，其他見官方下載頁。

{{% /details %}}

{{% details title="下載哪些檔案、怎麼校驗" %}}

在鏡像的 `releases/` 下選好架構（如 `amd64/`），然後：

- **安裝 ISO**：`autobuilds/current-install-amd64-minimal/` 裡的 `install-amd64-minimal-*.iso` + `.DIGESTS`；圖形版取 `current-livegui-amd64/` 裡的 `livegui-amd64-*.iso`
- **Stage3**：`autobuilds/current-stage3-amd64-*/` 裡的 `stage3-amd64-*.tar.xz` + `.DIGESTS`

下載後用 DIGESTS 校驗：

```bash
sha512sum install-amd64-minimal-*.iso          # 算 SHA512
cat install-amd64-minimal-*.iso.DIGESTS        # 跟 DIGESTS 裡的值對比
```

{{% /details %}}

## 下一步

裝好系統後給 Portage 換中國內陸源（git / rsync / distfiles），見 **[鏡像列表](/mirrorlist/)**；安裝流程參考 **[Gentoo 官方手冊（AMD64 · 中文）](https://wiki.gentoo.org/wiki/Handbook:AMD64/zh-cn)**。
