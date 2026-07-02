---
title: "gentoo-zh 仓库迁移公告与执行方案"
description: "gentoo-zh overlay 的正式维护仓库迁移到 GitHub 组织仓库"
date: 2026-07-02
featured: true
tags: ["announcement", "overlay"]
authors:
  - name: Locez
    image: /authors/locez.webp
    link: https://github.com/locez
  - name: Clover（审校）
    image: /contributors/simplewrite/feature.webp
    link: https://github.com/simpleWrite
  - name: Mame（审校）
    image: /contributors/yangmame/feature.webp
    link: https://github.com/YangMame
  - name: Zakk（排版）
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/Zakkaus
---

gentoo-zh overlay 的正式维护仓库迁移到 GitHub 组织仓库：

- 新仓库：https://github.com/gentoo-zh/gentoo-zh
- 原仓库：https://github.com/microcai/gentoo-zh

本次迁移由原仓库 owner 发起 GitHub repository transfer 完成。迁移完成后，`gentoo-zh/gentoo-zh` 作为 gentoo-zh overlay 的 canonical repository。

## 迁移背景

gentoo-zh overlay 迁移到 GitHub 组织仓库，是为了让维护权限、CI 配置、issue/PR 管理和发布流程统一由社区维护团队管理，降低单一账号对长期维护的影响。

本次迁移采用 GitHub 官方 repository transfer。迁移结果如下：

- 保留完整 Git commit 历史
- 保留 branches 和 tags
- 保留 releases
- 保留 GitHub issues
- 保留 GitHub pull requests
- 保留 GitHub stars 和 watchers
- 保留 fork network
- 保留原仓库 Git URL 的 redirect
- 保留原有 commit SHA

迁移完成后，访问 `microcai/gentoo-zh` 会跳转到 `gentoo-zh/gentoo-zh`。旧的 Git remote URL 继续可用；建议用户和贡献者在方便时更新到新 URL。

为避免破坏用户现有配置，迁移完成后旧路径 `microcai/gentoo-zh` 保持空置。GitHub 的旧地址跳转依赖旧路径未被重新占用；如果该路径被同名仓库或同名 fork 占用，旧 URL 将不再跳转到新仓库，仍在使用旧 URL 的用户会受到影响。原 owner 不在 `microcai` 账号下重新创建或 fork 名为 `gentoo-zh` 的仓库；如需保留个人 fork，应避免使用会占用旧路径的同名仓库。

## 用户切换操作

旧地址会由 GitHub redirect 到新仓库。手动配置过 remote 的用户，建议在方便时更新到新 URL。

重新添加 overlay：

```bash
sudo eselect repository remove gentoo-zh
sudo eselect repository add gentoo-zh git https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

直接修改现有 remote：

```bash
cd /var/db/repos/gentoo-zh
sudo git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

## 贡献者切换操作

新的 issue、pull request 和维护讨论统一提交到：

```text
https://github.com/gentoo-zh/gentoo-zh
```

已有本地工作副本的贡献者更新 upstream：

```bash
git remote set-url upstream https://github.com/gentoo-zh/gentoo-zh.git
git fetch upstream
```

新的工作分支从新仓库默认分支创建：

```bash
git checkout master
git pull upstream master
git checkout -b topic/name
```

## 迁移执行步骤

### 1. 迁移前准备

`gentoo-zh/gentoo-zh` 当前作为 `microcai/gentoo-zh` 的 fork 存在。执行 repository transfer 前释放目标仓库名称。

执行操作：

1. 删除现有 `gentoo-zh/gentoo-zh`
2. 确认 `gentoo-zh/gentoo-zh` 名称已释放
3. 确认 `gentoo-zh` 组织 owner 已准备接受 transfer
4. 确认原 owner 知悉迁移完成后不再占用 `microcai/gentoo-zh` 旧路径，不在 `microcai` 账号下重新创建或 fork 名为 `gentoo-zh` 的仓库，以免破坏旧 URL 到新仓库的跳转

### 2. 原 owner 发起 repository transfer

由 `microcai/gentoo-zh` 的 owner 在 GitHub 仓库设置中发起 transfer：

```text
Settings -> General -> Danger Zone -> Transfer ownership
```

目标 owner 填写：

```text
gentoo-zh
```

目标仓库名保持：

```text
gentoo-zh
```

### 3. gentoo-zh 组织接受迁移

`gentoo-zh` 组织 owner 接受 GitHub transfer 邀请。

接受完成后，仓库地址变为：

```text
https://github.com/gentoo-zh/gentoo-zh
```

### 4. 验证 transfer 结果

迁移完成后确认以下内容：

- 仓库位于 `gentoo-zh/gentoo-zh`
- 默认分支为 `master`
- issues 已迁移
- pull requests 已迁移
- stars 和 watchers 已保留
- fork network 已保留
- 旧地址 `https://github.com/microcai/gentoo-zh` 跳转到新地址
- `git clone https://github.com/microcai/gentoo-zh.git` 跳转到新仓库
- `git clone https://github.com/gentoo-zh/gentoo-zh.git` 正常工作
- `microcai/gentoo-zh` 旧路径未被重新创建为仓库或同名 fork

### 5. 更新仓库内维护入口

迁移完成后修改以下文件：

- `repo.xml`
- `README.md`
- `sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild`
- `.github/workflows/nvchecker.yml`
- `MIGRATION.md`

`repo.xml` 中的 source 更新为：

```xml
<source type="git">https://github.com/gentoo-zh/gentoo-zh.git</source>
```

`README.md` 中的 dependencies table 链接更新为：

```text
https://github.com/gentoo-zh/gentoo-zh/blob/deps-table/relation.md
```

`sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild` 中的支持入口更新为：

```text
https://github.com/gentoo-zh/gentoo-zh
```

ebuild 注释中指向原仓库 issue 的历史链接保留不变。repository transfer 会保留旧 issue 链接跳转，不需要批量替换历史 issue URL。

### 6. 添加 `MIGRATION.md`

在新仓库根目录新增 `MIGRATION.md`：

````md
# gentoo-zh repository migration / gentoo-zh 仓库迁移说明

## 中文

gentoo-zh overlay 已通过 GitHub repository transfer 从个人仓库迁移到社区组织仓库：

- 原仓库：https://github.com/microcai/gentoo-zh
- 当前仓库：https://github.com/gentoo-zh/gentoo-zh

迁移完成后，`gentoo-zh/gentoo-zh` 是 gentoo-zh overlay 的正式维护入口。GitHub 会将旧仓库地址自动跳转到新仓库；旧的 Git remote URL 也会继续跳转。

过去所有维护者和用户对 gentoo-zh 的贡献会随仓库迁移一并保留。后续维护在 `gentoo-zh/gentoo-zh` 继续进行。

为了让仓库地址与当前维护入口保持一致，建议在方便时将本地 remote 更新为：

```bash
git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
```

后续 issue、pull request 和维护讨论请使用当前仓库。

## English

The gentoo-zh overlay has been transferred from the personal repository to the community organization through GitHub repository transfer:

- Previous repository: https://github.com/microcai/gentoo-zh
- Current repository: https://github.com/gentoo-zh/gentoo-zh

After the transfer, `gentoo-zh/gentoo-zh` is the canonical maintenance repository for the gentoo-zh overlay. GitHub redirects the old repository URL to the new one, and old Git remote URLs continue to work through GitHub redirects.

Contributions from past maintainers and users are preserved as part of this repository transfer. Future maintenance continues at `gentoo-zh/gentoo-zh`.

To keep local remotes aligned with the current maintenance location, update them when convenient:

```bash
git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
```

Please use the current repository for future issues, pull requests, and maintenance discussions.
````

### 7. 更新 README

在 `README.md` 中添加一个简短迁移小节，放在安装说明前：

````md
> [!NOTE]
> gentoo-zh overlay has moved to https://github.com/gentoo-zh/gentoo-zh. Old GitHub URLs continue to redirect. If you manually configured a remote, update it when convenient.

## Repository migration

This repository was transferred from `microcai/gentoo-zh` to the `gentoo-zh` organization through GitHub repository transfer.

The current canonical repository is:

https://github.com/gentoo-zh/gentoo-zh

See [MIGRATION.md](./MIGRATION.md) for details.
````

### 8. 添加 Gentoo repository news

在 `metadata/news/` 中添加一个符合 GLEP 42 的 repository news item。该 news item 使用单个 `.en.txt` 文件；英文为 authoritative 正文，中文为补充说明，最后统一给出迁移命令。用户同步 overlay 后可通过 `eselect news read` 读取。

新增 news item 目录：

```text
metadata/news/2026-07-02-gentoo-zh-transfer/
```

news 文件：

```text
metadata/news/2026-07-02-gentoo-zh-transfer/2026-07-02-gentoo-zh-transfer.en.txt
```

内容：

```text
Title: Action required: gentoo-zh repository moved
Author: gentoo-zh maintainers <overlay@gentoozh.org>
Content-Type: text/plain
Posted: 2026-07-02
Revision: 1
News-Item-Format: 1.0

ACTION REQUIRED: Update manually configured gentoo-zh overlay remotes.

The gentoo-zh overlay has been transferred through GitHub repository transfer
from:

https://github.com/microcai/gentoo-zh

to the community organization repository:

https://github.com/gentoo-zh/gentoo-zh

GitHub redirects old repository URLs and old Git remote URLs to the new
repository. The new repository is the canonical maintenance location for the
gentoo-zh overlay.

Please use the new repository for future issues, pull requests, and
maintenance discussions.

gentoo-zh overlay 已通过 GitHub repository transfer 从以下仓库迁移：

https://github.com/microcai/gentoo-zh

到新的社区组织仓库：

https://github.com/gentoo-zh/gentoo-zh

GitHub 会将旧仓库地址和旧 Git remote URL 自动跳转到新仓库。新仓库
是 gentoo-zh overlay 后续维护的正式入口。

后续 issue、pull request 和维护讨论请使用新仓库。

Users who configured the gentoo-zh overlay remote manually should update it
as soon as possible.

手动配置过 gentoo-zh overlay remote 的用户请尽快更新为新地址：

cd /var/db/repos/gentoo-zh
sudo git remote set-url origin https://github.com/gentoo-zh/gentoo-zh.git
sudo emaint sync -r gentoo-zh
```

### 9. 更新 CI 与自动化配置

迁移后更新 GitHub Actions 和自动化任务中的仓库归属配置。

`.github/workflows/nvchecker.yml` 中的仓库名判断更新为：

```yaml
if: github.repository == 'gentoo-zh/gentoo-zh'
```

新仓库确认以下 Actions secrets：

- `GENTOO_ZH_NVCHECKER_PAT`

新仓库启用以下 Actions 权限：

- `Read and write permissions`
- `Allow GitHub Actions to create and approve pull requests`

`deps-table` 分支由 dependencies table workflow 自动更新。仓库 ruleset 对 `deps-table` 的 force push 权限单独放行给 GitHub Actions。

pull request CI 继续由 GitHub Actions 的 `pull_request` 事件触发。

### 10. 验证并提交迁移后仓库修改

仓库内迁移修改全部完成后统一验证并提交一次，避免把 README、metadata 和 news 拆成重复提交。

验证 news 可被读取：

```bash
eselect news list
eselect news read
```

提交本仓库内全部迁移修改：

```bash
git add metadata/news/2026-07-02-gentoo-zh-transfer README.md repo.xml sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild .github/workflows/nvchecker.yml MIGRATION.md
git commit -m "Update repository metadata after transfer"
git push origin master
```

### 11. 配置组织维护规则

在 `gentoo-zh/gentoo-zh` 仓库设置中完成以下配置：

- 默认分支设置为 `master`
- 禁止删除默认分支
- 禁止 force push 到默认分支
- 开启 branch protection 或 ruleset
- 默认分支合并必须经过 pull request
- 维护者通过 GitHub team 管理权限
- 仓库 description 设置为 `Gentoo Linux overlay for Chinese users`
- 仓库 homepage 设置为 gentoo-zh 社区主页

### 12. 更新 Gentoo overlay registry

同步更新 `gentoo/api-gentoo-org` 中的 overlay registry，让 `gentoo-zh` 指向新的组织仓库。

目标仓库：

```text
https://github.com/gentoo/api-gentoo-org
```

修改文件：

```text
files/overlays/repositories.xml
```

修改 `gentoo-zh` 条目中的以下字段：

```xml
<repo quality="experimental" status="unofficial">
  <name>gentoo-zh</name>
  <description>To provide programs useful to Chinese speaking users (merged
    from gentoo-china and gentoo-taiwan).</description>
  <homepage>https://github.com/gentoo-zh/gentoo-zh</homepage>
  <owner type="project">
    <email>overlay@gentoozh.org</email>
    <name>gentoozh</name>
  </owner>
  <source type="git">https://github.com/gentoo-zh/gentoo-zh.git</source>
  <source type="git">git+ssh://git@github.com/gentoo-zh/gentoo-zh.git</source>
  <feed>https://github.com/gentoo-zh/gentoo-zh/commits/master.atom</feed>
</repo>
```

本次 registry PR 更新以下字段：

- `homepage`
- `owner type`
- `owner/email`
- `owner/name`
- HTTPS `source`
- SSH `source`
- Atom `feed`

执行步骤：

```bash
git clone https://github.com/gentoo/api-gentoo-org.git
cd api-gentoo-org
git checkout -b update-gentoo-zh-overlay-metadata
```

编辑：

```text
files/overlays/repositories.xml
```

提交：

```bash
git add files/overlays/repositories.xml
git commit -m "Update gentoo-zh overlay metadata"
```

验证：

```bash
python bin/repositories-checker.py - files/overlays/repositories.xml
```

向 `gentoo/api-gentoo-org` 提交 pull request：

```text
Title: Update gentoo-zh overlay metadata

The gentoo-zh overlay repository has been transferred from microcai/gentoo-zh to gentoo-zh/gentoo-zh via GitHub repository transfer.

This updates the overlay registry homepage, Git sources, Atom feed URL, and owner metadata to the new canonical repository and maintainer organization.
```

## 后续维护事项

迁移完成后执行以下维护事项：

1. 更新 gentoo-zh overlay 内部元数据
2. 更新 README 和安装文档
3. 跟进 `gentoo/api-gentoo-org` 中 gentoo-zh registry PR 合并
4. 检查 GitHub Actions secrets 和 permissions
5. 配置 branch protection 和维护者 team
6. 确认 `eselect news read` 可读到迁移 news
7. 将后续贡献入口统一收敛到 `gentoo-zh/gentoo-zh`

## 补记：官网侧进度（zakkaus）

官网[贡献者墙](/contributors/)的自动统计（`update-contributors.py`）与相关页面说明已提前指向 `Gentoo-zh/gentoo-zh`——它每月 1 日自动更新，下次运行时迁移已完成。[Overlay 页](/overlay/)与[贡献指南](/contributing/)里 fork、issue 等教学链接仍指向 `microcai/gentoo-zh`，等迁移完成后再统一更新。
