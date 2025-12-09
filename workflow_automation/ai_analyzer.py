"""
AI 分析引擎模块
本小姐的智能分析大脑！(￣ω￣)ノ

功能：
- 三行摘要生成
- 观点提炼
- 证据链构建
- 趋势判断
- 弱信号识别
"""

import os
import logging
import urllib.parse
from typing import Dict, Any, List, Optional
from openai import OpenAI
from anthropic import Anthropic

from .utils import (
    load_config,
    load_prompts,
    format_three_line_summary,
    format_insight,
    get_current_date
)


class AIAnalyzer:
    """AI 分析引擎类"""

    def __init__(self, config_path: str = "config/config.yaml",
                 prompts_path: str = "config/prompts.yaml"):
        """
        初始化 AI 分析引擎

        Args:
            config_path: 配置文件路径
            prompts_path: 提示词文件路径
        """
        self.config = load_config(config_path)
        self.prompts = load_prompts(prompts_path)
        self.logger = logging.getLogger(__name__)

        # 初始化 AI 客户端
        self._init_ai_client()

    def _init_ai_client(self) -> None:
        """初始化 AI 客户端"""
        ai_config = self.config['ai']
        provider = ai_config.get('provider', 'openai')

        if provider == 'openai':
            api_key = ai_config.get('api_key')
            if not api_key or api_key == 'your-api-key-here':
                self.logger.warning("未配置 OpenAI API Key，请在 config.yaml 中设置")
                self.client = None
            else:
                self.client = OpenAI(api_key=api_key)
                self.model = ai_config.get('model', 'gpt-4')

        elif provider == 'anthropic':
            api_key = ai_config.get('api_key')
            if not api_key or api_key == 'your-api-key-here':
                self.logger.warning("未配置 Anthropic API Key，请在 config.yaml 中设置")
                self.client = None
            else:
                self.client = Anthropic(api_key=api_key)
                self.model = ai_config.get('model', 'claude-3-sonnet-20240229')

        elif provider == 'openrouter':
            # OpenRouter 配置（支持多种模型！本小姐最推荐的方式）
            openrouter_config = ai_config.get('openrouter', {})
            api_key = openrouter_config.get('api_key')

            if not api_key or api_key == 'your-openrouter-api-key-here':
                self.logger.warning("未配置 OpenRouter API Key，请在 config.yaml 的 ai.openrouter.api_key 中设置")
                self.client = None
            else:
                # OpenRouter 使用 OpenAI 兼容的 API 格式
                base_url = openrouter_config.get('base_url', 'https://openrouter.ai/api/v1')
                self.model = openrouter_config.get('model', 'anthropic/claude-3.5-sonnet')

                # 设置额外的 headers（OpenRouter 特有）
                extra_headers = {}
                if openrouter_config.get('site_url'):
                    site_url = openrouter_config['site_url']
                    try:
                        site_url.encode('ascii')
                        extra_headers['HTTP-Referer'] = site_url
                    except UnicodeEncodeError:
                        extra_headers['HTTP-Referer'] = urllib.parse.quote(site_url)
                        
                if openrouter_config.get('app_name'):
                    app_name = openrouter_config['app_name']
                    try:
                        app_name.encode('ascii')
                        extra_headers['X-Title'] = app_name
                    except UnicodeEncodeError:
                        extra_headers['X-Title'] = urllib.parse.quote(app_name)

                self.client = OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                    default_headers=extra_headers
                )
                self.logger.info(f"使用 OpenRouter 模型: {self.model}")

        elif provider == 'local':
            # 本地模型配置（如 Ollama）
            local_config = ai_config.get('local_model', {})
            self.endpoint = local_config.get('endpoint', 'http://localhost:11434')
            self.model = local_config.get('model_name', 'llama2')
            self.client = None  # 本地模型使用 requests 调用
            self.logger.info(f"使用本地模型: {self.model} @ {self.endpoint}")

        else:
            raise ValueError(f"不支持的 AI 提供商: {provider}")

        self.provider = provider
        self.temperature = ai_config.get('temperature', 0.7)
        self.max_tokens = ai_config.get('max_tokens', 2000)

    def _call_ai(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用 AI 模型

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词

        Returns:
            AI 生成的文本
        """
        if not self.client and self.provider != 'local':
            raise ValueError("AI 客户端未初始化，请检查配置文件中的 API Key")

        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content

            elif self.provider == 'openrouter':
                # OpenRouter 使用 OpenAI 兼容的 API 格式（本小姐最推荐的方式！）
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content

            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text

            elif self.provider == 'local':
                # 使用本地模型（Ollama）
                import requests
                response = requests.post(
                    f"{self.endpoint}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{user_prompt}",
                        "stream": False
                    }
                )
                return response.json()['response']

        except Exception as e:
            self.logger.error(f"AI 调用失败: {e}")
            raise

    def generate_three_line_summary(self, content: str, source: str = "",
                                    date: str = "") -> Dict[str, str]:
        """
        生成三行摘要

        Args:
            content: 材料内容
            source: 材料来源
            date: 材料时间

        Returns:
            三行摘要字典
        """
        self.logger.info("正在生成三行摘要...")

        if not date:
            date = get_current_date()

        # 获取提示词模板
        prompt_template = self.prompts['three_line_summary']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            content=content,
            source=source,
            date=date
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析响应（简单实现，实际可能需要更复杂的解析）
        lines = response.strip().split('\n')
        result = {
            'what_happened': '',
            'so_what': '',
            'now_what': '',
            'raw_response': response
        }

        for line in lines:
            if 'What happened' in line or '发生了什么' in line:
                result['what_happened'] = line.split('：')[-1].strip()
            elif 'So what' in line or '意味着什么' in line:
                result['so_what'] = line.split('：')[-1].strip()
            elif 'Now what' in line or '下一步如何' in line:
                result['now_what'] = line.split('：')[-1].strip()

        self.logger.info("三行摘要生成完成")
        return result

    def extract_insights(self, information: str, min_insights: int = 3) -> List[Dict[str, str]]:
        """
        提炼洞察

        Args:
            information: 信息汇总
            min_insights: 最少洞察数量

        Returns:
            洞察列表
        """
        self.logger.info(f"正在提炼至少 {min_insights} 个洞察...")

        # 获取提示词模板
        prompt_template = self.prompts['insight_extraction']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            min_insights=min_insights,
            information=information
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析洞察（简化实现）
        insights = []
        current_insight = {}

        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('### 洞察'):
                if current_insight:
                    insights.append(current_insight)
                current_insight = {'viewpoint': line.split('：')[-1].strip()}
            elif line.startswith('**依据：**'):
                current_insight['evidence'] = line.split('**依据：**')[-1].strip()
            elif line.startswith('**逻辑链：**'):
                current_insight['logic'] = line.split('**逻辑链：**')[-1].strip()
            elif line.startswith('**趋势：**'):
                current_insight['trend'] = line.split('**趋势：**')[-1].strip()
            elif line.startswith('**影响：**'):
                current_insight['impact'] = line.split('**影响：**')[-1].strip()

        if current_insight:
            insights.append(current_insight)

        self.logger.info(f"成功提炼 {len(insights)} 个洞察")
        return insights

    def build_evidence_chain(self, topic: str, information: str) -> Dict[str, List[str]]:
        """
        构建证据链

        Args:
            topic: 研究主题
            information: 已收集信息

        Returns:
            证据链字典 {维度: [证据列表]}
        """
        self.logger.info(f"正在为主题 '{topic}' 构建证据链...")

        # 获取提示词模板
        prompt_template = self.prompts['evidence_chain']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            topic=topic,
            information=information
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析证据链
        evidence_chain = {
            'F': [],  # Facts
            'D': [],  # Data
            'P': [],  # Policy
            'T': [],  # Trend
            'S': []   # Signal
        }

        current_dimension = None
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('**F') or line.startswith('### F'):
                current_dimension = 'F'
            elif line.startswith('**D') or line.startswith('### D'):
                current_dimension = 'D'
            elif line.startswith('**P') or line.startswith('### P'):
                current_dimension = 'P'
            elif line.startswith('**T') or line.startswith('### T'):
                current_dimension = 'T'
            elif line.startswith('**S') or line.startswith('### S'):
                current_dimension = 'S'
            elif line.startswith('-') and current_dimension:
                evidence_chain[current_dimension].append(line[1:].strip())

        self.logger.info("证据链构建完成")
        return evidence_chain

    def analyze_trend(self, domain: str, information: str,
                     timeframe: str = "未来1-3年") -> Dict[str, str]:
        """
        趋势判断分析

        Args:
            domain: 分析领域
            information: 相关信息
            timeframe: 时间范围

        Returns:
            趋势分析字典
        """
        self.logger.info(f"正在分析 '{domain}' 的发展趋势...")

        # 获取提示词模板
        prompt_template = self.prompts['trend_analysis']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            domain=domain,
            information=information,
            timeframe=timeframe
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析趋势分析
        trend_analysis = {
            'current_state': '',
            'drivers': '',
            'direction': '',
            'key_points': '',
            'risks': '',
            'raw_response': response
        }

        for line in response.split('\n'):
            if '当前状态' in line:
                trend_analysis['current_state'] = line.split('：')[-1].strip()
            elif '变化动因' in line or '驱动因素' in line:
                trend_analysis['drivers'] = line.split('：')[-1].strip()
            elif '发展方向' in line or '未来趋势' in line:
                trend_analysis['direction'] = line.split('：')[-1].strip()
            elif '关键节点' in line:
                trend_analysis['key_points'] = line.split('：')[-1].strip()
            elif '风险提示' in line:
                trend_analysis['risks'] = line.split('：')[-1].strip()

        self.logger.info("趋势分析完成")
        return trend_analysis

    def detect_weak_signals(self, content: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
        """
        识别弱信号

        Args:
            content: 信息内容
            focus_areas: 关注领域列表

        Returns:
            弱信号列表
        """
        self.logger.info("正在识别弱信号...")

        # 获取提示词模板
        prompt_template = self.prompts['weak_signal_detection']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            content=content,
            focus_areas=', '.join(focus_areas)
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析弱信号（简化实现）
        weak_signals = []
        current_signal = {}

        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('###') or line.startswith('**信号'):
                if current_signal:
                    weak_signals.append(current_signal)
                current_signal = {'description': line.strip('#').strip()}
            elif '可信度' in line:
                current_signal['credibility'] = line.split('：')[-1].strip()
            elif '重要性' in line:
                current_signal['importance'] = line.split('：')[-1].strip()
            elif '紧迫性' in line:
                current_signal['urgency'] = line.split('：')[-1].strip()
            elif '确定性' in line:
                current_signal['certainty'] = line.split('：')[-1].strip()

        if current_signal:
            weak_signals.append(current_signal)

        self.logger.info(f"识别到 {len(weak_signals)} 个弱信号")
        return weak_signals

    def classify_by_pidst(self, content: str) -> List[str]:
        """
        按 PIDST 框架分类

        Args:
            content: 内容

        Returns:
            分类维度列表
        """
        self.logger.info("正在进行 PIDST 分类...")

        # 获取提示词模板
        prompt_template = self.prompts['pidst_classification']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(content=content)

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        # 解析分类结果
        dimensions = []
        for line in response.split('\n'):
            if '主要维度' in line or '次要维度' in line:
                for dim in ['Policy', 'Industry', 'Data', 'Signals', 'Technology']:
                    if dim in line or dim[0] in line:
                        dimensions.append(dim)

        self.logger.info(f"分类结果: {', '.join(dimensions)}")
        return dimensions if dimensions else ['General']

    def generate_daily_summary(self, tasks: str, completed: str,
                              information: str, insights: str) -> str:
        """
        生成每日总结

        Args:
            tasks: 今日任务
            completed: 完成情况
            information: 收集信息
            insights: 生成洞察

        Returns:
            每日总结文本
        """
        self.logger.info("正在生成每日总结...")

        # 获取提示词模板
        prompt_template = self.prompts['daily_summary']
        system_prompt = prompt_template['system']
        user_prompt = prompt_template['user'].format(
            tasks=tasks,
            completed=completed,
            information=information,
            insights=insights
        )

        # 调用 AI
        response = self._call_ai(system_prompt, user_prompt)

        self.logger.info("每日总结生成完成")
        return response
