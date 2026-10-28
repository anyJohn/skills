# anyJohn Skills

AI agent skills curated by [anyJohn](https://github.com/anyJohn). Installable via [skills.sh](https://skills.sh).

```bash
npx skills add anyJohn/skills
```

Or install a single skill:

```bash
npx skills add anyJohn/skills --skill akshare
npx skills add anyJohn/skills --skill write-like-human-zh
```

## Skills

| Skill | Category | Description |
|---|---|---|
| [akshare](skills/akshare/) | Finance | Get Chinese financial data (A-share, funds, futures, bonds) via AKShare |
| [write-like-human-zh](skills/write-like-human-zh/) | Writing | 中文写作去 AI 腔：元话语、结构宣告、评价包装、坑叙事，以及翻译腔与连接词堆积的改写规则 |

## Deprecated

| Skill | Note |
|---|---|
| [snap-out](skills/deprecated/snap-out/) | 基准测试后弃用：与对照组任务成功率相同，保留源码与测试说明。要重新启用，把目录移回 `skills/` 并把 `scripts/snap-out.sh` 链到 PATH |

## License

MIT
