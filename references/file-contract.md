# 文件合同

Skill 只管理 `01_working/` 与 `02_delivery/`。`00_input/` 属于用户，只读，不修改。

## 项目结构

```text
project/
├── 00_input/
├── 01_working/
│   ├── 01_task-brief.md
│   ├── 02_material-index.md
│   ├── 03_gaps-and-conflicts.md
│   ├── 04_source-backed-outline.md
│   ├── 05_main-deliverable.md
│   ├── 06_one-page-summary.md
│   ├── 07_source-index.md
│   └── 08_audit-report.md
└── 02_delivery/
    ├── main-deliverable.md
    ├── one-page-summary.md
    ├── source-index.md
    └── readme.md
```

## 八个工作文件

### `01_task-brief.md`

记录任务目标、接收者、使用场景、希望促成的决定、交付类型、截止时间、已有材料、限制、AI 可以协助的部分、必须由用户决定的部分、验收标准和待确认事项。

### `02_material-index.md`

每份输入文件一行。必须记录文件名、材料类型、主要内容、材料身份、可支持部分、来源位置、敏感风险、能否使用和处理方式。

敏感信息只记风险类别，不复制具体值。

### `03_gaps-and-conflicts.md`

分开记录材料冲突、证据缺口、无法读取的文件、敏感风险、需要补充的材料和阻断状态。

### `04_source-backed-outline.md`

每个部分记录要回答的问题、接收者为什么需要、具体来源、允许写到什么程度、用户判断、待确认项和验收方式。

### `05_main-deliverable.md`

主成品的工作版本。内容结构由交付类型决定。工作版本可以保留内部来源标记，交付版本需要清理内部备注。

### `06_one-page-summary.md`

让接收者在一页内理解任务、关键事实、当前结论、风险、建议动作和待确认事项。不得出现主成品没有的新结论。

### `07_source-index.md`

每个关键事实一行，记录唯一编号、成品位置、事实或判断、来源文件、来源位置、材料身份、核实状态和人工复查状态。

### `08_audit-report.md`

记录审核范围、问题数量、具体位置、问题类型、来源依据、处理方式、已修改数量、仍需补材料数量和人工确认事项。

## 最终交付包

最终文件来自通过审核的工作文件：

| 最终文件 | 来源 |
|---|---|
| `main-deliverable.md` | `05_main-deliverable.md` |
| `one-page-summary.md` | `06_one-page-summary.md` |
| `source-index.md` | `07_source-index.md` |
| `readme.md` | 根据任务单与审核报告生成 |

最终包不得包含：

- `00_input/` 中的原始材料
- 提示词与聊天记录
- 未通过审核的草稿
- 内部修改记录
- 敏感值与本机绝对路径
- 未处理的 `{{...}}` 占位符

## 完成状态

工作文件可以使用以下状态：

- `draft`
- `waiting_for_user`
- `blocked`
- `reviewed`
- `ready`

只有审核完成、阻断问题为零且验证脚本通过时，最终交付状态才能写为 `ready`。
