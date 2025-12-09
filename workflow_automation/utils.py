"""
工具函数模块
本小姐的实用工具箱！(￣ω￣)ノ
"""

import os
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"配置文件格式错误: {e}")


def load_prompts(prompts_path: str = "config/prompts.yaml") -> Dict[str, Any]:
    """
    加载提示词模板

    Args:
        prompts_path: 提示词文件路径

    Returns:
        提示词字典
    """
    try:
        with open(prompts_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts
    except FileNotFoundError:
        raise FileNotFoundError(f"提示词文件不存在: {prompts_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"提示词文件格式错误: {e}")


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """
    设置日志系统

    Args:
        config: 配置字典

    Returns:
        日志记录器
    """
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = log_config.get('file', 'logs/workflow.log')

    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 配置日志
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger('workflow_automation')


def get_current_date() -> str:
    """
    获取当前日期字符串

    Returns:
        格式化的日期字符串 (YYYY-MM-DD)
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_current_datetime() -> str:
    """
    获取当前日期时间字符串

    Returns:
        格式化的日期时间字符串 (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dir(directory: str) -> None:
    """
    确保目录存在，不存在则创建

    Args:
        directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)


def read_markdown_file(file_path: str) -> str:
    """
    读取 Markdown 文件内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise IOError(f"读取文件失败: {e}")


def write_markdown_file(file_path: str, content: str) -> None:
    """
    写入 Markdown 文件

    Args:
        file_path: 文件路径
        content: 文件内容
    """
    try:
        # 确保目录存在
        ensure_dir(os.path.dirname(file_path))

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"写入文件失败: {e}")


def append_to_file(file_path: str, content: str) -> None:
    """
    追加内容到文件

    Args:
        file_path: 文件路径
        content: 要追加的内容
    """
    try:
        # 确保目录存在
        ensure_dir(os.path.dirname(file_path))

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"追加文件失败: {e}")


def extract_keywords(text: str, keywords_list: List[str]) -> List[str]:
    """
    从文本中提取关键词

    Args:
        text: 文本内容
        keywords_list: 关键词列表

    Returns:
        匹配到的关键词列表
    """
    matched_keywords = []
    text_lower = text.lower()

    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            matched_keywords.append(keyword)

    return matched_keywords


def classify_by_pidst(text: str, config: Dict[str, Any]) -> List[str]:
    """
    根据 PIDST 框架对文本进行分类

    Args:
        text: 文本内容
        config: 配置字典

    Returns:
        匹配到的维度列表
    """
    dimensions = config.get('pidst', {}).get('dimensions', [])
    matched_dimensions = []

    for dimension in dimensions:
        keywords = dimension.get('keywords', [])
        if extract_keywords(text, keywords):
            matched_dimensions.append(dimension['name'])

    return matched_dimensions if matched_dimensions else ['General']


def format_three_line_summary(title: str, what: str, so_what: str, now_what: str,
                              tags: List[str], date: str, source: str) -> str:
    """
    格式化三行摘要

    Args:
        title: 材料名称
        what: What happened
        so_what: So what
        now_what: Now what
        tags: 标签列表
        date: 日期
        source: 来源

    Returns:
        格式化的三行摘要文本
    """
    tags_str = "/".join(tags)

    return f"""### {title}
**1. What happened：** {what}
**2. So what：** {so_what}
**3. Now what：** {now_what}
**标签：** {tags_str}
**时间：** {date}
**来源：** {source}

---

"""


def format_insight(number: int, viewpoint: str, evidence: str,
                   logic: str, trend: str, impact: str) -> str:
    """
    格式化洞察

    Args:
        number: 洞察序号
        viewpoint: 核心观点
        evidence: 支撑证据
        logic: 推理过程
        trend: 未来走向
        impact: 可能影响

    Returns:
        格式化的洞察文本
    """
    return f"""### 洞察 {number}：{viewpoint}
**依据：** {evidence}
**逻辑链：** {logic}
**趋势：** {trend}
**影响：** {impact}

---

"""


def get_importance_marker(level: str, config: Dict[str, Any]) -> str:
    """
    获取重要程度标记

    Args:
        level: 重要程度 (high/medium/low)
        config: 配置字典

    Returns:
        重要程度标记符号
    """
    markers = config.get('analysis', {}).get('importance_levels', {})
    return markers.get(level, '⚪')


def find_markdown_files(directory: str, pattern: str = "*.md") -> List[str]:
    """
    查找目录下的 Markdown 文件

    Args:
        directory: 目录路径
        pattern: 文件匹配模式

    Returns:
        文件路径列表
    """
    path = Path(directory)
    return [str(f) for f in path.glob(pattern) if f.is_file()]


def parse_markdown_sections(content: str) -> Dict[str, str]:
    """
    解析 Markdown 文件的章节

    Args:
        content: Markdown 内容

    Returns:
        章节字典 {标题: 内容}
    """
    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith('##'):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line.strip('#').strip()
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def validate_config(config: Dict[str, Any]) -> bool:
    """
    验证配置文件的完整性

    Args:
        config: 配置字典

    Returns:
        是否有效
    """
    required_keys = ['ai', 'directories', 'pidst', 'analysis']

    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置文件缺少必需的键: {key}")

    return True
