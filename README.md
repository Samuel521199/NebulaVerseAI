# NebulaVerseAI

NebulaVerseAI 是一个基于 Google Gemini API 的智能对话系统，支持角色扮演和对话历史记录。

## 项目结构

```
NebulaVerseAI/
├── nebulaVerseAI.py      # 主程序入口
├── ai_persona.json       # AI角色配置文件
└── vector_db/            # 向量数据库模块
    ├── __init__.py      # 包初始化文件
    └── chroma_db.py     # ChromaDB管理类
```

## 功能特点

- 支持自定义AI角色设定
- 使用ChromaDB进行对话历史存储和检索
- 基于Google Gemini API的智能对话
- 支持多轮对话上下文
- 使用向量数据库实现高效的对话历史管理

## 环境要求

- Python 3.8+
- Google Gemini API密钥
- 依赖包：
  - requests
  - chromadb
  - json

## 使用方法

1. 设置环境变量：
   ```bash
   export GEMINI_API_KEY="你的API密钥"
   ```

2. 运行程序：
   ```bash
   python nebulaVerseAI.py
   ```

3. 如果没有设置环境变量，程序会提示输入API密钥

4. 开始对话，输入"exit"退出程序

## 配置说明

在 `ai_persona.json` 中配置AI角色：
```json
{
    "name": "角色名称",
    "description": "角色描述",
    "tone": "语气特点"
}
``` 