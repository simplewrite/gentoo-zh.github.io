#!/bin/bash
#
# Convert a zh-cn source file to zh-tw using OpenCC s2twp + targeted sed fixes.
#
# Notes on rule selection:
#   - OpenCC s2twp already converts most simplified->traditional + Taiwan
#     phrases (软件->軟體, 内存->記憶體, etc.). We do NOT duplicate those.
#   - Only add rules for terms that OpenCC misses or converts wrong for
#     this site's domain (Gentoo/Linux/Hugo).
#   - Do NOT add a blanket s/包/套件/g — it breaks 包含/包括/打包/包装.
#   - Do NOT add a blanket s/文件/檔案/g — OpenCC converts 文档->文件
#     (documentation); we keep 文件 as documentation.
#   - Cleanup pass at the end fixes known OpenCC phrase-dict artifacts.

set -euo pipefail

SOURCE_FILE=${1:-}
TARGET_FILE=${2:-}

export PATH="/opt/homebrew/bin:$PATH"

# 可移植的就地编辑：GNU sed（Linux / CI）用 `-i`，BSD/macOS sed 用 `-i ''`。
if sed --version >/dev/null 2>&1; then SEDI=(-i); else SEDI=(-i ''); fi

if [ -z "$SOURCE_FILE" ] || [ -z "$TARGET_FILE" ]; then
    echo "Usage: $0 <source_file> <target_file>" >&2
    exit 1
fi

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: source file '$SOURCE_FILE' not found" >&2
    exit 1
fi

# Step 1: OpenCC base conversion (simplified -> traditional w/ Taiwan phrases)
if command -v opencc &> /dev/null; then
    opencc -c s2twp -i "$SOURCE_FILE" -o "$TARGET_FILE"
else
    echo "Warning: opencc not found, falling back to cp." >&2
    cp "$SOURCE_FILE" "$TARGET_FILE"
fi

# Step 2: Domain-specific replacements OpenCC may miss.
# Keep this list short and word-specific. Multi-char phrases first to avoid
# greedy single-char matches.

sed "${SEDI[@]}" \
  -e 's/分区/分割/g' \
  -e 's/挂载/掛載/g' \
  -e 's/卸载/卸載/g' \
  -e 's/编译/編譯/g' \
  -e 's/源码/原始碼/g' \
  -e 's/源代码/原始碼/g' \
  -e 's/守护进程/守護程式/g' \
  -e 's/进程/行程/g' \
  -e 's/线程/執行緒/g' \
  -e 's/插件/外掛/g' \
  -e 's/脚本/指令碼/g' \
  -e 's/链接/連結/g' \
  -e 's/U盘/隨身碟/g' \
  -e 's/优盘/隨身碟/g' \
  -e 's/优化/最佳化/g' \
  -e 's/视频/影片/g' \
  -e 's/音频/音訊/g' \
  -e 's/接口/介面/g' \
  -e 's/界面/介面/g' \
  -e 's/分辨率/解析度/g' \
  -e 's/端口/連接埠/g' \
  -e 's/服务器/伺服器/g' \
  -e 's/客户端/客戶端/g' \
  -e 's/虚拟机/虛擬機/g' \
  -e 's/数据库/資料庫/g' \
  -e 's/算法/演算法/g' \
  -e 's/缓存/快取/g' \
  -e 's/网络/網路/g' \
  -e 's/网卡/網路卡/g' \
  -e 's/声卡/音效卡/g' \
  -e 's/键盘/鍵盤/g' \
  -e 's/鼠标/滑鼠/g' \
  -e 's/屏幕/螢幕/g' \
  -e 's/硬盘/硬碟/g' \
  -e 's/磁盘/磁碟/g' \
  -e 's/操作系统/作業系統/g' \
  -e 's/教程/教學/g' \
  -e 's/示例/範例/g' \
  -e 's/示範/範例/g' \
  -e 's/调试器/除錯器/g' \
  -e 's/调试/除錯/g' \
  -e 's/中转/中轉/g' \
  -e 's/性能/效能/g' \
  -e 's/兼容/相容/g' \
  -e 's/构建/構建/g' \
  -e 's/依赖/依賴/g' \
  -e 's/仓库/倉庫/g' \
  -e 's/项目/專案/g' \
  -e 's/账户/帳戶/g' \
  -e 's/默认/預設/g' \
  -e 's/计划/計畫/g' \
  -e 's/博客/部落格/g' \
  -e 's/字体/字型/g' \
  -e 's/布局/佈局/g' \
  -e 's/数据/資料/g' \
  -e 's/信息/資訊/g' \
  -e 's/信号/訊號/g' \
  -e 's/重定向/重新導向/g' \
  -e 's/环境变量/環境變數/g' \
  -e 's/变量/變數/g' \
  -e 's/函数/函式/g' \
  -e 's/参数/參數/g' \
  -e 's/选项/選項/g' \
  -e 's/返回值/回傳值/g' \
  -e 's/模块/模組/g' \
  -e 's/组件/元件/g' \
  -e 's/进阶/進階/g' \
  -e 's/查找/搜尋/g' \
  -e 's/命令/指令/g' \
  -e 's/终端/終端機/g' \
  -e 's/同步/同步/g' \
  -e 's/固件/韌體/g' \
  -e 's/电源/電源/g' \
  -e 's/电池/電池/g' \
  -e 's/主板/主機板/g' \
  -e 's/设备/裝置/g' \
  -e 's/路径/路徑/g' \
  -e 's/权限/權限/g' \
  -e 's/所有者/擁有者/g' \
  -e 's/根目录/根目錄/g' \
  -e 's/工作目录/工作目錄/g' \
  -e 's/目录/目錄/g' \
  -e 's/临时/暫時/g' \
  -e 's/解压/解壓/g' \
  -e 's/压缩/壓縮/g' \
  -e 's/传输/傳輸/g' \
  -e 's/启动/啟動/g' \
  -e 's/重启/重啟/g' \
  -e 's/登录/登入/g' \
  -e 's/注销/登出/g' \
  -e 's/连接/連線/g' \
  -e 's/断开/中斷/g' \
  -e 's/上传/上傳/g' \
  -e 's/下载/下載/g' \
  -e 's/创建/建立/g' \
  -e 's/删除/刪除/g' \
  -e 's/复制/複製/g' \
  -e 's/粘贴/貼上/g' \
  -e 's/保存/儲存/g' \
  -e 's/隐藏/隱藏/g' \
  -e 's/开启/開啟/g' \
  -e 's/关闭/關閉/g' \
  -e 's/编辑器/編輯器/g' \
  -e 's/编辑/編輯/g' \
  -e 's/编译器/編譯器/g' \
  -e 's/手册/手冊/g' \
  -e 's/制作/製作/g' \
  -e 's/简化/簡化/g' \
  -e 's/延伸阅读/延伸閱讀/g' \
  -e 's/结语/結語/g' \
  -e 's/可参考/可參考/g' \
  -e 's/著称/著稱/g' \
  -e 's/有线/有線/g' \
  -e 's/无线/無線/g' \
  -e 's/虚拟/虛擬/g' \
  -e 's/架构/架構/g' \
  -e 's/驱动/驅動/g' \
  -e 's/通过/透過/g' \
  -e 's/支持/支援/g' \
  -e 's/软件/軟體/g' \
  -e 's/硬件/硬體/g' \
  -e 's/内存/記憶體/g' \
  -e 's/内核/核心/g' \
  -e 's/显卡/顯示卡/g' \
  -e 's/顯卡/顯示卡/g' \
  -e 's/社区/社群/g' \
  -e 's/用户/使用者/g' \
  -e 's/用户组/使用者群組/g' \
  -e 's/文件系统/檔案系統/g' \
  -e 's/环境/環境/g' \
  -e 's/设置/設定/g' \
  -e 's/系统/系統/g' \
  -e 's/安装/安裝/g' \
  -e 's/注释/註釋/g' \
  -e 's/绑定/繫結/g' \
  -e 's/映射/對應/g' \
  "$TARGET_FILE"

# Step 3: Cleanup pass — fix OpenCC s2twp + sed phrase-dict artifacts.
# These run AFTER all substitutions above to undo known over-conversions.

sed "${SEDI[@]}" \
  -e 's/使用者名稱稱/使用者名稱/g' \
  -e 's/套件含/包含/g' \
  -e 's/套件括/包括/g' \
  -e 's/套件圍/包圍/g' \
  -e 's/打套件/打包/g' \
  -e 's/字地化/本地化/g' \
  -e 's/檔案翻譯/文件翻譯/g' \
  -e 's/中文檔案/中文文件/g' \
  -e 's/Overlay 檔案/Overlay 文件/g' \
  -e 's/映象/鏡像/g' \
  -e 's/映像源/鏡像源/g' \
  -e 's/映像列表/鏡像列表/g' \
  -e 's/解除安裝/卸載/g' \
  -e 's/軟體包/軟體套件/g' \
  -e 's/安裝包/安裝套件/g' \
  -e 's/包管理器/套件管理器/g' \
  -e 's/包管理/套件管理/g' \
  -e 's/包依賴/套件依賴/g' \
  -e 's/包安裝/套件安裝/g' \
  -e 's/包名/套件名/g' \
  -e 's/包列表/套件列表/g' \
  -e 's/包版本/套件版本/g' \
  -e 's/包源/套件源/g' \
  "$TARGET_FILE"

# Step 4: Mirror-source localization for Taiwan (TWAREN).
# Only fires when the source file references the BFSU mirror.

sed "${SEDI[@]}" \
  -e 's|https://mirrors\.bfsu\.edu\.cn/gentoo/releases/amd64/autobuilds/|http://ftp.twaren.net/Linux/Gentoo/releases/amd64/autobuilds/|g' \
  -e 's|GENTOO_MIRRORS="https://mirrors\.bfsu\.edu\.cn/gentoo/"|GENTOO_MIRRORS="http://ftp.twaren.net/Linux/Gentoo/"|g' \
  -e 's|sync-uri = https://mirrors\.bfsu\.edu\.cn/git/gentoo-portage\.git|sync-uri = https://github.com/gentoo-mirror/gentoo.git|g' \
  -e 's|以 BFSU 鏡像站|以 TWAREN 鏡像站|g' \
  "$TARGET_FILE"

# Step 4b: Terminology localization for Taiwan readers.
# 简体的「国内」对台湾读者指的是台湾；繁体版改用「中国内陆」把所指说清楚。
# 先用占位符保护「國內外」（国内外）以免被误伤成「中國內陸外」。
sed "${SEDI[@]}" \
  -e 's/國內外/GUONEIWAI_KEEP/g' \
  -e 's/國內/中國內陸/g' \
  -e 's/GUONEIWAI_KEEP/國內外/g' \
  "$TARGET_FILE"

# Step 5: Strip /zh-tw suffix from Gentoo wiki links (no Taiwan locale exists)
sed "${SEDI[@]}" \
  -e 's|wiki.gentoo.org/wiki/\([^)]*\)/zh-tw)|wiki.gentoo.org/wiki/\1)|g' \
  -e 's|wiki.gentoo.org/wiki/\([^)]*\)/zh-tw#|wiki.gentoo.org/wiki/\1#|g' \
  "$TARGET_FILE"

echo "Converted: $SOURCE_FILE -> $TARGET_FILE"
