# AI 与 SOA 研究资料

研究记录：2026-11-12 起。最近归档日期：2026-11-16。

## 当前入口

- [最新讨论基线与定位澄清](docs/strategy/current_baseline_2026-11-16.md)：区分协调职责、独立 VCC、Agent 化与大模型；明确本矩阵立足 SOA，不接管独立软件架构矩阵。
- [两份 HTML 汇报材料](presentations/soa_matrix/index.html)：车控 Agent 20 页，服务架构矩阵 18 页，包含生成源、逐页讲述提示、来源及浏览器验证结果。

下方历史专题按当时讨论保存；涉及定位差异时，优先采用最新基线。

本项目保存车控 Agent 可行性研究，以及服务架构矩阵组织提升研究的参考材料、讨论内容、阶段性关键结论与佐证材料。当前属于业务、组织与架构研究，不是已经实现的车控 Agent 软件工程。

核心共识：**开放受约束的目标组合能力，复用系统产品的执行能力，让 VCC 对其承接的 Mission 形成完整责任。**

## 按专题阅读

| 日期 | 专题 | 入口 |
| --- | --- | --- |
| 2026-11-12 | 车控 Agent 目标、边界、接口与多 Agent 分工 | [关键结论](docs/key_conclusions.md)、[完整报告](docs/research_report_2026-11-12.md) |
| 2026-11-13 | 服务架构矩阵升级、虚拟 COE、角色与交互 | [专题目录](docs/organization/README.md)、[关键结论](docs/organization/06_decisions_and_open_questions.md)、[讨论交互记录](docs/organization/07_discussion_record_2026-11-13.md) |
| 2026-11-16 | 战略对齐、必要性决策、最终矩阵边界与汇报 | [最新基线](docs/strategy/current_baseline_2026-11-16.md)、[HTML 汇报](presentations/soa_matrix/index.html) |

## 车控 Agent 专题建议阅读顺序

1. [关键结论](docs/key_conclusions.md)：快速回顾目标、边界、接口与分工。
2. [完整调研报告](docs/research_report_2026-11-12.md)：2026-11-12 整理到飞书的完整文稿，包含 18 节正文、7 个场景例子及接口示例。
3. [讨论脉络与判断依据](docs/research_notes.md)：从服务复用到目标组合、任务闭环和多 Agent 分工的推导过程。
4. [结论—证据对应表](evidence/evidence_matrix.md)：区分业务共识、原始文档、接口事实和示意内容。
5. [参考资料目录与来源边界](references/source_catalog.md)：查看来源、快照日期和未完整取得的材料。
6. [待讨论问题](docs/open_questions.md)：后续需要明确的业务问题，不是开发实施计划。

## 目录

```text
ai_soa_research/
  README.md
  docs/                       完整报告、关键结论、研究脉络和开放问题
    organization/             COE 定位、能力方向、角色、工作流、案例和讨论记录
  references/
    feishu/                   VCC 规划正文快照
    organization/             原矩阵规划、组织正文与关键白板快照
    industry/                 用户提供的行业文章正文
    protocols/                MCP／A2A 参考链接及使用边界
    soa_surveys/              既有 SOA 调研 Markdown 与结构化 JSON
    soa_runtime/              底座 API、E2E、错误处理和原 POC 文档快照
  evidence/
    evidence_matrix.md        关键结论与材料位置的映射
    platform_idl/             5 个代表性服务的 Proto 与 options
    soa_adaptor/              读取语义、状态契约、代码和验证样例
    service_arch/             架构平台说明与事实追溯相关代码
    feishu/                   2026-11-12 发布文档的回读快照
  examples/                   结构化目标请求、任务回执和 Proto 示意
  metadata/                   来源清单、版本、指纹与归档验证结果
  tools/verify_archive.py      归档完整性验证
```

## 线上文档

- [阶段性研究结论文档](https://nio.feishu.cn/docx/TkkCd0PbuoGKmFxiJEGcYJhknBe)
- [VCC 功能架构规划（WIP）](https://nio.feishu.cn/wiki/Znw9wg6BQiRwwMkauRRcA5BInEf)

## 材料使用说明

- 不同日期的研究与来源分别保存，保留原文和快照日期；2026-11-13 组织专题为阶段性暂存，不是正式组织章程。
- 代码与 IDL 是本机在归档时取得的选定文件快照，仓库 HEAD、工作区状态及 SHA-256 记录在 [来源清单](metadata/source_manifest.json) 中。
- 飞书 Markdown 可能包含依赖权限的图片、白板和链接；这些资源没有全部离线下载，原文链接仍需相应权限。
- 行业文章来自用户粘贴正文，车型、接口数量和实际产品实现没有独立核实。
- MCP／A2A 保存研究涉及的参考链接与判断边界，未宣称已保存其完整规范正文，也未决定采用其中某种协议。
- 保留了原 SOA 调研的日期和历史语境。早期建议与后续已确认策略有差异时，以当前 Demo README 和读取状态审查说明为准。
- 资料中的原路径是来源定位，不表示整个原工程已复制进来。选定代码用于佐证，不能作为完整可编译 SDK 或实车验证包。
- JSON／Proto 示例仅为语义示意，不是已冻结接口。原 soa_adaptor、service_arch 项目保持只读；本研究归档以独立仓库管理。

## 验证

在本目录运行：

```bash
python3 tools/verify_archive.py
```

该命令检查归档文件指纹、原始快照一致性、示例 JSON、报告章节和项目内相对链接，不执行底层软件或实车功能测试。
