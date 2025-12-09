"""
知识库管理系统模块
本小姐的知识宝库管理器！(￣ω￣)ノ

功能：
- 自动分类归档
- 智能标签生成
- 全文检索
- 知识关联发现
- 定期整理优化
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict

from .utils import (
    load_config,
    read_markdown_file,
    write_markdown_file,
    append_to_file,
    find_markdown_files,
    parse_markdown_sections,
    classify_by_pidst,
    get_current_date,
    get_current_datetime
)


class KnowledgeManager:
    """知识库管理系统类"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化知识库管理系统

        Args:
            config_path: 配置文件路径
        """
        self.config = load_config(config_path)
        self.logger = logging.getLogger(__name__)

        # 获取目录配置
        self.dirs = self.config['directories']
        self.kb_config = self.config['knowledge_base']

        # 知识库索引
        self.index_file = "logs/knowledge_index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """
        加载知识库索引

        Returns:
            索引字典
        """
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"加载索引失败: {e}，将创建新索引")

        return {
            'documents': {},
            'tags': defaultdict(list),
            'categories': defaultdict(list),
            'last_update': get_current_datetime()
        }

    def _save_index(self) -> None:
        """保存知识库索引"""
        try:
            os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
            self.index['last_update'] = get_current_datetime()

            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)

            self.logger.info("知识库索引已保存")
        except Exception as e:
            self.logger.error(f"保存索引失败: {e}")

    def archive_three_line_summary(self, summary: Dict[str, str],
                                   category: str = "General") -> str:
        """
        归档三行摘要

        Args:
            summary: 三行摘要字典
            category: 分类（Policy/Industry/Data/Signals/Technology）

        Returns:
            归档文件路径
        """
        self.logger.info(f"正在归档三行摘要到 {category} 类别...")

        # 确定归档目录
        if category in ['Policy', 'General']:
            archive_dir = "02-政策于宏观库"
        elif category == 'Industry':
            archive_dir = self.dirs['industry_library']
        elif category in ['Data', 'Signals', 'Technology']:
            archive_dir = self.dirs['industry_library']
        else:
            archive_dir = self.dirs['daily_workspace']

        # 创建归档文件路径
        date = get_current_date()
        archive_file = os.path.join(archive_dir, f"{category}_三行摘要_{date}.md")

        # 格式化摘要内容
        content = f"""
### {summary.get('title', '未命名材料')}
**1. What happened：** {summary.get('what_happened', '')}
**2. So what：** {summary.get('so_what', '')}
**3. Now what：** {summary.get('now_what', '')}
**标签：** {summary.get('tags', category)}
**时间：** {summary.get('date', date)}
**来源：** {summary.get('source', '未知')}

---

"""

        # 追加到归档文件
        try:
            append_to_file(archive_file, content)
            self.logger.info(f"三行摘要已归档到: {archive_file}")

            # 更新索引
            self._update_index(archive_file, summary, category)

            return archive_file
        except Exception as e:
            self.logger.error(f"归档失败: {e}")
            raise

    def archive_insight(self, insight: Dict[str, str], topic: str = "General") -> str:
        """
        归档洞察

        Args:
            insight: 洞察字典
            topic: 主题

        Returns:
            归档文件路径
        """
        self.logger.info(f"正在归档洞察到主题 '{topic}'...")

        # 创建洞察库目录
        insights_dir = os.path.join(self.dirs['topic_library'], "洞察库")
        os.makedirs(insights_dir, exist_ok=True)

        # 创建归档文件路径
        date = get_current_date()
        archive_file = os.path.join(insights_dir, f"{topic}_洞察_{date}.md")

        # 格式化洞察内容
        content = f"""
### 洞察：{insight.get('viewpoint', '未命名洞察')}
**依据：** {insight.get('evidence', '')}
**逻辑链：** {insight.get('logic', '')}
**趋势：** {insight.get('trend', '')}
**影响：** {insight.get('impact', '')}
**时间：** {date}

---

"""

        # 追加到归档文件
        try:
            append_to_file(archive_file, content)
            self.logger.info(f"洞察已归档到: {archive_file}")

            # 更新索引
            self._update_index(archive_file, insight, 'Insight')

            return archive_file
        except Exception as e:
            self.logger.error(f"归档失败: {e}")
            raise

    def archive_evidence_chain(self, evidence_chain: Dict[str, List[str]],
                               topic: str) -> str:
        """
        归档证据链

        Args:
            evidence_chain: 证据链字典
            topic: 主题

        Returns:
            归档文件路径
        """
        self.logger.info(f"正在归档证据链到主题 '{topic}'...")

        # 创建证据链库目录
        evidence_dir = os.path.join(self.dirs['topic_library'], "证据链库")
        os.makedirs(evidence_dir, exist_ok=True)

        # 创建归档文件路径
        date = get_current_date()
        archive_file = os.path.join(evidence_dir, f"{topic}_证据链_{date}.md")

        # 格式化证据链内容
        content = f"""
# {topic} - 证据链

**生成时间：** {date}

## F (Facts) - 事实
"""
        for evidence in evidence_chain.get('F', []):
            content += f"- {evidence}\n"

        content += "\n## D (Data) - 数据\n"
        for evidence in evidence_chain.get('D', []):
            content += f"- {evidence}\n"

        content += "\n## P (Policy) - 政策\n"
        for evidence in evidence_chain.get('P', []):
            content += f"- {evidence}\n"

        content += "\n## T (Trend) - 趋势\n"
        for evidence in evidence_chain.get('T', []):
            content += f"- {evidence}\n"

        content += "\n## S (Signal) - 弱信号\n"
        for evidence in evidence_chain.get('S', []):
            content += f"- {evidence}\n"

        content += "\n---\n\n"

        # 写入文件
        try:
            write_markdown_file(archive_file, content)
            self.logger.info(f"证据链已归档到: {archive_file}")

            # 更新索引
            self._update_index(archive_file, evidence_chain, 'EvidenceChain')

            return archive_file
        except Exception as e:
            self.logger.error(f"归档失败: {e}")
            raise

    def archive_weak_signal(self, signal: Dict[str, Any], domain: str = "General") -> str:
        """
        归档弱信号

        Args:
            signal: 弱信号字典
            domain: 领域

        Returns:
            归档文件路径
        """
        self.logger.info(f"正在归档弱信号到领域 '{domain}'...")

        # 创建弱信号库目录
        signals_dir = os.path.join(self.dirs['topic_library'], "弱信号库")
        os.makedirs(signals_dir, exist_ok=True)

        # 创建归档文件路径
        date = get_current_date()
        archive_file = os.path.join(signals_dir, f"{domain}_弱信号_{date}.md")

        # 格式化弱信号内容
        content = f"""
### 弱信号：{signal.get('description', '未命名信号')}
**可信度：** {signal.get('credibility', '未评估')}
**重要性：** {signal.get('importance', '未评估')}
**紧迫性：** {signal.get('urgency', '未评估')}
**确定性：** {signal.get('certainty', '未评估')}
**发现时间：** {date}

---

"""

        # 追加到归档文件
        try:
            append_to_file(archive_file, content)
            self.logger.info(f"弱信号已归档到: {archive_file}")

            # 更新索引
            self._update_index(archive_file, signal, 'WeakSignal')

            return archive_file
        except Exception as e:
            self.logger.error(f"归档失败: {e}")
            raise

    def _update_index(self, file_path: str, content: Dict[str, Any],
                     doc_type: str) -> None:
        """
        更新知识库索引

        Args:
            file_path: 文件路径
            content: 内容字典
            doc_type: 文档类型
        """
        doc_id = f"{doc_type}_{get_current_datetime()}"

        self.index['documents'][doc_id] = {
            'file_path': file_path,
            'type': doc_type,
            'created_at': get_current_datetime(),
            'content_preview': str(content)[:200]
        }

        # 自动生成标签
        if self.kb_config.get('auto_tagging', True):
            tags = self._generate_tags(content)
            for tag in tags:
                if tag not in self.index['tags']:
                    self.index['tags'][tag] = []
                if doc_id not in self.index['tags'][tag]:
                    self.index['tags'][tag].append(doc_id)

        # 保存索引
        self._save_index()

    def _generate_tags(self, content: Dict[str, Any]) -> List[str]:
        """
        自动生成标签

        Args:
            content: 内容字典

        Returns:
            标签列表
        """
        tags = []

        # 从内容中提取关键词作为标签
        text = str(content)

        # PIDST 维度标签
        for dimension in self.config['pidst']['dimensions']:
            keywords = dimension['keywords']
            for keyword in keywords:
                if keyword in text:
                    tags.append(dimension['label'])
                    break

        return list(set(tags))

    def search(self, query: str, doc_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        搜索知识库

        Args:
            query: 搜索关键词
            doc_type: 文档类型过滤

        Returns:
            搜索结果列表
        """
        self.logger.info(f"正在搜索: {query}")

        results = []
        query_lower = query.lower()

        for doc_id, doc_info in self.index['documents'].items():
            # 类型过滤
            if doc_type and doc_info['type'] != doc_type:
                continue

            # 关键词匹配
            if query_lower in doc_info['content_preview'].lower():
                results.append({
                    'doc_id': doc_id,
                    'file_path': doc_info['file_path'],
                    'type': doc_info['type'],
                    'created_at': doc_info['created_at'],
                    'preview': doc_info['content_preview']
                })

        self.logger.info(f"找到 {len(results)} 个结果")
        return results

    def find_related_knowledge(self, doc_id: str, threshold: float = 0.75) -> List[str]:
        """
        发现关联知识

        Args:
            doc_id: 文档ID
            threshold: 相似度阈值

        Returns:
            关联文档ID列表
        """
        self.logger.info(f"正在查找与 {doc_id} 相关的知识...")

        if doc_id not in self.index['documents']:
            self.logger.warning(f"文档 {doc_id} 不存在")
            return []

        # 获取文档标签
        doc_tags = []
        for tag, doc_ids in self.index['tags'].items():
            if doc_id in doc_ids:
                doc_tags.append(tag)

        # 查找具有相似标签的文档
        related_docs = []
        for other_doc_id in self.index['documents'].keys():
            if other_doc_id == doc_id:
                continue

            # 计算标签重叠度
            other_tags = []
            for tag, doc_ids in self.index['tags'].items():
                if other_doc_id in doc_ids:
                    other_tags.append(tag)

            if not other_tags:
                continue

            overlap = len(set(doc_tags) & set(other_tags))
            similarity = overlap / max(len(doc_tags), len(other_tags))

            if similarity >= threshold:
                related_docs.append(other_doc_id)

        self.logger.info(f"找到 {len(related_docs)} 个相关文档")
        return related_docs

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取知识库统计信息

        Returns:
            统计信息字典
        """
        stats = {
            'total_documents': len(self.index['documents']),
            'document_types': defaultdict(int),
            'total_tags': len(self.index['tags']),
            'last_update': self.index.get('last_update', 'Unknown')
        }

        for doc_info in self.index['documents'].values():
            stats['document_types'][doc_info['type']] += 1

        return dict(stats)

    def cleanup_old_files(self, days: int = 90) -> int:
        """
        清理旧文件

        Args:
            days: 保留天数

        Returns:
            清理的文件数量
        """
        self.logger.info(f"正在清理 {days} 天前的旧文件...")

        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0

        docs_to_remove = []
        for doc_id, doc_info in self.index['documents'].items():
            try:
                created_at = datetime.strptime(doc_info['created_at'], "%Y-%m-%d %H:%M:%S")
                if created_at < cutoff_date:
                    docs_to_remove.append(doc_id)
            except Exception as e:
                self.logger.warning(f"解析日期失败: {e}")

        # 从索引中移除
        for doc_id in docs_to_remove:
            del self.index['documents'][doc_id]
            cleaned_count += 1

        if cleaned_count > 0:
            self._save_index()
            self.logger.info(f"已清理 {cleaned_count} 个旧文档记录")

        return cleaned_count

    def rebuild_index(self) -> None:
        """重建知识库索引"""
        self.logger.info("正在重建知识库索引...")

        # 清空现有索引
        self.index = {
            'documents': {},
            'tags': defaultdict(list),
            'categories': defaultdict(list),
            'last_update': get_current_datetime()
        }

        # 扫描所有知识库目录
        directories = [
            self.dirs['industry_library'],
            self.dirs['topic_library'],
            "02-政策于宏观库"
        ]

        for directory in directories:
            if not os.path.exists(directory):
                continue

            md_files = find_markdown_files(directory)
            for file_path in md_files:
                try:
                    content = read_markdown_file(file_path)
                    doc_id = f"Rebuilt_{os.path.basename(file_path)}_{get_current_datetime()}"

                    self.index['documents'][doc_id] = {
                        'file_path': file_path,
                        'type': 'Unknown',
                        'created_at': get_current_datetime(),
                        'content_preview': content[:200]
                    }
                except Exception as e:
                    self.logger.warning(f"处理文件 {file_path} 失败: {e}")

        self._save_index()
        self.logger.info(f"索引重建完成，共索引 {len(self.index['documents'])} 个文档")
