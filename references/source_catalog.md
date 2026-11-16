# 参考资料来源与可用范围

研究日期：2026-11-12；本地归档：2026-11-13。

本目录原主体对应 2026-11-12 车控 Agent 研究；2026-11-13 新增的组织专题资料见下方第 10 节。

## 1. 昨日研究产物

- [完整报告原稿](../docs/research_report_2026-11-12.md)：昨天发布到飞书时使用的 Markdown。
- [飞书回读正文](../evidence/feishu/research_report_readback_2026-11-12.md)：发布后回读，可能包含飞书转换后的表格和格式标记。
- [线上文档](https://nio.feishu.cn/docx/TkkCd0PbuoGKmFxiJEGcYJhknBe)。

这两份本地文件都是昨天的实际留存，不是今日重新改写。

## 2. VCC 原始规划

- [正文快照](feishu/vcc_function_architecture_2026-11-12.md)。
- [原文链接](https://nio.feishu.cn/wiki/Znw9wg6BQiRwwMkauRRcA5BInEf)。
- 标题：Vehicle Cabin Control (VCC) function architecture_0.0.1(WIP)。
- 范围：已取得正文与表格。图片、白板、附件及所有被引用文档没有全部离线保存或审阅。
- 原文中“个人理解简述”等内容作为讨论参考，不认定为全部正式冻结结论。

昨日未取得正文的关联资料：

- VCC｜以 NCM 为技术底座的车端 Cabin Brain V1：`https://nio.feishu.cn/wiki/Vk5lwrCrsiDjIykcSXjc8SQ5nwc`。
- 如何避免 VCC 成为中央脚本：`https://nio.feishu.cn/docx/T6pkdUPljozdLHxBD6mccW4zndh`。

这两份仅保留来源线索；不放入空文件冒充已经取得的资料。

## 3. 行业文章

- [用户提供正文](industry/soa_agent_article_user_supplied.md)。
- 原始链接：`https://mp.weixin.qq.com/s/OHO7nkG4QOU-508hnsuEag`。
- 取材方式：用户在对话中粘贴全文。原链接访问出现环境验证，昨日抓取到的页面不是文章正文，故未当作有效文章归档。
- 产品相关陈述为原材料观点，未独立核实。

## 4. SOA 历史调研

下列 Markdown 和同名 JSON 已保存于本项目，保留原统计与证据边界：

- [AmbLiMgr Client 清单](soa_surveys/amblimgr_client_inventory.md)。
- [服务与字段使用覆盖](soa_surveys/amblimgr_client_coverage.md)。
- [请求字段实际使用](soa_surveys/request_field_usage_survey.md)。
- [接口场景与 Event＋FF 归一评估](soa_surveys/interface_scenario_survey.md)。

来源为 soa_adaptor 项目既有调研。它们是当前研究的背景资料，不能将样本统计解释为所有软件或所有车型的普遍结论。

历史报告中保留的绝对路径是当时证据定位；并非所有被引用的完整源工程均复制进本目录。

## 5. 平台 IDL 快照

[平台 IDL 目录](../evidence/platform_idl/) 保存以下 5 个服务的 `.proto` 与 `.options`：

- AmbLiMgr：参数请求、场景请求、状态与可写 Field。
- WinMgr：目标位置 FF、部分 RR 与状态。
- AiCabinFuncMgr：热场景、座椅空间模式及相应状态。
- SmartSceneMgr：场景信息事件，体现“有场景名称”不等于“可执行场景”。
- AmbLiSceneMgr：既有场景更新、控制和状态。

这些用于接口事实佐证，未打包完整平台依赖，不宣称可独立编译。

## 6. 底座与桥接状态材料

- [底座 Glue Code API](soa_runtime/mcu_glue_code_api.md)。
- [E2E 通信保护](soa_runtime/mcu_e2e_communication_protection.md)。
- [SOA 错误处理](soa_runtime/soa_error_handlings.md)。
- [原 POC 方案](soa_runtime/soa_poc_source.md)：历史设想，不能替代当前实现说明。
- [当前桥接 Demo README 快照](../evidence/soa_adaptor/README.md)。
- [读取状态审查快照](../evidence/soa_adaptor/docs/Client_Read_State_Review.md)。

这部分支撑“请求发送与目标完成不同”“buffer 读取不等于新帧”“状态质量必须有真实来源”等判断。原项目中的主机测试结果不等于实车结果，本次归档没有重跑软件测试。

## 7. service_arch 材料

- [项目说明](../evidence/service_arch/README.md)。
- [平台规则](../evidence/service_arch/platform_README.md)。
- [SourceEvidence 实现](../evidence/service_arch/backend/source_evidence.py)。
- 同目录的服务实例、字段约束、Proto 与部署解析代码快照。

这些证明架构平台能保存和追溯静态服务事实，不证明车控目标和执行结果能自动从 IDL 推导出来。

## 8. 协议参考

见 [MCP／A2A 来源索引](protocols/protocol_references.md)。本次归档保存链接和研究用途，不把未下载的规范称作离线全文。

## 9. 版本和指纹

每份复制材料的来源路径、源仓库 HEAD、选定文件工作区状态与 SHA-256 见 [source_manifest.json](../metadata/source_manifest.json)。

源文件快照、讨论共识与接口示例有不同证据强度。对照使用时请同时查看 [证据对应表](../evidence/evidence_matrix.md)。

## 10. 2026-11-13 矩阵组织提升专题

- [来源说明](organization/README.md)：两份原组织与技术规划，以及三张关键白板节点快照和文字索引。
- [分层讨论入口](../docs/organization/README.md)：COE 定位、能力方向、角色职责、工作流和案例。
- [讨论交互记录](../docs/organization/07_discussion_record_2026-11-13.md)：保留用户明确输入、两次关键澄清和方案收敛。

旧规划作为现有基础的参考；用户已明确多数条目完成可关闭，且矩阵为虚拟 COE、没有强交付属性。不能用旧计划代替当前状态或将研究建议视为正式组织授权。
