---
title: "gentoo-zh Repository Migration: Announcement and Execution Plan"
description: "The canonical maintenance repository for the gentoo-zh overlay has moved to a GitHub organization repo."
date: 2026-07-02
featured: true
tags: ["announcement", "overlay"]
authors:
  - name: Locez
    image: /authors/locez.webp
    link: https://github.com/locez
  - name: Clover (review)
    image: /contributors/simplewrite/feature.webp
    link: https://github.com/simpleWrite
  - name: Mame (review)
    image: /contributors/yangmame/feature.webp
    link: https://github.com/YangMame
  - name: Zakk (layout)
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/Zakkaus
---

{{< callout type="info" >}}
**Update (2026-07-05)**: this repo was later renamed from `Gentoo-zh/gentoo-zh` to **[`Gentoo-zh/overlay`](https://github.com/gentoo-zh/overlay)** (the current canonical address); see [the note at the end](#rename-to-overlay) for the full story. The "For Users" and "For Contributors" sections below already use the new address; the "Background" and "Migration Steps" are the record from that time and still use the name `gentoo-zh/gentoo-zh`.
{{< /callout >}}

The canonical maintenance repository for the gentoo-zh overlay has moved to a GitHub organization repo:

- New repository: https://github.com/gentoo-zh/gentoo-zh
- Original repository: https://github.com/microcai/gentoo-zh

The original repository owner carried out the migration via a GitHub repository transfer. After the transfer, `gentoo-zh/gentoo-zh` is the canonical repository for the gentoo-zh overlay.

## Background

Moving the gentoo-zh overlay to a GitHub organization repo lets the community maintenance team manage maintenance permissions, CI configuration, issue/PR management, and the release process in one place, and reduces the impact a single account has on long-term maintenance.

The migration used GitHub's official repository transfer. The results:

- Full Git commit history preserved
- Branches and tags preserved
- Releases preserved
- GitHub issues preserved
- GitHub pull requests preserved
- GitHub stars and watchers preserved
- Fork network preserved
- Redirects from the original repository Git URL preserved
- Original commit SHAs preserved

After the transfer, `microcai/gentoo-zh` redirects to `gentoo-zh/gentoo-zh`. Old Git remote URLs keep working. Users and contributors should update to the new URL when convenient.

To avoid breaking existing user configurations, the old path `microcai/gentoo-zh` is left empty after the transfer. GitHub's redirect from the old address depends on the old path not being taken again. If that path is occupied by a repository or fork of the same name, the old URL no longer redirects to the new repository, and users still on the old URL are affected. The original owner does not recreate or fork a repository named `gentoo-zh` under the `microcai` account. Anyone who wants to keep a personal fork should avoid a same-named repository that would occupy the old path.

## For Users

GitHub redirects the old address to the new repository. If you configured the remote manually, update it to the new URL when convenient.

Re-add the overlay:

```bash
sudo eselect repository remove gentoo-zh
sudo eselect repository add gentoo-zh git https://github.com/gentoo-zh/overlay.git
sudo emaint sync -r gentoo-zh
```

Or edit the relevant config file under `/etc/portage/repos.conf/` (`gentoo-zh.conf` if you added it manually, or `eselect-repo.conf` if you used eselect) and change the `sync-uri` in the `[gentoo-zh]` section to the new address:

```ini
[gentoo-zh]
location = /var/db/repos/gentoo-zh
sync-type = git
sync-uri = https://github.com/gentoo-zh/overlay.git
auto-sync = yes
```

Then run `emerge --sync gentoo-zh`.

## For Contributors

Submit new issues, pull requests, and maintenance discussions to:

```text
https://github.com/gentoo-zh/overlay
```

Contributors with an existing local working copy should update upstream:

```bash
git remote set-url upstream https://github.com/gentoo-zh/overlay.git
git fetch upstream
```

Create new working branches from the new repository's default branch:

```bash
git checkout master
git pull upstream master
git checkout -b topic/name
```

## Migration Steps

### 1. Preparation

`gentoo-zh/gentoo-zh` currently exists as a fork of `microcai/gentoo-zh`. Free up the target repository name before running the repository transfer.

Steps:

1. Delete the existing `gentoo-zh/gentoo-zh`
2. Confirm the `gentoo-zh/gentoo-zh` name is free
3. Confirm the `gentoo-zh` organization owner is ready to accept the transfer
4. Confirm the original owner understands that after the transfer the old `microcai/gentoo-zh` path stays unoccupied, with no repository named `gentoo-zh` recreated or forked under the `microcai` account, so the redirect from old URLs to the new repository is not broken

### 2. Original owner initiates the repository transfer

The owner of `microcai/gentoo-zh` initiates the transfer in the GitHub repository settings:

```text
Settings -> General -> Danger Zone -> Transfer ownership
```

Target owner:

```text
gentoo-zh
```

Keep the target repository name as:

```text
gentoo-zh
```

### 3. The gentoo-zh organization accepts the transfer

The `gentoo-zh` organization owner accepts the GitHub transfer invitation.

After acceptance, the repository address becomes:

```text
https://github.com/gentoo-zh/gentoo-zh
```

### 4. Verify the transfer

After the transfer, confirm the following:

- The repository is at `gentoo-zh/gentoo-zh`
- The default branch is `master`
- Issues migrated
- Pull requests migrated
- Stars and watchers preserved
- Fork network preserved
- The old address `https://github.com/microcai/gentoo-zh` redirects to the new one
- `git clone https://github.com/microcai/gentoo-zh.git` redirects to the new repository
- `git clone https://github.com/gentoo-zh/gentoo-zh.git` works
- The old `microcai/gentoo-zh` path has not been recreated as a repository or same-named fork

### 5. Update maintenance entry points in the repository

After the transfer, update the following files:

- `repo.xml`
- `README.md`
- `sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild`
- `.github/workflows/nvchecker.yml`
- `MIGRATION.md`

Update the source in `repo.xml` to:

```xml
<source type="git">https://github.com/gentoo-zh/gentoo-zh.git</source>
```

Update the dependencies table link in `README.md` to:

```text
https://github.com/gentoo-zh/gentoo-zh/blob/deps-table/relation.md
```

Update the support link in `sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild` to:

```text
https://github.com/gentoo-zh/gentoo-zh
```

Historical links in ebuild comments that point to issues in the original repository stay as they are. The repository transfer preserves old issue link redirects, so there is no need to bulk-replace historical issue URLs.

### 6. Add `MIGRATION.md`

Add `MIGRATION.md` to the root of the new repository:

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

### 7. Update the README

Add a short migration section to `README.md`, before the installation instructions:

````md
> [!NOTE]
> gentoo-zh overlay has moved to https://github.com/gentoo-zh/gentoo-zh. Old GitHub URLs continue to redirect. If you manually configured a remote, update it when convenient.

## Repository migration

This repository was transferred from `microcai/gentoo-zh` to the `gentoo-zh` organization through GitHub repository transfer.

The current canonical repository is:

https://github.com/gentoo-zh/gentoo-zh

See [MIGRATION.md](./MIGRATION.md) for details.
````

### 8. Add Gentoo repository news

Add a GLEP 42 repository news item under `metadata/news/`. The news item uses a single `.en.txt` file: English is the authoritative body, Chinese is a supplement, and the migration commands come at the end. After users sync the overlay, they can read it with `eselect news read`.

New news item directory:

```text
metadata/news/2026-07-02-gentoo-zh-transfer/
```

News file:

```text
metadata/news/2026-07-02-gentoo-zh-transfer/2026-07-02-gentoo-zh-transfer.en.txt
```

Contents:

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

### 9. Update CI and automation configuration

After the transfer, update the repository-ownership configuration in GitHub Actions and automation jobs.

Update the repository-name check in `.github/workflows/nvchecker.yml` to:

```yaml
if: github.repository == 'gentoo-zh/gentoo-zh'
```

Confirm the following Actions secrets on the new repository:

- `GENTOO_ZH_NVCHECKER_PAT`

Enable the following Actions permissions on the new repository:

- `Read and write permissions`
- `Allow GitHub Actions to create and approve pull requests`

The `deps-table` branch is updated automatically by the dependencies table workflow. The repository ruleset grants force-push permission on `deps-table` to GitHub Actions specifically.

Pull request CI continues to be triggered by the GitHub Actions `pull_request` event.

### 10. Verify and commit the post-transfer repository changes

Once all in-repo migration changes are done, verify and commit them together in one commit, instead of splitting README, metadata, and news into repeated commits.

Verify the news item can be read:

```bash
eselect news list
eselect news read
```

Commit all migration changes in this repository:

```bash
git add metadata/news/2026-07-02-gentoo-zh-transfer README.md repo.xml sys-kernel/cachyos-sources/cachyos-sources-6.18.6.ebuild .github/workflows/nvchecker.yml MIGRATION.md
git commit -m "Update repository metadata after transfer"
git push origin master
```

### 11. Configure organization maintenance rules

Complete the following configuration in the `gentoo-zh/gentoo-zh` repository settings:

- Set the default branch to `master`
- Disallow deleting the default branch
- Disallow force push to the default branch
- Enable branch protection or a ruleset
- Require a pull request to merge into the default branch
- Manage maintainer permissions through a GitHub team
- Set the repository description to `Gentoo Linux overlay for gentoo users`
- Set the repository homepage to the gentoo-zh community homepage

### 12. Update the Gentoo overlay registry

Update the overlay registry in `gentoo/api-gentoo-org` so that `gentoo-zh` points to the new organization repository.

Target repository:

```text
https://github.com/gentoo/api-gentoo-org
```

File to edit:

```text
files/overlays/repositories.xml
```

Update the following fields in the `gentoo-zh` entry:

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

This registry PR updates the following fields:

- `homepage`
- `owner type`
- `owner/email`
- `owner/name`
- HTTPS `source`
- SSH `source`
- Atom `feed`

Steps:

```bash
git clone https://github.com/gentoo/api-gentoo-org.git
cd api-gentoo-org
git checkout -b update-gentoo-zh-overlay-metadata
```

Edit:

```text
files/overlays/repositories.xml
```

Commit:

```bash
git add files/overlays/repositories.xml
git commit -m "Update gentoo-zh overlay metadata"
```

Verify:

```bash
python bin/repositories-checker.py - files/overlays/repositories.xml
```

Open a pull request against `gentoo/api-gentoo-org`:

```text
Title: Update gentoo-zh overlay metadata

The gentoo-zh overlay repository has been transferred from microcai/gentoo-zh to gentoo-zh/gentoo-zh via GitHub repository transfer.

This updates the overlay registry homepage, Git sources, Atom feed URL, and owner metadata to the new canonical repository and maintainer organization.
```

## Follow-Up Maintenance

After the transfer, carry out the following maintenance tasks:

1. Update the internal metadata of the gentoo-zh overlay
2. Update the README and installation docs
3. Follow up on merging the gentoo-zh registry PR in `gentoo/api-gentoo-org`
4. Check the GitHub Actions secrets and permissions
5. Configure branch protection and the maintainer team
6. Confirm the migration news item shows up in `eselect news read`
7. Consolidate future contributions onto `gentoo-zh/gentoo-zh`

## Postscript: Website Progress (zakkaus)

The website's [contributor wall](/contributors/) auto-stats (`update-contributors.py`) and the related page notes now point to `Gentoo-zh/overlay`, and they refresh automatically on the 1st of each month. Now that the migration is in effect, the fork, issue, and other how-to links on the [Overlay page](/overlay/) and in the [contributing guide](/contributing/) have all been updated to the new repository. The old personal repository `microcai/gentoo-zh` 301-redirects to the new one; if you configured the old address locally, update it to the new URL when convenient.

## Postscript: the repo was later renamed to gentoo-zh/overlay {#rename-to-overlay}

The transfer above landed the repository at `Gentoo-zh/gentoo-zh` (a GitHub transfer keeps the original repository name). The community then voted on the canonical name, `gentoo-zh/overlay` won 21 to 9, and `Gentoo-zh/gentoo-zh` was renamed to **[`Gentoo-zh/overlay`](https://github.com/gentoo-zh/overlay)**, which is the current canonical address:

- New address: <https://github.com/gentoo-zh/overlay>, with `sync-uri` set to `https://github.com/gentoo-zh/overlay.git`
- Both old paths, `microcai/gentoo-zh` and `Gentoo-zh/gentoo-zh`, **301-redirect in a single hop** to the new repo (web and git), so users on an old address aren't affected and can update when convenient (see "For Users" above)
- Gentoo's official overlay registry (homepage / git source / feed / owner) has been updated to the new address too, see [gentoo/api-gentoo-org#829](https://github.com/gentoo/api-gentoo-org/pull/829)
