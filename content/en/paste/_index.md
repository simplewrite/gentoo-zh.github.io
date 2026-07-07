---
title: "Pastebin"
---

The community's self-hosted pastebin for code and logs. Web: [paste.gentoozh.org](https://paste.gentoozh.org); backend [wastebin](https://github.com/matze/wastebin); CLI tool [gzpaste](https://github.com/gentoo-zh/gzpaste) (MIT).

{{< callout type="warning" >}}
Links are public. Strip passwords, keys, and tokens before pasting.
{{< /callout >}}

## Web

Open [paste.gentoozh.org](https://paste.gentoozh.org), paste or drag a file in, pick highlighting and how long to keep it, then submit and copy the link.

## Command line

Install [`gzpaste`](https://github.com/gentoo-zh/gzpaste). Needs only `curl`. Goes to `~/.local/bin`, so make sure that's on your PATH:

```bash
mkdir -p ~/.local/bin && curl -fsSL https://gentoozh.org/gzpaste.sh -o ~/.local/bin/gzpaste && chmod +x ~/.local/bin/gzpaste
```

Pipe a command's output:

```bash
emerge --info | gzpaste                    # system info, always wanted when asking for help
emerge -pv app-text/gzpaste | gzpaste      # what a package pulls in / how USE resolves
```

Paste a file (give the path):

```bash
gzpaste /etc/portage/make.conf                                  # config
gzpaste /etc/portage/package.use/00-desktop                     # USE settings
gzpaste /var/tmp/portage/app-text/gzpaste-0.1.3/temp/build.log  # a failed build log
```

On Gentoo you can also use the overlay: add the [gentoo-zh overlay](/overlay/), then:

```bash
emerge app-text/gzpaste
```

{{% details closed="true" title="All options" %}}

| Option | What it does |
| --- | --- |
| `-e, --ext EXT` | syntax-highlight language, an extension or filename (see below); omit for no highlighting |
| `-x, --expires SECS` | expire after SECS seconds |
| `-b, --burn` | burn after reading (delete on first view) |
| `-p, --password PW` | encrypt (read with the `wastebin-password` header) |
| `-r, --raw` | print the `/raw/` plain-text URL |
| `-m, --md` | print the `/md/` rendered-Markdown URL |
| `-o, --owner` | also print the owner token (needed to delete later) |
| `-v, --verbose` | print progress to stderr (URL still on stdout) |
| `-h, --help` | show help |
| `-V, --version` | show version |
| `del <id> <owner>` | delete a paste |

`gzpaste -h` shows the same.

{{% /details %}}

{{% details closed="true" title="Highlight languages (178)" %}}

`-e` takes an extension or filename; the web form lists them all in a dropdown too:

```text
adb                haml               rails
adoc               hh.in              rb
adp                h.in               rd
applescript        hs                 re
as                 htm.j2             rego
asa                html               requirements.txt
asp                html.eex           resolv.conf
attributes         http               rkt
authorized_keys    idr                robot
awk                ini                rs
bat                j2                 rst
bib                java               rxml
build              jl                 sass
c                  jq                 scala
cabal              js                 scss
cfml               js.erb             sh
clj                json               show-nonprintable
CMakeCache.txt     jsonnet            slim
CMakeLists.txt     jsp                sml
cmd-help           known_hosts        sol
coffee             kt                 sources.list
COMMIT_EDITMSG     lean               sql
conf.erb           less               ssh_config
cpp                lhs                sshd_config
cpuinfo            lisp               strace
cr                 ll                 sty
cs                 log                styl
css                ls                 sv
csv                lua                svlt
d                  m                  swift
dart               .mailmap           syslog
diff               make               tab
Dockerfile         man                tcl
dot                matlab             tex
elm                md                 textile
eml                mediawiki          tf
.env               meminfo            tfstate
envvars            ml                 todo.txt
erbsql             mll                toml
erl                mly                ts
ex                 mm                 tsv
exclude            namelist           tsx
f                  nim                twig
f90                ninja              txt
fish               nix                typ
fs                 nsi                v
fstab              odin               varlink
gd                 org                vhd
.git               pas                vim
gitconfig          passwd             vs
gitlog             pb.txt             vue
git-rebase-todo    php                vy
go                 pl                 wgsl
go.mod             pp                 xml
go.sum             properties         yaml
gp                 proto              yasm
graphql            purs               yaws
groff              py                 zig
groovy             qml
group              R
```

{{% /details %}}

{{% details closed="true" title="Run without installing" %}}

Paste stdin:

```bash
some-cmd | sh -c "$(curl -fsSL https://gentoozh.org/gzpaste.sh)"
```

Paste a file:

```bash
curl -fsSL https://gentoozh.org/gzpaste.sh | sh -s -- FILE
```

{{% /details %}}

{{% details closed="true" title="Without gzpaste? Raw curl" %}}

gzpaste itself only needs curl. Doing it by hand needs [jq](https://github.com/jqlang/jq/wiki/Installation):

```bash
echo "content" | jq -Rs '{text: .}' \
  | curl -s -H 'content-type: application/json' --data-binary @- https://paste.gentoozh.org/ \
  | jq -r '"https://paste.gentoozh.org" + .path'
```

Full HTTP API in the [wastebin docs](https://github.com/matze/wastebin#api-endpoints).

{{% /details %}}

## Reading

Put `/raw/` before the id for plain text, handy for scripts or a direct `curl`; pass `-r` when pasting to get it directly:

```bash
curl https://paste.gentoozh.org/raw/ID
```

For a Markdown document, `/md/ID` shows it rendered; pass `-m` when pasting to get that link.

For an encrypted paste, pass the password in the `wastebin-password` header (without it you only get a password prompt, the content isn't exposed):

```bash
curl -H 'wastebin-password: your-password' https://paste.gentoozh.org/raw/ID
```

## Notes

- Anonymous, 10 MB per paste, kept 7 days by default (1 hour to 1 month when you submit).
- Questions? Contact channels are on the [About page](/about/).
