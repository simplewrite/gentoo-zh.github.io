---
title: "Recent Community Updates: Live ISO, Website, Download Site, and Speedtest"
description: "A roundup of what the community has worked on lately: the custom KDE Live ISO, the Calamares installer, the gig overlay, the build pipeline, the website (migrated to Hextra, now with English), the download site, and the speedtest page."
date: 2026-06-09
tags: ["announcement"]
authors:
  - name: Zakk
    image: /contributors/zakkaus/feature.webp
    link: https://github.com/zakkaus
---

A roundup of what the community has worked on recently, project by project. Each item links to its repo, so you can dig into the full history if you want.

## Live ISO

The Chinese community's custom KDE Plasma 6 desktop Live ISO ([Gentoo-zh/Live-ISO](https://github.com/Gentoo-zh/Live-ISO)):

- **Three languages out of the box**: the boot menu offers Simplified / Traditional / English, and the whole live environment follows your choice; the installed system also keeps whatever language you picked in the installer.
- **Chinese input methods preinstalled**: fcitx5 + rime, ready to type out of the box, with Luna Pinyin, Zhuyin, Wubi86, Cangjie, and Cantonese Pinyin built in.
- **Proprietary NVIDIA, optional**: pick the NVIDIA entry in the boot menu to load the proprietary driver normally (disable Secure Boot first); otherwise it uses open-source nouveau.
- **Handy live-only desktop switches**: the desktop has a few one-click toggles meant just for the live session, there when you need them — temporarily turn off auto-sleep / lock (so a long session or install isn't interrupted), enable passwordless sudo, and start SSH (handy for a remote install or debugging).
- **The installed system is clean**: those live conveniences (along with the default passwordless SDDM autologin) only exist in the live session; the installer resets / clears them on install, so the installed system goes back to KDE's normal defaults — login needs a password, sudo needs authorization, and sleep/lock behave normally.
- **Out-of-the-box details**: PipeWire audio, networking connects on boot, and MAKEOPTS / CPU instruction sets adapt to your machine.

For actually installing a system, following the [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:AMD64) step by step is the more solid route; the live ISO also ships a graphical installer (Calamares) if you want a quick install.

## The installer (Calamares)

The installer config lives in [Gentoo-zh/calamares-settings-gig](https://github.com/Gentoo-zh/calamares-settings-gig): after an install it clears out the live-only leftover settings and configures NVIDIA according to the GPU option you chose in the live session. The install flow has been tested with a real QEMU install.

## The overlay the Live ISO uses

The packages the Live ISO builds from come from [Gentoo-zh/gig](https://github.com/Gentoo-zh/gig) — a fork of the Gig OS overlay, specific to the Live ISO, and *not* the same thing as the community's main overlay, [gentoo-zh](https://github.com/microcai/gentoo-zh). This round updated its Calamares to 3.3.14-r8 (which supports Python 3.14), fixed an `emerge --sync` error, and cleaned out a batch of redundant / broken packages.

## Build and release

The build pipeline, [Zakkaus/gentoozh-liveiso-infra](https://github.com/Zakkaus/gentoozh-liveiso-infra): the Live ISO is compiled automatically every Monday, uploaded to the download site, and the landing page re-rendered. The pipeline does a byte-for-byte check that "what's on the download site == what was just built", and only publishes when they match; it also copes with the USE / keyword churn of a rolling-tree transition automatically (see the [Python 3.14](/posts/2026-06-01-python-314-default/) post).

## Website

The website, [www.gentoo.org.cn](https://www.gentoo.org.cn/) (source: [gentoo-zh.github.io](https://github.com/Gentoo-zh/gentoo-zh.github.io)), migrated from Blowfish to Hextra — lighter, faster, and friendlier to docs and text browsers (details in the [migration post](/posts/2026-05-29-migrate-to-hextra/)). The presentation layer was split out into a standalone Hextra patch package, [gentoozh-theme](https://github.com/Gentoo-zh/gentoozh-theme), which also rounded out SEO, the footer, and accessibility. The download page was wired up to the download site, with notes on the Live ISO's features and hardware requirements, plus a new FAQ page. This round also added **English** to the public pages, so you can switch between Simplified / Traditional / English.

## Download site

The download site, [mirror.gentoozh.org](https://mirror.gentoozh.org/) (source: [Zakkaus/gentoozh-mirror](https://github.com/Zakkaus/gentoozh-mirror)): the landing page and the usage guide were reworked into Simplified / Traditional / English (with the i18n pulled into a shared module), it supports light / dark mode, cross-links with the speedtest site, and gained a Telegram channel link and an MIT license; it also fixed the SHA256 checksum overflowing sideways on mobile.

## Speedtest site

The speedtest site, [speed.gentoozh.org](https://speed.gentoozh.org/) ([Zakkaus/gentoozh-speed](https://github.com/Zakkaus/gentoozh-speed)): a custom LibreSpeed-based speed test page, also in Simplified / Traditional / English.

---

Want to try the Live ISO? Head to the [download page](/download/). Questions are welcome on [Telegram](https://t.me/gentoo_zh) or each project's GitHub.
