# LOG

## 2026-04-18

### Wiki構造の初期化
- ディレクトリ構成を作成: `raw/`, `wiki/`, `content/`, `scripts/`, `.github/workflows/`
- `raw/` のサブディレクトリ: `slack/`, `minutes/`, `documents/`, `assets/`
- `wiki/` のサブディレクトリ: `entities/`, `concepts/`, `events/`, `topics/`, `timeline/`, `sources/`
- CLAUDE.md（スキーマ）を作成
- wiki/index.md, wiki/overview.md, wiki/log.md を作成
- content/_index.md を作成（Quartz公開用トップページ）

### ソースの取り込みとWikiページ生成
- digitaldemocracy2030/website リポジトリから `src/history/` を取得
- 50週分（week1_20250319〜week50_20260415）、218個のMarkdownファイルを `raw/history/` に配置
- 全週のslack.mdとプロダクト別mdをスキャンし、以下のWikiページを生成:
  - wiki/overview.md — プロジェクト全体の概要
  - wiki/entities/kouchou-ai.md — 広聴AI
  - wiki/entities/idobata.md — いどばた
  - wiki/entities/polimoney.md — Polimoney
  - wiki/entities/coreloop.md — コアループ（Project Coreloop）
  - wiki/entities/broad-listening-book.md — ブロードリスニング本
  - wiki/concepts/broad-listening.md — ブロードリスニング
  - wiki/concepts/deliberative-democracy.md — 熟議民主主義
  - wiki/timeline/quarterly-summary.md — 時系列まとめ（四半期）
  - wiki/index.md — 目次を更新
