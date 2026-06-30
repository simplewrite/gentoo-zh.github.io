---
title: "Linux 内核 DirtyClone 本地提权漏洞：Gentoo 更新建议"
description: "DirtyClone（CVE-2026-43503，CVSS 8.8）可让本地攻击者篡改只读文件的页缓存并提权。Gentoo 受支持内核已有修复，用户应更新并重启。"
date: 2026-06-27
tags: ["security", "announcement", "kernel"]
authors:
  - name: Zakk
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/zakkaus
  - name: Clover（审校）
    image: /contributors/simplewrite/feature.webp
    link: https://github.com/simpleWrite
---

JFrog 安全研究团队于 2026 年 6 月 25 日公开了 Linux 内核本地提权利用 **DirtyClone**。它利用 [CVE-2026-43503](https://cveawg.mitre.org/api/cve/CVE-2026-43503) 中 socket buffer（skb）共享分片标志传递不完整的问题，可将原本只读的文件页缓存变成内核中的写入目标。该漏洞的 CVSS v3.1 评分为 8.8。

{{< callout type="important" >}}
截至 2026-06-27，Gentoo 目前提供的受支持内核版本已经包含 CVE-2026-43503 的上游修复。**更新内核软件包后需要重启才能切换到新版本；旧内核仍在运行期间不受保护。**
{{< /callout >}}

## 修复方案

Gentoo 对以下三个内核软件包提供安全支持：

| 软件包名称 | 目前状态 |
|---|---|
| `sys-kernel/gentoo-kernel` | 目前版本已覆盖上游修复 |
| `sys-kernel/gentoo-kernel-bin` | 目前版本已覆盖上游修复 |
| `sys-kernel/gentoo-sources` | 目前版本已覆盖上游修复 |

`sys-kernel/vanilla-sources` 不在 Gentoo 安全支持范围内。

先同步仓库，再更新自己正在使用的内核软件包。Gentoo 的 [Distribution Kernel 文档](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)说明，这类内核通过 Portage 安装并随软件包更新。下面以预编译内核为例；使用其他受支持内核时替换软件包名称：

```bash
emerge --sync
emerge --ask --update sys-kernel/gentoo-kernel-bin
```

`gentoo-kernel` 和 `gentoo-kernel-bin` 用户应确认新内核已经安装并由引导程序选中。`gentoo-sources` 用户还需要按自己的配置重新编译和安装内核。随后重启，并确认实际运行的版本：

```bash
uname -r
```

Linux CNA 记录列出的各稳定分支修复下限如下；主线方面，JFrog 记录的首个修复标签是 v7.1-rc5，Linux CNA 列出的正式修复版本是 7.1。使用自行配置的内核或不受 Gentoo 支持的内核软件包时，可据此检查：

| 内核分支 | 首个修复版本 |
|---|---|
| 5.10 | 5.10.257 |
| 5.15 | 5.15.208 |
| 6.1 | 6.1.174 |
| 6.6 | 6.6.141 |
| 6.12 | 6.12.91 |
| 6.18 | 6.18.33 |
| 7.0 | 7.0.10 |
| 7.1 | v7.1-rc5；正式版为 7.1 |

{{< callout type="warning" >}}
Gentoo 已宣布正在终止对 5.10 和 5.15 分支的支持，并计划于 2026-07-03 从仓库移除相关包。仍在使用这些分支的用户应迁移到受支持的新 LTS 分支。
{{< /callout >}}

## 漏洞影响

成功利用需要同时具备以下条件：

- 系统运行缺少完整修复的内核；
- 攻击者能够在本机执行代码；
- 攻击者拥有或能够在用户/网络命名空间中取得 `CAP_NET_ADMIN`；
- 内核允许攻击者配置所需的 XFRM/IPsec 和数据包（packet）复制路径。

非特权用户命名空间常被用来取得网络命名空间内的 `CAP_NET_ADMIN`，因此启用该功能的主机风险更高。允许不受信任工作负载创建用户和网络命名空间，或向容器授予网络管理能力的多租户与容器环境，也应优先更新。

JFrog 的利用会让 IPsec 对文件页缓存执行原地解密，从而修改内存中的特权程序，例如 `/usr/bin/su`。磁盘文件本身不会改变，常规的磁盘完整性检查可能无法发现攻击；研究人员也没有观察到相应的内核日志或审计记录。

## 技术原因

`SKBFL_SHARED_FRAG` 表示 skb 的分片引用了由外部持有或与其他对象共享的内存。后续代码准备原地写入时，应根据这个标志先执行写时复制，避免修改仍与文件页缓存共享的物理页。

CVE-2026-43503 修复前，`__pskb_copy_fclone()`、`skb_shift()`、`skb_gro_receive()`、`skb_gro_receive_list()`、`skb_segment()` 和 `tcp_clone_payload()` 等分片转移路径没有完整传递该标志。复制后的 skb 仍引用相同页面，却被错误报告为没有共享分片。攻击者可借助数据包（packet）复制路径将这样的 skb 送入 ESP 原地解密流程，最终写入只读文件的页缓存。

该修复提交的 author date 是 5 月 16 日，5 月 21 日由网络子系统维护者合并；包含该提交的首个主线标签是 5 月 24 日发布的 Linux v7.1-rc5。CVE 于 5 月 23 日公开，JFrog 于 6 月 25 日发布完整分析。

## 缓解方案

以下措施只用于暂时阻断公开的 DirtyClone 利用路径，不能替代内核更新。所有命令需要以 root 身份执行（`sudo su` 或在每条命令前加 `sudo`）。

### 禁止创建新的用户命名空间

Gentoo 可以使用 Linux 官方 [`max_user_namespaces`](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/user.html#max-user-namespaces) 参数，临时设置并写入持久配置：

```bash
sysctl -w user.max_user_namespaces=0
printf '%s\n' 'user.max_user_namespaces=0' > /etc/sysctl.d/99-disable-userns.conf
```

`sysctl -w` 执行时会直接输出确认行：

```
user.max_user_namespaces = 0
```

确认当前值和持久配置均已生效：

```bash
sysctl user.max_user_namespaces
# user.max_user_namespaces = 0

cat /etc/sysctl.d/99-disable-userns.conf
# user.max_user_namespaces=0
```

这会把当前用户命名空间中任一用户可新建的用户命名空间数量设为 0；在宿主机的初始用户命名空间中执行时，也会限制特权进程。已经存在的命名空间不会因此消失；如果依赖这项措施临时防护，建议写入持久配置后在维护窗口重启。依赖用户命名空间的程序和沙盒可能受到影响。

这项措施只阻止一般本地用户通过新建用户命名空间取得 `CAP_NET_ADMIN`。它不能防护已经持有该 capability 的程序、特权容器或既有用户命名空间中的攻击者，也不能阻断不依赖用户命名空间的 Copy Fail 和 DirtyFrag/RxRPC 路径；这类环境必须更新内核，或确认相应模块已被有效阻断。

部分 Debian/Ubuntu 内核另有 `kernel.unprivileged_userns_clone` 参数，它不是通用的上游或 Gentoo 内核接口。

### 阻断相关内核模块

不使用 IPsec 或 RxRPC 的系统可以阻止相关模块加载，并卸载已经加载的模块。对 DirtyClone 本身，关键是 `esp4`/`esp6`；`rxrpc` 对应的是较早的 DirtyFrag/RxRPC（CVE-2026-43500）路径：

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

根据 kmod 官方手册，`modprobe.d` 的 [`install` 指令](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd)会用指定命令替代正常模块加载，`modprobe` 的 [`-r` 参数](https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.8.scd)用于卸载模块。不要忽略卸载错误或检查命令的输出。如果模块正在使用、已经编入内核，或由 initramfs 提前加载，这项措施不会完整生效；配置还需要进入 initramfs，或改用禁止用户命名空间或更新内核。屏蔽 `esp4`/`esp6` 会停用相应的 IPv4/IPv6 ESP 功能并影响依赖它们的 IPsec 连接。

### 更新内核后撤销缓解措施

完成内核更新并重启到新版本后，可以移除临时配置并恢复默认值：

```bash
rm /etc/modprobe.d/block-dirtyfrag.conf
rm /etc/sysctl.d/99-disable-userns.conf
sysctl -w user.max_user_namespaces=2147483647
```

移除 modprobe.d 配置后，`esp4`/`esp6`/`rxrpc` 恢复按需加载，无需手动执行 `modprobe`。`sysctl -w` 立即恢复 user namespace 限制；`2147483647` 是该参数的内核默认值。

## 与早期漏洞的关系

DirtyClone 延续了 DirtyFrag 的页缓存写入手法，但 Copy Fail、DirtyFrag 的两条路径和 Fragnesia 各有不同根因，临时阻断方式也不能互换。参见背景文章：[Linux 页缓存写入型提权漏洞梳理：Copy Fail、DirtyFrag、Fragnesia 与 DirtyClone]({{< relref "/posts/2026-06-27-linux-page-cache-lpe" >}})。

Gentoo 于 5 月 19 日公告，受支持内核当时已经包含最新的 Fragnesia v5 补丁。该公告早于 DirtyClone 修复，不能单独说明 CVE-2026-43503 的状态；本文以 Linux CVE 记录和 Gentoo 在 6 月 27 日提供的内核版本为准。

## 参考资料

- [Linux CNA 的 CVE-2026-43503 JSON 记录](https://cveawg.mitre.org/api/cve/CVE-2026-43503)
- [上游修复提交 48f6a5356a33](https://git.kernel.org/linus/48f6a5356a33dd78e7144ae1faef95ffc990aae0)
- [Dissecting and Exploiting Linux LPE Variant: DirtyClone](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/) — JFrog Security Research
- [Ubuntu CVE-2026-43503](https://ubuntu.com/security/CVE-2026-43503)
- [Copy Fail, Dirty Frag, and Fragnesia kernel vulnerabilities](https://www.gentoo.org/news/2026/05/19/copy-fail-fragnesia-vulnerabilities.html) — Gentoo Linux
- [Gentoo 内核软件包版本：gentoo-kernel](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel) / [gentoo-kernel-bin](https://packages.gentoo.org/packages/sys-kernel/gentoo-kernel-bin) / [gentoo-sources](https://packages.gentoo.org/packages/sys-kernel/gentoo-sources)
- [Gentoo Distribution Kernel 文档](https://wiki.gentoo.org/wiki/Project:Distribution_Kernel)
- [Linux user sysctl 文档](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/user.html)
- [Copy Fail（CVE-2026-31431）](https://copy.fail/)
