#!/bin/bash
# 同步 baoyu-skills 到 .claude/skills 目录

TRAE_SKILLS="../../.trae/skills"
CLAUDE_SKILLS="."

echo "开始同步 baoyu-skills..."

for skill in "$TRAE_SKILLS"/baoyu-*; do
    if [ -d "$skill" ]; then
        skill_name=$(basename "$skill")

        # 如果已存在,先删除
        if [ -e "$CLAUDE_SKILLS/$skill_name" ]; then
            rm -rf "$CLAUDE_SKILLS/$skill_name"
        fi

        # 创建符号链接
        ln -s "$skill" "$CLAUDE_SKILLS/$skill_name"
        echo "✓ $skill_name"
    fi
done

echo "同步完成!"
