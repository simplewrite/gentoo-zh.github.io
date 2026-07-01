# Gentoo 中文社区

[Gentoo 中文社区](https://gentoozh.org/) 官方网站，基于 [Hugo](https://gohugo.io/) 静态网站生成器与 [Hextra](https://imfing.github.io/hextra/) 主题构建，部署在 GitHub Pages 上。

## 特性

- Hugo 静态网站生成器 + Hextra 主题（通过 [Hugo Modules](https://gohugo.io/hugo-modules/) 引入，见 `go.mod`，无需 Node 工具链）
- 简体 / 传统中文双语并存（zh-cn 在根路径 `/`，zh-tw 在 `/zh-tw/`）
- 站内全文搜索（FlexSearch）、暗色模式、响应式布局
- 贡献者列表每周自动从 [gentoo-zh Overlay](https://github.com/microcai/gentoo-zh) 抓取并更新
- RSS 订阅

## 本地开发

需要 **Hugo extended** 版本；因为主题通过 Hugo Modules 引入，还需要 **Go** 工具链。

```bash
# Gentoo
emerge --ask www-apps/hugo dev-lang/go

# macOS
brew install hugo go
```

启动开发服务器（模块会在首次构建时自动拉取，无需 git submodule）：

```bash
hugo server -D     # 访问 http://localhost:1313
```

构建网站（输出到 `public/`）：

```bash
hugo --gc --minify
```

## 项目结构

```
.
├── config/_default/          # Hugo 配置
│   ├── hugo.toml             # 主配置（站点信息、分类法、Markdown 渲染、输出格式）
│   ├── languages.toml        # 双语配置（[zh-cn] / [zh-tw]，含 contentDir）
│   ├── menus.zh-cn.toml      # 简体导航菜单
│   ├── menus.zh-tw.toml      # 传统导航菜单
│   └── params.toml           # 主题参数
├── content/
│   ├── zh-cn/                # 简体中文内容
│   │   ├── about/ download/ mirrorlist/ overlay/
│   │   ├── posts/            # 文章（content/zh-cn/posts/<slug>/index.md）
│   │   ├── contributors/     # 贡献者页面（脚本自动生成，勿手动编辑）
│   │   ├── contributing/     # 投稿指南
│   │   └── changelog/        # 更新记录
│   └── zh-tw/                # 传统中文内容（结构与 zh-cn 一致，由脚本转换生成）
├── i18n/                     # 界面翻译（zh-cn.yaml / zh-tw.yaml）
├── layouts/                  # 自定义模板（首页 bento、贡献者页，及 custom/ 钩子）
├── assets/                   # Hugo 处理的资源（css/custom.css、logo）
├── static/                   # 原样输出的静态文件（CNAME、favicon、图片）
├── scripts/                  # 贡献者自动更新脚本（见 scripts/README.md）
├── sync_to_tw.sh             # 简体 → 传统中文转换（OpenCC s2twp + 术语修正）
├── go.mod / go.sum           # Hextra 主题的 Hugo Module 依赖
└── .github/workflows/        # CI/CD（hugo.yml 部署 + update-contributors.yml 贡献者更新）
```

## 简繁转换

以简体版为源，用脚本生成传统版（需先安装 [OpenCC](https://github.com/BYVoid/OpenCC)）：

```bash
./sync_to_tw.sh content/zh-cn/posts/<slug>/index.md content/zh-tw/posts/<slug>/index.md
```

## 贡献

欢迎投稿与改进，详见站点的[贡献指南](https://gentoozh.org/contributing/)（`content/zh-cn/contributing/`）。

## 更新主题

主题是 Hugo Module，用 `hugo mod` 升级（不再操作 submodule）：

```bash
hugo mod get -u github.com/imfing/hextra
hugo mod tidy
```

## GitHub Pages 部署

推送到 `master` 分支后，由 `.github/workflows/hugo.yml` 经 GitHub Actions 自动构建并部署到 GitHub Pages。

## 链接

- [Hugo 文档](https://gohugo.io/documentation/)
- [Hextra 主题](https://imfing.github.io/hextra/)
- [Gentoo 官方](https://www.gentoo.org/)
