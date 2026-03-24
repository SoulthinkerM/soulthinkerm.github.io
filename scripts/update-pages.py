#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客自动更新脚本
功能：扫描所有文章，自动更新到时间线、标签分类、最新文章等页面
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path('/workspace')
ARCHIVES_DIR = WORKSPACE / 'archives'
CATEGORIES_DIR = WORKSPACE / 'categories'
TIMELINE_FILE = WORKSPACE / 'timeline' / 'index.html'
INDEX_FILE = WORKSPACE / 'index.html'
TAGS_FILE = WORKSPACE / 'works' / 'tag-categories' / 'index.html'

def extract_posts_from_archives():
    """从 archives 目录提取所有文章信息"""
    posts = []
    
    for year_dir in sorted(ARCHIVES_DIR.iterdir(), reverse=True):
        if not year_dir.is_dir() or year_dir.name == 'index.html':
            continue
            
        year = year_dir.name
        
        for month_dir in sorted(year_dir.iterdir(), reverse=True):
            if not month_dir.is_dir():
                continue
                
            month = month_dir.name
            index_file = month_dir / 'index.html'
            
            if index_file.exists():
                content = index_file.read_text(encoding='utf-8')
                pattern = r'<article class="archive-item">\s*<a class="archive-item-link" href="([^"]+)">([^<]+)</a>\s*<span class="archive-item-date">([^<]+)</span>'
                matches = re.findall(pattern, content)
                
                for match in matches:
                    url, title, date_str = match
                    lang = 'zh-CN'
                    if '/en/' in url:
                        lang = 'en'
                    elif '/zh/' in url:
                        lang = 'zh-CN'
                    
                    try:
                        date_obj = datetime.strptime(date_str.strip(), '%Y/%m/%d')
                    except:
                        date_obj = datetime.now()
                    
                    posts.append({
                        'url': url,
                        'title': title.strip(),
                        'date': date_str.strip(),
                        'date_obj': date_obj,
                        'year': year,
                        'month': month,
                        'lang': lang
                    })
    
    posts.sort(key=lambda x: x['date_obj'], reverse=True)
    return posts

def extract_categories(posts):
    """从分类页面提取分类信息"""
    categories = {
        '人生游戏化': {'zh_name': '人生游戏化', 'en_name': 'Life Gamification', 'posts_zh': [], 'posts_en': []},
        '人生拆迁': {'zh_name': '人生拆迁', 'en_name': 'Life Demolition', 'posts_zh': [], 'posts_en': []},
        '研究日志': {'zh_name': '研究日志', 'en_name': 'Research Logs', 'posts_zh': [], 'posts_en': []},
        '随笔': {'zh_name': '随笔', 'en_name': 'Essays', 'posts_zh': [], 'posts_en': []}
    }
    
    for post in posts:
        url = post['url']
        if '人生游戏化' in url or 'Life-Gamification' in url:
            cat_key = '人生游戏化'
        elif '人生拆迁' in url or 'Life-Demolition' in url:
            cat_key = '人生拆迁'
        elif '研究日志' in url or 'Research' in url:
            cat_key = '研究日志'
        elif '随笔' in url or 'Essays' in url:
            cat_key = '随笔'
        else:
            continue
        
        if post['lang'] == 'zh-CN':
            categories[cat_key]['posts_zh'].append(post)
        else:
            categories[cat_key]['posts_en'].append(post)
    
    return categories

def generate_post_html(post, read_more_text):
    """生成文章 HTML 片段"""
    return f'''      <article class="post-item" data-lang="{post['lang']}" style="margin-bottom: 30px; padding: 15px; border-radius: 8px; background: #f9f9f9;">
        <h3 class="post-title" style="margin: 0 0 10px 0; font-size: 16px;">
          <a href="{post['url']}" style="color: #ff7242; text-decoration: none;">{post['title']}</a>
        </h3>
        <div class="post-meta" style="color: #999; font-size: 12px; margin-bottom: 10px;">{post['date']} | 未分类</div>
        <div class="post-excerpt" style="color: #666; font-size: 14px; line-height: 1.6;">暂无摘要</div>
        <a class="read-more" href="{post['url']}" style="color: #ff7242; font-size: 14px; text-decoration: none; margin-top: 10px; display: inline-block;">{read_more_text}</a>
      </article>'''

def update_timeline_page(posts):
    """更新时间线页面"""
    if not TIMELINE_FILE.exists():
        return False
    
    content = TIMELINE_FILE.read_text(encoding='utf-8')
    timeline_posts_html = []
    posts_by_year = {}
    
    for post in posts:
        year = post['year']
        if year not in posts_by_year:
            posts_by_year[year] = []
        posts_by_year[year].append(post)
    
    for year in sorted(posts_by_year.keys(), reverse=True):
        year_posts = posts_by_year[year]
        timeline_posts_html.append(f'\n    <div class="timeline-year" style="margin-bottom: 40px;">\n      <h3 style="color: #ff7242; border-bottom: 2px solid #ff7242; padding-bottom: 10px; margin-bottom: 20px;">{year}</h3>')
        
        for post in year_posts:
            timeline_posts_html.append(f'''
      <article class="timeline-post" data-lang="{post['lang']}" style="margin-bottom: 20px; padding-left: 20px; border-left: 3px solid #eee;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <a href="{post['url']}" style="color: #333; text-decoration: none; font-weight: 500;">{post['title']}</a>
          <span style="color: #999; font-size: 12px;">{post['date']}</span>
        </div>
      </article>''')
        timeline_posts_html.append('\n    </div>')
    
    timeline_html = '\n'.join(timeline_posts_html)
    pattern = r'(<section class="post-content">\s*)(</section>)'
    replacement = r'\1' + timeline_html + r'\n        \2'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        TIMELINE_FILE.write_text(new_content, encoding='utf-8')
        print("✓ 时间线页面已更新")
        return True
    return False

def update_category_pages(categories):
    """更新分类页面"""
    updated = False
    for cat_name, cat_data in categories.items():
        cat_file = CATEGORIES_DIR / cat_name / 'index.html'
        if not cat_file.exists():
            continue
        
        content = cat_file.read_text(encoding='utf-8')
        all_posts_html = []
        
        for post in cat_data['posts_zh']:
            all_posts_html.append(generate_post_html(post, '阅读全文 →'))
        for post in cat_data['posts_en']:
            all_posts_html.append(generate_post_html(post, 'Read More →'))
        
        if not all_posts_html:
            continue
        
        posts_html = '\n\n'.join(all_posts_html)
        pattern = r'(<!-- 所有分类文章：先隐藏，前端筛选对应语言 -->\s*)(.*?)(\s*<!-- 筛选后的文章容器 -->)'
        replacement = r'\1\n' + posts_html + r'\n\3'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            cat_file.write_text(new_content, encoding='utf-8')
            print(f"✓ 分类页面 [{cat_name}] 已更新")
            updated = True
    
    return updated

def update_index_page(posts):
    """更新首页最新文章"""
    if not INDEX_FILE.exists():
        return False
    
    content = INDEX_FILE.read_text(encoding='utf-8')
    latest_posts = posts[:10]
    posts_html = []
    
    for post in latest_posts:
        read_more = '阅读全文 →' if post['lang'] == 'zh-CN' else 'Read More →'
        posts_html.append(generate_post_html(post, read_more))
    
    if not posts_html:
        return False
    
    posts_html_str = '\n\n'.join(posts_html)
    pattern = r'(<!-- 所有文章：先隐藏，前端筛选后显示对应语言的 -->\s*<div id="all-posts" style="display: none;">\s*)(.*?)(\s*</div>\s*<!-- 筛选后的文章显示容器 -->)'
    replacement = r'\1\n' + posts_html_str + r'\n\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        INDEX_FILE.write_text(new_content, encoding='utf-8')
        print("✓ 首页最新文章已更新")
        return True
    return False

def update_tags_page(posts, categories):
    """更新标签分类页面"""
    if not TAGS_FILE.exists():
        return False
    
    content = TAGS_FILE.read_text(encoding='utf-8')
    tags_html = []
    
    for cat_name, cat_data in categories.items():
        if not cat_data['posts_zh'] and not cat_data['posts_en']:
            continue
        
        tags_html.append(f'\n            <div class="category-group" style="margin-bottom: 30px;">')
        tags_html.append(f'              <h3 style="color: #ff7242; margin-bottom: 15px; font-size: 16px;">{cat_data["zh_name"]} / {cat_data["en_name"]}</h3>')
        
        all_cat_posts = cat_data['posts_zh'] + cat_data['posts_en']
        all_cat_posts.sort(key=lambda x: x['date_obj'], reverse=True)
        
        for post in all_cat_posts[:5]:
            tags_html.append(f'''              <article class="archive-item" data-lang="{post['lang']}">
                <a class="archive-item-link" href="{post['url']}">{post['title']}</a>
                <span class="archive-item-date">{post['date']}</span>
              </article>''')
        tags_html.append('            </div>')
    
    if not tags_html:
        return False
    
    tags_html_str = '\n\n'.join(tags_html)
    pattern = r'(<div class="categories-list">\s*)(.*?)(\s*</div>\s*<!-- 分类文章列表结束 -->)'
    replacement = r'\1\n' + tags_html_str + r'\n\3'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        TAGS_FILE.write_text(new_content, encoding='utf-8')
        print("✓ 标签分类页面已更新")
        return True
    return False

def main():
    print("=" * 50)
    print("博客自动更新脚本")
    print("=" * 50)
    
    print("\n1. 扫描文章...")
    posts = extract_posts_from_archives()
    print(f"   找到 {len(posts)} 篇文章")
    
    if not posts:
        print("   没有找到文章，跳过更新")
        return
    
    print("\n2. 整理分类...")
    categories = extract_categories(posts)
    
    print("\n3. 更新页面...")
    updated = False
    
    if update_timeline_page(posts):
        updated = True
    if update_category_pages(categories):
        updated = True
    if update_index_page(posts):
        updated = True
    if update_tags_page(posts, categories):
        updated = True
    
    print("\n" + "=" * 50)
    if updated:
        print("✓ 所有页面更新完成！")
    else:
        print("没有需要更新的页面")
    print("=" * 50)

if __name__ == '__main__':
    main()
