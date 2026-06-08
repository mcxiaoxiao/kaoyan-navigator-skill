# 考研择校预测 Skill：历年数据调研、爆热风险与冲稳保分析

一个面向 **Codex、Claude Code 和通用 AI Agent** 的中国考研择校研究 Skill。输入目标学校、学院和专业后，Agent 会先从学校官网、研究生院、研招网和公开名单中寻找历年数据；只有关键数据确实找不到时，才向用户索取 CSV、Excel、JSON、PDF、截图或链接。

> 不做“算命式预测”。本项目输出的是可审计的风险信号、证据质量和置信度。

## 适合解决什么问题

- 某学校某专业今年考研会不会“爆”？
- 近三年复试线、招生计划、统考名额、推免比例怎么变？
- 复试线很低，实际录取分数是不是很高？
- 改考 408、专业拆分、学院调整会带来什么风险？
- 我的目标分数适合冲、稳还是保？
- 我有自己的历年数据，如何让 Agent 自动校验并分析？

## 核心升级

本项目借鉴了 [kaoyan-burst-predictor](https://github.com/Uoldady/kaoyan-burst-predictor) 的六指标思路，并参考预测型多 Agent 系统的研究流程进行扩展：

- 多角色研究：政策、供给、分数、竞争、热度和独立审计。
- 证据优先级：官方原文优先，社交媒体只作为弱信号。
- 先检索再追问：尽量自行找到资料，只请求最小必要补充。
- 反方审查：每个高风险结论必须主动寻找缓释证据。
- 留出验证：有四年以上数据时，避免拿最新结果反向调阈值。
- 风险与置信度分离：数据不足不会被误判为安全。
- 用户数据导入：支持 CSV/JSON 校验，可继续处理 Excel、PDF 和截图。

## 仓库结构

```text
kaoyan-risk-skill/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── data-schema.md
│   ├── report-template.md
│   ├── research-playbook.md
│   └── risk-model.md
├── scripts/validate_data.py
└── examples/sample.csv
```

## 安装

### Codex

将仓库目录复制到 Codex skills 目录：

```bash
git clone https://github.com/YOUR_NAME/kaoyan-risk-skill.git
cp -R kaoyan-risk-skill ~/.codex/skills/kaoyan-risk
```

然后在对话中使用：

```text
使用 $kaoyan-risk，分析 2027 考研某大学计算机学院 085404 计算机技术。
```

### Claude Code

Claude Code 可以直接读取 `SKILL.md` 的流程，也可以将核心指令改造成项目 command。不同版本的技能目录可能不同，请以当前官方文档为准。

### 其他 Agent

让 Agent 加载 `SKILL.md`，并授予网页搜索、文件读取和代码执行能力。Skill 不绑定某个专有工具名。

## 导入自己的历年数据

参考 [examples/sample.csv](examples/sample.csv)，然后运行：

```bash
python3 scripts/validate_data.py examples/sample.csv
```

空值请留空，不要用 `0` 代替未知。详细字段见 [references/data-schema.md](references/data-schema.md)。

## 示例提示词

```text
使用 $kaoyan-risk 分析 2027 年入学的 XX 大学 XX 学院 085404。
先联网找 2024-2026 年官方数据。如果拟录取分数找不到，再明确告诉我需要上传什么。
我本科双非，目标 350 分，接受调剂但不接受非全，请给冲稳保建议。
```

```text
使用 $kaoyan-risk 分析我上传的 CSV。先检查不同学院、专业代码和培养方式是否混用，
再给出缩招、推免挤压、复试线虚低和科目变化风险。
```

## SEO 关键词

考研择校、考研院校分析、考研报录比、考研复试线、考研招生人数、统考名额、推免比例、考研爆冷、考研爆热、408 考研、考研 AI Agent、Codex Skill、Claude Code Skill。

## 参考项目

- [Uoldady/kaoyan-burst-predictor](https://github.com/Uoldady/kaoyan-burst-predictor)
- [datawhalechina/hello-agents：如何写出好的 Skill.md](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-%E5%A6%82%E4%BD%95%E5%86%99%E5%87%BA%E5%A5%BD%E7%9A%84Skill.md)
- [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- [AI4Finance-Foundation/FinRobot](https://github.com/AI4Finance-Foundation/FinRobot)
- [AI4Finance-Foundation/FinGPT](https://github.com/AI4Finance-Foundation/FinGPT)

## 免责声明

本项目仅用于信息整理和择校辅助。招生政策、名额和分数线可能变化，最终请以教育部、研招网和目标院校官方公告为准。

## License

MIT

