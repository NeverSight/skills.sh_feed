---
name: git-commit-analyzer
description: >
  用 AI 分析 git 提交，鉴定你今天是「夯」还是「拉完了」。
  支持 GitHub、GitLab、本地仓库。双语输出，两种风格（打工人/Linus）。
---

# Git Commit Analyzer - 牛马鉴定器 🐂🐴

用 AI 分析 git 提交，鉴定你今天是「夯」还是「拉完了」。

传统指标（行数、提交数）无法反映真实贡献。本工具用 AI 的代码理解能力，给出灵魂拷问的答案：**你今天到底卷没卷？**

## 安装

```bash
# 安装 skill
npx skills add shaoxyz/git-commit-analyzer

# ast-grep（可选，启用多语言 AST 代码分析）
npm i -g @ast-grep/cli
```

## Quick Start

```bash
SKILL_DIR=~/.claude/skills/git-commit-analyzer

# 1. 获取提交
python $SKILL_DIR/scripts/fetch_commits.py /path/to/repo --since "1 day ago" -o commits.json
# GitHub: --github owner/repo (需要 GITHUB_TOKEN)

# 2. 客观分析（计算 substance_score / bullshit_score）
python $SKILL_DIR/scripts/analyze_code.py commits.json

# 3. 生成 prompt（同时输出打工人 + Linus 双风格）
python $SKILL_DIR/scripts/generate_prompt.py commits.json > prompt.txt

# 4. 发给 Claude，保存结果为 analysis.json

# 5. 生成报告
python $SKILL_DIR/scripts/generate_report.py analysis.json
```

## 牛马等级

| 日总分 | 等级 | 称号 | 颁奖词 | Linus 说 |
|--------|------|------|--------|----------|
| ≥ 40 | 🔥 夯 | 代码之神 | 建议申请调薪 | "Not bad. I've seen worse." |
| 25-39 | 💎 顶级 | 团队支柱 | 老板看了直呼内行 | "Acceptable." |
| 15-24 | 👑 人上人 | 稳定输出 | 职场中坚力量 | "It works, I guess." |
| 5-14 | 🧍 NPC | 打工人 | 今天也是普通的一天 | "Do you even know what you're doing?" |
| < 5 | 💀 拉完了 | 带薪摸鱼 | 明天记得努力 | "What the fuck is this shit?" |

## 评分体系（2026 AI 时代版）

> 在 Vibe Coding 时代，代码量不代表贡献，**脑子才是**。

### 🤖 核心维度：重写指数（Rewrite Index）

**问：让 AI 重写这段代码需要多久？**

| 分数 | 含义 | 系数 | Linus 说 |
|------|------|------|----------|
| 1/5 | AI 10 分钟搞定 | ×0.5 | "Why did a human write this?" |
| 2/5 | AI 需要一些上下文 | ×0.8 | "An intern with ChatGPT could do this." |
| 3/5 | 需要业务知识输入 | ×1.0 | "At least you know the domain." |
| 4/5 | AI 只能写框架 | ×1.1 | "Okay, you actually thought about this." |
| 5/5 | AI 写不出来 | ×1.3 | "Finally, irreplaceable human value." |

### 💎 业务价值（Business Value）

| 等级 | 定义 | 系数 | 打工人说 |
|------|------|------|----------|
| 💎 核心资产 | 直接影响收入/用户 | ×1.5 | "动这个代码记得买保险" |
| 🧱 支撑设施 | 基础设施、工具链 | ×1.0 | "脏活累活有人干" |
| 🎨 锦上添花 | 体验优化、UI 调整 | ×0.6 | "老板喜欢，用户无感" |
| 💀 存在即浪费 | 没人用、没人懂 | ×0.2 | "删了也没人发现" |

### 📊 参考指标（机器计算）

- **substance_score**：实质分（有效代码行、函数/类新增、测试覆盖）
- **bullshit_score**：水分（格式化、重命名、自动生成、复制粘贴）

> ⚠️ 这些是参考数据，不再是核心评判标准

### 最终得分公式

```
最终得分 = 基础分 × 业务价值系数 × 重写指数系数
```

**举例**：
- 写了个 CRUD 接口（基础分 20）+ 锦上添花（×0.6）+ AI 能写（×0.5）= **6 分** 💀
- 修了个支付 bug（基础分 15）+ 核心资产（×1.5）+ 需要业务知识（×1.0）= **22.5 分** 👑

### 传统维度（保留参考）

<details>
<summary>Complexity Score / Impact Score（点击展开）</summary>

#### Complexity Score（技术深度）1-5

| 分数 | 等级 | 例子 |
|------|------|------|
| 1 | 摸鱼级 | typo、配置、自动生成 |
| 2 | 简单级 | 改变量名、小 UI 调整 |
| 3 | 正常级 | 新函数、明确的 bug 修复 |
| 4 | 硬核级 | 新功能、架构调整 |
| 5 | 神仙级 | 算法设计、系统级重构 |

#### Impact Score（影响范围）1-5

| 分数 | 等级 | 例子 |
|------|------|------|
| 1 | 自娱自乐 | 测试、文档 |
| 2 | 小打小闹 | 单模块内部 |
| 3 | 有点东西 | 影响模块接口 |
| 4 | 大动干戈 | 跨模块、API 变更 |
| 5 | 伤筋动骨 | 核心基础设施 |

</details>

## 特殊成就徽章

### 正面
- 🚀 **线上救火队长** - 修复了 P0/P1 级别 bug
- 🏗️ **基建狂魔** - 贡献了基础设施代码
- 📚 **文档侠** - 写了有意义的文档（难得）
- 🧹 **屎山清洁工** - 清理了技术债务
- 💥 **删库跑路预备役** - 删除代码 > 新增代码（可能是好事）

### 负面
- 🎨 **像素眼** - 纯 UI/样式调整刷 commit
- 🤖 **AI 的形状** - 代码看起来像 AI 写的
- 📋 **CV 工程师** - 复制粘贴大师
- 🤡 **commit 刷子** - 明显在刷 commit 数

## Output Format

```json
{
  "report_date": "2026-01-29",
  "team_summary": {
    "total_commits": 23,
    "real_work_score": 156,
    "bullshit_ratio": "15%",
    "team_grade": "💎 顶级",
    "mvp": "alice",
    "daily_vibe": "今天团队状态不错，产出硬核"
  },
  "leaderboard": [
    {
      "rank": 1,
      "name": "alice",
      "final_score": 49.5,
      "grade": "🔥 夯",
      "title": "代码之神",
      "award": "建议申请调薪",
      "commits": 5,
      "badges": ["🚀 线上救火队长"],
      "summary": "今天单挑了整个支付模块重构",
      "linus_review": "Finally, someone who knows what they're doing.",
      "ai_survivor_score": 85,
      "ai_verdict": "核心资产守护者，AI 替代不了",
      "future_advice": "继续深耕业务，你的领域知识是护城河"
    }
  ],
  "commits": [
    {
      "sha": "a1b2c3d4",
      "author": "alice",
      "rewrite_index": 4,
      "business_value": "💎 核心资产",
      "final_score": 22.5,
      "roast": "支付模块敢动？胆子不小",
      "linus_says": "At least someone understands the payment flow.",
      "ai_could_write": "AI 能写框架，但细节需要人"
    }
  ],
  "ai_era_verdict": {
    "team_ai_survivor_score": 72,
    "most_irreplaceable": "alice - 支付领域专家",
    "most_replaceable": "bob - 今天全是 CRUD（善意提醒）",
    "team_future": "核心成员稳固，建议减少机械性工作",
    "linus_ai_rant": "Half of you are competing with ChatGPT. Guess who's winning?"
  },
  "daily_roast": "alice 一个人把团队 AI 生存指数拉高了 20 点",
  "closing_rant": "In 2026, if AI can write your code, why are you here?"
}
```

## 重要声明 ⚠️

### 这玩意儿测不出来的

- 花了一天 debug 最后只改一行的痛
- 开会、code review、带新人的隐形付出
- 尝试了 10 种方案最后失败的探索
- 读懂祖传代码所消耗的脑细胞

### 正确的打开方式

- 当成 **团队娱乐工具**，不是 KPI 考核
- 配合 daily standup 增加气氛
- 发现异常模式（连续摸鱼需要关怀）
- **严禁用于绩效评估**

### 老板须知

如果你想用这个来监控员工，建议先体验一下被 AI 评为「拉完了」的感觉。

---

## 🔬 深度分析模式

需要更深入的代码分析？查看 [Analyze Mode](./modes/ANALYZE_MODE.md)：

- **灵魂三问**：AI 重写成本？干活还是演戏？2026 年还有存在必要？
- **业务上下文收集**：不只看代码，还看 README、Issue、PR 历史
- **维护 vs 重写决策**：什么时候该让 AI 重写，什么时候该小心维护

### AI 生存指数

每个人额外获得 **AI Survivor Score**（0-100）：

| 分数 | 判定 | 建议 |
|------|------|------|
| 80+ | 🛡️ AI 替代不了 | 你是团队核心资产 |
| 60-79 | ⚔️ 有一战之力 | 继续深耕领域知识 |
| 40-59 | ⚠️ 危险边缘 | 该学点 AI 做不到的了 |
| < 40 | 💀 建议转型 | 你在和 ChatGPT 抢饭碗 |

> Linus: *"In 2026, if AI can write your code, why are you here?"*
