# 结构化目标组合示例

这些内容从 2026-11-12 完整研究报告提取，用于解释动态组合的表达方式，不是冻结接口或可部署功能。

- [mission_request.json](mission_request.json)：二排右侧稍暖、灯光稍暗、不改变前排、尽量省电。
- [mission_receipt.json](mission_receipt.json)：接受任务的示例回执；不表示任务完成。
- [mission_contract.example.proto](mission_contract.example.proto)：最小目标组合和提交接口示意，未包含完整平台依赖、能力发现及结果生命周期。

关键含义：预先定义目标类型和约束语义；提交时组合这些目标，不必为每种场景建立专用接口。新增能力语义仍需要正式扩展，不能由任意 JSON 自动获得。
