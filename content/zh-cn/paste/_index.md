---
title: "Paste"
---

社区自建的 pastebin,贴代码和日志。网页 [paste.gentoozh.org](https://paste.gentoozh.org),后端 [wastebin](https://github.com/matze/wastebin),命令行工具 [gzpaste](https://github.com/gentoo-zh/gzpaste)(MIT)。

{{< callout type="warning" >}}
链接是公开的,贴之前把密码、密钥、token 删干净。
{{< /callout >}}

## 网页

打开 [paste.gentoozh.org](https://paste.gentoozh.org),粘贴或把文件拖进去,选好高亮和保留时间,提交拿链接。

## 命令行

装 [`gzpaste`](https://github.com/gentoo-zh/gzpaste),需要 `curl` 和 `jq`(Gentoo 上 `emerge app-misc/jq`,其它发行版见 [jq 下载页](https://jqlang.org/download/))。装到 `~/.local/bin`,确保在 PATH 里:

```bash
mkdir -p ~/.local/bin && curl -fsSL https://gentoozh.org/gzpaste.sh -o ~/.local/bin/gzpaste && chmod +x ~/.local/bin/gzpaste
```

贴命令输出(管道进去):

```bash
emerge --info | gzpaste                    # 系统信息,求助必贴
emerge -pv app-text/gzpaste | gzpaste      # 看某个包会装什么、USE 怎么算
```

贴文件(给出路径):

```bash
gzpaste /etc/portage/make.conf                                  # 配置
gzpaste /etc/portage/package.use/00-desktop                     # USE 设置
gzpaste /var/tmp/portage/app-text/gzpaste-0.1.1/temp/build.log  # 构建失败的日志
```

Gentoo 也可以走 overlay:先加 [gentoo-zh overlay](/overlay/),再:

```bash
emerge app-text/gzpaste
```

{{% details closed="true" title="全部选项" %}}

| 选项 | 作用 |
| --- | --- |
| `-e, --ext EXT` | 语法高亮扩展名(`py`、`rs`、`sh` …);不写就是纯文本 |
| `-x, --expires 秒` | 多少秒后过期 |
| `-b, --burn` | 阅后即焚,第一次打开后删除 |
| `-p, --password 密码` | 加密,读取时带 `wastebin-password` 头 |
| `-r, --raw` | 直接输出 `/raw/` 纯文本链接 |
| `-o, --owner` | 连 owner 一起输出(之后删除要用) |
| `-h, --help` | 显示帮助 |
| `del <id> <owner>` | 删除一份 paste |

`gzpaste -h` 也一样。

{{% /details %}}

{{% details closed="true" title="免安装,直接跑" %}}

贴标准输入:

```bash
某命令 | sh -c "$(curl -fsSL https://gentoozh.org/gzpaste.sh)"
```

贴文件:

```bash
curl -fsSL https://gentoozh.org/gzpaste.sh | sh -s -- 文件
```

{{% /details %}}

{{% details closed="true" title="不装 gzpaste?原始 curl" %}}

直接用 `curl` + `jq`:

```bash
echo "内容" | jq -Rs '{text: .}' \
  | curl -s -H 'content-type: application/json' --data-binary @- https://paste.gentoozh.org/ \
  | jq -r '"https://paste.gentoozh.org" + .path'
```

完整 HTTP API 见 [wastebin 文档](https://github.com/matze/wastebin#api-endpoints)。

{{% /details %}}

## 读取

链接的 ID 前面加 `/raw/` 就是纯文本,方便脚本或 `curl` 直接读,贴的时候加 `-r` 也能直接拿到:

```bash
curl https://paste.gentoozh.org/raw/ID
```

加密的 paste,读取时把密码放在 `wastebin-password` 头里(不带密码打开只会看到密码框,内容不泄露):

```bash
curl -H 'wastebin-password: 你的密码' https://paste.gentoozh.org/raw/ID
```

## 说明

- 匿名、单份最大 10 MB、默认存 7 天(提交时可选 1 小时到 1 个月)。
- 有问题去 [关于页](/about/) 找联系方式。
