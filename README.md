# Gentoo 中文社区

基于 Hugo 和 Blowfish 主题的 Gentoo 中文社区网站。

## 特性

- Hugo 静态网站生成器
- Blowfish 现代化主题
- 完整的繁简体中文双语支持
- 响应式设计
- 快速构建速度
- RSS 订阅

## 本地开发

### 安装依赖

```bash
# Gentoo
emerge www-apps/hugo
```

### 启动开发服务器

```bash
hugo server
```

访问 http://localhost:1313

### 构建网站

```bash
hugo
```

生成的文件在 `public/` 目录。

## 项目结构

```
.
├── config/_default/          # Hugo 配置
│   ├── hugo.toml             # 主配置
│   ├── languages.zh-cn.toml  # 简体中文站点配置
│   ├── languages.zh-tw.toml  # 传统中文站点配置
│   ├── menus.zh-cn.toml      # 简体菜单
│   ├── menus.zh-tw.toml      # 传统菜单
│   ├── params.toml           # 主题参数
│   └── markup.toml           # Markdown 配置
├── content/                  # 内容（每个文档配对 index.zh-cn.md / index.zh-tw.md）
│   ├── posts/                # 文章
│   ├── contributors/         # 贡献者页面（自动生成）
│   ├── authors/              # 作者
│   ├── about/, download/, mirrorlist/, overlay/, contributing/, changelog/
│   └── categories/           # 分类
├── data/authors/             # 作者元数据（JSON）
├── i18n/                     # 字串翻译覆盖
├── layouts/                  # 自定义模板（贡献者、SEO 头）
├── assets/                   # Hugo 处理的资源（logo 等）
├── static/                   # 原样输出的静态文件（favicon、CNAME）
├── scripts/                  # 贡献者更新脚本
├── sync_to_tw.sh             # 简体 → 传统中文翻译辅助脚本
├── themes/blowfish/          # 主题（git submodule）
└── .github/workflows/        # CI/CD（Hugo 构建 + 贡献者自动更新）
```

## GitHub Pages 部署

项目已配置为可直接在 GitHub Pages 上部署。推送到 GitHub 后，通过 GitHub Actions 自动构建。

## 链接

- [Hugo 文档](https://gohugo.io/documentation/)
- [Blowfish 主题](https://blowfish.page/)
- [Gentoo 官方](https://www.gentoo.org/)
