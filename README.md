# Zotero → Obsidian 文献阅读 Skills

**简体中文** | [English](README.en.md)

这是一套供 Codex 本地使用的两个独立 skill：

- `life-science-literature-card`：分拣摘要、生成完整卡片、升级已有卡片、批量处理 Zotero 集合，或只重做 AI 图表摘要封面。
- `life-science-reading-session`：围绕 PDF、Zotero 高亮和已有卡片进行精读问答，并在用户要求时整合笔记。

文献笔记默认以中文为主；[英文版说明](README.en.md) 提供对应的安装与使用指南。

两个 skill 不包含 Zotero 数据、Obsidian Vault、MinerU CLI、API token 或作者本机配置。默认在 Vault 中使用 `文献笔记`、`图片资源/literature_cards` 和 `sources/mineru`；可在安装卡片时选择其他相对目录。可选的 Obsidian Bases 卡片墙视图和 CSS snippet 位于 `skills/life-science-literature-card/assets/card-wall/`。

## v2 日常使用

- “快速看看这篇”：分拣卡，只读元数据/摘要，不调用 MinerU。
- “做完整卡片”：全文卡，按研究类型核对证据；复杂型先画全文证据地图。
- “处理集合中还没做卡片的论文”：先列出数量、档位和封面选项，确认后开始。
- “升级这张分拣卡”：保留精读状态和用户记录，补齐全文与封面。
- “只重新生成封面”：复用已保存 brief，更新封面和生成记录。

默认封面采用白灰为主、少量低饱和颜色区分模块的期刊图表摘要风格，中文标签。按论文故事选择布局，以来源核验的统计量、结论示意图和简短文字呈现发现；不要求每篇使用相同版式。文字、科学方向、数字、证据类型、未测器官和卡通化元素是硬性检查；字号与面积只作参考。通常每张生成一次，最多两次，仅硬性失败允许第三次。每张记录耗时与调用次数。辅助 SVG 和封面共享色值，数字需核验来源。

新卡有 `card_tier`、`study_type`、`verdict`、`date_added`；旧卡无需迁移仍能显示。安装器支持备份更新、跳过已有条目和批量失败隔离。详细流程见 [skill](skills/life-science-literature-card/SKILL.md)，实施验收见 [v2 review](docs/v2-review.md)。

## 在 Windows 上安装 skill

需要 Codex、Zotero Desktop、Obsidian，以及 Python 3.10 或更新版本。先在 Obsidian 中创建或打开自己的 Vault。

在你的 Codex 中说：

> 用 `$skill-installer` 从 `https://github.com/minjiahaoKAI/codex-literature-skills` 安装 `skills/life-science-literature-card` 和 `skills/life-science-reading-session`。安装后确认两个 skill 可见，不要复制任何人的 Zotero 数据、Obsidian Vault 或密钥。

也可以下载仓库并把 `skills/` 下的两个完整文件夹放进你电脑上的 `C:\Users\<用户名>\.agents\skills\`。如果 Codex 没有立即显示，重启 Codex。请勿只复制 `SKILL.md`；卡片 skill 还依赖 `references/` 和 `scripts/`。

## 配置本机来源

1. 在你的电脑上启动 Zotero Desktop，确认目标论文有可打开的本地 PDF。没有 Zotero 集成时，直接把 PDF 路径交给 Codex 也能开始初读卡片。
2. 告诉 Codex 你自己的 Obsidian Vault 绝对路径，或在本机设置 `OBSIDIAN_VAULT_PATH` 环境变量。不要把真实路径提交到 GitHub。
3. 安装 MinerU Open API CLI，并使用你自己的账号配置 token（见下方 MinerU 安装说明）。
4. 如果希望自动读取 Zotero 高亮，可以另装 [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp)。这是可选依赖；它有独立的笔记布局和写入流程。先确认两者目标目录，再让 Codex 使用它的写入功能。

## 添加文献卡片墙（可选）

文献卡片墙使用 Obsidian 内置的 **Bases** 卡片视图。让 Codex 读取 [卡片墙安装说明](skills/life-science-literature-card/references/card-wall-setup.md)，把两份 `Literature_Card_Wall` 文件放入你自己的文献笔记目录，把 CSS snippet 放入你自己的 `.obsidian/snippets/`，然后在 Obsidian 的「设置 → 外观 → CSS 代码片段」中启用它。只需安装仓库附带的三个可复用文件。

可以直接对你的 Codex 说：

> 请更新我从 `https://github.com/minjiahaoKAI/codex-literature-skills` 安装的 `life-science-literature-card` skill，并按照其中的 `references/card-wall-setup.md`，用仓库附带的三个 `assets/card-wall/` 文件，在我的 Obsidian Vault 中添加文献卡片墙。先确认我的 Vault 路径和 Bases 已启用；若目标文件已存在，先比较并保留原文件。安装后打开 `Literature_Card_Wall.base`，检查现有卡片的封面、摘要和跳转。

## 告诉 Codex 安装 MinerU

把下面这段发给**你自己的 Codex**：

> 请在我的 Windows 电脑上，先确认是否已有 `mineru-open-api`。如果没有，请核对 [MinerU 官方 CLI 安装说明](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md)，下载并检查官方 Windows 安装脚本，然后安装 CLI；用 `mineru-open-api version` 验证。不要安装完整的本地 MinerU 模型来替代这个 Open API CLI，也不要运行来源不明的脚本。安装后给我 [MinerU token 页面](https://mineru.net/apiManage/token) 的链接，让我自己登录并生成 token。不要索取、读取、打印或保存我的 token 到聊天、仓库或工作区文件。指导我在本机终端运行 `mineru-open-api auth` 并按提示输入 token，再运行 `mineru-open-api auth --verify` 检查本地格式。不要上传论文 PDF 做测试，除非我明确同意。

本仓库使用的 Windows 安装命令是 `irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex`；安装前让 Codex 核对官方说明并检查脚本内容，再执行。CLI 默认从 `MINERU_TOKEN` 或用户目录下的 `.mineru/config.yaml` 读取 token。`auth --verify` 只验证 token 格式，不能证明在线解析一定成功；首次使用还需在用户同意上传 PDF 后确认 `extract` 成功。

## 验收

让 Codex 用你 Zotero 中一篇允许发送给 MinerU 的 PDF 做完整试运行：找到来源 → 精准提取 → 在工作区生成卡片、PNG 和 SVG → 安装脚本 dry run → 获得 Vault 写入权限后安装 → 在 Obsidian 中查看两个图片。再用精读 skill 询问一个具体图表或方法，并核对回答指向原文。

本仓库按 [MIT License](LICENSE) 发布。不要把真实论文、图片、注释、Vault、`.mineru/`、token、本机配置或生成的卡片加入仓库。

## 参考资料

- [Codex skill 的安装与分发](https://learn.chatgpt.com/docs/build-skills)
- [MinerU Open API CLI](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md)
- [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp)

分拣卡默认不生成封面；卡片墙使用按研究类型共享的占位图。升级为完整卡时生成专属封面。
