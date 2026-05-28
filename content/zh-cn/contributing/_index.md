---
title: "贡献指南"
description: "如何为 Gentoo 中文社区网站做出贡献"
---

欢迎来一起建设 Gentoo 中文社区网站！这篇指南会带你了解网站的项目结构，以及想参与贡献该从哪里入手。

## 项目概况

本网站使用 [Hugo](https://gohugo.io/) 静态网站生成器和 [Hextra](https://imfing.github.io/hextra/) 主题构建，托管在 GitHub Pages 上。主题通过 [Hugo Modules](https://gohugo.io/hugo-modules/) 引入（见 `go.mod`），不再使用 git submodule。

**项目仓库**：<https://github.com/Gentoo-zh/gentoo-zh.github.io>

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

- 界面翻译：`i18n/zh-cn.yaml`（简体）、`i18n/zh-tw.yaml`（传统）
- 默认语言为简体中文，位于站点根路径 `/`；传统中文位于 `/zh-tw/`
- 简繁转换由仓库内的 `sync_to_tw.sh` 脚本完成（见下文）

### 主题与资源

- 主题 Hextra 通过 Hugo Modules 引入，版本固定在 `go.mod`，不在仓库内保存主题源码
- `layouts/` — 站点自定义模板（覆盖主题默认，如首页 `shortcodes/home-bento.html`、贡献者页等）
- `assets/css/custom.css` — 在 Hextra 样式之上的站点样式覆盖
- `static/` — 静态资源（`CNAME`、图片等）

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

## 如何贡献

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

主题是 Hugo Module，用 `hugo mod` 升级，不再操作 submodule：

```bash
hugo mod get -u github.com/imfing/hextra
hugo mod tidy
git add go.mod go.sum
git commit -m "更新 Hextra 主题"
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
