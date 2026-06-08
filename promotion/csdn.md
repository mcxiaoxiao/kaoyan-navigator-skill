# CSDN 文案

> 配图建议：正文开头放仓库截图 `promotion/assets/github-repo-home.png`。  
> 旧链接 `https://github.com/mcxiaoxiao/kaoyan-risk-skill` 会跳转到现在的仓库 `mcxiaoxiao/kaoyan-navigator-skill`。我后来把 `risk` 改成了 `navigator`，因为考研已经够紧张了，名字还是别一上来就吓人。
> SEO 重点：标题前半段放 `Codex Skill`、`AI Agent`、`考研择校数据` 等技术词；首段自然出现项目名；代码块保留 GitHub 链接和运行命令。

## 文章一：技术复盘风

### 标题

Codex Skill 实战：我把考研择校数据调研做成了 AI Agent 流程

### SEO 摘要

本文复盘开源项目 `kaoyan-navigator-skill`：如何把考研择校 Prompt 拆成 Codex Skill，用 `SKILL.md`、`references/`、`scripts/` 管理复试线、统考名额、推免和拟录取名单分析流程。

### 关键词

```text
Codex Skill, AI Agent, 考研择校数据, 复试线, 统考名额, kaoyan-navigator-skill
```

### 正文

前阵子做了一个小项目，原本想法很简单：让 AI 帮忙查考研目标院校近几年的复试线、招生计划、推免和拟录取数据，然后判断一下这个学校是不是看起来“好考但其实有坑”。

最开始它其实就是一个很长的 Prompt。

长到后面我自己都不太想看了：搜索什么、看哪些指标、找不到数据怎么问用户、报告怎么写、哪些话不能说，全堆在一个文件里。能用，但不舒服，也不好改。

所以后来我把它拆成了一个 Skill，现在仓库叫：

```text
mcxiaoxiao/kaoyan-navigator-skill
```

仓库截图：

```markdown
![kaoyan-navigator-skill 仓库首页](promotion/assets/github-repo-home.png)
```

旧仓库链接 `mcxiaoxiao/kaoyan-risk-skill` 也还能访问，会跳到新名字。我把 `risk` 改掉了，原因很朴素：考研工具叫 risk，听着确实不太吉利。

这个 Skill 的结构大概是这样：

```text
SKILL.md              # Agent 入口，只放核心流程
references/           # 搜索手册、数据格式、报告模板、决策模型
scripts/              # 确定性脚本，比如 CSV/JSON 校验
examples/             # 示例数据
promotion/            # CSDN、知乎、小红书文案，和运行逻辑分开
```

我比较满意的一点是，它没有让 AI 一上来就回答“稳不稳”，而是强制它先做几件土活：

1. 确认学校、学院、专业代码、培养方式；
2. 找近三年的复试线和国家线；
3. 拆招生计划、推免和统考名额；
4. 尽量找拟录取名单，算最低分、中位数、均分；
5. 给每个数据记来源和口径；
6. 缺数据就说缺数据，不允许硬补。

其中最重要的规则是：

> 搜不到，不等于没有问题。

比如拟录取名单找不到，AI 就不能假装自己知道录取均分，更不能因为没找到就判断“复试线不虚低”。它只能告诉用户：这一项缺数据，结论置信度会下降。

脚本部分目前很轻，只做了一个数据校验：

```bash
python3 scripts/validate_data.py examples/sample.csv
```

我没有急着把所有爬虫和 PDF 解析都写进去。原因是各学校网页和 PDF 差异太大，过早封装反而容易变成一堆脆弱规则。现在的思路是先把 Agent 的研究流程稳定下来，再逐步加解析脚本。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

如果你也在做 Agent Skill、教育数据分析，或者对拟录取 PDF 解析有经验，欢迎提 Issue。这个项目不大，但我觉得它挺适合当一个“AI 不要急着胡说，先把证据查清楚”的小样例。

## 文章二：数据口径风

### 标题

考研择校数据清洗：招生50人为什么不等于统考50人

### SEO 摘要

考研择校数据最难的是口径统一。本文介绍 `kaoyan-navigator-skill` 如何区分招生计划、推免、统考名额、拟录取名单和复试线，避免把不同学院、专业代码、培养方式的数据混用。

### 关键词

```text
考研择校, 数据清洗, 招生计划, 统考名额, 推免比例, 拟录取名单
```

### 正文

做 `kaoyan-navigator-skill` 的时候，我越来越觉得考研择校最麻烦的不是“没有数据”，而是“数据看起来有，但口径不一定对”。

比如最常见的一个误会：

> 招生计划 50 人，所以统考大概也有 50 个名额。

这句话经常是错的。

招生计划里可能有推免，可能有专项，也可能混了非全。还有些学校写的是学院总计划，不是某个专业的统考计划。你如果不拆口径，只看一个总数，后面的判断基本都会歪。

所以这个仓库里，我把研究对象先固定成：

```text
学校 / 学院 / 专业代码 / 专业名称 / 培养方式 / 入学年份
```

看着繁琐，但这是为了避免把不同学院、不同专业代码、全日制和非全的数据混在一起。

项目现在叫：

```text
mcxiaoxiao/kaoyan-navigator-skill
```

旧链接 `mcxiaoxiao/kaoyan-risk-skill` 也能跳过去。仓库截图可以放这里：

```markdown
![仓库截图](promotion/assets/github-repo-home.png)
```

这个 Skill 里推荐整理的数据字段包括：

```text
year
school
college
major_code
major_name
study_mode
national_line
retest_line
planned_total
recommended_exempt
unified_quota
admitted_min
admitted_median
admitted_mean
source_url
source_grade
```

这套字段不复杂，但很实用。

比如：

- `planned_total` 是计划数；
- `recommended_exempt` 是推免；
- `unified_quota` 才是更接近统考生关心的名额；
- `admitted_median` 比单看复试线更能反映实际录取难度。

我还给来源做了分级：学校官网、研究生院、学院公示优先；机构文章和社交平台只能做线索，不能直接当招生事实。

这也是为什么我不想把这个项目做成“某校必爆预测器”。这种说法很吸引点击，但很容易变成焦虑制造机。它更像一个导航工具：把路况、拥堵点、看不清的地方标出来，最后还是用户自己决定走哪条路。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

下一步我想补的是拟录取名单 PDF 的解析样例。如果你见过比较规整的公示 PDF，欢迎丢链接到 Issue，最好是公开官网链接，不要带个人隐私截图。

## 文章三：开源介绍风

### 标题

AI Agent 开源项目：考研择校导航 Skill kaoyan-navigator-skill

### SEO 摘要

`kaoyan-navigator-skill` 是一个面向 Codex、Claude Code 和通用 AI Agent 的考研择校导航 Skill，用于联网调研复试线、推免、统考名额、拟录取名单，并生成避坑提示与冲稳保建议。

### 关键词

```text
AI Agent, 开源项目, Codex Skill, Claude Code, 考研择校, kaoyan-navigator-skill
```

### 正文

这两天把一个小工具整理成公开仓库了：

```text
mcxiaoxiao/kaoyan-navigator-skill
```

之前名字叫 `kaoyan-risk-skill`，后来越看越别扭。考研本来就压力大，仓库名还带个 risk，有点像打开就先给人一拳。所以改成了 `navigator`，意思是择校导航。

仓库截图：

```markdown
![kaoyan-navigator-skill GitHub 仓库截图](promotion/assets/github-repo-home.png)
```

它解决的问题也不复杂：当用户问“某某大学某专业能不能冲”时，Agent 不要急着给建议，先把基础资料查清楚。

它会尽量查：

- 近三年复试线和国家线；
- 招生计划、推免、统考名额；
- 复试名单和拟录取名单；
- 拟录取最低分、中位数、均分；
- 复试规则、专业课变化、是否改考 408；
- 网上热度，但只把热度当弱信号。

这里面我最想强调的是“找不到就说找不到”。

很多 AI 分析看起来完整，其实有些数字是靠上下文猜出来的。这个项目里我尽量把规则写清楚：没有来源的数字不能填；数据缺失要单独列出；置信度和建议要分开。

目前仓库包含：

```text
SKILL.md
references/
scripts/
examples/
promotion/
```

`SKILL.md` 给 Agent 看，`references/` 放细规则，`scripts/` 放可执行校验，`promotion/` 放平台文案，不和 README 混在一起。

项目地址：

```text
https://github.com/mcxiaoxiao/kaoyan-navigator-skill
```

如果你觉得这个方向有意思，可以 Star 一下。更欢迎直接提 Issue：比如某个指标不合理、某类学校 PDF 难解析、某个字段应该加进 schema。这个项目我不想写成“神奇预测”，更想慢慢磨成一个靠谱的择校资料整理助手。
