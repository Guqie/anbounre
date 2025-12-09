#!/usr/bin/env python3
"""
智库工作流自动化系统 - 主入口脚本
本小姐的完美作品！(￣▽￣)／

使用方法：
    python main.py [命令] [选项]

命令：
    init            初始化系统
    daily           生成每日任务模板
    analyze         分析材料并生成摘要
    insight         提炼洞察
    evidence        构建证据链
    trend           趋势分析
    archive         归档知识
    review          生成复盘模板
    weekly          生成周总结
    search          搜索知识库
    stats           查看统计信息

Author: 哈雷酱 (傲娇大小姐工程师)
Version: 1.0.0
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from workflow_automation import AIAnalyzer, KnowledgeManager, TaskScheduler, DatabaseManager
from workflow_automation.utils import (
    load_config,
    setup_logging,
    get_current_date,
    read_markdown_file
)


def init_system(args):
    """初始化系统"""
    print("🎉 欢迎使用智库工作流自动化系统！")
    print("本小姐将为你初始化系统配置...(￣▽￣)／\n")

    config = load_config()
    logger = setup_logging(config)

    # 检查必要的目录
    dirs = config['directories']
    for dir_name, dir_path in dirs.items():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ 创建目录: {dir_path}")

    # 检查配置文件
    ai_config = config['ai']
    if ai_config.get('api_key') == 'your-api-key-here':
        print("\n⚠️  警告：请在 config/config.yaml 中配置你的 AI API Key！")
        print("   否则 AI 分析功能将无法使用哦！(￣へ￣)")

    print("\n✨ 系统初始化完成！")
    print("   使用 'python main.py --help' 查看所有可用命令")
    print("   哼，本小姐的系统可是很强大的呢！(*￣︶￣)\n")


def generate_daily_task(args):
    """生成每日任务模板"""
    print("📋 正在生成每日任务模板...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    scheduler = TaskScheduler()
    task_file = scheduler.generate_daily_task_template(args.date)

    print(f"✅ 每日任务模板已生成: {task_file}")
    print("   快去填写今天的任务吧，笨蛋！(￣▽￣)／\n")


def analyze_material(args):
    """分析材料并生成三行摘要"""
    print("🔍 正在分析材料...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    # 读取材料内容
    if args.file:
        content = read_markdown_file(args.file)
    else:
        content = args.content

    # 初始化 AI 分析器
    analyzer = AIAnalyzer()

    # 生成三行摘要
    summary = analyzer.generate_three_line_summary(
        content=content,
        source=args.source or "未知",
        date=args.date or get_current_date()
    )

    print("✅ 三行摘要生成完成：\n")
    print(f"**1. What happened：** {summary['what_happened']}")
    print(f"**2. So what：** {summary['so_what']}")
    print(f"**3. Now what：** {summary['now_what']}\n")

    # 归档
    if args.archive:
        km = KnowledgeManager()
        dimensions = analyzer.classify_by_pidst(content)
        category = dimensions[0] if dimensions else "General"

        summary_dict = {
            'title': args.title or "未命名材料",
            'what_happened': summary['what_happened'],
            'so_what': summary['so_what'],
            'now_what': summary['now_what'],
            'tags': category,
            'date': args.date or get_current_date(),
            'source': args.source or "未知"
        }

        archive_file = km.archive_three_line_summary(summary_dict, category)
        print(f"✅ 已归档到: {archive_file}\n")

    print("哼，本小姐的分析还不错吧？(￣▽￣)／\n")


def extract_insights(args):
    """提炼洞察"""
    print("💡 正在提炼洞察...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    # 读取信息内容
    if args.file:
        information = read_markdown_file(args.file)
    else:
        information = args.content

    # 初始化 AI 分析器
    analyzer = AIAnalyzer()

    # 提炼洞察
    insights = analyzer.extract_insights(
        information=information,
        min_insights=args.min_insights or 3
    )

    print(f"✅ 成功提炼 {len(insights)} 个洞察：\n")
    for i, insight in enumerate(insights, 1):
        print(f"### 洞察 {i}：{insight.get('viewpoint', '未命名')}")
        print(f"**依据：** {insight.get('evidence', '')}")
        print(f"**趋势：** {insight.get('trend', '')}\n")

    # 归档
    if args.archive:
        km = KnowledgeManager()
        for insight in insights:
            km.archive_insight(insight, args.topic or "General")
        print(f"✅ 洞察已归档\n")

    print("这些洞察可是本小姐精心提炼的哦！(*￣︶￣)\n")


def build_evidence_chain(args):
    """构建证据链"""
    print("🔗 正在构建证据链...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    # 读取信息内容
    if args.file:
        information = read_markdown_file(args.file)
    else:
        information = args.content

    # 初始化 AI 分析器
    analyzer = AIAnalyzer()

    # 构建证据链
    evidence_chain = analyzer.build_evidence_chain(
        topic=args.topic,
        information=information
    )

    print("✅ 证据链构建完成：\n")
    for dimension, evidences in evidence_chain.items():
        if evidences:
            print(f"**{dimension}：**")
            for evidence in evidences:
                print(f"  - {evidence}")
            print()

    # 归档
    if args.archive:
        km = KnowledgeManager()
        archive_file = km.archive_evidence_chain(evidence_chain, args.topic)
        print(f"✅ 已归档到: {archive_file}\n")

    print("完美的证据链，这才是专业水准呢！(￣▽￣)／\n")


def analyze_trend(args):
    """趋势分析"""
    print("📈 正在分析趋势...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    # 读取信息内容
    if args.file:
        information = read_markdown_file(args.file)
    else:
        information = args.content

    # 初始化 AI 分析器
    analyzer = AIAnalyzer()

    # 趋势分析
    trend_analysis = analyzer.analyze_trend(
        domain=args.domain,
        information=information,
        timeframe=args.timeframe or "未来1-3年"
    )

    print("✅ 趋势分析完成：\n")
    print(f"**当前状态：** {trend_analysis.get('current_state', '')}")
    print(f"**发展方向：** {trend_analysis.get('direction', '')}")
    print(f"**风险提示：** {trend_analysis.get('risks', '')}\n")

    print("本小姐的趋势判断可是很准的哦！(*￣︶￣)\n")


def archive_knowledge(args):
    """归档知识"""
    print("📚 正在归档知识...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    km = KnowledgeManager()

    if args.type == 'summary':
        # 归档三行摘要
        summary = {
            'title': args.title,
            'what_happened': input("What happened: "),
            'so_what': input("So what: "),
            'now_what': input("Now what: "),
            'tags': args.category,
            'date': args.date or get_current_date(),
            'source': args.source or "未知"
        }
        archive_file = km.archive_three_line_summary(summary, args.category)

    elif args.type == 'insight':
        # 归档洞察
        insight = {
            'viewpoint': args.title,
            'evidence': input("依据: "),
            'logic': input("逻辑链: "),
            'trend': input("趋势: "),
            'impact': input("影响: ")
        }
        archive_file = km.archive_insight(insight, args.topic or "General")

    else:
        print("⚠️  不支持的归档类型！")
        return

    print(f"✅ 已归档到: {archive_file}")
    print("知识沉淀完成，本小姐的知识库又丰富了呢！(￣▽￣)／\n")


def generate_review(args):
    """生成复盘模板"""
    print("📝 正在生成复盘模板...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    scheduler = TaskScheduler()
    review_file = scheduler.generate_review_template(args.date)

    print(f"✅ 复盘模板已生成: {review_file}")
    print("   记得认真填写复盘内容哦，笨蛋！(￣へ￣)\n")


def generate_weekly_summary(args):
    """生成周总结"""
    print("📊 正在生成周总结...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    scheduler = TaskScheduler()
    summary_file = scheduler.generate_weekly_summary(args.start_date, args.end_date)

    print(f"✅ 周总结模板已生成: {summary_file}")
    print("   一周的努力都在这里了呢！(*￣︶￣)\n")


def search_knowledge(args):
    """搜索知识库"""
    print(f"🔍 正在搜索: {args.query}...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    km = KnowledgeManager()
    results = km.search(args.query, args.type)

    if results:
        print(f"✅ 找到 {len(results)} 个结果：\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['type']}] {result['file_path']}")
            print(f"   创建时间: {result['created_at']}")
            print(f"   预览: {result['preview'][:100]}...\n")
    else:
        print("⚠️  没有找到相关结果")
        print("   换个关键词试试吧，笨蛋！(￣へ￣)\n")


def show_statistics(args):
    """显示统计信息"""
    print("📊 正在统计知识库信息...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    km = KnowledgeManager()
    stats = km.get_statistics()

    print("✅ 知识库统计：\n")
    print(f"📚 总文档数: {stats['total_documents']}")
    print(f"🏷️  总标签数: {stats['total_tags']}")
    print(f"📅 最后更新: {stats['last_update']}\n")

    print("文档类型分布：")
    for doc_type, count in stats['document_types'].items():
        print(f"  - {doc_type}: {count}")

    print("\n本小姐的知识库管理得很好吧？(￣▽￣)／\n")


def import_government(args):
    """
    批量导入政府库材料（CSV/JSON）

    Args:
        args: 命令行参数

    Returns:
        None
    """
    print("🏛️ 正在导入政府库材料...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    dm = DatabaseManager()
    count = 0
    if args.csv:
        count = dm.add_bulk_from_csv(args.csv, entry_type='government')
    elif args.json:
        count = dm.add_bulk_from_json(args.json, entry_type='government')
    else:
        item = {
            'type': 'government',
            'title': args.title or '',
            'agency': args.agency,
            'doc_number': args.doc_number,
            'date': args.date,
            'url': args.url,
            'source': args.source,
            'content': args.content
        }
        if item['title']:
            dm.add_material(item)
            count = 1

    print(f"✅ 导入完成：{count} 条\n")


def import_industry(args):
    """
    批量导入行业库材料（CSV/JSON）

    Args:
        args: 命令行参数

    Returns:
        None
    """
    print("🏭 正在导入行业库材料...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    dm = DatabaseManager()
    count = 0
    if args.csv:
        count = dm.add_bulk_from_csv(args.csv, entry_type='industry')
    elif args.json:
        count = dm.add_bulk_from_json(args.json, entry_type='industry')
    else:
        item = {
            'type': 'industry',
            'title': args.title or '',
            'subject': args.subject,
            'event_type': args.event_type,
            'key_data': args.key_data,
            'date': args.date,
            'url': args.url,
            'source': args.source,
            'content': args.content
        }
        if item['title']:
            dm.add_material(item)
            count = 1

    print(f"✅ 导入完成：{count} 条\n")


def process_queue(args):
    """
    处理待办队列（生成三行摘要并归档）

    Args:
        args: 命令行参数

    Returns:
        None
    """
    print("⚙️ 正在处理队列...(￣ω￣)ノ\n")

    config = load_config()
    logger = setup_logging(config)

    dm = DatabaseManager()
    analyzer = AIAnalyzer()
    km = KnowledgeManager()

    pending = dm.get_pending(limit=args.limit or 10)
    if not pending:
        print("⚠️ 队列为空\n")
        return

    for item in pending:
        dm.update_status(item['id'], 'processing')
        title = item.get('title') or '未命名材料'
        content = item.get('content') or ''
        composed = content or f"{title}\n{item.get('key_data','') or ''}"
        try:
            summary = analyzer.generate_three_line_summary(
                content=composed,
                source=item.get('source') or '未知',
                date=item.get('date') or get_current_date()
            )
            dimensions = analyzer.classify_by_pidst(composed)
            category = dimensions[0] if dimensions else 'General'
            summary_dict = {
                'title': title,
                'what_happened': summary['what_happened'],
                'so_what': summary['so_what'],
                'now_what': summary['now_what'],
                'tags': category,
                'date': item.get('date') or get_current_date(),
                'source': item.get('source') or '未知'
            }
            archive_file = km.archive_three_line_summary(summary_dict, category)
            dm.update_status(item['id'], 'completed', result={
                'category': category,
                'archive_file': archive_file,
                'summary': summary_dict
            })
            print(f"✅ 已处理并归档：[{item['type']}] {title}")
        except Exception as e:
            dm.update_status(item['id'], 'error', error_msg=str(e))
            print(f"❌ 处理失败：{title} -> {e}")
    print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智库工作流自动化系统 - 本小姐的完美作品！(￣▽￣)／",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # init 命令
    parser_init = subparsers.add_parser('init', help='初始化系统')

    # daily 命令
    parser_daily = subparsers.add_parser('daily', help='生成每日任务模板')
    parser_daily.add_argument('--date', help='日期 (YYYY-MM-DD)')

    # analyze 命令
    parser_analyze = subparsers.add_parser('analyze', help='分析材料并生成三行摘要')
    parser_analyze.add_argument('--file', help='材料文件路径')
    parser_analyze.add_argument('--content', help='材料内容')
    parser_analyze.add_argument('--source', help='材料来源')
    parser_analyze.add_argument('--date', help='材料时间')
    parser_analyze.add_argument('--title', help='材料标题')
    parser_analyze.add_argument('--archive', action='store_true', help='是否归档')

    # insight 命令
    parser_insight = subparsers.add_parser('insight', help='提炼洞察')
    parser_insight.add_argument('--file', help='信息文件路径')
    parser_insight.add_argument('--content', help='信息内容')
    parser_insight.add_argument('--min-insights', type=int, default=3, help='最少洞察数量')
    parser_insight.add_argument('--topic', help='主题')
    parser_insight.add_argument('--archive', action='store_true', help='是否归档')

    # evidence 命令
    parser_evidence = subparsers.add_parser('evidence', help='构建证据链')
    parser_evidence.add_argument('--topic', required=True, help='研究主题')
    parser_evidence.add_argument('--file', help='信息文件路径')
    parser_evidence.add_argument('--content', help='信息内容')
    parser_evidence.add_argument('--archive', action='store_true', help='是否归档')

    # trend 命令
    parser_trend = subparsers.add_parser('trend', help='趋势分析')
    parser_trend.add_argument('--domain', required=True, help='分析领域')
    parser_trend.add_argument('--file', help='信息文件路径')
    parser_trend.add_argument('--content', help='信息内容')
    parser_trend.add_argument('--timeframe', help='时间范围')

    # archive 命令
    parser_archive = subparsers.add_parser('archive', help='归档知识')
    parser_archive.add_argument('--type', required=True, choices=['summary', 'insight'], help='归档类型')
    parser_archive.add_argument('--title', required=True, help='标题')
    parser_archive.add_argument('--category', help='分类')
    parser_archive.add_argument('--topic', help='主题')
    parser_archive.add_argument('--source', help='来源')
    parser_archive.add_argument('--date', help='日期')

    # review 命令
    parser_review = subparsers.add_parser('review', help='生成复盘模板')
    parser_review.add_argument('--date', help='日期 (YYYY-MM-DD)')

    # weekly 命令
    parser_weekly = subparsers.add_parser('weekly', help='生成周总结')
    parser_weekly.add_argument('--start-date', required=True, help='开始日期 (YYYY-MM-DD)')
    parser_weekly.add_argument('--end-date', required=True, help='结束日期 (YYYY-MM-DD)')

    # search 命令
    parser_search = subparsers.add_parser('search', help='搜索知识库')
    parser_search.add_argument('query', help='搜索关键词')
    parser_search.add_argument('--type', help='文档类型过滤')

    # stats 命令
    parser_stats = subparsers.add_parser('stats', help='查看统计信息')

    # import-gov 命令
    parser_import_gov = subparsers.add_parser('import-gov', help='批量导入政府库')
    parser_import_gov.add_argument('--csv', help='CSV 文件路径')
    parser_import_gov.add_argument('--json', help='JSON 文件路径')
    parser_import_gov.add_argument('--title', help='标题')
    parser_import_gov.add_argument('--agency', help='发布机构')
    parser_import_gov.add_argument('--doc-number', dest='doc_number', help='文号')
    parser_import_gov.add_argument('--date', help='日期 (YYYY-MM-DD)')
    parser_import_gov.add_argument('--url', help='链接')
    parser_import_gov.add_argument('--source', help='来源')
    parser_import_gov.add_argument('--content', help='正文内容')

    # import-ind 命令
    parser_import_ind = subparsers.add_parser('import-ind', help='批量导入行业库')
    parser_import_ind.add_argument('--csv', help='CSV 文件路径')
    parser_import_ind.add_argument('--json', help='JSON 文件路径')
    parser_import_ind.add_argument('--title', help='标题')
    parser_import_ind.add_argument('--subject', help='主题')
    parser_import_ind.add_argument('--event-type', dest='event_type', help='事件类型')
    parser_import_ind.add_argument('--key-data', dest='key_data', help='关键数据')
    parser_import_ind.add_argument('--date', help='日期 (YYYY-MM-DD)')
    parser_import_ind.add_argument('--url', help='链接')
    parser_import_ind.add_argument('--source', help='来源')
    parser_import_ind.add_argument('--content', help='正文内容')

    # process 命令
    parser_process = subparsers.add_parser('process', help='处理待办队列并归档')
    parser_process.add_argument('--limit', type=int, default=10, help='处理数量上限')

    args = parser.parse_args()

    # 执行命令
    if args.command == 'init':
        init_system(args)
    elif args.command == 'daily':
        generate_daily_task(args)
    elif args.command == 'analyze':
        analyze_material(args)
    elif args.command == 'insight':
        extract_insights(args)
    elif args.command == 'evidence':
        build_evidence_chain(args)
    elif args.command == 'trend':
        analyze_trend(args)
    elif args.command == 'archive':
        archive_knowledge(args)
    elif args.command == 'review':
        generate_review(args)
    elif args.command == 'weekly':
        generate_weekly_summary(args)
    elif args.command == 'search':
        search_knowledge(args)
    elif args.command == 'stats':
        show_statistics(args)
    elif args.command == 'import-gov':
        import_government(args)
    elif args.command == 'import-ind':
        import_industry(args)
    elif args.command == 'process':
        process_queue(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
