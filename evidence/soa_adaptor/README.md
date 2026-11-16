# AmbLiMgr Client SM 桥接 Demo

当前实现覆盖12个Client端点、9条订阅和22条FF发送。对内全部使用底座形式的VMBC `sm_*` API，AmbLiMgr Server及5条保留接收仍沿用平台接口。Reference只读。本次2026-11-04修改落实已确认的读取状态与E2E转发语义；历史审查记录不作为当前策略说明。

本阶段是手工桥接POC，使用官方nanopb与主机SM Mock验证。正式SDK生成、链接、ECU部署和通信尚未验证。

## 接收行为

当前九个订阅全部按无history queue的buffer模式，每个10ms周期各读取一次。SUCCESS只表示取得当前buffer值，不表示源端收到新帧；同值不去重，读取不消费buffer。

| 业务读取结果 | 业务值 | 独立读取信号 |
| --- | --- | --- |
| SUCCESS | 更新并转发本次值 | read_success=true，read_error=false |
| 失败，已有历史值 | 转发最后一次成功读取值 | read_success=false，read_error=true |
| 失败，无历史值 | 不制造默认值、不提供业务字段 | read_success=false，read_error=true |

这里的历史成功值不要求E2E通过。adaptor不对成功读出的payload再做连接/E2E/超时门控，不加入业务debounce、安全值或关灯策略。业务读取失败原因不传给应用。ERR_NO_MSG=7表示本次没有可读取值，也不能使用输出参数。

`have_value`表示存在历史成功读取值；`data_valid`在此Demo与其同义，不表示源端新帧或E2E通过。`sample_seq/receive_time_ms`仅表示adaptor成功读取次数/最近成功读取时间，失败与重放不刷新。应用通过已有Snapshot状态通道、`AmbLiMgrVmbc_RxState(channel)`读取独立信号；此getter仅返回应用从SM取得的状态副本，不访问producer缓存。

通用history queue场景应按周期起始缓存数量有界消费，并完整保留批次。当前Demo没有queue订阅，也没有实现通用queue生成器；配置为queue会在生成前拒绝，不会静默只保留最后一条。

## E2E 行为与配置

仅MotionCtrlInfo/MotionCtrlInfoPri.IfCommInfo开启`e2e_state`，其他八个订阅关闭。是否向应用暴露状态不改变源平台E2E配置，更不取消Server FF/Field Set的强制校验。

源端两路分别周期读取：

- 业务：`sm_read_*_on_notify_*`。
- E2E：`sm_read_*_on_e2e_state_*`，与文档命名一致；正式SDK需核对实际接口、类型与布局。

状态仅来自第二路成功读取的原始值。0..6及未来状态值原样传递，不二次归类，不区分底座未提供的CRC细类；状态2是通用ERROR，4是NONEWDATA。状态读取失败不更新`e2e_state`，不推导OK或timeout。独立`e2e_read_success/e2e_read_error`表示该通路读取结果；关闭的通路两者均false。

Motion业务消息的两项业务字段及`e2e_state`采用proto3 optional；缺席表示本消息不更新该字段，0和false带presence时仍更新。首次只有状态时仅发送状态；已有历史业务值时可同时携带历史值与本次状态。应用只合并消息携带且本周期允许消费的字段，不增加实际灯光业务的E2E故障处理。两路最新快照不承诺逐帧关联，不保留E2E观测FIFO，不把轮询次数当作底座故障上报次数。

静态配置位于`contract/amblimgr_state_config.json`的`e2e_state_used`。修改后执行：

```sh
python3 tools/configure_e2e.py
python3 tools/configure_e2e.py --check
```

工具同步Motion IDL字段及`inc/soa_bridge_config.h`编译开关，不运行时解释JSON。关闭配置的验证会独立生成无E2E字段的nanopb类型，并编译adaptor及实际应用。IDL指纹变化需显式更新获批版本记录`contract/client_rx_idl_revision.json`；旧`manifest.json`保留最初IDL阶段的历史指纹。

LOCAL原生E2E getter可能始终SUCCESS却未接通状态通路，因此`SoaSmBindings.motion_e2e_report_supported`默认false；真实集成确认源端支持状态报告后才置true。不能用VMBC LOCAL原生E2E状态代替源端状态，也不以默认零冒充OK。

## 调度与错误隔离

```text
SoaAdaptor_AmbLiMgr_10ms
  输入：应用SM Lifecycle心跳 → adaptor平台业务/E2E读取与裁剪
       → 每通道最多一次VMBC buffer写入 → Snapshot
  应用：读取Snapshot → AmbLiMgr_timer_10ms
       → VMBC sm_read业务值 → 业务逻辑 → VMBC sm_write请求
  输出：请求回调通过SM取请求 → 有界队列 → 平台SM发送
```

单个源订阅读取失败不阻断其他接口、AmbLiMgr或输出。内部Lifecycle/Snapshot交付失败属于另一类故障，仍停止该次模型执行并清旧请求，下周期恢复。Snapshot的consumer_epoch和sequence防止旧buffer冒充本周期握手。业务buffer不能循环读空，也不因单接口失败统一清掉其他输出。

应用根据当前Snapshot的have_value及delivery_pending控制消费，避免adaptor重建后将底座残留业务buffer合并到当前输入。Motion状态字段另要求本周期状态读取成功。内部业务写失败保留pending，下周期用最新快照覆盖并重试，不停止平台buffer轮询。

FF规则保持：每RPC核心队列深度4，跨RPC按观测到达顺序转发；满队列拒绝新请求，断连清旧命令，发送前复查连接epoch，每条请求只尝试一次、不自动重试。DynPrmSet.seg_node_pri恢复平台默认0。SM写成功不等于Server执行成功。

## 部署与初始化

- adaptor消费12个平台端点，提供12个VMBC业务端点及1个辅助服务。
- AmbLiMgr保留4个平台Client，新增13个LOCAL VMBC Client。
- 22个业务FF及Lifecycle使用到达回调；业务订阅和Snapshot周期轮询，disable_callback=true。
- 正式分配VMBC service_id及组件object_id后，用底座工具生成`_af_api.h`及实现，并生成匹配的nanopb消息。
- 设置长生命周期`SoaSmBindings`，提供连接/错误适配及原生返回码分类。接收普通数据九路及Motion独立E2E读取已直接调用原生SM形式，不再要求三路逐样本E2E回调绑定。
- 先绑定VMBC classifier、创建平台/应用端口、初始化核心和时钟，再由底座生命周期激活辅助服务及AmbLiMgr，最后启动唯一10ms入口。
- 所有回调与三段Runnable同核串行；SDK必须在输出阶段前交付本周期请求回调。10ms不是已验证的WCET或通信时延。
- 固件工程include`cmake/firmware.cmake`，只链接正式底座SM及nanopb，不纳入tests。确认源session隔离、首次写入有效性检查、初始化顺序及正式SDK类型布局。

接口依据：[MCU Glue Code API](https://nio.feishu.cn/wiki/wikcnQPgoX5lGBqPBIwSDiTlsCf)、[错误处理](https://nio.feishu.cn/wiki/KTO4wSw7ziHAvJkTr6bcgG00ncb)、[E2E文档](https://nio.feishu.cn/wiki/UIWRwgOvMidN7ek0dR8cdvounod)。SM调用错误、SOA异步错误和E2E属于不同域；不能因为数值同为8就合并语义。

## 主机验证

```sh
cmake -S /home/shaun/soa_adaptor/workbench/soa_adaptor \
  -B /tmp/amblimgr-bridge-build -G Ninja \
  -DSOA_TOOLS_PYTHON=/tmp/soa-vmbc-idl-venv/bin/python
cmake --build /tmp/amblimgr-bridge-build
ctest --test-dir /tmp/amblimgr-bridge-build --output-on-failure
```

| CTest | 验证内容 |
| --- | --- |
| bridge_behavior | 三段顺序、业务裁剪、无质量门控、历史值、FF队列和重启 |
| actual_amblimgr_10ms | 实际模型100正常周期、内部快照失败恢复、单接口失败隔离、E2E合并、0/false、adaptor单独重建 |
| sm_port_binding | 九路原生业务读取、Motion独立状态读取、官方返回码分类、LOCAL能力限制 |
| all_31_mappings | 9RX/22TX独立nanopb期望值比对 |
| bridge_failure_boundaries | 最新值背压、计时回绕、FF顺序/不重试、错误队列及重启 |
| source_and_configuration_boundaries | 102输入指纹、31条SM调用、原Server和唯一周期、八份不变IDL及获批Motion变更 |
| vmbc_sm_transport | 原生形式请求读写/回调、延迟交付、顺序、SDK拒绝及生命周期 |
| all_31_sm_mappings | 全部31映射穿过VMBC SM并核对结果 |
| vmbc_sm_state_recovery | 原始E2E 0..6及未来码、纯状态、独立读取失败、历史值、buffer、presence、写失败恢复 |
| client_read_policy | SDK有payload就转发，不受数据meta中的E2E影响 |
| e2e_configuration_off | 关闭字段后生成nanopb，编译核心、SM适配、VMBC传输及真实应用 |

Mock保留buffer最新值，读取不消费、写入覆盖；FF仍使用队列。首次未写返回ERR_NO_MSG，模拟启用首次写入有效性检查的底座。主机测试不证明真实SDK具有同样配置。正式SDK生成头、nRPC元数据、源端状态上报能力、ECU通信与硬件时序需要集成验证。
