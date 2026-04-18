---
title: Polimoney
aliases: [Polimoney]
tags: [dd2030, product, polimoney]
sources: [raw/history/week5_20250416/polimoney.md, raw/history/week15_20250625/polimoney.md, raw/history/week25_20250903/polimoney.md, raw/history/week35_20251112/polimoney.md, raw/history/week40_20251217/polimoney.md]
created: 2026-04-18
updated: 2026-04-18
---

# Polimoney

## 概要

**Polimoney（ポリマネー）** は、政治資金収支報告書のPDFをAI（Gemini）でOCR解析し、政治資金の流れを可視化するツール。政治の透明性向上を目指すdd2030のプロダクトの1つ。

ブランド名は2025年8月にコミュニティ投票で「Polimoney」に決定。

## 技術スタック

- OCR: Google Gemini AI（PDF→画像→解析）
- データ処理: TypeScript
- DB: Supabase（PostgreSQL）
- 可視化: サンキー図、ツリーマップ、サンバースト図

## 機能

- 政治資金収支報告書のPDF解析・データ化
- 選挙運動費用収支報告書の解析（2025年8月〜対応）
- 収支データの可視化（サンキー図等）
- 全国47都道府県の政治資金データ対応を構想

## 開発の歩み

### 初期（2025年4月〜5月）
- Week5で本格始動。PDF→画像→Gemini解析パイプラインの構築
- データ変換スクリプト（TypeScript）の実装
- 収支データの型定義

### データ基盤整備（2025年6月〜8月）
- `Transaction`型によるデータフォーマット統一
- 翌年繰越額のバグ修正
- 選挙運動費用収支報告書への対応開始（CLIツールとして追加）
- ExcelファイルのJSON出力

### 拡張期（2025年9月〜12月）
- 複数JSONファイルの結合・チェックサム検証
- DBスキーマ策定（総務省定義の地域コード活用）
- 外部API連携を見据えた設計
- テレビ番組で紹介が決定
- SaaSモデルへの転換議論
- Supabase導入
- 「まる見え（政治資金DX）」のリリースが話題に

### 現在（2026年〜）
- 比較記事・利用者インタビュー記事をSNSで周知
- 県予算配分の可視化ツールの試作

## メディア露出

- テレビ番組での紹介（2025年12月）
- 比較記事・インタビュー記事の公開（2026年3月）

## 関連ページ

- [[overview]] — プロジェクト全体の概要
