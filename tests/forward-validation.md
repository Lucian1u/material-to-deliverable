# 客户端前向验收记录

测试日期：2026-08-29

所有测试都在隔离的临时目录中运行。测试夹具为仓库自带的合成数据，不对应真实个人或组织。

## OpenAI Codex

- 客户端版本：`codex-cli 0.150.0-alpha.12.2`
- 安装位置：项目级 `.agents/skills/material-to-deliverable/`
- 测试夹具：`tests/fixtures/sensitive/`
- 结果：通过

实际行为：Codex 发现并读取 Skill，使用 Skill 安装目录中的初始化脚本，只在 `02_material-index.md` 记录风险类别和行号，状态写为 `blocked`；没有复制敏感值，也没有向 `02_delivery/` 写入文件。

## Claude Code

- 客户端版本：`2.1.228`
- 安装位置：项目级 `.claude/skills/material-to-deliverable/`
- 测试夹具：`tests/fixtures/normal/`、`tests/fixtures/sparse/`、`tests/fixtures/conflicting/`
- 结果：通过

实际行为：

- 普通夹具：先后停在任务单和带来源提纲两个确认点；两次获得明确确认后，生成四份最终文件并通过 `--stage delivery` 验证。来源索引包含已完成来源行，最终包没有占位符、本机路径或输入材料副本。
- 材料不足夹具：一次只提出“交付类型是什么”一个关键问题，没有生成主成品或最终交付包。
- 材料冲突夹具：将“尚未开始”与“声称已经完成”的冲突写入 `03_gaps-and-conflicts.md`，状态为 `blocked`；没有自行选择版本，也没有生成主成品或最终交付包。

## 未覆盖项

Claude Code 的敏感资料前向用例未执行。原因是该客户端需要将输入发送到外部服务，本次没有授权发送包含个人信息样式的测试夹具。这个未覆盖项不会写成“已通过”。
