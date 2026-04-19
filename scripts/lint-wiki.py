#!/usr/bin/env python3
"""
wiki/ の整合性チェック（lint）

チェック項目:
1. 孤立ページ（他のどのページからもリンクされていない）
2. 赤リンク（リンク先ページが存在しない）
3. index.md に未登録のページ
4. フロントマターの不備（title, tags, aliases の欠落）
5. 空セクション（TODO/プレースホルダが残っている）
6. 相互リンクの欠如（AがBにリンクしているがBがAにリンクしていない）
"""

import os
import re
import yaml

WIKI_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wiki'))


def extract_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, content


def build_page_map(wiki_dir):
    """slug → {filepath, fm, content, title, aliases}"""
    pages = {}
    for root, dirs, files in os.walk(wiki_dir):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, wiki_dir)
            slug = rel.replace(os.sep, '/').removesuffix('.md')
            fm, content = extract_frontmatter(filepath)
            names = set()
            names.add(slug)
            names.add(fname.removesuffix('.md'))
            if fm.get('title'):
                names.add(fm['title'])
            for a in (fm.get('aliases') or []):
                names.add(a)
            pages[slug] = {
                'filepath': filepath,
                'fm': fm,
                'content': content,
                'title': fm.get('title', slug),
                'names': names,
            }
    return pages


def extract_wikilinks(content):
    """コンテンツ内の全wikilinkを抽出（コードブロック・インラインコード内は除外）"""
    # コードブロックとインラインコードを除去してからマッチ
    cleaned = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    cleaned = re.sub(r'`[^`]+`', '', cleaned)
    links = []
    for m in re.finditer(r'\[\[([^\]]+)\]\]', cleaned):
        inner = m.group(1)
        if '|' in inner:
            target = inner.split('|')[0].strip()
        else:
            target = inner.strip()
        links.append(target)
    return links


def resolve_name(name, pages):
    """名前からslugを解決"""
    for slug, info in pages.items():
        if name in info['names']:
            return slug
    return None


def main():
    pages = build_page_map(WIKI_DIR)
    issues = []
    warnings = []

    # 名前→slug の逆引きマップ
    name_to_slug = {}
    for slug, info in pages.items():
        for name in info['names']:
            name_to_slug[name] = slug

    # === 各ページの outgoing links を収集 ===
    outgoing = {}  # slug → set of target slugs
    for slug, info in pages.items():
        links = extract_wikilinks(info['content'])
        targets = set()
        for link in links:
            resolved = resolve_name(link, pages)
            if resolved:
                targets.add(resolved)
        outgoing[slug] = targets

    # === 1. 孤立ページ（インバウンドリンクなし） ===
    inbound = {slug: set() for slug in pages}
    for src_slug, targets in outgoing.items():
        for tgt in targets:
            if tgt in inbound:
                inbound[tgt].add(src_slug)

    orphans = []
    for slug, sources in inbound.items():
        if slug == 'index' or slug == 'log':
            continue
        if not sources:
            orphans.append(slug)
    if orphans:
        issues.append(('孤立ページ（他のページからリンクされていない）', orphans))

    # === 2. 赤リンク（リンク先不在） ===
    dead_links = []
    for slug, info in pages.items():
        links = extract_wikilinks(info['content'])
        for link in links:
            # frontmatter内のaliasesは除外
            resolved = resolve_name(link, pages)
            if not resolved:
                dead_links.append((slug, link))
    if dead_links:
        issues.append(('赤リンク（リンク先ページが存在しない）', dead_links))

    # === 3. index.md に未登録のページ ===
    index_content = pages.get('index', {}).get('content', '')
    index_links = set()
    for link in extract_wikilinks(index_content):
        resolved = resolve_name(link, pages)
        if resolved:
            index_links.add(resolved)

    unlisted = []
    for slug in pages:
        if slug in ('index', 'log'):
            continue
        if slug not in index_links:
            unlisted.append(slug)
    if unlisted:
        warnings.append(('index.md に未登録のページ', unlisted))

    # === 4. フロントマターの不備 ===
    fm_issues = []
    for slug, info in pages.items():
        fm = info['fm']
        missing = []
        if not fm.get('title'):
            missing.append('title')
        if not fm.get('tags'):
            missing.append('tags')
        if slug not in ('index', 'log') and not fm.get('aliases'):
            missing.append('aliases')
        if missing:
            fm_issues.append((slug, missing))
    if fm_issues:
        warnings.append(('フロントマター不備', fm_issues))

    # === 5. 空セクション / プレースホルダ ===
    placeholders = []
    for slug, info in pages.items():
        content = info['content']
        for pattern in [r'（ソース取り込み後に記述）', r'<!-- 今後追加', r'TODO']:
            if re.search(pattern, content):
                placeholders.append((slug, pattern))
    if placeholders:
        warnings.append(('プレースホルダ / 空セクションが残っている', placeholders))

    # === 6. 相互リンクの欠如 ===
    missing_backlinks = []
    for src_slug, targets in outgoing.items():
        for tgt in targets:
            if tgt in outgoing and src_slug not in outgoing[tgt]:
                # log, index は相互リンク不要
                if src_slug in ('index', 'log') or tgt in ('index', 'log'):
                    continue
                missing_backlinks.append((tgt, src_slug))

    # 重複除去
    seen = set()
    unique_backlinks = []
    for tgt, src in missing_backlinks:
        key = (tgt, src)
        if key not in seen:
            seen.add(key)
            unique_backlinks.append((tgt, src))

    if unique_backlinks:
        warnings.append(('相互リンクの欠如（A→Bはあるが B→Aがない）', unique_backlinks))

    # === レポート出力 ===
    print("=" * 60)
    print("dd2030 Wiki Lint Report")
    print("=" * 60)
    print(f"\n総ページ数: {len(pages)}")
    print(f"総リンク数: {sum(len(v) for v in outgoing.values())}")
    print()

    if not issues and not warnings:
        print("問題なし！")
        return

    if issues:
        print("--- ISSUES（要対応） ---\n")
        for title, items in issues:
            print(f"### {title}")
            for item in items:
                if isinstance(item, tuple):
                    print(f"  - {item[0]} → [[{item[1]}]]")
                else:
                    print(f"  - {item}")
            print()

    if warnings:
        print("--- WARNINGS（改善推奨） ---\n")
        for title, items in warnings:
            print(f"### {title}")
            for item in items:
                if isinstance(item, tuple) and len(item) == 2:
                    if isinstance(item[1], list):
                        print(f"  - {item[0]}: {', '.join(item[1])}")
                    else:
                        print(f"  - {item[0]} → {item[1]}")
                else:
                    print(f"  - {item}")
            print()


if __name__ == '__main__':
    main()
