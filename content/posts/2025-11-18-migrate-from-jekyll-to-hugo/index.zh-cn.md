---
title: "网站从 Jekyll 迁移至 Hugo"
date: 2025-11-18
categories: ["announcement"]
authors: ["zakkaus"]
---

经创始人 [@biergaizi](https://github.com/biergaizi) 授权，[@Zakkaus](https://github.com/zakkaus) 于 2025 年接手本站日常维护，并将站点从 Jekyll 迁移到 Hugo。

## 为什么换 Hugo

Jekyll 依赖 Ruby 环境，构建较慢，主题生态也不如以往活跃。Hugo 是单一 Go 二进制，构建速度快、部署简单，原生支持多语言。主题选用 [Blowfish](https://blowfish.page/)。

## 迁移内容

- `_posts` 目录改用 Hugo 的 Page Bundles 组织（`content/posts/<slug>/index.zh-cn.md`）
- Front matter 从 YAML 改为 TOML
- 简繁双语并存（zh-CN / zh-TW）
- 作者数据集中到 `data/authors/`
- 部署改走 GitHub Actions，每周自动更新贡献者列表

## 反馈

- Telegram 群：[@gentoo_zh](https://t.me/gentoo_zh)
- Telegram 频道：[@gentoocn](https://t.me/gentoocn)
- 提交 Issue / PR：[GitHub](https://github.com/gentoo-zh/gentoo-zh.github.io)

感谢 [@biergaizi](https://github.com/biergaizi) 与 [@zhcj](https://github.com/zhcj) 创立并长期维护 Gentoo 中文社区，也感谢 Blowfish 主题的开发者。
