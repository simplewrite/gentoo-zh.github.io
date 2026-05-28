#!/usr/bin/env python3
"""
更新貢獻者資訊腳本
- 從 GitHub API 抓取貢獻者列表和詳細資訊
- 下載並轉換頭像為 WebP 格式
- 更新每位貢獻者的提交次數、部落格、X (Twitter) 等資訊
- 自動計算權重用於排序

使用方法:
    python3 scripts/update-contributors.py [選項]

選項:
    --min-commits N    只處理提交次數 >= N 的貢獻者 (預設: 10)
    --skip-avatars     跳過頭像下載
    --skip-info        跳過個人資訊更新
    --commits-only     只更新提交次數和權重 (CI 排程用)
    --dry-run          只顯示會做什麼，不實際修改檔案
"""

import argparse
import json
import re
import subprocess
import tempfile
import time
import yaml
from datetime import datetime, timezone
from pathlib import Path

CONTENT_DIR = Path("content/contributors")
CONFIG_FILE = Path(__file__).parent / "contributors-config.yaml"

# 重試設定
MAX_RETRIES = 4
BACKOFF_BASE = 2  # 秒；指數退避 2 / 4 / 8 / 16

# curl 超時
CURL_TIMEOUT = 30


def load_config():
    """從配置檔載入設定，提供預設值"""
    default_config = {
        'repository': 'microcai/gentoo-zh',
        'min_commits': 10,
        'blocklist': [],
        'avatar_sizes': {'card': 200, 'single': 240},
    }

    if not CONFIG_FILE.exists():
        print(f"警告: 配置檔 {CONFIG_FILE} 不存在，使用預設配置")
        return default_config

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
        for key, value in default_config.items():
            config.setdefault(key, value)
        return config
    except Exception as e:
        print(f"警告: 讀取配置檔失敗: {e}，使用預設配置")
        return default_config


config = load_config()
REPO = config['repository']
AVATAR_SIZES = config['avatar_sizes']
MIN_COMMITS_DEFAULT = config['min_commits']
BLOCKLIST = set(config['blocklist'])


def run_command(cmd, check=True, timeout=None):
    """執行命令並回傳結果"""
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
        timeout=timeout,
    )


def run_with_retry(cmd, *, what, allow_empty=False, timeout=60):
    """帶指數退避重試的命令執行。回傳 stdout（已 .strip()）

    用於 gh api 等可能 rate-limit 或 5xx 的呼叫。
    """
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = run_command(cmd, check=True, timeout=timeout)
            out = result.stdout
            if not allow_empty and not out.strip():
                raise RuntimeError(f"{what}: 空白輸出")
            return out
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, RuntimeError) as e:
            last_err = e
            if attempt < MAX_RETRIES:
                wait = BACKOFF_BASE ** attempt
                stderr = getattr(e, 'stderr', '') or ''
                msg = stderr.strip()[:200] if stderr else str(e)[:200]
                print(f"  {what} 第 {attempt} 次失敗（{msg}），{wait}s 後重試…")
                time.sleep(wait)
    raise RuntimeError(f"{what} 重試 {MAX_RETRIES} 次後仍失敗: {last_err}")


def parse_json(text, what):
    """解析 JSON，失敗時帶上下文重新拋出"""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        head = text[:300].replace('\n', ' ')
        raise RuntimeError(f"{what}: JSON 解析失敗 ({e})；前 300 字元: {head!r}")


def atomic_write_text(path: Path, content: str):
    """原子寫入：先寫入暫存檔，fsync 後 rename。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        import os
        with open(tmp_fd, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            Path(tmp_name).unlink()
        except FileNotFoundError:
            pass
        raise


def fetch_contributors():
    """從 GitHub 取得貢獻者列表（自動分頁，有重試）"""
    print("正在取得貢獻者列表...")

    contributors = []
    page = 1
    while True:
        out = run_with_retry(
            ['gh', 'api', f'/repos/{REPO}/contributors?per_page=100&page={page}'],
            what=f"取得第 {page} 頁貢獻者",
            allow_empty=True,
        )
        data = parse_json(out, f"contributors page {page}")
        if not data:
            break
        contributors.extend(data)
        print(f"  已取得第 {page} 頁: {len(data)} 位貢獻者")
        page += 1
        if page > 50:
            # 避免極端意外的無窮迴圈（GitHub 最多回傳 500 位的 default API）
            print("  警告: 已達分頁上限 50，提早結束")
            break

    print(f"總共找到 {len(contributors)} 位貢獻者\n")
    return contributors


def fetch_user_info(login):
    """取得使用者詳細資訊。404 時回傳僅含 login 的 dict。"""
    try:
        out = run_with_retry(
            ['gh', 'api', f'/users/{login}'],
            what=f"取得 {login} 個人資訊",
        )
        return parse_json(out, f"user {login}")
    except RuntimeError as e:
        # 帳號可能被刪除，退回到只用 login
        print(f"  警告: 無法取得 {login} 詳細資訊（{e}），僅以 login 為名稱")
        return {'login': login}


def update_index_timestamp(dry_run=False):
    """更新索引頁的時間戳"""
    now_utc = datetime.now(timezone.utc)
    timestamp = now_utc.strftime("%Y年%m月%d日 %H:%M UTC")

    updated = False
    for lang in ('zh-cn', 'zh-tw'):
        file_path = CONTENT_DIR / f"_index.{lang}.md"
        if not file_path.exists():
            print(f"  警告: {file_path} 不存在")
            continue

        content = file_path.read_text(encoding='utf-8')
        if lang == 'zh-tw':
            label = f'最後更新時間 {timestamp}（每週一自動更新）'
        else:
            label = f'最后更新时间 {timestamp}（每周一自动更新）'

        new_content, count = re.subn(
            r'最[後后]更新[時时][間间].*',
            label,
            content,
        )
        if count == 0:
            # 沒有時間戳行，附加到檔尾
            new_content = content.rstrip() + '\n\n' + label + '\n'

        if new_content != content:
            if not dry_run:
                atomic_write_text(file_path, new_content)
                print(f"  已更新 {file_path.name} 的時間戳")
            else:
                print(f"  [DRY-RUN] 會更新 {file_path.name} 的時間戳為: {timestamp}")
            updated = True

    return updated


def download_and_convert_avatar(login, avatar_url, dry_run=False):
    """下載並轉換頭像為 WebP（多尺寸）。失敗時不破壞既有檔案。"""
    contrib_dir = CONTENT_DIR / login

    if dry_run:
        print(f"  [DRY-RUN] 會下載頭像: {avatar_url}")
        return

    contrib_dir.mkdir(parents=True, exist_ok=True)

    # 用 mkstemp 避免並行 / 殘留問題
    fd, temp_path = tempfile.mkstemp(
        prefix=f".avatar_{login}_",
        suffix=".png",
        dir=str(contrib_dir),
    )
    import os
    os.close(fd)
    temp_avatar = Path(temp_path)

    try:
        try:
            run_command(
                ['curl', '-sSLf', '--max-time', str(CURL_TIMEOUT),
                 '-o', str(temp_avatar), avatar_url],
                check=True,
                timeout=CURL_TIMEOUT + 5,
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"  警告: 下載 {login} 頭像失敗（{e}），跳過頭像處理")
            return

        if not temp_avatar.exists() or temp_avatar.stat().st_size == 0:
            print(f"  警告: {login} 頭像檔為空，跳過")
            return

        for size_name, size in AVATAR_SIZES.items():
            output_file = contrib_dir / f"avatar_{size_name}.webp"
            # 先寫到暫存檔再 rename 以保留舊版直到新版完成
            tmp_out = output_file.with_suffix('.webp.tmp')
            try:
                run_command(
                    ['cwebp', '-quiet', '-q', '90',
                     '-resize', str(size), str(size),
                     str(temp_avatar), '-o', str(tmp_out)],
                    check=True,
                    timeout=30,
                )
                os.replace(str(tmp_out), str(output_file))
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"  警告: 轉換 {login} {size_name} 失敗（{e}）")
                try:
                    tmp_out.unlink()
                except FileNotFoundError:
                    pass
    finally:
        try:
            temp_avatar.unlink()
        except FileNotFoundError:
            pass


def update_commits_only(login, commits, dry_run=False):
    """只更新提交次數與權重"""
    contrib_dir = CONTENT_DIR / login
    weight = 10000 - commits

    updated = False
    for lang in ('zh-cn', 'zh-tw'):
        file_path = contrib_dir / f"index.{lang}.md"
        if not file_path.exists():
            continue

        content = file_path.read_text(encoding='utf-8')

        new_content = re.sub(
            r'^weight: \d+',
            f'weight: {weight}',
            content,
            flags=re.MULTILINE,
        )
        new_content = re.sub(
            r'\d+ 次提交',
            f'{commits} 次提交',
            new_content,
        )

        if new_content != content:
            if not dry_run:
                atomic_write_text(file_path, new_content)
            updated = True

    return updated


def generate_frontmatter(login, name, links, weight, tag, commits):
    """產生貢獻者頁的 frontmatter + 內容"""
    lines = [
        '---',
        f'title: "{name}"',
        f"tags: ['{tag}']",
        f'externalUrl: "https://github.com/{login}"',
    ]
    if links:
        lines.append('links:')
        for link in links:
            lines.append(f'  - name: "{link["name"]}"')
            lines.append(f'    url: "{link["url"]}"')
    lines.extend([
        f'weight: {weight}',
        'showDate: false',
        'showAuthor: false',
        'showReadingTime: false',
        'showEdit: false',
        'showLikes: false',
        'showViews: false',
        'layoutBackgroundHeaderSpace: false',
        '---',
        '',
        f'{commits} 次提交',
        '',
    ])
    return '\n'.join(lines)


def create_contributor_page(login, user_data, commits, dry_run=False):
    """建立或更新貢獻者頁（首次建立用）"""
    contrib_dir = CONTENT_DIR / login

    name = user_data.get('name') or login
    blog = (user_data.get('blog') or '').strip()
    twitter = (user_data.get('twitter_username') or '').strip()

    links = []
    if blog:
        if not blog.startswith(('http://', 'https://')):
            blog = 'https://' + blog
        links.append({'name': 'blog', 'url': blog})
    if twitter:
        # Twitter 已 rebrand 為 X
        links.append({'name': 'twitter', 'url': f'https://x.com/{twitter}'})

    weight = 10000 - commits
    tag_cn = "Overlay 贡献者"
    tag_tw = "Overlay 貢獻者"

    if dry_run:
        print(f"  [DRY-RUN] 會建立/更新: {login} ({name})")
        print(f"    提交: {commits}, 權重: {weight}, 標籤: {tag_cn}")
        if links:
            print(f"    連結: {', '.join(l['name'] for l in links)}")
        return

    contrib_dir.mkdir(parents=True, exist_ok=True)

    for lang, tag in (('zh-cn', tag_cn), ('zh-tw', tag_tw)):
        file_path = contrib_dir / f"index.{lang}.md"
        atomic_write_text(file_path, generate_frontmatter(
            login, name, links, weight, tag, commits))


def main():
    parser = argparse.ArgumentParser(
        description='更新 Gentoo 中文社群貢獻者資訊',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--min-commits', type=int, default=MIN_COMMITS_DEFAULT,
                        help=f'只處理提交次數 >= N 的貢獻者 (預設: {MIN_COMMITS_DEFAULT})')
    parser.add_argument('--skip-avatars', action='store_true', help='跳過頭像下載')
    parser.add_argument('--skip-info', action='store_true', help='跳過個人資訊更新')
    parser.add_argument('--commits-only', action='store_true',
                        help='只更新提交次數和權重，不修改標籤、連結等')
    parser.add_argument('--dry-run', action='store_true',
                        help='只顯示會做什麼，不實際修改檔案')

    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN 模式 ===\n")

    contributors = fetch_contributors()

    filtered = [
        c for c in contributors
        if c['contributions'] >= args.min_commits and c['login'] not in BLOCKLIST
    ]
    excluded = [c['login'] for c in contributors if c['login'] in BLOCKLIST]
    if excluded:
        print(f"已屏蔽使用者: {', '.join(excluded)}")
    print(f"過濾後剩餘 {len(filtered)} 位貢獻者 (>= {args.min_commits} 次提交)\n")

    updated_count = 0
    skipped_count = 0
    failed_count = 0

    for contrib in filtered:
        login = contrib['login']
        commits = contrib['contributions']
        avatar_url = contrib['avatar_url']

        print(f"處理 {login} ({commits} 次提交)...")

        try:
            if args.commits_only:
                contrib_dir = CONTENT_DIR / login
                if not contrib_dir.exists():
                    print(f"  [新貢獻者] 建立頁面...")
                    user_data = fetch_user_info(login)
                    download_and_convert_avatar(login, avatar_url, args.dry_run)
                    create_contributor_page(login, user_data, commits, args.dry_run)
                    updated_count += 1
                elif update_commits_only(login, commits, args.dry_run):
                    updated_count += 1
                    weight = 10000 - commits
                    print(f"  更新: 提交 {commits}, 權重 {weight}")
                else:
                    skipped_count += 1
                continue

            user_data = {'login': login} if args.skip_info else fetch_user_info(login)

            if not args.skip_avatars:
                download_and_convert_avatar(login, avatar_url, args.dry_run)

            if not args.skip_info:
                create_contributor_page(login, user_data, commits, args.dry_run)

            updated_count += 1
        except Exception as e:
            print(f"  錯誤: {e}")
            failed_count += 1
            continue

    print(f"\n正在更新索引頁時間戳...")
    update_index_timestamp(args.dry_run)

    print(f"\n{'=' * 50}")
    print(f"完成！")
    print(f"  已更新: {updated_count} 位")
    if skipped_count > 0:
        print(f"  無變化: {skipped_count} 位")
    if failed_count > 0:
        print(f"  失敗:   {failed_count} 位")

    if args.dry_run:
        print("\n(這是 DRY RUN，沒有實際修改任何檔案)")

    # 有失敗時以非零退出，讓 CI 顯示警示
    if failed_count > 0:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
