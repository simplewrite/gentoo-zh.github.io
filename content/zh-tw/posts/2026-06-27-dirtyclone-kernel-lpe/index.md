---
title: "Linux 核心 DirtyClone 本地提權漏洞：Gentoo 更新建議"
description: "DirtyClone（CVE-2026-43503，CVSS 8.8）可讓本地攻擊者篡改只讀檔案的頁快取並提權。Gentoo 受支援核心已有修復，使用者應更新並重啟。"
date: 2026-06-27
tags: ["security", "announcement", "kernel"]
authors:
  - name: Zakk
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/zakkaus
  - name: Clover（審校）
    image: /contributors/simplewrite/feature.webp
    link: https://github.com/simpleWrite
---

JFrog 安全研究團隊於 2026 年 6 月 25 日公開了 Linux 核心本地提權利用 **DirtyClone**。它利用 [CVE-2026-43503](https://cveawg.mitre.org/api/cve/CVE-2026-43503) 中 socket buffer（skb）共享分片標誌傳遞不完整的問題，可將原本只讀的檔案頁快取變成核心中的寫入目標。該漏洞的 CVSS v3.1 評分為 8.8。

{{< callout type="important" >}}
截至 2026-06-27，Gentoo 目前提供的受支援核心版本已經包含 CVE-2026-43503 的上游修復。**更新核心軟體包後需要重啟才能切換到新版本；舊核心仍在執行期間不受保護。**
{{< /callout >}}

## 修復方案

Gentoo 對以下三個核心軟體包提供安全支援：

| 軟體包名稱 | 目前狀態 |
|---|---|
| `sys-kernel/gentoo-kernel` | 目前版本已覆蓋上游修復 |
| `sys-kernel/gentoo-kernel-bin` | 目前版本已覆蓋上游修復 |
| `sys-kernel/gentoo-sources` | 目前版本已覆蓋上游修復 |

`sys-kernel/vanilla-sources` 不在 Gentoo 安全支援範圍內。

先同步倉庫，再更新自己正在使用的核心軟體包。Gentoo 的 [Distribution Kernel 文件](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)說明，這類核心透過 Portage 安裝並隨軟體包更新。下面以預編譯核心為例；使用其他受支援核心時替換軟體包名稱：

```bash
emerge --sync
emerge --ask --update sys-kernel/gentoo-kernel-bin
```

`gentoo-kernel` 和 `gentoo-kernel-bin` 使用者應確認新核心已經安裝並由載入程式選中。`gentoo-sources` 使用者還需要按自己的配置重新編譯和安裝核心。隨後重啟，並確認實際執行的版本：

```bash
uname -r
```

Linux CNA 記錄列出的各穩定分支修復下限如下；主線方面，JFrog 記錄的首個修復標籤是 v7.1-rc5，Linux CNA 列出的正式修復版本是 7.1。使用自行配置的核心或不受 Gentoo 支援的核心軟體包時，可據此檢查：

| 核心分支 | 首個修復版本 |
|---|---|
| 5.10 | 5.10.257 |
| 5.15 | 5.15.208 |
| 6.1 | 6.1.174 |
| 6.6 | 6.6.141 |
| 6.12 | 6.12.91 |
| 6.18 | 6.18.33 |
| 7.0 | 7.0.10 |
| 7.1 | v7.1-rc5；正式版為 7.1 |

{{< callout type="warning" >}}
Gentoo 已宣佈正在終止對 5.10 和 5.15 分支的支援，並計劃於 2026-07-03 從倉庫移除相關包。仍在使用這些分支的使用者應遷移到受支援的新 LTS 分支。
{{< /callout >}}

## 漏洞影響

成功利用需要同時具備以下條件：

- 系統執行缺少完整修復的核心；
- 攻擊者能夠在本機執行程式碼；
- 攻擊者擁有或能夠在使用者/網路名稱空間中取得 `CAP_NET_ADMIN`；
- 核心允許攻擊者配置所需的 XFRM/IPsec 和資料包（packet）複製路徑。

非特權使用者名稱空間常被用來取得網路名稱空間內的 `CAP_NET_ADMIN`，因此啟用該功能的主機風險更高。允許不受信任工作負載建立使用者和網路名稱空間，或向容器授予網路管理能力的多租戶與容器環境，也應優先更新。

JFrog 的利用會讓 IPsec 對檔案頁快取執行原地解密，從而修改記憶體中的特權程式，例如 `/usr/bin/su`。磁碟檔案本身不會改變，常規的磁碟完整性檢查可能無法發現攻擊；研究人員也沒有觀察到相應的核心日誌或審計記錄。

## 技術原因

`SKBFL_SHARED_FRAG` 表示 skb 的分片引用了由外部持有或與其他物件共享的記憶體。後續程式碼準備原地寫入時，應根據這個標誌先執行寫時複製，避免修改仍與檔案頁快取共享的物理頁。

CVE-2026-43503 修復前，`__pskb_copy_fclone()`、`skb_shift()`、`skb_gro_receive()`、`skb_gro_receive_list()`、`skb_segment()` 和 `tcp_clone_payload()` 等分片轉移路徑沒有完整傳遞該標誌。複製後的 skb 仍引用相同頁面，卻被錯誤報告為沒有共享分片。攻擊者可借助資料包（packet）複製路徑將這樣的 skb 送入 ESP 原地解密流程，最終寫入只讀檔案的頁快取。

該修復提交的 author date 是 5 月 16 日，5 月 21 日由網路子系統維護者合併；包含該提交的首個主線標籤是 5 月 24 日釋出的 Linux v7.1-rc5。CVE 於 5 月 23 日公開，JFrog 於 6 月 25 日釋出完整分析。

## 緩解方案

以下措施只用於暫時阻斷公開的 DirtyClone 利用路徑，不能替代核心更新。所有命令需要以 root 身份執行（`sudo su` 或在每條命令前加 `sudo`）。

### 禁止建立新的使用者名稱空間

Gentoo 可以使用 Linux 官方 [`max_user_namespaces`](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/user.html#max-user-namespaces) 引數，臨時設定並寫入持久配置：

```bash
sysctl -w user.max_user_namespaces=0
printf '%s\n' 'user.max_user_namespaces=0' > /etc/sysctl.d/99-disable-userns.conf
```

`sysctl -w` 執行時會直接輸出確認行：

```
user.max_user_namespaces = 0
```

確認當前值和持久配置均已生效：

```bash
sysctl user.max_user_namespaces
# user.max_user_namespaces = 0

cat /etc/sysctl.d/99-disable-userns.conf
# user.max_user_namespaces=0
```

這會把當前使用者名稱空間中任一使用者可新建的使用者名稱空間數量設為 0；在宿主機的初始使用者名稱空間中執行時，也會限制特權程序。已經存在的名稱空間不會因此消失；如果依賴這項措施臨時防護，建議寫入持久配置後在維護視窗重啟。依賴使用者名稱空間的程式和沙盒可能受到影響。

這項措施只阻止一般本地使用者透過新建使用者名稱空間取得 `CAP_NET_ADMIN`。它不能防護已經持有該 capability 的程式、特權容器或既有使用者名稱空間中的攻擊者，也不能阻斷不依賴使用者名稱空間的 Copy Fail 和 DirtyFrag/RxRPC 路徑；這類環境必須更新核心，或確認相應模組已被有效阻斷。

部分 Debian/Ubuntu 核心另有 `kernel.unprivileged_userns_clone` 引數，它不是通用的上游或 Gentoo 核心介面。

### 阻斷相關核心模組

不使用 IPsec 或 RxRPC 的系統可以阻止相關模組載入，並解除安裝已經載入的模組。對 DirtyClone 本身，關鍵是 `esp4`/`esp6`；`rxrpc` 對應的是較早的 DirtyFrag/RxRPC（CVE-2026-43500）路徑：

```bash
mkdir -p /etc/modprobe.d
printf '%s\n' \
  'install esp4 /bin/false' \
  'install esp6 /bin/false' \
  'install rxrpc /bin/false' \
  > /etc/modprobe.d/block-dirtyfrag.conf

modprobe -r esp4 esp6 rxrpc

for module in esp4 esp6 rxrpc; do
  test ! -d "/sys/module/$module" || echo "$module is still active"
done
```

根據 kmod 官方手冊，`modprobe.d` 的 [`install` 指令](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd)會用指定命令替代正常模組載入，`modprobe` 的 [`-r` 引數](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.8.scd)用於解除安裝模組。不要忽略解除安裝錯誤或檢查命令的輸出。如果模組正在使用、已經編入核心，或由 initramfs 提前載入，這項措施不會完整生效；配置還需要進入 initramfs，或改用禁止使用者名稱空間或更新核心。遮蔽 `esp4`/`esp6` 會停用相應的 IPv4/IPv6 ESP 功能並影響依賴它們的 IPsec 連線。

### 更新核心後撤銷緩解措施

完成核心更新並重啟到新版本後，可以移除臨時配置並恢復預設值：

```bash
rm /etc/modprobe.d/block-dirtyfrag.conf
rm /etc/sysctl.d/99-disable-userns.conf
sysctl -w user.max_user_namespaces=2147483647
```

移除 modprobe.d 配置後，`esp4`/`esp6`/`rxrpc` 恢復按需載入，無需手動執行 `modprobe`。`sysctl -w` 立即恢復 user namespace 限制；`2147483647` 是該引數的核心預設值。

## 與早期漏洞的關係

DirtyClone 延續了 DirtyFrag 的頁快取寫入手法，但 Copy Fail、DirtyFrag 的兩條路徑和 Fragnesia 各有不同根因，臨時阻斷方式也不能互換。參見背景文章：[Linux 頁快取寫入型提權漏洞梳理：Copy Fail、DirtyFrag、Fragnesia 與 DirtyClone]({{< relref "/posts/2026-06-27-linux-page-cache-lpe" >}})。

Gentoo 於 5 月 19 日公告，受支援核心當時已經包含最新的 Fragnesia v5 補丁。該公告早於 DirtyClone 修復，不能單獨說明 CVE-2026-43503 的狀態；本文以 Linux CVE 記錄和 Gentoo 在 6 月 27 日提供的核心版本為準。

## 參考資料

- [Linux CNA 的 CVE-2026-43503 JSON 記錄](https://cveawg.mitre.org/api/cve/CVE-2026-43503)
- [上游修復提交 48f6a5356a33](https://git.kernel.org/linus/48f6a5356a33dd78e7144ae1faef95ffc990aae0)
- [Dissecting and Exploiting Linux LPE Variant: DirtyClone](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/) — JFrog Security Research
- [Ubuntu CVE-2026-43503](https://ubuntu.com/security/CVE-2026-43503)
- [Copy Fail, Dirty Frag, and Fragnesia kernel vulnerabilities](https://www.gentoo.org/news/2026/05/19/copy-fail-fragnesia-vulnerabilities.html) — Gentoo Linux
- [Gentoo 核心軟體包版本：gentoo-kernel](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel) / [gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin) / [gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources)
- [Gentoo Distribution Kernel 文件](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)
- [Linux user sysctl 文件](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/user.html)
- [Copy Fail（CVE-2026-31431）](https://copy.fail/)
