# Client读取状态与E2E转发审查记录

日期：2026-11-04。范围：AmbLiMgr Client接收侧，保持原FF发送及平台Server路径。

已按用户逐项确认实施：周期buffer读取、读取失败保留历史成功值并提供独立失败信号、E2E只从独立SM读取原样转发、仅Motion暴露状态字段、取消本地超时和接收质量门控、单接口失败不阻断10ms链路。

## 回归与修复证据

新增`client_read_policy`先在旧实现上运行，`deliveries==1`断言失败，证明旧的E2E门控会拒绝SDK成功读取的payload；随后修改实现，测试通过。该测试同时检查连接异常不覆盖成功读取结果、失败输出参数不得污染历史值、业务读取失败不向应用发原因错误事件。

Mock从消费式单槽改成覆盖式非消费buffer，移除应用“读到空”清理。原FF队列及诊断事件队列保持既有测试假设。Snapshot自身为buffer，通过epoch和sequence识别握手，不能把旧快照当成本周期成功交付。

独立审查发现1项Important：adaptor单独重建后，底座业务buffer可能保留旧值；Snapshot.have_value=false，但模型仍可能合并旧buffer。已在九条实际SM业务读取后增加当前Snapshot消费门禁；Motion分别按have_value和e2e_read_success合并optional字段。`test_model.c`使用真实模型验证重建、源读取失败、SM旧buffer仍存在时不重新合并旧数据。

清理了旧通用E2E枚举和应用状态结构中的原始质量字段。应用通过Motion业务消息获取原始状态；Snapshot仅提供独立读取结果。源LOCAL状态getter不接通却返回SUCCESS的问题，通过显式`motion_e2e_report_supported`能力绑定避免默认伪造OK。

复审结论：上述Important闭环，未发现新增Critical或Important。审查者只读源码与测试，不修改文件。

## 验证范围

- C99核心及传输适配使用`-Wall -Wextra -Werror -Wpedantic`。
- 原31条映射及FF顺序、满队列、断连隔离、生命周期继续回归。
- 实际AmbLiMgr及helper参与100个正常周期和额外故障/恢复周期验证。
- nanopb验证optional的0/false、纯状态消息、Snapshot独立读取信号。
- 状态码0..6及未来码保留；业务与状态读取失败相互独立；无本地超时。
- E2E关闭配置独立生成无状态字段IDL，并编译全部接收实现及实际应用。
- Reference的102个输入保持原指纹；原九份VMBC业务IDL中只允许获批Motion变更，其他八份保持。

正式SDK生成接口及状态结构布局未集成编译，源平台E2E通路能力、首次写入有效性检查、源session隔离、真实调度及ECU通信仍需集成验证。当前Demo仅有buffer订阅，不宣称实现通用history queue批次桥接。
