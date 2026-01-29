---
name: ace-serena-collaborator
description: |
  Ace-Tool 与 Serena MCP 协作流程。触发场景：(1) 需要理解代码库结构 (2) 语义代码搜索 (3) 符号级代码定位 (4) 代码导航和分析。提供两阶段协作：Ace-Tool 语义搜索→Serena 精确定位，强调只读安全与工具互补。
---

# Ace-Tool & Serena 协作指南

两个 MCP 工具的协作流程，用于高效理解和导航代码库。

## 工具定位

| 工具 | 核心能力 | 适用场景 |
|------|----------|----------|
| **Ace-Tool** | 语义搜索、自然语言查询 | 不知道代码在哪、探索性搜索 |
| **Serena** | 符号级精确定位、LSP 集成 | 知道符号名、需要精确引用 |

## 核心约束（MUST）

- **Serena 仅用于检索/定位，严禁修改代码**
- Ace-Tool 的 `search_context` 用于语义搜索
- 两个工具都是只读工具，不执行任何写操作

## 协作流程

### 场景 1：探索未知代码

```
用户："用户认证是怎么实现的？"

1. Ace-Tool search_context
   → 语义搜索 "用户认证实现"
   → 获取相关文件和代码片段

2. Serena find_symbol (可选)
   → 对搜索结果中的关键符号深入分析
   → 获取精确的符号定义和引用
```

### 场景 2：定位已知符号

```
用户："找到 AuthService 类的所有引用"

1. Serena find_symbol
   → 直接定位 AuthService
   → 获取定义位置

2. Serena find_referencing_symbols
   → 查找所有引用该符号的位置
```

### 场景 3：混合搜索

```
用户："数据库连接池是怎么配置的？"

1. Ace-Tool search_context
   → 语义搜索 "数据库连接池配置"
   → 获取相关配置文件和代码

2. Serena (如果需要深入)
   → 对发现的配置类进行符号分析
```

## 工具选择决策树

```
需要理解代码？
├── 不知道在哪 → Ace-Tool search_context
├── 知道符号名 → Serena find_symbol
└── 需要引用关系 → Serena find_referencing_symbols

搜索类型？
├── 自然语言描述 → Ace-Tool
├── 精确符号名 → Serena
└── 模糊 + 精确 → Ace-Tool → Serena
```

## 工具调用规范

### Ace-Tool search_context

```
参数：
- project_root_path: 项目根目录绝对路径
- query: 自然语言查询（支持中英文）

示例查询：
- "用户登录流程的实现"
- "API 错误处理机制"
- "数据库事务管理"
```

### Serena 常用工具

| 工具 | 用途 |
|------|------|
| `find_symbol` | 查找符号定义 |
| `find_referencing_symbols` | 查找符号引用 |
| `get_symbol_definition` | 获取符号完整定义 |
| `list_symbols_in_file` | 列出文件中的所有符号 |

详细参数见 [references/serena-tools.md](references/serena-tools.md)

## 最佳实践

1. **先广后深**：Ace-Tool 广泛搜索 → Serena 精确定位
2. **语义优先**：不确定时先用 Ace-Tool 语义搜索
3. **符号追踪**：需要引用关系时用 Serena
4. **只读原则**：两个工具都不修改代码，修改使用 Edit/Write 工具
