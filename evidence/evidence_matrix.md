# 关键结论与佐证对应表

本表将“共同认同的业务判断”和“可从现有材料观察到的事实”分开。架构共识不等于已有实现，接口事实也不等于所有车型已经具备相同功能。

原文关键位置见 [带行号摘录](source_excerpts.md)，机器可读定位见 [evidence_locators.json](../metadata/evidence_locators.json)。

| 编号 | 结论或判断 | 材料及定位 | 证据强度与限制 |
| --- | --- | --- | --- |
| C01 | 开放受约束目标组合，复用系统产品执行，VCC 对承接 Mission 负责 | [讨论脉络第 5 节](../docs/research_notes.md)；[VCC 原文](../references/feishu/vcc_function_architecture_2026-11-12.md)，E01—E04 | 用户明确认同的业务方向；原规划也支持该责任划分，不代表全部契约已冻结 |
| C02 | 单系统实现继续归属产品，VCC 管整体协调 | VCC 规划 E02—E04；[报告第 4、10 节](../docs/research_report_2026-11-12.md) | 架构边界共识；原文部分时序与执行措辞仍待统一 |
| C03 | 座舱懂用户、智驾懂外界、车控懂车辆响应 | [讨论脉络第 8 节](../docs/research_notes.md)；[报告第 5 节](../docs/research_report_2026-11-12.md) | 本次讨论形成的推荐分工，不声称源代码已实现多 Agent 协议 |
| C04 | 精确控制与模糊目标应同时支持 | [报告第 6 节](../docs/research_report_2026-11-12.md)；WinMgr E06、AiCabinFuncMgr E07—E08 | 业务需求加代表性接口事实；具体外部输入契约尚未冻结 |
| C05 | 动态场景通过已知目标类型组合，不逐项新增场景编号 | [目标请求 JSON](../examples/mission_request.json)；[Proto 示意](../examples/mission_contract.example.proto) | 说明表达可行性的例子，不是运行实现或已批准平台 IDL |
| C06 | 预定义、参数化与动态场景可以并存 | [报告第 7 节](../docs/research_report_2026-11-12.md)；既有场景接口 E05、E08、E10 | 业务共识；现有场景接口只证明有可复用形式，不证明动态规划已实现 |
| C07 | 请求被接受／发送成功与目标完成分开 | [Demo README](soa_adaptor/README.md)，E13；WinMgr E06；[回执示意](../examples/mission_receipt.json) | 通信与接口事实支撑该语义要求；正式任务状态机和完成证据需继续定义 |
| C08 | buffer 读取成功不能当作源端产生新样本 | [Demo README](soa_adaptor/README.md)，E11；[底座 API](../references/soa_runtime/mcu_glue_code_api.md) | 当前 Demo 行为和底座语义；不能将读取计数当作底座上报次数 |
| C09 | E2E 状态有真实来源，应用按需处理 | [Demo README](soa_adaptor/README.md)，E12；[E2E 文档](../references/soa_runtime/mcu_e2e_communication_protection.md) | 已确认的桥接语义；不由此规定所有 Agent 业务必须使用相同质量门控 |
| C10 | 有场景名称不代表有可调用场景执行能力 | [SmartSceneMgr IDL](platform_idl/srv.vehctl.scnmgr.smartscenemgr.proto)，E09 | 可直接核对该快照的 EVENT 类型；仅限所归档版本 |
| C11 | 优先复用已有较高层次能力 | [AiCabinFuncMgr IDL](platform_idl/srv.thermal.hvac.aicabinfuncmgr.proto)，E07—E08 | 请求含场景、相对调温、区域、身体部位等字段；不证明所有模式已量产实现 |
| C12 | service_arch 支撑静态事实及来源追溯 | [平台规则](service_arch/platform_README.md)、[SourceEvidence](service_arch/backend/source_evidence.py)，E14—E15 | 选定代码和项目说明可验证；不能自动生成业务策略或实际完成判定 |
| C13 | Event＋FF 是样本中占比高的默认形态，但事务语义不能吞掉 | [既有接口场景调研](../references/soa_surveys/interface_scenario_survey.md)，E16 | 原样本统计支持默认路线，不是所有软件可无损转换率，也不是 Agent 能力成熟度统计 |
| C14 | 个人场景可通过伴生走向产品预定义场景 | [讨论脉络第 7 节](../docs/research_notes.md)；[报告第 12 节](../docs/research_report_2026-11-12.md) | 用户提出并认同的业务演进目标，非已有场景学习系统的运行证明 |
| C15 | 协议不替代业务契约，暂未决定采用 MCP 或 A2A | [协议来源](../references/protocols/protocol_references.md)；[报告第 14 节](../docs/research_report_2026-11-12.md) | 保留研究参考和讨论边界；本项目没有协议兼容性测试或完整规范离线镜像 |
| C16 | 行业材料提供组合方向，具体产品陈述不作为已验证事实 | [用户提供的文章](../references/industry/soa_agent_article_user_supplied.md)；[报告第 17 节](../docs/research_report_2026-11-12.md) | 用户正文为材料来源；产品实施情况未独立核实 |

## 使用这些证据时的注意事项

1. 源码与 IDL 快照的版本和指纹见 [来源清单](../metadata/source_manifest.json)。
2. 昨日发布结果可与 [飞书回读快照](feishu/research_report_readback_2026-11-12.md) 交叉核对。
3. 原 SOA 调研中的历史建议不能覆盖后来确认的读取策略；当前行为优先查阅 Demo README 与读取状态审查。
4. 当前没有实车完成 Mission 或多 Agent 编排的测试报告；主机桥接测试也不能被转述为车控 Agent 已实现。
