# Zotero �� Obsidian �����Ķ� Skills

����һ�׹� Codex ����ʹ�õ��������� skill��

- `life-science-literature-card`���� Zotero PDF �� MinerU ȫ����ȡ���ɳ�����Ƭ��ͼ��ժҪ���߼�ͼ��
- `life-science-reading-session`��Χ�� PDF��Zotero ���������п�Ƭ���о����ʴ𣬲����û�Ҫ��ʱ���ϱʼǡ�

���� skill ������ Zotero ���ݡ�Obsidian Vault��MinerU CLI��API token �����߱������á�Ĭ���� Vault ��ʹ�� `���ױʼ�`��`ͼƬ��Դ/literature_cards` �� `sources/mineru`�����ڰ�װ��Ƭʱѡ���������Ŀ¼��CSS snippet �Ϳ�Ƭǽ��ͼ�ǿ�ѡ�ģ�δ�����ڱ��ֿ⡣

## �� Windows �ϰ�װ skill

��Ҫ Codex��Zotero Desktop��Obsidian���Լ� Python 3.10 ����°汾������ Obsidian �д�������Լ��� Vault��

������ Codex ��˵��

> �� `$skill-installer` �� `https://github.com/minjiahaoKAI/codex-literature-skills` ��װ `skills/life-science-literature-card` �� `skills/life-science-reading-session`����װ��ȷ������ skill �ɼ�����Ҫ�����κ��˵� Zotero ���ݡ�Obsidian Vault ����Կ��

Ҳ�������زֿⲢ�� `skills/` �µ����������ļ��зŽ����� `C:\Users\<�û���>\.agents\skills\`����� Codex û��������ʾ������ Codex������ֻ���� `SKILL.md`����Ƭ skill ������ `references/` �� `scripts/`��

## ���ñ�����Դ

1. �����ĵ��������� Zotero Desktop��ȷ��Ŀ�������пɴ򿪵ı��� PDF��û�� Zotero ����ʱ��ֱ�Ӱ� PDF ·������ Codex Ҳ�ܿ�ʼ������Ƭ��
2. ���� Codex ���Լ��� Obsidian Vault ����·�������ڱ������� `OBSIDIAN_VAULT_PATH` ������������Ҫ����ʵ·���ύ�� GitHub��
3. ��װ MinerU Open API CLI���������Լ����˺������� token����һ�ڣ���
4. ���ϣ���Զ���ȡ Zotero ������������װ [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp)�����ǿ�ѡ���������ж����ıʼǲ��ֺ�д�����̡���ȷ������Ŀ��Ŀ¼������ Codex ʹ������д�빦�ܡ�

## ���� Codex ��װ MinerU

��������η���**���Լ��� Codex**��

> �����ҵ� Windows �����ϣ���ȷ���Ƿ����� `mineru-open-api`�����û�У���˶� [MinerU �ٷ� CLI ��װ˵��](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md)�����ز����ٷ� Windows ��װ�ű���Ȼ��װ CLI���� `mineru-open-api version` ��֤����Ҫ��װ�����ı��� MinerU ģ���������� Open API CLI��Ҳ��Ҫ������Դ�����Ľű�����װ����� [MinerU token ҳ��](https://mineru.net/apiManage/token) �����ӣ������Լ���¼������ token����Ҫ��ȡ����ȡ����ӡ�򱣴��ҵ� token �����졢�ֿ�������ļ���ָ�����ڱ����ն����� `mineru-open-api auth` ������ʾ���� token�������� `mineru-open-api auth --verify` ��鱾�ظ�ʽ����Ҫ�ϴ����� PDF �����ԣ���������ȷͬ�⡣

�ٷ� Windows ��װ����Ŀǰ�� `irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex`���� Codex �ȼ����Դ�ͽű����ݣ���ִ�С�CLI Ĭ�ϴ� `MINERU_TOKEN` ���û�Ŀ¼�µ� `.mineru/config.yaml` ��ȡ token��`auth --verify` ֻ��֤ token ��ʽ������֤�����߽���һ���ɹ����״�ʹ�û������û�ͬ���ϴ� PDF ��ȷ�� `extract` �ɹ���

## ����

�� Codex ���� Zotero ��һƪ�������͸� MinerU �� PDF �����������У��ҵ���Դ �� ��׼��ȡ �� �ڹ��������ɿ�Ƭ��PNG �� SVG �� ��װ�ű� dry run �� ��� Vault д��Ȩ�޺�װ �� �� Obsidian �в鿴����ͼƬ�����þ��� skill ѯ��һ������ͼ���򷽷������˶Իش�ָ��ԭ�ġ�

���ֿⰴ [MIT License](LICENSE) ��������Ҫ����ʵ���ġ�ͼƬ��ע�͡�Vault��`.mineru/`��token���������û����ɵĿ�Ƭ����ֿ⡣

## �ο�����

- [Codex skill �İ�װ��ַ�](https://learn.chatgpt.com/docs/build-skills)
- [MinerU Open API CLI](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/cli/mineru-open-api/README.md)
- [Obsidian Vault MCP](https://github.com/luffysolution-svg/obsidian-vault-mcp)
