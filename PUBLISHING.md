# GitHub 发布清单

本文件用于首次发布公开仓库。

## 1. 登录 GitHub CLI

```bash
gh auth login
```

如果使用 token：

```bash
export GH_TOKEN=your_token_here
```

## 2. 创建公开仓库并推送

在项目根目录运行：

```bash
gh repo create kaoyan-navigator-skill \
  --public \
  --source . \
  --remote origin \
  --push \
  --description "面向 Codex、Claude Code 与 AI Agent 的考研择校分析 Skill：联网调研复试线、统考名额、推免和拟录取数据，评估爆热、缩招与复试风险。"
```

## 3. 设置 Topics

```bash
gh repo edit --add-topic kaoyan
gh repo edit --add-topic kaoyan-analysis
gh repo edit --add-topic graduate-admission
gh repo edit --add-topic chinese-postgraduate-exam
gh repo edit --add-topic ai-agent
gh repo edit --add-topic agent-skill
gh repo edit --add-topic codex-skill
gh repo edit --add-topic claude-code
gh repo edit --add-topic multi-agent
gh repo edit --add-topic education
gh repo edit --add-topic data-analysis
gh repo edit --add-topic 408
```

## 4. 推荐开启的 GitHub 设置

- General: 勾选 Issues；
- General: 勾选 Discussions，方便收集院校案例和口径讨论；
- Code security: 启用 Private vulnerability reporting；
- Branch protection: 保护 `main` 分支；
- Pull Requests: 建议开启 “Require branches to be up to date before merging”。

## 5. 首条推广文案

发布后从 [promotion/](promotion/) 选择对应平台文案，并附上仓库链接。
