# CSDN 文案

## 文章一：技术实现风

### 标题

我把考研择校流程做成了一个 Codex Skill：先查数据，再给建议

### 正文

最近做了一个开源项目：`kaoyan-navigator-skill`。

它不是一个 Web App，也不是一个简单 Prompt，而是一个给 AI Agent 使用的 Skill。用户输入目标学校、学院和专业后，Agent 会先搜索公开资料，再整理近三年的复试线、招生计划、推免、统考名额和拟录取数据，最后输出带来源和置信度的择校分析。

为什么要做成 Skill？

普通 Prompt 很容易越写越长，最后变成一份不可维护的“大作文”。Skill 的好处是可以分层：

- `SKILL.md` 只保留核心工作流；
- `references/` 放搜索手册、数据 schema、报告模板和指标说明；
- `scripts/` 放确定性脚本，比如 CSV/JSON 校验；
- `promotion/` 放推广文案，避免污染项目 README。

项目目前的核心流程是：

1. 规范化研究对象：学校、学院、专业代码、培养方式、入学年份；
2. 优先搜索官方来源：研究生院、招生网、学院官网、研招网；
3. 建立证据账本：数值、年份、口径、URL、来源等级；
4. 区分招生计划、推免人数和统考名额；
5. 从拟录取名单计算最低分、中位数和平均分；
6. 检查缩招、复试线虚低、专业课变化和网络热度；
7. 输出建议，但保留缺失数据和不确定性。

一个很重要的设计原则是：数据不足不能自动算安全。

比如某专业查不到拟录取名单，那么 Agent 不应该编一个“录取均分”，也不应该把“复试线虚低”这一项判为无问题，而是应该告诉用户：缺少拟录取分数，因此这一维度置信度不足。

仓库里还提供了示例 CSV 和校验脚本：

```bash
python3 scripts/validate_data.py examples/sample.csv
```

后续可以继续扩展 PDF 拟录取名单解析、OCR、Excel 数据导入、院校案例 benchmark 和专业代码变更识别。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

推荐标签：`AI Agent`、`Codex`、`Claude Code`、`数据分析`、`开源`、`教育数据`、`Python`。

## 文章二：数据工程风

### 标题

考研择校数据为什么难处理？从复试线、推免到拟录取名单

### 正文

很多人以为考研择校数据就是“复试线 + 招生人数 + 报录比”。

实际处理起来会发现，这些数字最难的不是找，而是确认它们是不是同一个口径。

常见问题包括：

- 同一个专业名可能分属不同学院；
- 专业代码变化后，历年数据不能直接拼接；
- 招生计划可能包含推免、专项、非全；
- 拟录取名单里可能混有调剂、专项和非全；
- 复试线和实际录取分数不是一回事；
- 报录比可能是学院口径，不是专业口径。

`kaoyan-navigator-skill` 试图把这件事拆成 Agent 能执行的工作流。

第一步是建立研究对象：

```text
学校 / 学院 / 专业代码 / 专业名称 / 方向 / 培养方式 / 入学年份
```

只要对象没定义清楚，后面的数据都会混。

第二步是来源分级。官方招生目录、研究生院公告、学院复试细则和拟录取公示优先级最高；第三方机构和社交平台只能作为线索，不能直接作为核心事实。

第三步是结构化数据。项目提供了推荐字段：

```text
year, school, college, major_code, major_name, study_mode,
national_line, retest_line, planned_total, recommended_exempt,
unified_quota, admitted_min, admitted_median, admitted_mean,
source_url, source_grade
```

第四步才是判断。招生计划下降、推免比例上升、复试线和录取中位数差距过大、改考 408 等，都只是信号，不是绝对结论。

我希望这个项目后续能沉淀成一个教育数据清洗和 Agent 调研的开源样例：既能服务考研学生，也能给开发者展示如何把非结构化公开数据变成可审计报告。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

推荐标签：`数据治理`、`数据清洗`、`AI Agent`、`PDF解析`、`教育数据`、`开源工具`。

## 文章三：开源项目介绍风

### 标题

开源项目 kaoyan-navigator-skill：给 AI Agent 的考研择校导航能力

### 正文

项目名：`kaoyan-navigator-skill`

一句话介绍：

```text
让 AI 先查证据，再帮你做考研择校导航。
```

它适合这些场景：

- 想分析目标院校近三年复试线和录取情况；
- 想核对招生计划是否包含推免；
- 想判断拟录取分数和复试线差距；
- 想把自己的 CSV/JSON 数据交给 Agent 分析；
- 想让 Codex 或 Claude Code 复用一套固定择校流程。

仓库结构：

```text
SKILL.md
references/
scripts/
examples/
agents/
promotion/
```

其中 `SKILL.md` 是 Agent 的入口，`references/` 存放详细规则，`scripts/` 提供确定性校验工具。

项目不承诺预测结果，也不输出“稳上”这种结论。它更像一个研究助理：先找数据，再整理来源，再说明哪些地方可靠，哪些地方缺证据。

这是我觉得 AI Agent 在严肃决策场景里应该具备的基本素养：不是急着回答，而是先把证据边界讲清楚。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

如果你觉得有用，欢迎 Star、提 Issue，或者贡献院校数据口径和解析脚本。

推荐标签：`开源项目`、`AI Agent`、`Codex Skill`、`Claude Code`、`考研`、`Python`。

