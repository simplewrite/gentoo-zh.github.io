---
title: "Linux 頁快取寫入型提權漏洞梳理：Copy Fail、DirtyFrag、Fragnesia 與 DirtyClone"
description: "梳理 2026 年 Copy Fail、DirtyFrag、Fragnesia 與 DirtyClone 的共同利用模型、不同根因、修復關係和 Gentoo 應對方式。"
date: 2026-06-27
tags: ["security", "kernel", "analysis"]
authors:
  - name: Zakk
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/zakkaus
---

2026 年 3 月至 6 月，研究人員陸續報告或公開了多組能夠修改 Linux 檔案頁快取的本地提權漏洞。Copy Fail、DirtyFrag、Fragnesia 和 DirtyClone 經常被放在一起討論，因為它們都能把只讀檔案對映成核心中的寫入目標，但它們不是同一個漏洞，也不共享完全相同的觸發條件。

{{< callout type="important" >}}
Copy Fail 不屬於 DirtyFrag 的同一根因：它發生在 AF_ALG；DirtyFrag、Fragnesia 和 DirtyClone 則集中在網路 skb、XFRM/ESP 或 RxRPC 路徑。只緩解其中一條路徑，不能證明其他路徑也安全。
{{< /callout >}}

## 共同的利用結果

這些漏洞利用的共同點是 Linux 頁快取和零複製路徑之間的記憶體共享：

1. 攻擊者以只讀方式開啟 `/usr/bin/su` 等特權程式，使目標頁面進入頁快取；
2. `splice()`、`vmsplice()` 或相關零複製路徑讓核心緩衝區繼續引用同一物理頁；
3. 加密或解密程式碼在原地寫回資料，但沒有先建立私有副本；
4. 頁快取中的可執行程式碼被修改，磁碟檔案通常保持不變；
5. 再次執行目標程式時，核心使用已被修改的快取頁面，攻擊者由此取得 root 權限。

這裡的關鍵不是繞過檔案權限直接寫磁碟，而是讓核心誤把仍與只讀檔案共享的頁面當成可寫緩衝區。因為修改發生在記憶體中，磁碟完整性檢查可能看不到變化。

這一共同模型分別見於 [Copy Fail 原始公告](https://copy.fail/)、[DirtyFrag 原始研究](https://github.com/V4bel/dirtyfrag)、[Fragnesia 原始研究](https://github.com/v12-security/pocs/tree/main/fragnesia)和 [JFrog 的 DirtyClone 分析](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)。

## 差異一覽

| 名稱 | CVE | 主要問題 | 舊核心的臨時阻斷方式 |
|---|---|---|---|
| Copy Fail | CVE-2026-31431 | AF_ALG `algif_aead` 原地操作 | 禁止 `algif_aead`，或用 seccomp 阻止 AF_ALG socket |
| DirtyFrag（ESP） | CVE-2026-43284 | UDP splice 分片未正確標記，ESP 對共享分片原地解密 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |
| DirtyFrag（RxRPC） | CVE-2026-43500 | RxRPC 未對外部共享分片建立私有副本 | 禁止 `rxrpc`；關閉 user namespace 單獨無效 |
| Fragnesia | CVE-2026-46300 | `skb_try_coalesce()` 合併分片時丟失共享旗標 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |
| DirtyClone | CVE-2026-43503 | 多個分片轉移函式未傳遞共享旗標 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |

更新核心始終是首選。表中的模組和 namespace 設定只適合無法立即更新的舊系統，而且必須結合實際核心配置驗證是否生效。

## Copy Fail：AF_ALG 原地操作

Copy Fail（[CVE-2026-31431](https://www.cve.org/CVERecord?id=CVE-2026-31431)）位於核心加密介面 AF_ALG。`algif_aead` 曾對來自不同對映的源和目標執行原地操作，使與檔案頁快取共享的頁面進入可寫目標 scatterlist。公開利用透過 AF_ALG、`splice()` 和 `authencesn` 構造受控寫入，不需要網路連線、使用者名稱空間或 `CAP_NET_ADMIN`。[原始公告](https://copy.fail/)給出了利用條件、修復提交和披露時間線。

上游修復 [a664bf3d603d](https://git.kernel.org/linus/a664bf3d603dc3bdcf9ae47cc21e0daec706d7a5) 撤銷了 2017 年引入的 `algif_aead` 原地最佳化，恢復源、目標分離。無法更新時可禁止模組：

```bash
printf '%s\n' 'install algif_aead /bin/false' > /etc/modprobe.d/disable-algif-aead.conf
modprobe -r algif_aead
```

對於容器、CI runner 等不受信任工作負載，還可以透過 seccomp 禁止建立 AF_ALG socket。該措施只覆蓋 Copy Fail，不會阻止 DirtyFrag 的 ESP 或 RxRPC 路徑。

## DirtyFrag：兩條漏洞鏈在一起

根據[原始研究](https://github.com/V4bel/dirtyfrag)，DirtyFrag 不是單一 CVE，而是公開利用中串聯的兩條頁快取寫入路徑：

- **[CVE-2026-43284](https://www.cve.org/CVERecord?id=CVE-2026-43284)（XFRM/ESP）**：IPv4/IPv6 的 UDP splice 路徑沒有為外部共享分片設定 `SKBFL_SHARED_FRAG`，ESP 隨後跳過寫時複製並原地解密。
- **[CVE-2026-43500](https://www.cve.org/CVERecord?id=CVE-2026-43500)（RxRPC）**：RxRPC 過去只在 skb 已克隆時建立私有線性副本，沒有覆蓋仍持有外部共享分頁分片的 skb。

ESP 路徑寫入能力強、模組普遍存在，但配置 XFRM 通常需要在網路名稱空間中取得 `CAP_NET_ADMIN`。RxRPC 路徑不要求建立 user namespace，卻依賴系統提供並載入 `rxrpc` 模組。原始研究將兩條路徑組合，是為了覆蓋不同發行版的預設配置，而不是因為兩者必須同時觸發。

兩條主線修復分別是 [f4c50a4034e6](https://git.kernel.org/linus/f4c50a4034e62ab75f1d5cdd191dd5f9c77fdff4) 和 [aa54b1d27fe0](https://git.kernel.org/linus/aa54b1d27fe0c2b78e664a34fd0fdf7cd1960d71)。

## Fragnesia：合併 skb 時丟失旗標

Fragnesia（[CVE-2026-46300](https://www.cve.org/CVERecord?id=CVE-2026-46300)）是獨立的後續漏洞。`skb_try_coalesce()` 把來源 skb 的分頁分片掛到目標 skb 時，沒有同步 `SKBFL_SHARED_FRAG`。後續 ESP 程式碼因此認為目標 skb 沒有共享分片，並在頁快取頁面上原地解密。[V12 的原始說明](https://github.com/v12-security/pocs/tree/main/fragnesia)記錄了利用模型、受影響條件和臨時緩解。

公開利用使用 ESP-in-TCP：先把檔案頁面 splice 到 TCP 接收佇列，再切換到 `espintcp` ULP 處理已有資料。攻擊者在新建的 user/network namespace 中取得 `CAP_NET_ADMIN`，配置 XFRM 狀態並控制 AES-GCM 引數，最終逐位元組修改 `/usr/bin/su` 的頁快取副本。

## DirtyClone：旗標在更多轉移路徑中丟失

DirtyClone 是 JFrog 對 [CVE-2026-43503](https://www.cve.org/CVERecord?id=CVE-2026-43503) 中 `__pskb_copy_fclone()` 利用變種的命名。按照 [JFrog 的技術分析](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)，攻擊者使用 netfilter `TEE` 或等價的 `nf_dup_ipv4()` 路徑複製資料包；複製後的 skb 繼續引用檔案頁快取，卻沒有保留共享分片旗標。它隨後進入 ESP 原地解密路徑，形成受控寫入。

CVE-2026-43503 的上游修復不只處理 `__pskb_copy_fclone()`，還覆蓋 `skb_shift()`、`skb_segment()`、`skb_gro_receive()`、`skb_gro_receive_list()` 和 `tcp_clone_payload()` 等分片轉移函式。主線提交為 [48f6a5356a33](https://git.kernel.org/linus/48f6a5356a33dd78e7144ae1faef95ffc990aae0)，5 月 21 日合併；首個包含修復的主線標籤是 5 月 24 日釋出的 v7.1-rc5。

詳細的 Gentoo 更新和臨時緩解指令參見：[Linux 核心 DirtyClone 本地提權漏洞：Gentoo 更新建議]({{< relref "/posts/2026-06-27-dirtyclone-kernel-lpe" >}})。

## 為什麼修復會連續出現

最初的修復處理了會直接寫入共享頁面的加密路徑，也開始使用 `SKBFL_SHARED_FRAG` 標記外部分片。後續研究發現，只要某個 skb 合併、複製或分片轉移函式沒有傳遞該旗標，寫入端仍可能把共享頁面誤判為私有頁面。

因此這些修補不是簡單重複：DirtyFrag 修正初始標記和寫入端檢查，Fragnesia 修正合併路徑，CVE-2026-43503 再補齊其他分片轉移路徑。JFrog 的結論是，只有應用整組已知修復，才能覆蓋當前公開的利用模型。

## 披露與修復時間線

| 日期 | 事件 |
|---|---|
| 2026-03-23 | Copy Fail 報告給 Linux 核心安全團隊 |
| 2026-04-01 | Copy Fail 修復進入主線 |
| 2026-04-22 | CVE-2026-31431 釋出 |
| 2026-04-29 | Copy Fail 公開披露；DirtyFrag/RxRPC 的漏洞詳情和修補提交核心安全團隊及 netdev |
| 2026-04-30 | DirtyFrag/ESP 的漏洞詳情和初版修補提交核心安全團隊及 netdev |
| 2026-05-01 | CVE-2026-43500 在 Linux CNA 記錄中預留 |
| 2026-05-04 | DirtyFrag/ESP 的 shared-frag 方案修補提交 netdev；它後來成為最終合併的修復 |
| 2026-05-07 | DirtyFrag/ESP 修復 `f4c50a4034e6` 合併到 netdev；DirtyFrag 研究完整公開 |
| 2026-05-08 | `f4c50a4034e6` 合併到主線；CVE-2026-43284 釋出 |
| 2026-05-10 | DirtyFrag 的 RxRPC 修復進入主線 |
| 2026-05-11 | CVE-2026-43500 釋出 |
| 2026-05-13 | Fragnesia 披露並向 netdev 提交修復；該提交在主線 linux.git 中的 committer date 為 5 月 14 日 |
| 2026-05-16 | 覆蓋多個分片轉移函式的修補寫成並提交上游；這是 `48f6a5356a33` 的 author date |
| 2026-05-19 | Gentoo 釋出核心公告；JFrog 報告獨立發現的 `__pskb_copy_fclone()` 變種 |
| 2026-05-21 | CVE-2026-43503 修復合併到主線 |
| 2026-05-23 | CVE-2026-46300 與 CVE-2026-43503 釋出 |
| 2026-05-24 | Linux v7.1-rc5 釋出，成為首個包含 CVE-2026-43503 修復的主線標籤 |
| 2026-06-25 | JFrog 釋出 DirtyClone 完整分析 |

時間線分別依據 [Copy Fail 公告](https://copy.fail/)、[DirtyFrag 詳細時間線](https://github.com/V4bel/dirtyfrag/blob/master/assets/write-up.md)、[Fragnesia 說明](https://github.com/v12-security/pocs/tree/main/fragnesia)、[JFrog 時間線](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)、上游提交後設資料和 Linux CNA 的 CVE 釋出記錄整理。

`f4c50a4034e6` 的修補郵件頭顯示作者日期為 5 月 4 日、committer date 為 5 月 5 日，但這兩個日期本身不是 netdev 或主線的合併日期。DirtyFrag 的詳細時間線明確記錄該修補在 5 月 7 日進入 netdev、5 月 8 日進入主線。README 概述中“5 月 7 日公開時沒有 patch 或 CVE”的註釋與詳細時間線所列的 4 月 30 日、5 月 4 日公開修補不一致，因此本文以事件更完整、帶有郵件列表及提交連結的詳細時間線為準，不用該註釋推導合併時間。

## 每個漏洞在哪個版本修復

下表按 Linux CNA 的 CVE JSON、上游提交後設資料和原始研究整理。“上游修復記錄”明確區分提交物件日期、子系統開發樹和主線 linux.git；任何日期都不表示所有發行版從當天起自動安全，穩定分支和發行版仍需分別回移修補。

| 漏洞 | 上游修復記錄 | Linux CNA 的主線修復版本 | Linux CVE 記錄中的穩定分支修復版本 |
|---|---|---|---|
| Copy Fail（CVE-2026-31431） | 2026-04-01 | 7.0 | 5.10.254、5.15.204、6.1.170、6.6.137、6.12.85、6.18.22、6.19.12 |
| DirtyFrag/ESP（CVE-2026-43284） | 2026-05-07 進入 netdev；5 月 8 日進入主線 | 7.1 | 5.10.255、5.15.205/206、6.1.171/172、6.6.138、6.12.87、6.18.28、7.0.5 |
| DirtyFrag/RxRPC（CVE-2026-43500） | 2026-05-10 | 7.1 | 6.6.140、6.12.88、6.18.29、7.0.6；5.10、5.15、6.1 沒有列出官方穩定版修復下限 |
| Fragnesia（CVE-2026-46300） | 2026-05-13 披露並提交 netdev；該提交在主線 linux.git 中的 committer date 為 5 月 14 日 | 7.1 | 5.10.257、5.15.208、6.1.174、6.6.141、6.12.91、6.18.33、7.0.10 |
| DirtyClone（CVE-2026-43503） | 2026-05-16 提交；5 月 21 日合併；5 月 24 日釋出首個修復標籤 | 7.1；首個修復標籤為 v7.1-rc5 | 5.10.257、5.15.208、6.1.174、6.6.141、6.12.91、6.18.33、7.0.10 |

CVE-2026-43284 的 Linux CVE 記錄目前在 5.15 和 6.1 分支各列出兩個連續修復版本，表中如實保留。使用這兩個分支時應選擇較新的 5.15.206、6.1.172 或更高版本，並繼續檢查發行版是否回移了 CVE-2026-43500。

## 哪個版本以後才覆蓋整條漏洞鏈

如果使用未經發行版額外打修補的上游穩定核心，必須同時滿足五個 CVE。下表是將五份 Linux CNA 記錄逐分支比較、取其中最晚修復下限後得到的結果；它是對官方版本資料的彙總計算，不是某一份 CVE 記錄單獨給出的整組結論：

| 上游分支 | 覆蓋本文五個 CVE 的最低可確認版本 | 結論 |
|---|---|---|
| 5.10 | 無法只憑版本確認 | CVE-2026-43500 沒有列出該分支的官方修復下限，必須核對發行版或自行回移的修補 |
| 5.15 | 無法只憑版本確認 | 同上 |
| 6.1 | 無法只憑版本確認 | 同上 |
| 6.6 | 6.6.141 | 該版本及以後覆蓋五個 CVE |
| 6.12 | 6.12.91 | 該版本及以後覆蓋五個 CVE |
| 6.18 | 6.18.33 | 該版本及以後覆蓋五個 CVE |
| 6.19 | 無法只憑版本確認 | Linux CNA 只為 Copy Fail 列出 6.19.12，後續四個 CVE 沒有列出 6.19 穩定版修復下限；應遷移到受維護分支 |
| 7.0 | 7.0.10 | 該版本及以後覆蓋五個 CVE |
| 7.1 | 7.1 | 正式版覆蓋五個 CVE；CVE-2026-43503 從 v7.1-rc5 起已修復 |

{{< callout type="warning" >}}
不存在“某個日期以後編譯的核心一定安全”這種判斷方法。修補在主線合併後，各穩定分支和發行版的回移時間不同；相反，發行版也可能在較舊的版本號上提前回移修補。應同時檢查核心分支、完整軟體套件版本和發行版安全狀態。
{{< /callout >}}

## Gentoo 使用者如何判斷是否安全

判斷整個漏洞鏈是否修復，不能只檢查某一個 CVE，也不能只看核心主版本。發行版可能提前回移修補，也可能保留同一版本號而增加修訂字尾。

Gentoo 在 5 月 19 日的公告中說明，`sys-kernel/gentoo-kernel`、`sys-kernel/gentoo-kernel-bin` 和 `sys-kernel/gentoo-sources` 是安全支援範圍，當時已經包含最新的 Fragnesia v5 修補。6 月 27 日可用的受支援版本也已經達到 CVE-2026-43503 的上游修復版本。

截至 2026-06-27，可作為 Gentoo **已知受保護基線**的穩定軟體套件版本如下。“受保護”包括修補修復，也包括 Gentoo 明確採用的功能停用緩解；不同架構的穩定關鍵字可能不同，應以本機 `emerge -pv` 的結果為準：

| 分支 | `gentoo-kernel` / `gentoo-kernel-bin` | `gentoo-sources` | 狀態 |
|---|---|---|---|
| 5.10 | 不再列為安全基線 | 不再列為安全基線 | Gentoo 正在終止該分支的支援，計劃於 2026-07-03 移除 |
| 5.15 | 不再列為安全基線 | 不再列為安全基線 | 同上 |
| 6.1 | 6.1.174_p1 | 6.1.174-r1 | CVE-2026-43503 已修復；Gentoo patchset 將 AF_RXRPC 標為 `BROKEN`，阻斷缺少上游回移的 RxRPC 路徑 |
| 6.6 | 6.6.141_p1 | 6.6.141-r1 | 當前穩定受保護基線 |
| 6.12 | 6.12.93 / 6.12.93-r1 | 6.12.93-r1 | 當前穩定受保護基線 |
| 6.18 | 6.18.35 / 6.18.35-r1 | 6.18.35-r1 | 當前穩定受保護基線 |

6.1 的處理可以在 `gentoo-kernel` / `gentoo-kernel-bin` 的 [6.1.174_p1 patchset](https://distfiles.gentoo.org/pub/proj/dist-kernel/patchsets/6.1/linux-gentoo-patches-6.1.174_p1.tar.xz)以及 `gentoo-sources` 的 [genpatches-6.1-190.base](https://distfiles.gentoo.org/pub/proj/kernel/genpatches/genpatches-6.1-190.base.tar.xz) 中核對：前者的 `0013-net-rxrpc-mark-AF_RXRPC-as-BROKEN-and-reverse-depend.patch` 和後者的 `1525_net-rxrpc-mark-AF_RXRPC-as-BROKEN.patch` 都將 AF_RXRPC 標記為 `BROKEN`。這是一項緩解，不應寫成已經回移 CVE-2026-43500 的修復程式碼。

其他版本資訊來自 Gentoo 軟體套件資料庫：[gentoo-kernel](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel)、[gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin)和 [gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources)。這裡列的是 6 月 27 日倉庫中的已知受保護穩定基線，不是永久固定的推薦版本。使用者應同步倉庫、更新到當前可用版本並重啟，而不是繼續停留在表中的最低版本或依賴臨時 workaround。

測試分支方面，7.0.12 及以上的 `gentoo-kernel` / `gentoo-kernel-bin` / `gentoo-sources` 已超過上游 7.0.10 的完整修復下限；`gentoo-sources` 7.1.x 也包含整組修復。這些版本在 6 月 27 日仍使用 `~arch` 關鍵字，不應與穩定分支混為一談。

`sys-kernel/vanilla-sources` 不在 Gentoo 安全支援範圍內。自行配置的核心、其他核心軟體套件或自行挑選修補的使用者，應分別核對以下五個 CVE：

- CVE-2026-31431
- CVE-2026-43284
- CVE-2026-43500
- CVE-2026-46300
- CVE-2026-43503

尤其要注意：CVE-2026-43500 的官方穩定分支回移範圍與其他漏洞不同，不能僅憑 CVE-2026-43503 的修復版本推斷整個漏洞鏈已經補齊。

## 參考資料

- [Copy Fail（CVE-2026-31431）](https://copy.fail/)
- [Dirty Frag: Universal Linux LPE](https://github.com/V4bel/dirtyfrag)
- [Fragnesia（CVE-2026-46300）](https://github.com/v12-security/pocs/tree/main/fragnesia)
- [Dissecting and Exploiting Linux LPE Variant: DirtyClone](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/) — JFrog Security Research
- [Copy Fail, Dirty Frag, and Fragnesia kernel vulnerabilities](https://www.gentoo.org/news/2026/05/19/copy-fail-fragnesia-vulnerabilities.html) — Gentoo Linux
- [Gentoo Distribution Kernel 文件](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)
- [kmod 的 modprobe.d 與 modprobe 官方手冊](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd) / [modprobe.8.scd](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.8.scd)
- Linux CNA CVE JSON：[CVE-2026-31431](https://cveawg.mitre.org/api/cve/CVE-2026-31431) / [CVE-2026-43284](https://cveawg.mitre.org/api/cve/CVE-2026-43284) / [CVE-2026-43500](https://cveawg.mitre.org/api/cve/CVE-2026-43500) / [CVE-2026-46300](https://cveawg.mitre.org/api/cve/CVE-2026-46300) / [CVE-2026-43503](https://cveawg.mitre.org/api/cve/CVE-2026-43503)
