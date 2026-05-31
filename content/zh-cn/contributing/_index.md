---
title: "贡献指南"
description: "如何为 gentoo-zh Overlay 与 Gentoo 中文社区网站做出贡献"
---

欢迎参与 Gentoo 中文社区！贡献分两条线，入口和登上[贡献者墙](/contributors/)的方式都不一样，先看你想做哪种：

- **为 gentoo-zh Overlay 贡献**（软件包 / ebuild）——社区主线，也是[贡献者墙](/contributors/)的来源（脚本每月抓取 [microcai/gentoo-zh](https://github.com/microcai/gentoo-zh) 提交 5 次以上者）。详见下方「为 gentoo-zh Overlay 贡献」。
- **为社区网站贡献**（文章 / 翻译 / 修正）——在 [gentoo-zh.github.io](https://github.com/Gentoo-zh/gentoo-zh.github.io) 仓库，详见本页后半「为社区网站贡献」。

## 为 gentoo-zh Overlay 贡献

gentoo-zh 是一个 `masters = gentoo` 的 Gentoo overlay（叠加在官方 Portage 树之上），收录 450 多个包，源码在 [microcai/gentoo-zh](https://github.com/microcai/gentoo-zh)。新增或更新 ebuild、修 bug、跟进新版本，都通过 GitHub Pull Request 提交；发现问题也欢迎提 [issue](https://github.com/microcai/gentoo-zh/issues)。

{{< callout type="info" >}}
首页[贡献者墙](/contributors/)统计的就是这种贡献——脚本每月抓取本仓库提交 5 次以上者。
{{< /callout >}}

### 准备

```bash
# 提交/QA 工具：pkgdev 生成提交信息与 Manifest，pkgcheck 做检查
# （二者已取代旧的 repoman，是现行官方工具）
emerge --ask dev-util/pkgdev   # 连带装上 pkgcheck
```

到 [GitHub](https://github.com/microcai/gentoo-zh) fork 仓库、clone 你的 fork、新建分支；本地启用 overlay 方便测试（见上文「添加 gentoo-zh」或 [Overlay 页](/overlay/)）。

### 提交一个 ebuild 的标准流程

本仓库遵循官方 Gentoo ebuild 仓库规范，写法权威参考是 [Devmanual](https://devmanual.gentoo.org/)：

1. **放对位置**：`<category>/<package>/<package>-<version>.ebuild`，目录与命名按官方分类。
2. **写 ebuild**：用本仓库主流的 `EAPI=8` 与标准两行版权头（`# Copyright <年> Gentoo Authors` + GPL-2 声明）；填好 `DESCRIPTION`、`HOMEPAGE`、`SRC_URI`、`LICENSE`、`SLOT`、依赖（`DEPEND`/`RDEPEND`/`BDEPEND`）、`IUSE` 等。
3. **KEYWORDS 只用测试关键字**（`~amd64`、`~arm64` 等）——**本仓库不收 stable 关键字**。
4. **写 `metadata.xml`**：每个包都要有，声明维护者与各 USE 的用途说明（官方规范要求，`pkgcheck` 会查）。
5. **生成 Manifest**：`pkgdev manifest`。本仓库用 thin manifest（`thin-manifests = true`），只记 distfiles 校验，ebuild 完整性交给 git。
6. **本地测试构建**：`emerge` 或 `ebuild <文件> install`，并在它 `KEYWORDS` 声明的**每个架构上都实测**——没测过就别声明支持。
7. **QA 自查**：`pkgcheck scan --commits --net`（PR 模板要求你勾选确认已在本地跑过；CI 也会另跑 `pkgcheck`）。
8. **提交**：用 `pkgdev commit` 生成规范提交信息（格式见下）；一个 PR 含单个贡献的全部提交，ebuild 连它的 `Manifest` 一起提，别拆成两个 PR。
9. **开 PR**：CI 会自动 `emerge` 该包并跑 `pkgcheck`，按 PR 模板逐项勾选后才会合并。

{{< callout type="warning" >}}
**唯一规则：别弄坏别人的系统（DO NOT BREAK PEOPLE'S SYSTEM）。**
{{< /callout >}}

### 提交信息规范

推荐用 `pkgdev commit` 自动生成符合规范的提交信息。

{{% details title="提交信息格式示例" %}}

普通（非版本更新）改动：

```text
$category/$package: 一句话简述

多行说明改动的原因；若是修 bug 且 GitHub 上有对应 issue，把链接附在这里。
```

版本更新（bump）：

```text
$category/$package: add $new_version, drop $old_version
```

{{% /details %}}

### 跟进上游新版本（nvchecker）

仓库用 [nvchecker](https://github.com/lilydjwg/nvchecker) 每天自动比对各包的上游版本（配置在 `.github/workflows/overlay.toml`），有新版本就自动开/更新对应的 [GitHub issue](https://github.com/microcai/gentoo-zh/issues)——**不知道从哪下手，挑一个版本更新（bump）issue 来做最省心**。新增包时，记得也在 `overlay.toml` 中加一条 nvchecker 规则（写明上游版本来源），让它一并纳入版本追踪。

### 官方规范与参考

- [Gentoo Devmanual](https://devmanual.gentoo.org/)——写 ebuild 的权威手册（EAPI、变量、依赖、`metadata.xml` 等）
- [Ebuild 仓库格式](https://wiki.gentoo.org/wiki/Repository_format)与 [Overlay 项目](https://wiki.gentoo.org/wiki/Project:Overlays)
- `pkgdev` / `pkgcheck`（`app-portage`）——现行的提交与 QA 工具
- 本仓库 [README](https://github.com/microcai/gentoo-zh#readme)（铁规矩与提交规范原文）与[依赖关系表](https://github.com/microcai/gentoo-zh/blob/deps-table/relation.md)

---

以下是**为社区网站（文章 / 翻译 / 文档）贡献**的指南。

## 项目概况

本网站使用 [Hugo](https://gohugo.io/) 静态网站生成器构建，托管在 GitHub Pages 上。表现层（主题）是 [Hextra](https://imfing.github.io/hextra/) 再加上本站的补丁包 [gentoozh-theme](https://github.com/Gentoo-zh/gentoozh-theme)——后者通过 [Hugo Modules](https://gohugo.io/hugo-modules/) 引入并在 Hextra 之上叠加覆盖，依赖链为 **站点 → gentoozh-theme → Hextra**。所以本仓库只放内容与配置，模板/样式源码都在补丁包里。

**项目仓库**：内容/配置 <https://github.com/Gentoo-zh/gentoo-zh.github.io>；主题补丁包 <https://github.com/Gentoo-zh/gentoozh-theme>

## 项目结构

### 内容组织

内容按语言分目录存放，简体中文在 `content/zh-cn/`，传统中文在 `content/zh-tw/`，两者目录结构完全一致：

- `download/` — 下载页面（镜像源和安装介质）
- `overlay/` — gentoo-zh Overlay 说明
- `mirrorlist/` — 镜像列表（Portage 树和 Distfiles 配置）
- `about/` — 关于页面（项目历史、社区频道、网站语言说明）
- `contributors/` — 贡献者页面（**自动更新，无需手动编辑**）
- `contributing/` — 贡献指南（本页面）
- `changelog/` — 更新记录
- `posts/` — 新闻文章和教程

> 同一篇内容的简体版放在 `content/zh-cn/...`、传统版放在对应的 `content/zh-tw/...`，文件名都是 `index.md` / `_index.md`（**不再**使用 `index.zh-cn.md` 这种语言后缀）。

### 配置文件

主要配置位于 `config/_default/` 目录：

- `hugo.toml` — Hugo 主配置（站点信息、分类法、Markdown 渲染、输出格式等）
- `languages.toml` — 语言配置（简繁双语，单文件内分 `[zh-cn]` / `[zh-tw]`）
- `menus.zh-cn.toml` / `menus.zh-tw.toml` — 各语言导航菜单
- `params.toml` — 主题参数（外观、功能开关）

### 多语言支持

- 界面字串翻译（`i18n/zh-cn.yaml`、`i18n/zh-tw.yaml`）属于表现层，在 **gentoozh-theme 补丁包**里；本仓库只放正文内容
- 默认语言为简体中文，位于站点根路径 `/`；传统中文位于 `/zh-tw/`
- 简繁转换由仓库内的 `sync_to_tw.sh` 脚本完成（见下文）

### 主题与资源

表现层拆成了独立的补丁包模块 **[gentoozh-theme](https://github.com/Gentoo-zh/gentoozh-theme)**（在 Hextra 之上叠加，仍跟随上游更新），本仓库不再放模板/样式源码：

- 模板（`layouts/`，含首页 `home-bento`、贡献者页等）、站点样式（`assets/css/custom.css`，Gentoo 品牌紫等）、界面字串（`i18n/`）都在 gentoozh-theme 里
- 站点通过 `config/_default/hugo.toml` 的 `[[module.imports]]` 引入它，并在 `go.mod` pin 版本
- `static/`（`CNAME`、favicon、logo、og 图等）仍在本仓库
- **改模板 / 样式 → 去 [gentoozh-theme](https://github.com/Gentoo-zh/gentoozh-theme) 仓库；改内容 → 在本仓库**

## 环境准备

需要 **Hugo extended** 版本；因为主题通过 Hugo Modules 引入，还需要 **Go** 工具链。

```bash
# Gentoo
emerge --ask www-apps/hugo dev-lang/go

# macOS
brew install hugo go
```

Fork 并 clone 仓库（**无需** `git submodule`，模块会在构建时自动拉取）：

```bash
git clone https://github.com/你的用户名/gentoo-zh.github.io.git
cd gentoo-zh.github.io
```

本地预览：

```bash
hugo server -D
# 访问 http://localhost:1313 预览
```

## 如何为网站贡献

### 1. 提交新文章

在 `content/zh-cn/posts/` 下按 `YYYY-MM-DD-article-name` 建立目录，写简体版 `index.md`：

```bash
mkdir -p content/zh-cn/posts/2026-05-29-my-article
$EDITOR content/zh-cn/posts/2026-05-29-my-article/index.md
```

front matter 示例：

```yaml
---
title: "文章标题"
date: 2026-05-29
tags: ["tutorial"]
---

文章正文……（作者署名见下方第 3 节）
```

可选的标签（`tags`，显示在文章列表与文章页的 `#标签`、链接到 `/tags/` 聚合页，首页文章卡片也会显示首个标签）：`tutorial`（教程）、`news`（新闻）、`announcement`（公告）、`website`（站务）。

写完简体版后，用脚本生成传统中文版（见下一节），传统版放在对应的 `content/zh-tw/posts/.../index.md`。

### 2. 简繁转换

`sync_to_tw.sh` 封装了 OpenCC（`s2twp`）+ 针对本站术语的修正与已知误转清理，**接收「源文件 → 目标文件」两个路径参数**：

```bash
# 先安装 OpenCC
emerge --ask app-i18n/opencc   # Gentoo
brew install opencc            # macOS
sudo apt install opencc        # Debian/Ubuntu

# 简体 → 传统
./sync_to_tw.sh \
  content/zh-cn/posts/2026-05-29-my-article/index.md \
  content/zh-tw/posts/2026-05-29-my-article/index.md
```

转换后建议人工检查台湾用语差异。

### 3. 文章署名与头像

在文章 front matter 的 `authors` 用「映射」形式写明作者，Hextra 会在署名处显示头像 + 姓名 + 链接：

```yaml
authors:
  - name: 你的名字
    image: /contributors/<你的标识>/feature.webp
    link: https://github.com/yourname
```

`image` 可指向贡献者页里的头像；省略 `image` 则只显示姓名。

### 4. 改进现有内容 / 技术改进

错别字、过时信息、使用技巧、缺失的传统中文翻译，看到了都欢迎随手修正。模板、样式、性能、功能等技术层面，也欢迎提改进。

> **贡献者列表（`content/*/contributors/`）由脚本自动维护**，抓取 [gentoo-zh Overlay](https://github.com/microcai/gentoo-zh) 中提交 5 次以上者，显示提交次数并按提交量排序，每月自动更新（`scripts/update-contributors.py` + GitHub Actions）。**请勿手动编辑该目录**；首页贡献者展示也随之自动更新。

## 提交 Pull Request

```bash
git checkout -b your-feature-branch
git add .
git commit -m "描述你的更改"
git push origin your-feature-branch
# 然后在 GitHub 上创建 Pull Request
```

## 写作规范

### Markdown 格式

- 使用标准 Markdown 语法
- 代码块标注语言（如 ` ```bash `）
- 图片放在文章目录内并使用相对路径
- 链接使用 Markdown 格式

### 中文排版

- 中英文之间留一个空格
- 使用全角中文标点
- 数字、英文用半角
- 专有名词保持原文（如 Gentoo、Hugo、Hextra、Portage）

## 常见问题

### 如何更新主题？

主题层是独立的 [gentoozh-theme](https://github.com/Gentoo-zh/gentoozh-theme) 补丁包模块，**升级 Hextra 在那个仓库里做**：

```bash
# 在 gentoozh-theme 仓库
hugo mod get -u github.com/imfing/hextra
hugo mod tidy
git commit -am "bump hextra"
git tag vX.Y.Z          # 打个新版本
```

然后回到**本站**仓库，把补丁包 pin 到新版本：

```bash
hugo mod get github.com/Gentoo-zh/gentoozh-theme@vX.Y.Z
git commit -am "bump gentoozh-theme"
```

### 如何添加新的栏目页面？

在 `content/zh-cn/<栏目>/` 下建 `_index.md`，用脚本生成 `content/zh-tw/<栏目>/_index.md`；若要进入顶部导航，再到 `config/_default/menus.zh-cn.toml` 和 `menus.zh-tw.toml` 各加一条 `[[main]]`。

### 简繁内容不一致怎么办？

以简体版为源，重新运行 `sync_to_tw.sh`（用法见上）覆盖生成传统版，再人工校对。请勿手动维护两份正文导致内容漂移。

## 社区交流

遇到问题或有建议？

- **Telegram 频道**：[@gentoocn](https://t.me/gentoocn)
- **Telegram 群组**：[@gentoo_zh](https://t.me/gentoo_zh)
- **GitHub Issues**：<https://github.com/Gentoo-zh/gentoo-zh.github.io/issues>

更多频道（IRC / Matrix / 闲聊群等）见[关于页面](/about/)。

## 许可协议

本站内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可协议，除非另有说明。代码贡献遵循项目的 MIT 许可。

---

改一个错字、补一句翻译、提个 PR，都算数。Gentoo 中文社区就是这么一点点攒起来的。
