---
title: "Overlay"
---

Gentoo 的 Overlay 机制可以让用户使用官方 Portage 树以外的软件包，作为一个软件来源的扩充和叠加。
故名为 Overlay（意为叠加）。

gentoo-zh Overlay 是 Gentoo 社区历史悠久的老牌 Overlay 之一，其前身是 2003 年创立的 gentoo-tw
和随后创立的 gentoo-china。后来，台湾和大陆社区的共同努力下，合并为了 gentoo-zh overlay。

到现在，gentoo-zh 已经收录了 450 多个软件包，大致是这么几类：

* **中文 / CJK 相关**：fcitx 输入法和一大堆插件、码表（rime、chinese-addons 等），搜狗 / 萌娘 / zhwiki 拼音词库，中文字体，以及一些软件的 CJK 补丁。
* **网络、开发工具等官方源里还没有的**：毕竟是 gentoo 用户，谁手里没几个自己维护的包。
* **打好补丁的桌面 / 性能向内核**：cachyos-sources、xanmod、liquorix 这些，省得自己一个个打补丁。
* **跟进新版本**：有些包官方源里暂时没人管、更新不及时，这边自己接着出新版本。
* **错误修复**：开发者自己踩到 bug，解决后会第一时间把补丁推回源里。

overlay 有条立身的铁规矩——「别弄坏别人的系统」，所以每个 ebuild 都得在支持的架构上测过才进源。

## 仓库地址

gentoo-zh overlay 的源代码托管在 GitHub 上：

<https://github.com/microcai/gentoo-zh>

## 如何使用

{{< callout type="warning" >}}
**重要提示**（更新时间：2025-10-07）

根据 [Gentoo 官方公告](https://www.gentoo.org/support/news-items/2025-10-07-cache-enabled-mirrors-removal.html)，Gentoo 已停止为第三方仓库提供缓存镜像支持。从 2025-10-30 起，所有第三方仓库（包括 gentoo-zh）的镜像配置将从官方仓库列表中移除。

**这意味着什么？**
- `eselect repository` 和 `layman` 等工具仍可正常使用
- 官方将不再提供缓存镜像，改为直接从上游源（GitHub）同步
- 官方仓库（::gentoo、::guru、::kde、::science）不受影响，仍可使用镜像

**如果您之前已添加 gentoo-zh overlay，请按下方命令更新同步 URI。**
{{< /callout >}}

```bash
# 查看已安装的仓库
eselect repository list -i

# 移除旧配置
eselect repository remove gentoo-zh

# 重新启用（将自动使用正确的上游源）
eselect repository enable gentoo-zh
```

### 手动配置

在 `/etc/portage/repos.conf/` 目录下创建 `gentoo-zh.conf` 文件，内容如下：

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://github.com/microcai/gentoo-zh.git
auto-sync = yes
```

然后同步：

```bash
emerge --sync gentoo-zh
```

## 镜像加速

国内直连 GitHub 或官方 distfiles 偏慢时，用下面的国内镜像加速。

### distfiles 镜像

把 overlay 软件包的源码缓存了一份，直连慢的时候从这儿拉。源站：<https://distfiles.gentoocn.org/>

**镜像站点**：
- 重庆大学：<https://mirrors.cqu.edu.cn/gentoo-zh/>
- 南京大学：<https://mirror.nju.edu.cn/gentoo-zh>

在 `/etc/portage/make.conf` 的 `GENTOO_MIRRORS` 中，于官方源之后追加 gentoo-zh distfiles 源：

```bash
GENTOO_MIRRORS="https://mirrors.bfsu.edu.cn/gentoo"               # ::gentoo 官方 distfiles
GENTOO_MIRRORS="${GENTOO_MIRRORS} https://distfiles.gentoocn.org" # ::gentoo-zh distfiles
```

{{< callout type="info" >}}
如果因版权问题或其他原因不想 mirror 某些 distfiles，请在对应 ebuild 中加入 `RESTRICT="mirror"`。
{{< /callout >}}

### Git 仓库镜像

国内直连 GitHub 不稳或太慢时，把 overlay 同步切到国内镜像，更稳更快。源仓库：<https://github.com/microcai/gentoo-zh.git>

**镜像站点**：
- 重庆大学：<https://mirrors.cqu.edu.cn/git/gentoo-zh.git>
- 南京大学：<https://mirror.nju.edu.cn/git/gentoo-zh.git>

在 `/etc/portage/repos.conf/gentoo-zh.conf` 中，把 `sync-uri` 指向镜像即可：

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://mirrors.cqu.edu.cn/git/gentoo-zh.git
auto-sync = yes
```

配置帮助见 [cqu mirror wiki](https://mirrors.cqu.edu.cn/#/wiki/mirror-wiki/gentoo-zh.git)。

本节镜像站汇总与配置说明整理自 [peeweep](/contributors/peeweep/) 的[公告](https://t.me/gentoocn/56)，感谢！

## 使用 overlay 中的软件包

配置好之后，gentoo-zh 里的软件包就和官方源一样，直接 emerge 就行：

```bash
emerge --ask <package-name>
```

如果想查看 overlay 提供了哪些软件包，可以使用：

```bash
eix -RO gentoo-zh
```

## 参与贡献

欢迎给 gentoo-zh overlay 添砖加瓦：到 GitHub 仓库提个 Pull Request 即可，发现问题也欢迎提 issue。
