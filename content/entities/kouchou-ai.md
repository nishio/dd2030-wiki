---
title: 広聴AI
aliases: [広聴AI]
tags: [dd2030, product, kouchou-ai]
sources: [raw/history/week1_20250319/kouchou-ai.md, raw/history/week10_20250521/kouchou-ai.md, raw/history/week20_20250730/kouchou-ai.md, raw/history/week30_20251008/kouchou-ai.md, raw/history/week44_20260121/kouchou-ai.md, raw/history/week50_20260415/kouchou-ai.md]
created: 2026-04-18
updated: 2026-04-18
---

# 広聴AI（kouchou-ai）

## 概要

**広聴AI**は、大量の市民意見（パブリックコメント、アンケート、SNS等）をAIで分析・クラスタリングし、論点ごとに可視化する[[concepts/broad-listening|ブロードリスニング]]ツール。dd2030の中核プロダクトの1つ。

「広聴」とは市民の声を広く聴くことを意味し、従来の行政の「広報」（情報を発信する）に対する概念。

## 技術スタック

- フロントエンド: Next.js
- バックエンド: Python
- LLM: OpenAI / Azure OpenAI / OpenRouter / Gemini（マルチプロバイダ対応）
- クラスタリング: UMAP, HDBSCAN
- デプロイ: Docker, Azure（GitHub Actionsで自動デプロイ）

## 機能

- CSVアップロードによる大量意見の取り込み
- AIによる意見のクラスタリング・要約
- セグメントビュー（全体・濃い意見・階層）の切り替え表示
- 属性フィルタ機能
- トークン使用量の可視化
- Windows / Mac / Linux対応

## 開発の歩み

### 初期（2025年3月〜4月）
- GitHubリポジトリ公開。Docker環境でのローカル実行が可能に
- 数百件のサンプルデータでレポート生成を確認
- 3万件規模のパブコメ対応を想定した設計議論
- Azure対応、APIコスト最適化が課題として浮上

### 成長期（2025年5月〜7月）
- **v3.0.0リリース**（2025年5月）
- OpenRouter対応でマルチLLMプロバイダ化
- Windows直実行サポート
- Embedding時のAzure/OpenRouter対応
- 技術解説スライドが「神資料」と評判に
- 宇多津町（香川）での実証が公開

### 社会実装期（2025年8月〜12月）
- 広島県で市民向け活用事例が公開・拡散
- LGWAN環境対応の議論（自治体イントラへの導入）
- APIキーのサーバーサイド管理強化（セキュリティ向上）
- 4パターンの提供形態を整理（研究用Jupyter・CLIツール・WebUI・お試しホスティング）
- AIツール利用時のコントリビュートルールを文書化

### v5.0への移行（2026年1月〜）
- 大規模リファクタリング開始
- **プラグイン方式**への転換（入力・分析・可視化を独立拡張可能に）
- **PyPI（Pythonパッケージ）化**によるCLI提供を構想
- Next.js 16.xへのアップデート（セキュリティ修正含む）

## 自治体での導入事例

- 宇多津町（香川県）— 実証実験
- 広島県 — 市民向け活用事例
- 奈良市 — 導入議論
- その他複数の自治体が関心を表明

## 関連ページ

- [[concepts/broad-listening|ブロードリスニング]] — 広聴AIが実現する概念
- [[entities/broad-listening-book|ブロードリスニング本]] — 書籍化プロジェクト
- [[entities/idobata|いどばた]] — 姉妹プロダクト（対話型）
- [[overview]] — プロジェクト全体の概要
