---
title: "Linux 页缓存写入型提权漏洞梳理：Copy Fail、DirtyFrag、Fragnesia 与 DirtyClone"
description: "梳理 2026 年 Copy Fail、DirtyFrag、Fragnesia 与 DirtyClone 的共同利用模型、不同根因、修复关系和 Gentoo 应对方式。"
date: 2026-06-27
tags: ["security", "kernel", "analysis"]
authors:
  - name: Zakk
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/zakkaus
---

2026 年 3 月至 6 月，研究人员陆续报告或公开了多组能够修改 Linux 文件页缓存的本地提权漏洞。Copy Fail、DirtyFrag、Fragnesia 和 DirtyClone 经常被放在一起讨论，因为它们都能把只读文件映射成内核中的写入目标，但它们不是同一个漏洞，也不共享完全相同的触发条件。

{{< callout type="important" >}}
Copy Fail 不属于 DirtyFrag 的同一根因：它发生在 AF_ALG；DirtyFrag、Fragnesia 和 DirtyClone 则集中在网络 skb、XFRM/ESP 或 RxRPC 路径。只缓解其中一条路径，不能证明其他路径也安全。
{{< /callout >}}

## 共同的利用结果

这些漏洞利用的共同点是 Linux 页缓存和零复制路径之间的内存共享：

1. 攻击者以只读方式打开 `/usr/bin/su` 等特权程序，使目标页面进入页缓存；
2. `splice()`、`vmsplice()` 或相关零复制路径让内核缓冲区继续引用同一物理页；
3. 加密或解密代码在原地写回数据，但没有先建立私有副本；
4. 页缓存中的可执行代码被修改，磁盘文件通常保持不变；
5. 再次执行目标程序时，内核使用已被修改的缓存页面，攻击者由此取得 root 权限。

这里的关键不是绕过文件权限直接写磁盘，而是让内核误把仍与只读文件共享的页面当成可写缓冲区。因为修改发生在内存中，磁盘完整性检查可能看不到变化。

这一共同模型分别见于 [Copy Fail 原始公告](https://copy.fail/)、[DirtyFrag 原始研究](https://github.com/V4bel/dirtyfrag)、[Fragnesia 原始研究](https://github.com/v12-security/pocs/tree/main/fragnesia)和 [JFrog 的 DirtyClone 分析](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)。

## 差异一览

| 名称 | CVE | 主要问题 | 旧内核的临时阻断方式 |
|---|---|---|---|
| Copy Fail | CVE-2026-31431 | AF_ALG `algif_aead` 原地操作 | 禁止 `algif_aead`，或用 seccomp 阻止 AF_ALG socket |
| DirtyFrag（ESP） | CVE-2026-43284 | UDP splice 分片未正确标记，ESP 对共享分片原地解密 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |
| DirtyFrag（RxRPC） | CVE-2026-43500 | RxRPC 未对外部共享分片建立私有副本 | 禁止 `rxrpc`；关闭 user namespace 单独无效 |
| Fragnesia | CVE-2026-46300 | `skb_try_coalesce()` 合并分片时丢失共享标志 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |
| DirtyClone | CVE-2026-43503 | 多个分片转移函数未传递共享标志 | 阻止取得 `CAP_NET_ADMIN`，或禁止 `esp4`、`esp6` |

更新内核始终是首选。表中的模块和 namespace 设置只适合无法立即更新的旧系统，而且必须结合实际内核配置验证是否生效。

## Copy Fail：AF_ALG 原地操作

Copy Fail（[CVE-2026-31431](https://www.cve.org/CVERecord?id=CVE-2026-31431)）位于内核加密接口 AF_ALG。`algif_aead` 曾对来自不同映射的源和目标执行原地操作，使与文件页缓存共享的页面进入可写目标 scatterlist。公开利用通过 AF_ALG、`splice()` 和 `authencesn` 构造受控写入，不需要网络连接、用户命名空间或 `CAP_NET_ADMIN`。[原始公告](https://copy.fail/)给出了利用条件、修复提交和披露时间线。

上游修复 [a664bf3d603d](https://git.kernel.org/linus/a664bf3d603dc3bdcf9ae47cc21e0daec706d7a5) 撤销了 2017 年引入的 `algif_aead` 原地优化，恢复源、目标分离。无法更新时可禁止模块：

```bash
printf '%s\n' 'install algif_aead /bin/false' > /etc/modprobe.d/disable-algif-aead.conf
modprobe -r algif_aead
```

对于容器、CI runner 等不受信任工作负载，还可以通过 seccomp 禁止创建 AF_ALG socket。该措施只覆盖 Copy Fail，不会阻止 DirtyFrag 的 ESP 或 RxRPC 路径。

## DirtyFrag：两条漏洞链在一起

根据[原始研究](https://github.com/V4bel/dirtyfrag)，DirtyFrag 不是单一 CVE，而是公开利用中串联的两条页缓存写入路径：

- **[CVE-2026-43284](https://www.cve.org/CVERecord?id=CVE-2026-43284)（XFRM/ESP）**：IPv4/IPv6 的 UDP splice 路径没有为外部共享分片设置 `SKBFL_SHARED_FRAG`，ESP 随后跳过写时复制并原地解密。
- **[CVE-2026-43500](https://www.cve.org/CVERecord?id=CVE-2026-43500)（RxRPC）**：RxRPC 过去只在 skb 已克隆时建立私有线性副本，没有覆盖仍持有外部共享分页分片的 skb。

ESP 路径写入能力强、模块普遍存在，但配置 XFRM 通常需要在网络命名空间中取得 `CAP_NET_ADMIN`。RxRPC 路径不要求创建 user namespace，却依赖系统提供并加载 `rxrpc` 模块。原始研究将两条路径组合，是为了覆盖不同发行版的默认配置，而不是因为两者必须同时触发。

两条主线修复分别是 [f4c50a4034e6](https://git.kernel.org/linus/f4c50a4034e62ab75f1d5cdd191dd5f9c77fdff4) 和 [aa54b1d27fe0](https://git.kernel.org/linus/aa54b1d27fe0c2b78e664a34fd0fdf7cd1960d71)。

## Fragnesia：合并 skb 时丢失标志

Fragnesia（[CVE-2026-46300](https://www.cve.org/CVERecord?id=CVE-2026-46300)）是独立的后续漏洞。`skb_try_coalesce()` 把来源 skb 的分页分片挂到目标 skb 时，没有同步 `SKBFL_SHARED_FRAG`。后续 ESP 代码因此认为目标 skb 没有共享分片，并在页缓存页面上原地解密。[V12 的原始说明](https://github.com/v12-security/pocs/tree/main/fragnesia)记录了利用模型、受影响条件和临时缓解。

公开利用使用 ESP-in-TCP：先把文件页面 splice 到 TCP 接收队列，再切换到 `espintcp` ULP 处理已有数据。攻击者在新建的 user/network namespace 中取得 `CAP_NET_ADMIN`，配置 XFRM 状态并控制 AES-GCM 参数，最终逐字节修改 `/usr/bin/su` 的页缓存副本。

## DirtyClone：标志在更多转移路径中丢失

DirtyClone 是 JFrog 对 [CVE-2026-43503](https://www.cve.org/CVERecord?id=CVE-2026-43503) 中 `__pskb_copy_fclone()` 利用变种的命名。按照 [JFrog 的技术分析](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)，攻击者使用 netfilter `TEE` 或等价的 `nf_dup_ipv4()` 路径复制数据包；复制后的 skb 继续引用文件页缓存，却没有保留共享分片标志。它随后进入 ESP 原地解密路径，形成受控写入。

CVE-2026-43503 的上游修复不只处理 `__pskb_copy_fclone()`，还覆盖 `skb_shift()`、`skb_segment()`、`skb_gro_receive()`、`skb_gro_receive_list()` 和 `tcp_clone_payload()` 等分片转移函数。主线提交为 [48f6a5356a33](https://git.kernel.org/linus/48f6a5356a33dd78e7144ae1faef95ffc990aae0)，5 月 21 日合并；首个包含修复的主线标签是 5 月 24 日发布的 v7.1-rc5。

详细的 Gentoo 更新和临时缓解命令参见：[Linux 内核 DirtyClone 本地提权漏洞：Gentoo 更新建议]({{< relref "/posts/2026-06-27-dirtyclone-kernel-lpe" >}})。

## 为什么修复会连续出现

最初的修复处理了会直接写入共享页面的加密路径，也开始使用 `SKBFL_SHARED_FRAG` 标记外部分片。后续研究发现，只要某个 skb 合并、复制或分片转移函数没有传递该标志，写入端仍可能把共享页面误判为私有页面。

因此这些补丁不是简单重复：DirtyFrag 修正初始标记和写入端检查，Fragnesia 修正合并路径，CVE-2026-43503 再补齐其他分片转移路径。JFrog 的结论是，只有应用整组已知修复，才能覆盖当前公开的利用模型。

## 披露与修复时间线

| 日期 | 事件 |
|---|---|
| 2026-03-23 | Copy Fail 报告给 Linux 内核安全团队 |
| 2026-04-01 | Copy Fail 修复进入主线 |
| 2026-04-22 | CVE-2026-31431 发布 |
| 2026-04-29 | Copy Fail 公开披露；DirtyFrag/RxRPC 的漏洞详情和补丁提交内核安全团队及 netdev |
| 2026-04-30 | DirtyFrag/ESP 的漏洞详情和初版补丁提交内核安全团队及 netdev |
| 2026-05-01 | CVE-2026-43500 在 Linux CNA 记录中预留 |
| 2026-05-04 | DirtyFrag/ESP 的 shared-frag 方案补丁提交 netdev；它后来成为最终合并的修复 |
| 2026-05-07 | DirtyFrag/ESP 修复 `f4c50a4034e6` 合并到 netdev；DirtyFrag 研究完整公开 |
| 2026-05-08 | `f4c50a4034e6` 合并到主线；CVE-2026-43284 发布 |
| 2026-05-10 | DirtyFrag 的 RxRPC 修复进入主线 |
| 2026-05-11 | CVE-2026-43500 发布 |
| 2026-05-13 | Fragnesia 披露并向 netdev 提交修复；该提交在主线 linux.git 中的 committer date 为 5 月 14 日 |
| 2026-05-16 | 覆盖多个分片转移函数的补丁写成并提交上游；这是 `48f6a5356a33` 的 author date |
| 2026-05-19 | Gentoo 发布内核公告；JFrog 报告独立发现的 `__pskb_copy_fclone()` 变种 |
| 2026-05-21 | CVE-2026-43503 修复合并到主线 |
| 2026-05-23 | CVE-2026-46300 与 CVE-2026-43503 发布 |
| 2026-05-24 | Linux v7.1-rc5 发布，成为首个包含 CVE-2026-43503 修复的主线标签 |
| 2026-06-25 | JFrog 发布 DirtyClone 完整分析 |

时间线分别依据 [Copy Fail 公告](https://copy.fail/)、[DirtyFrag 详细时间线](https://github.com/V4bel/dirtyfrag/blob/master/assets/write-up.md)、[Fragnesia 说明](https://github.com/v12-security/pocs/tree/main/fragnesia)、[JFrog 时间线](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/)、上游提交元数据和 Linux CNA 的 CVE 发布记录整理。

`f4c50a4034e6` 的补丁邮件头显示作者日期为 5 月 4 日、committer date 为 5 月 5 日，但这两个日期本身不是 netdev 或主线的合并日期。DirtyFrag 的详细时间线明确记录该补丁在 5 月 7 日进入 netdev、5 月 8 日进入主线。README 概述中“5 月 7 日公开时没有 patch 或 CVE”的注释与详细时间线所列的 4 月 30 日、5 月 4 日公开补丁不一致，因此本文以事件更完整、带有邮件列表及提交链接的详细时间线为准，不用该注释推导合并时间。

## 每个漏洞在哪个版本修复

下表按 Linux CNA 的 CVE JSON、上游提交元数据和原始研究整理。“上游修复记录”明确区分提交对象日期、子系统开发树和主线 linux.git；任何日期都不表示所有发行版从当天起自动安全，稳定分支和发行版仍需分别回移补丁。

| 漏洞 | 上游修复记录 | Linux CNA 的主线修复版本 | Linux CVE 记录中的稳定分支修复版本 |
|---|---|---|---|
| Copy Fail（CVE-2026-31431） | 2026-04-01 | 7.0 | 5.10.254、5.15.204、6.1.170、6.6.137、6.12.85、6.18.22、6.19.12 |
| DirtyFrag/ESP（CVE-2026-43284） | 2026-05-07 进入 netdev；5 月 8 日进入主线 | 7.1 | 5.10.255、5.15.205/206、6.1.171/172、6.6.138、6.12.87、6.18.28、7.0.5 |
| DirtyFrag/RxRPC（CVE-2026-43500） | 2026-05-10 | 7.1 | 6.6.140、6.12.88、6.18.29、7.0.6；5.10、5.15、6.1 没有列出官方稳定版修复下限 |
| Fragnesia（CVE-2026-46300） | 2026-05-13 披露并提交 netdev；该提交在主线 linux.git 中的 committer date 为 5 月 14 日 | 7.1 | 5.10.257、5.15.208、6.1.174、6.6.141、6.12.91、6.18.33、7.0.10 |
| DirtyClone（CVE-2026-43503） | 2026-05-16 提交；5 月 21 日合并；5 月 24 日发布首个修复标签 | 7.1；首个修复标签为 v7.1-rc5 | 5.10.257、5.15.208、6.1.174、6.6.141、6.12.91、6.18.33、7.0.10 |

CVE-2026-43284 的 Linux CVE 记录目前在 5.15 和 6.1 分支各列出两个连续修复版本，表中如实保留。使用这两个分支时应选择较新的 5.15.206、6.1.172 或更高版本，并继续检查发行版是否回移了 CVE-2026-43500。

## 哪个版本以后才覆盖整条漏洞链

如果使用未经发行版额外打补丁的上游稳定内核，必须同时满足五个 CVE。下表是将五份 Linux CNA 记录逐分支比较、取其中最晚修复下限后得到的结果；它是对官方版本数据的汇总计算，不是某一份 CVE 记录单独给出的整组结论：

| 上游分支 | 覆盖本文五个 CVE 的最低可确认版本 | 结论 |
|---|---|---|
| 5.10 | 无法只凭版本确认 | CVE-2026-43500 没有列出该分支的官方修复下限，必须核对发行版或自行回移的补丁 |
| 5.15 | 无法只凭版本确认 | 同上 |
| 6.1 | 无法只凭版本确认 | 同上 |
| 6.6 | 6.6.141 | 该版本及以后覆盖五个 CVE |
| 6.12 | 6.12.91 | 该版本及以后覆盖五个 CVE |
| 6.18 | 6.18.33 | 该版本及以后覆盖五个 CVE |
| 6.19 | 无法只凭版本确认 | Linux CNA 只为 Copy Fail 列出 6.19.12，后续四个 CVE 没有列出 6.19 稳定版修复下限；应迁移到受维护分支 |
| 7.0 | 7.0.10 | 该版本及以后覆盖五个 CVE |
| 7.1 | 7.1 | 正式版覆盖五个 CVE；CVE-2026-43503 从 v7.1-rc5 起已修复 |

{{< callout type="warning" >}}
不存在“某个日期以后编译的内核一定安全”这种判断方法。补丁在主线合并后，各稳定分支和发行版的回移时间不同；相反，发行版也可能在较旧的版本号上提前回移补丁。应同时检查内核分支、完整软件包版本和发行版安全状态。
{{< /callout >}}

## Gentoo 用户如何判断是否安全

判断整个漏洞链是否修复，不能只检查某一个 CVE，也不能只看内核主版本。发行版可能提前回移补丁，也可能保留同一版本号而增加修订后缀。

Gentoo 在 5 月 19 日的公告中说明，`sys-kernel/gentoo-kernel`、`sys-kernel/gentoo-kernel-bin` 和 `sys-kernel/gentoo-sources` 是安全支持范围，当时已经包含最新的 Fragnesia v5 补丁。6 月 27 日可用的受支持版本也已经达到 CVE-2026-43503 的上游修复版本。

截至 2026-06-27，可作为 Gentoo **已知受保护基线**的稳定软件包版本如下。“受保护”包括补丁修复，也包括 Gentoo 明确采用的功能停用缓解；不同架构的稳定关键字可能不同，应以本机 `emerge -pv` 的结果为准：

| 分支 | `gentoo-kernel` / `gentoo-kernel-bin` | `gentoo-sources` | 状态 |
|---|---|---|---|
| 5.10 | 不再列为安全基线 | 不再列为安全基线 | Gentoo 正在终止该分支的支持，计划于 2026-07-03 移除 |
| 5.15 | 不再列为安全基线 | 不再列为安全基线 | 同上 |
| 6.1 | 6.1.174_p1 | 6.1.174-r1 | CVE-2026-43503 已修复；Gentoo patchset 将 AF_RXRPC 标为 `BROKEN`，阻断缺少上游回移的 RxRPC 路径 |
| 6.6 | 6.6.141_p1 | 6.6.141-r1 | 当前稳定受保护基线 |
| 6.12 | 6.12.93 / 6.12.93-r1 | 6.12.93-r1 | 当前稳定受保护基线 |
| 6.18 | 6.18.35 / 6.18.35-r1 | 6.18.35-r1 | 当前稳定受保护基线 |

6.1 的处理可以在 `gentoo-kernel` / `gentoo-kernel-bin` 的 [6.1.174_p1 patchset](https://distfiles.gentoo.org/pub/proj/dist-kernel/patchsets/6.1/linux-gentoo-patches-6.1.174_p1.tar.xz)以及 `gentoo-sources` 的 [genpatches-6.1-190.base](https://distfiles.gentoo.org/pub/proj/kernel/genpatches/genpatches-6.1-190.base.tar.xz) 中核对：前者的 `0013-net-rxrpc-mark-AF_RXRPC-as-BROKEN-and-reverse-depend.patch` 和后者的 `1525_net-rxrpc-mark-AF_RXRPC-as-BROKEN.patch` 都将 AF_RXRPC 标记为 `BROKEN`。这是一项缓解，不应写成已经回移 CVE-2026-43500 的修复代码。

其他版本信息来自 Gentoo 软件包数据库：[gentoo-kernel](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel)、[gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin)和 [gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources)。这里列的是 6 月 27 日仓库中的已知受保护稳定基线，不是永久固定的推荐版本。用户应同步仓库、更新到当前可用版本并重启，而不是继续停留在表中的最低版本或依赖临时 workaround。

测试分支方面，7.0.12 及以上的 `gentoo-kernel` / `gentoo-kernel-bin` / `gentoo-sources` 已超过上游 7.0.10 的完整修复下限；`gentoo-sources` 7.1.x 也包含整组修复。这些版本在 6 月 27 日仍使用 `~arch` 关键字，不应与稳定分支混为一谈。

`sys-kernel/vanilla-sources` 不在 Gentoo 安全支持范围内。自行配置的内核、其他内核软件包或自行挑选补丁的用户，应分别核对以下五个 CVE：

- CVE-2026-31431
- CVE-2026-43284
- CVE-2026-43500
- CVE-2026-46300
- CVE-2026-43503

尤其要注意：CVE-2026-43500 的官方稳定分支回移范围与其他漏洞不同，不能仅凭 CVE-2026-43503 的修复版本推断整个漏洞链已经补齐。

## 参考资料

- [Copy Fail（CVE-2026-31431）](https://copy.fail/)
- [Dirty Frag: Universal Linux LPE](https://github.com/V4bel/dirtyfrag)
- [Fragnesia（CVE-2026-46300）](https://github.com/v12-security/pocs/tree/main/fragnesia)
- [Dissecting and Exploiting Linux LPE Variant: DirtyClone](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/) — JFrog Security Research
- [Copy Fail, Dirty Frag, and Fragnesia kernel vulnerabilities](https://www.gentoo.org/news/2026/05/19/copy-fail-fragnesia-vulnerabilities.html) — Gentoo Linux
- [Gentoo Distribution Kernel 文档](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)
- [kmod 的 modprobe.d 与 modprobe 官方手册](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd) / [modprobe.8.scd](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.8.scd)
- Linux CNA CVE JSON：[CVE-2026-31431](https://cveawg.mitre.org/api/cve/CVE-2026-31431) / [CVE-2026-43284](https://cveawg.mitre.org/api/cve/CVE-2026-43284) / [CVE-2026-43500](https://cveawg.mitre.org/api/cve/CVE-2026-43500) / [CVE-2026-46300](https://cveawg.mitre.org/api/cve/CVE-2026-46300) / [CVE-2026-43503](https://cveawg.mitre.org/api/cve/CVE-2026-43503)
