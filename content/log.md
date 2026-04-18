---
title: Wiki作業ログ
tags: [dd2030, log]
created: 2026-04-18
updated: 2026-04-18
---

# Wiki 作業ログ

取り込み・更新・メンテナンスの記録。

## [2026-04-18] init | Wiki構造の初期化

- ディレクトリ構成を作成
- CLAUDE.md（スキーマ）を作成
- index.md, overview.md, log.md を作成
- Quartz公開用の設定ファイルを準備

## [2026-04-18] ingest | website歴史データ50週分の取り込み

- digitaldemocracy2030/website の src/history/ から50週分のデータを取得
- raw/history/ に配置（218ファイル）
- 以下のWikiページを生成:
  - overview.md, entities/kouchou-ai.md, entities/idobata.md, entities/polimoney.md
  - entities/coreloop.md, entities/broad-listening-book.md
  - concepts/broad-listening.md, concepts/deliberative-democracy.md
  - timeline/quarterly-summary.md
- index.md を更新
