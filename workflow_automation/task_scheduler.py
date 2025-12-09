"""
任务调度器模块
本小姐的时间管理大师！(￣ω￣)ノ

功能：
- 每日任务模板生成
- 工作流程提醒
- 进度追踪
- 复盘报告生成
"""

import os
import logging
from datetime import datetime, time
from typing import Dict, Any, List, Optional

from .utils import (
    load_config,
    read_markdown_file,
    write_markdown_file,
    append_to_file,
    get_current_date,
    get_current_datetime
)


class TaskScheduler:
    """任务调度器类"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化任务调度器

        Args:
            config_path: 配置文件路径
        """
        self.config = load_config(config_path)
        self.logger = logging.getLogger(__name__)

        # 获取配置
        self.dirs = self.config['directories']
        self.scheduler_config = self.config['scheduler']

    def generate_daily_task_template(self, date: Optional[str] = None) -> str:
        """
        生成每日任务模板

        Args:
            date: 日期（默认为今天）

        Returns:
            任务文件路径
        """
        if not date:
            date = get_current_date()

        self.logger.info(f"正在生成 {date} 的每日任务模板...")

        # 创建任务文件路径
        task_file = os.path.join(
            self.dirs['daily_workspace'],
            "00-今日任务",
            f"今日任务_{date}.md"
        )

        # 生成任务模板内容
        template = f"""# 今日任务 - {date}

## 📋 今日最重要的三件事（MIT）
1. [ ] [具体任务1 - 描述清楚要做什么]
2. [ ] [具体任务2 - 描述清楚要做什么]
3. [ ] [具体任务3 - 描述清楚要做什么]

## 🎯 任务类型分类

### 政府库/行业库更新
- [ ] [具体更新内容]

### 决策支持研究
- [ ] [具体项目，如中远海运跟踪]

### 专题研究推进
- [ ] [具体专题推进]

## 📊 今日最小交付物（MVP）
- [明确的输出物描述]

## ⏰ 时间规划

### 信息采集阶段（45-90分钟）
- **开始时间：** 09:00
- **结束时间：** 10:30
- **PIDST 检索清单：**
  - [ ] P - 政策层面
  - [ ] I - 产业层面
  - [ ] D - 数据层面
  - [ ] S - 信号层面
  - [ ] T - 技术层面

### 分析思考阶段（30分钟）
- **开始时间：** 10:30
- **结束时间：** 11:00
- **任务：**
  - [ ] 信息归类和分级
  - [ ] 识别趋势和模式
  - [ ] 发现弱信号

### 观点提炼阶段（15分钟）
- **开始时间：** 11:00
- **结束时间：** 11:15
- **目标：** 提炼至少 3 个核心洞察

### 结构化输出阶段（30-60分钟）
- **开始时间：** 14:00
- **结束时间：** 15:00
- **输出物：** [根据任务类型确定]

### 知识沉淀阶段（15-20分钟）
- **开始时间：** 17:30
- **结束时间：** 17:50
- **任务：**
  - [ ] 三行摘要归档
  - [ ] 弱信号更新
  - [ ] 观点更新
  - [ ] 专题内容归档

## 📝 工作记录

### 完成情况
-

### 遇到的问题
-

### 解决方案
-

## 💡 今日洞察
1.
2.
3.

---

*生成时间：{get_current_datetime()}*
*本模板由智库工作流自动化系统生成*
"""

        # 写入文件
        try:
            os.makedirs(os.path.dirname(task_file), exist_ok=True)
            write_markdown_file(task_file, template)
            self.logger.info(f"每日任务模板已生成: {task_file}")
            return task_file
        except Exception as e:
            self.logger.error(f"生成任务模板失败: {e}")
            raise

    def generate_review_template(self, date: Optional[str] = None) -> str:
        """
        生成复盘模板

        Args:
            date: 日期（默认为今天）

        Returns:
            复盘文件路径
        """
        if not date:
            date = get_current_date()

        self.logger.info(f"正在生成 {date} 的复盘模板...")

        # 创建复盘文件路径
        review_file = os.path.join(
            self.dirs['daily_workspace'],
            "00-今日任务",
            f"今日复盘_{date}.md"
        )

        # 生成复盘模板内容
        template = f"""# 今日复盘 - {date}

## ✅ 今天做得好的3件事
1. [具体成果1 - 说明为什么做得好]
2. [具体成果2 - 说明为什么做得好]
3. [具体成果3 - 说明为什么做得好]

## 📊 任务完成情况

### 计划任务
- [ ] 任务1：[完成情况]
- [ ] 任务2：[完成情况]
- [ ] 任务3：[完成情况]

### 完成率
- **计划任务数：**
- **实际完成数：**
- **完成率：** %

## 🎯 输出物清单
- [输出物1 - 文件路径或描述]
- [输出物2 - 文件路径或描述]
- [输出物3 - 文件路径或描述]

## 💡 今日核心洞察
1. [洞察1 - 简要描述]
2. [洞察2 - 简要描述]
3. [洞察3 - 简要描述]

## 📚 知识沉淀
- **三行摘要数量：**
- **归档文件：**
- **新增标签：**
- **关联知识：**

## ⚠️ 今天遇到的问题

### 问题1：[问题描述]
- **原因分析：**
- **解决方案：**
- **经验教训：**

### 问题2：[问题描述]
- **原因分析：**
- **解决方案：**
- **经验教训：**

## 🔄 流程优化建议
- [优化建议1]
- [优化建议2]
- [优化建议3]

## 📈 明日优化点
- [改进方向1]
- [改进方向2]
- [改进方向3]

## 🎯 明日重点任务
1. [明日任务1 - 优先级：高/中/低]
2. [明日任务2 - 优先级：高/中/低]
3. [明日任务3 - 优先级：高/中/低]

## 📊 时间分配分析

### 实际时间分配
- **信息采集：** 分钟
- **分析思考：** 分钟
- **观点提炼：** 分钟
- **结构化输出：** 分钟
- **知识沉淀：** 分钟

### 时间效率评估
- **高效时段：**
- **低效时段：**
- **改进建议：**

## 💪 个人成长
- **新学到的知识：**
- **提升的能力：**
- **需要加强的方面：**

---

*生成时间：{get_current_datetime()}*
*本模板由智库工作流自动化系统生成*
"""

        # 写入文件
        try:
            os.makedirs(os.path.dirname(review_file), exist_ok=True)
            write_markdown_file(review_file, template)
            self.logger.info(f"复盘模板已生成: {review_file}")
            return review_file
        except Exception as e:
            self.logger.error(f"生成复盘模板失败: {e}")
            raise

    def check_task_progress(self, task_file: str) -> Dict[str, Any]:
        """
        检查任务进度

        Args:
            task_file: 任务文件路径

        Returns:
            进度统计字典
        """
        self.logger.info(f"正在检查任务进度: {task_file}")

        try:
            content = read_markdown_file(task_file)

            # 统计任务完成情况
            total_tasks = content.count('- [ ]') + content.count('- [x]') + content.count('- [X]')
            completed_tasks = content.count('- [x]') + content.count('- [X]')

            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            progress = {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': total_tasks - completed_tasks,
                'completion_rate': round(completion_rate, 2)
            }

            self.logger.info(f"任务进度: {completed_tasks}/{total_tasks} ({completion_rate:.2f}%)")
            return progress

        except Exception as e:
            self.logger.error(f"检查任务进度失败: {e}")
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'completion_rate': 0
            }

    def generate_weekly_summary(self, start_date: str, end_date: str) -> str:
        """
        生成周总结

        Args:
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            周总结文件路径
        """
        self.logger.info(f"正在生成 {start_date} 至 {end_date} 的周总结...")

        # 创建周总结文件路径
        summary_file = os.path.join(
            self.dirs['daily_workspace'],
            "00-今日任务",
            f"周总结_{start_date}_to_{end_date}.md"
        )

        # 生成周总结模板
        template = f"""# 周总结 - {start_date} 至 {end_date}

## 📊 本周工作概览

### 核心成果
1. [成果1]
2. [成果2]
3. [成果3]

### 任务完成情况
- **计划任务总数：**
- **实际完成数：**
- **完成率：** %

## 💡 本周核心洞察

### 洞察1：[标题]
- **描述：**
- **影响：**
- **行动建议：**

### 洞察2：[标题]
- **描述：**
- **影响：**
- **行动建议：**

### 洞察3：[标题]
- **描述：**
- **影响：**
- **行动建议：**

## 📚 知识沉淀统计
- **三行摘要数量：**
- **洞察数量：**
- **证据链数量：**
- **弱信号数量：**
- **新增文档：**

## 🎯 重点项目进展

### 项目1：[项目名称]
- **本周进展：**
- **完成度：** %
- **下周计划：**

### 项目2：[项目名称]
- **本周进展：**
- **完成度：** %
- **下周计划：**

## ⚠️ 问题与挑战
1. [问题1及解决方案]
2. [问题2及解决方案]
3. [问题3及解决方案]

## 🔄 流程优化
- [优化点1]
- [优化点2]
- [优化点3]

## 📈 下周重点
1. [重点任务1]
2. [重点任务2]
3. [重点任务3]

## 💪 个人成长
- **新掌握的技能：**
- **提升的能力：**
- **下周学习目标：**

---

*生成时间：{get_current_datetime()}*
*本模板由智库工作流自动化系统生成*
"""

        # 写入文件
        try:
            os.makedirs(os.path.dirname(summary_file), exist_ok=True)
            write_markdown_file(summary_file, template)
            self.logger.info(f"周总结模板已生成: {summary_file}")
            return summary_file
        except Exception as e:
            self.logger.error(f"生成周总结失败: {e}")
            raise

    def is_workday(self, date: Optional[datetime] = None) -> bool:
        """
        判断是否为工作日

        Args:
            date: 日期（默认为今天）

        Returns:
            是否为工作日
        """
        if not date:
            date = datetime.now()

        weekday = date.isoweekday()  # 1=周一, 7=周日
        workdays = self.scheduler_config.get('workdays', [1, 2, 3, 4, 5])

        return weekday in workdays

    def should_send_reminder(self, reminder_type: str) -> bool:
        """
        判断是否应该发送提醒

        Args:
            reminder_type: 提醒类型（daily_reminder/review_reminder）

        Returns:
            是否应该发送提醒
        """
        # 检查是否为工作日
        if not self.is_workday():
            return False

        # 获取提醒时间配置
        reminder_time_str = self.scheduler_config.get(reminder_type, "09:00")
        reminder_hour, reminder_minute = map(int, reminder_time_str.split(':'))

        # 获取当前时间
        now = datetime.now()
        current_time = time(now.hour, now.minute)
        reminder_time = time(reminder_hour, reminder_minute)

        # 判断是否到达提醒时间（允许5分钟误差）
        time_diff = abs((now.hour * 60 + now.minute) - (reminder_hour * 60 + reminder_minute))

        return time_diff <= 5

    def get_pending_tasks(self, task_file: str) -> List[str]:
        """
        获取待办任务列表

        Args:
            task_file: 任务文件路径

        Returns:
            待办任务列表
        """
        try:
            content = read_markdown_file(task_file)
            pending_tasks = []

            for line in content.split('\n'):
                if '- [ ]' in line:
                    task = line.replace('- [ ]', '').strip()
                    if task:
                        pending_tasks.append(task)

            return pending_tasks

        except Exception as e:
            self.logger.error(f"获取待办任务失败: {e}")
            return []

    def mark_task_completed(self, task_file: str, task_text: str) -> bool:
        """
        标记任务为已完成

        Args:
            task_file: 任务文件路径
            task_text: 任务文本

        Returns:
            是否成功
        """
        try:
            content = read_markdown_file(task_file)

            # 替换任务状态
            updated_content = content.replace(
                f"- [ ] {task_text}",
                f"- [x] {task_text}"
            )

            if content != updated_content:
                write_markdown_file(task_file, updated_content)
                self.logger.info(f"任务已标记为完成: {task_text}")
                return True
            else:
                self.logger.warning(f"未找到任务: {task_text}")
                return False

        except Exception as e:
            self.logger.error(f"标记任务失败: {e}")
            return False

    def generate_reminder_message(self, reminder_type: str) -> str:
        """
        生成提醒消息

        Args:
            reminder_type: 提醒类型

        Returns:
            提醒消息
        """
        if reminder_type == 'daily_reminder':
            return f"""
🌅 早上好！新的一天开始了！

📋 今日工作提醒：
1. 打开今日任务文件，明确核心任务
2. 按照 PIDST 框架进行信息采集
3. 记得完成三行摘要处理
4. 提炼至少 3 个核心洞察

💪 加油！本小姐相信你能完成今天的任务！(￣▽￣)／

---
*提醒时间：{get_current_datetime()}*
"""

        elif reminder_type == 'review_reminder':
            return f"""
🌆 一天的工作快结束了！

📝 复盘提醒：
1. 回顾今日任务完成情况
2. 记录今天的核心洞察
3. 完成知识库归档
4. 填写今日复盘模板
5. 设定明日重点任务

🎯 坚持复盘，持续成长！(￣ω￣)ノ

---
*提醒时间：{get_current_datetime()}*
"""

        else:
            return "未知的提醒类型"
