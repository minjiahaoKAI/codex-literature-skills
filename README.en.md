# Zotero → Obsidian Literature Reading Skills

[简体中文](README.md) | **English**

Two standalone skills for use with Codex on your own computer:

- `life-science-literature-card`: create initial reading cards, graphical abstracts, and logic maps from Zotero PDFs and full text extracted with MinerU.
- `life-science-reading-session`: discuss a paper using its PDF, Zotero highlights, and existing card, then integrate the reading notes when requested.

The skills produce Chinese-first literature notes. This page provides the setup and usage guide in English.

The package does not include Zotero data, an Obsidian vault, the MinerU CLI, API tokens, or the author's local configuration. The default vault folders are `文献笔记` (literature notes), `图片资源/literature_cards` (image assets), and `sources/mineru`. You can choose other relative folders when installing a card. The optional Obsidian Bases card-wall view and CSS snippet are in `skills/life-science-literature-card/assets/card-wall/`.

## Install the skills on Windows

You need Codex, Zotero Desktop, Obsidian, and Python 3.10 or later. Create or open your own vault in Obsidian first.

Ask Codex:

> Use `$skill-installer` to install `skills/life-science-literature-card` and `skills/life-science-reading-session` from `https://github.com/minjiahaoKAI/codex-literature-skills`. Confirm that both skills are available after installation. Do not copy anyone else's Zotero data, Obsidian vault, or credentials.

You can also download the repository and place both complete folders from `skills/` in `C:\Users\<username>\.agents\skills\` on your computer. Restart Codex if they do not appear immediately. Copy the complete folders: the card skill also needs its `references/` and `scripts/` resources.

## Configure your local sources

1. Start Zotero Desktop and confirm that you can open the paper's local PDF. If a Zotero integration is unavailable, you can give Codex the PDF path to start an initial reading card.
2. Give Codex the absolute path to your own Obsidian vault, or set the local `OBSIDIAN_VAULT_PATH` environment variable. Keep your actual local paths out of the public repository.
3. Install the MinerU Open API CLI and configure a token for your own account, as described below.
4. For automated access to Zotero highlights, you may also install [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp). This is optional and has its own note layout and writing workflow. Check the destination folders before asking Codex to use its writing tools.

## Add the literature card wall (optional)

The literature card wall uses Obsidian's built-in **Bases** Cards view. Ask Codex to follow the [card-wall setup guide](skills/life-science-literature-card/references/card-wall-setup.md), place the two `Literature_Card_Wall` files in your literature notes folder, and place the CSS snippet in your vault's `.obsidian/snippets/` folder. Enable the snippet under **Settings → Appearance → CSS snippets**. Only the three reusable files supplied by this repository are needed.

You can ask Codex:

> Update the `life-science-literature-card` skill I installed from `https://github.com/minjiahaoKAI/codex-literature-skills`. Follow its `references/card-wall-setup.md` to add the literature card wall to my Obsidian vault using the three bundled files in `assets/card-wall/`. First confirm my vault path and that Bases is enabled. If destination files already exist, compare them and preserve the originals. After installation, open `Literature_Card_Wall.base` and check the covers, summaries, and links of my existing cards.

## Ask Codex to install MinerU

Send this prompt to **Codex on your own computer**:

> On my Windows computer, first check whether `mineru-open-api` is installed. If it is missing, check the [official MinerU CLI installation guide](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md), download and inspect the official Windows installer, then install the Open API CLI. Verify it with `mineru-open-api version`. Do not substitute the full local MinerU model installation or run scripts from unknown sources. Then give me the [MinerU token page](https://mineru.net/apiManage/token) so I can sign in and generate my own token. Do not ask me to paste the token into chat, read or print it, or save it in the repository or workspace. Guide me through running `mineru-open-api auth` in my local terminal and entering the token at its prompt, then running `mineru-open-api auth --verify` to check its local format. Do not upload a paper PDF for testing unless I explicitly agree.

The Windows installation command documented for this package is `irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex`. Ask Codex to check the official source and inspect the script before running it. The CLI reads the token from `MINERU_TOKEN` or `.mineru/config.yaml` in your user directory. `auth --verify` checks the token format locally; a successful online extraction still needs to be confirmed with `extract` after you approve uploading a PDF.

## Verify the workflow

Ask Codex to run the complete workflow with a PDF from your Zotero library that you permit it to send to MinerU: locate the source → run precision extraction → generate the card, PNG, and SVG in a staging workspace → run the installer with `--dry-run` → install after any required vault-write approval → open the note in Obsidian and check both images. Then use the reading-session skill to ask about a specific figure or method and check its answer against the paper.

This repository is released under the [MIT License](LICENSE). Keep actual papers, images, annotations, vault contents, `.mineru/`, tokens, local configuration, and generated reading cards out of this repository.

## References

- [Install and distribute Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [MinerU Open API CLI](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md)
- [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp)
