![把散乱资料，沉淀成自己的知识资产。](assets/hero.jpg)

# 把散乱资料，沉淀成自己的知识资产

Material to Deliverable｜资料整理与交付 Skill

把项目文档、会议记录、课程笔记和调研文件，整理成能复用的文稿与摘要。关键内容保留来源，下次写汇报、做复盘或重新判断时，不用再从头翻文件。

**[下载 Skill](https://github.com/Lucian1u/material-to-deliverable/archive/refs/heads/main.zip)** · [快速开始](#快速开始) · [使用示例](#使用示例)

`v0.1.0 beta`。兼容性与已验证范围见[下方说明](#兼容性)。

这是一个面向学生、职场人和内容工作者的开源 Agent Skill。它会先检查材料、确认任务，再生成带来源索引的汇报、方案、复盘、调研或课程展示。这里的“知识资产”指这些可复用、可核验的文字成果，不是自动建立或维护知识库。

## 为什么做这个项目

资料存了不少，真正要用的时候，还是得重新读一遍。直接交给 AI，又可能只得到一份长摘要：哪些是事实，哪些是意见，关键结论出自哪里，都不够清楚。

这个项目把整理过程和来源一起留下来。交付的不只是一篇文稿，还有摘要、来源索引和使用说明，方便之后核对、更新和继续使用。

## 核心能力

- 先澄清任务。一次只问一个会改变成品的问题，任务单确认后才继续。
- 保留证据边界。分开来源事实、反馈、用户判断和待确认信息；材料不足时停止。
- 留下审核记录。为关键事实建立来源索引，重新读取原始材料后再整理最终交付包。

## 快速开始

### 1. 安装 Skill

下载并解压完整仓库，把文件夹命名为 `material-to-deliverable`，放入兼容 Agent 配置的 Skills 目录。仓库根目录的 `SKILL.md` 是 Skill 入口。

项目级安装可使用标准目录：

```text
.agents/skills/material-to-deliverable/
```

不同客户端也可能使用自己的 Skills 目录，安装时以对应客户端当前文档为准。未列入下方验证记录的环境，需要自行确认加载是否成功。

### 2. 准备项目

直接在仓库根目录试用时运行：

```bash
python3 scripts/init_project.py /absolute/path/to/your-project
```

Agent 从 Skills 目录加载本项目时，会从 Skill 的安装目录调用同一脚本，用户项目中不需要另有 `scripts/`。

脚本会创建 `00_input/`、八个工作模板和空的 `02_delivery/`。如果生成文件已经存在，脚本会拒绝覆盖。

把真实材料放进：

```text
/absolute/path/to/your-project/00_input/
```

### 3. 让 Agent 执行

```text
请使用 material-to-deliverable，把 /absolute/path/to/your-project/00_input 中的真实资料整理成一份调研交付包。
```

Agent 会先检查敏感信息和任务缺口，再逐步建立工作文件。遇到敏感材料、证据不足或未确认的提纲时会暂停，等待你确认。

## 使用示例

### 项目汇报

```text
请使用 material-to-deliverable，根据当前项目 00_input 中的会议纪要、数据表和项目要求，制作一份给部门负责人的汇报。希望对方看完后决定下月是否继续试验。
```

预期结果：先得到任务单、材料索引和带来源提纲；确认以后生成主成品、摘要、来源索引与审核报告。

### 课程展示

```text
请使用 material-to-deliverable，根据 00_input 中的课程要求、讲义、我的笔记和老师反馈，制作一份课程展示。不要替我补写个人学习经历。
```

预期结果：课程事实、个人理解和待确认信息分开，最终展示中的关键内容可以回到材料核对。

## 工作原理

![从散乱资料到知识资产：先检查材料，再确认任务单与提纲，回读来源审核后整理交付包。](assets/workflow.jpg)

工作流要求保留 `00_input/` 原件不动。发现敏感信息时，只记录风险类别与文件位置，等待你确认。任务单和带来源提纲分别确认后，才继续写作；主成品完成后再回读原始材料审核。验证脚本只做结构与部分残留检查，不判断事实真伪，也不能代替人工检查内容是否完整。

## 交付内容

### 工作文件

| 内容 | 作用 |
|---|---|
| `01_working/01_task-brief.md` | 记录任务、接收者、限制和验收标准 |
| `01_working/02_material-index.md` | 记录每份材料的身份、用途和风险 |
| `01_working/03_gaps-and-conflicts.md` | 保留证据缺口与材料冲突 |
| `01_working/04_source-backed-outline.md` | 为提纲中的每个部分绑定来源 |
| `01_working/05_main-deliverable.md` | 保存主成品工作版本 |
| `01_working/06_one-page-summary.md` | 保存一页摘要 |
| `01_working/07_source-index.md` | 记录关键事实与原始位置 |
| `01_working/08_audit-report.md` | 记录审核问题和处理结果 |

### 最终交付

| 内容 | 作用 |
|---|---|
| `02_delivery/main-deliverable.md` | 通过审核的主成品 |
| `02_delivery/one-page-summary.md` | 给接收者快速阅读的摘要 |
| `02_delivery/source-index.md` | 最终版本的来源索引 |
| `02_delivery/readme.md` | 使用顺序与人工确认事项 |

## 边界与限制

这个项目不会：

- 生成虚构演示材料、客户经历、学生反馈或工作结果
- 用常识、联网搜索或模型记忆补齐缺少的事实
- 自动修改或脱敏 `00_input/` 中的原始文件
- 代替用户完成隐私授权、事实确认和最终放行

它适合已有真实材料的文字交付任务。单文件润色、开放式创意写作、图片生成和没有来源的代写不在第一版范围内。

当前仍是 beta。请使用普通的新建项目目录，不要把工作目录或输出文件链接到原始材料目录、其他目录。验证通过不等于内容完整、路径风险已全部排除或成品已获人工放行。

## 隐私与安全

- Skill 默认只处理用户指定的本地项目目录，不需要联网。
- 发现姓名、联系方式、客户资料、合同、财务、健康、教育记录、账号或凭证时，先暂停等待用户确认。
- 最终交付包禁止包含原始材料、聊天记录、提示词、内部草稿、敏感值和本机绝对路径。

请勿提交真实敏感材料作为 Issue 或测试夹具。安全问题的报告方式见 [`SECURITY.md`](SECURITY.md)。

## 兼容性

| 环境 | 状态 | 说明 |
|---|---|---|
| Agent Skills 标准格式 | 已实现 | 根目录包含标准 `SKILL.md` |
| Python 3.11 | 已验证 | 两个脚本仅使用标准库；12 项单元测试通过 |
| OpenAI Codex | 已验证 | 项目级发现、初始化和敏感信息暂停用例通过 |
| Claude Code | 已验证 | 普通全流程、材料不足停止和材料冲突停止用例通过 |

上述客户端验证记录日期为 2026-08-29，见 [`tests/forward-validation.md`](tests/forward-validation.md)。验证只覆盖记录中列出的路径，不代表所有版本和安装方式都已覆盖。

## 仓库结构

```text
material-to-deliverable/
├── SKILL.md
├── assets/
│   ├── hero.jpg
│   ├── workflow.jpg
│   ├── social-preview.jpg
│   └── project-templates/
├── references/
├── scripts/
├── tests/
├── .github/workflows/ci.yml
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## 开发与验收

运行单元测试：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

检查已完成的用户项目：

```bash
python3 scripts/validate_project.py /absolute/path/to/your-project --stage delivery
```

现有单元测试与夹具覆盖：

- 普通文件场景下，初始化拒绝覆盖已有工作文件或交付文件
- 验证器对占位符、额外文件、原始材料副本和部分本机路径的检查
- 普通、材料不足、材料冲突和敏感信息四类行为夹具已经建立

这些检查有覆盖范围，不等于对所有异常路径或内容完整性的保证。语义审核和最终放行仍需人参与。

## 项目状态

- 当前版本：`v0.1.0 beta`
- 已完成：Skill 入口、参考规则、八个模板、初始化脚本、验证脚本、测试夹具和 CI
- 已验收：Python 3.11 单元测试、Codex 敏感暂停用例、Claude Code 普通资料全流程、材料不足停止与材料冲突停止用例
- 尚未覆盖：Claude Code 的敏感资料前向用例；2026-08-29 的验证未执行这一项，原因见验证记录
- 版本记录：[`CHANGELOG.md`](CHANGELOG.md)

## 参与项目

提交问题或改动前，请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## License

MIT，见 [`LICENSE`](LICENSE)。
