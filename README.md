# dd2030 Wiki

[デジタル民主主義2030（dd2030）](https://dd2030.org)プロジェクトの活動を整理したWikiです。1年間のSlackログや議事録から情報を抽出し、プロジェクトに初めて来た人が理解しやすい形にまとめています。

**公開サイト**: https://nishio.github.io/dd2030-wiki/

## 仕組み

[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) パターンに基づいています。LLMがソース資料を読み、Wikiページを生成・維持します。人間はソースの追加と方向づけを行い、LLMが要約・相互参照・整理を担当します。

```
wiki/（シンプルな [[ページ名]] で記述）
  ↓ scripts/resolve-links.py（リンクをファイルパスに自動解決）
content/（Quartz が読むディレクトリ）
  ↓ npx quartz build
public/（HTML）
  ↓ GitHub Actions
GitHub Pages
```

## Forkして自分で動かす

### 1. Forkとクローン

```bash
# GitHubでForkしてから
git clone https://github.com/<your-username>/dd2030-wiki.git
cd dd2030-wiki
```

### 2. 依存のインストール

```bash
# Node.js (22+) と Python (3.10+) が必要
corepack enable
pnpm install
pip install pyyaml
```

### 3. ローカルで確認

```bash
python3 scripts/resolve-links.py   # wiki/ → content/ のリンク解決
npx quartz build --serve            # http://localhost:8080 で確認
```

### 4. GitHub Pagesの設定

1. `quartz.config.ts` の `baseUrl` を `<your-username>.github.io/dd2030-wiki` に変更
2. GitHubリポジトリの Settings → Pages → Build and deployment の Source を **GitHub Actions** に設定
3. pushすると自動でビルド・デプロイされる

### 5. Wikiの編集

`wiki/` 配下のMarkdownを編集してpushするだけです。

```bash
# 例: 新しいページを追加
vim wiki/concepts/new-concept.md

# ローカル確認
python3 scripts/resolve-links.py && npx quartz build --serve

# pushすれば自動デプロイ
git add wiki/
git commit -m "Add new concept page"
git push
```

リンクは `[[ページタイトル]]` とシンプルに書けます。ビルド時にスクリプトがファイルパスに自動解決します。

## ディレクトリ構成

```
dd2030-wiki/
├── wiki/                    # LLMが生成・維持するWikiページ（ここを編集する）
│   ├── index.md             # 目次
│   ├── overview.md          # プロジェクト概要
│   ├── entities/            # プロダクト・組織のページ
│   ├── concepts/            # 概念・用語の説明
│   ├── events/              # イベント・会議
│   ├── topics/              # テーマ別の横断整理
│   ├── timeline/            # 時系列の活動まとめ
│   └── sources/             # ソース資料の要約
├── raw/                     # 元資料（不変）
│   └── history/             # websiteリポジトリの週次レポート（50週分）
├── content/                 # 自動生成（直接編集しない）
├── scripts/
│   └── resolve-links.py     # wikilink解決スクリプト
├── quartz/                  # Quartzフレームワーク
├── quartz.config.ts         # Quartz設定
├── CLAUDE.md                # LLM向けスキーマ（ページ規約・操作フロー）
└── .github/workflows/       # GitHub Actions（自動デプロイ）
```

## LLMと一緒に使う

このWikiはLLM（Claude Code等）と一緒にメンテナンスすることを前提としています。

```bash
# 新しいソースを取り込む
# 1. raw/ にファイルを置く
# 2. LLMに「raw/xxx.md を取り込んで」と指示
# → LLMがソース要約を作成し、関連ページを更新し、indexに追加する
```

LLM向けの規約は [CLAUDE.md](CLAUDE.md) に記載しています。他のLLMエージェント（Codex, OpenCode等）を使う場合は、CLAUDE.mdの内容をそのエージェントの設定ファイル（AGENTS.md等）にコピーしてください。

## ライセンス

Wikiコンテンツ（`wiki/`, `raw/`）: CC BY 4.0
Quartzフレームワーク: MIT（[jackyzha0/quartz](https://github.com/jackyzha0/quartz)）
