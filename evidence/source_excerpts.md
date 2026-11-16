# 关键原文摘录与定位

摘录直接来自本项目已经复制的文件。行号定位于本地快照，不表示源仓库未来版本保持相同行号。

## E01：VCC 依赖系统能力实现端到端

材料：[vcc_function_architecture_2026-11-12.md](../references/feishu/vcc_function_architecture_2026-11-12.md)，第 3—4 行。

```text
0003: - 本文档范围为VCC(Vehicle cabin control)功能的架构设计，<text underline="true">依赖系统能力实现端到端，一般不提供标准能力</text>。
0004: - 从功能、性能要求出发，转化功能实现方案。以系统能力划分章节。
```

## E02：Mission 与系统产品分工

材料：[vcc_function_architecture_2026-11-12.md](../references/feishu/vcc_function_architecture_2026-11-12.md)，第 1018—1022 行。

```text
1018: - **VCC：**管理Mission、跨域目标、约束、生命周期和整车完成条件。
1019: - **目标适配层：**将Goal转化为本域策略，完成使能与安全判断并返回Result。
1020: - **SOA能力层：**提供稳定的动作、状态、实时闭环、诊断和安全保护。
1021: 
1022: #### 非中央化设计准则
```

## E03：非中央化功能边界

材料：[vcc_function_architecture_2026-11-12.md](../references/feishu/vcc_function_architecture_2026-11-12.md)，第 1024—1027 行。

```text
1024: 1. **明确功能归属。**仅将需要统一任务对象、跨域目标、共享生命周期、整车完成判定或统一降级协调的功能纳入VCC；单一系统可独立闭环的功能继续归属系统产品。
1025: 1. **升级交互契约。**VCC与系统产品之间由“动作命令 + 状态订阅”逐步升级为“Goal Contract + Result Contract”；Goal描述期望结果和约束，Result表达完成、降级、拒绝及其原因和证据。
1026: 
1027: <mention-doc token="T6pkdUPljozdLHxBD6mccW4zndh" type="docx">如何避免VCC成为中央脚本：功能边界、接口形式、优势与代价</mention-doc>
```

## E04：域内执行与 SOA 复用

材料：[vcc_function_architecture_2026-11-12.md](../references/feishu/vcc_function_architecture_2026-11-12.md)，第 1113—1121 行。

```text
1113: 不推翻现有SOA，仅增加两层：VCC侧的Mission Runtime，以及系统产品侧的目标适配层。
1114: 
1115: 1. **VCC ↔ 系统产品：**使用Goal Contract向下传递目标，使用Result Contract向上返回结果。
1116: 1. **目标适配层 ↔ SOA能力层：**继续使用稳定的Capability Command、State和Event完成域内执行与反馈。
1117: 1. **执行原则：**VCC不直接调用硬件动作；域内时序、状态机、安全闭环和故障处理继续由系统产品负责。
1118: 
1119: <image token="GirWbuaCPonPPgxgUn6cWkcynzb" width="1672" height="941" align="center"/>
1120: 
1121: ### 功能场景列表
```

## E05：AmbLiMgr 请求与状态接口并存

材料：[srv.body.intrlight.amblimgr.proto](../evidence/platform_idl/srv.body.intrlight.amblimgr.proto)，第 196—222 行。

```text
0196: service AmbLiMgr {
0197:     option(service_id) = 2095;
0198: 
0199:     rpc AmbLiParamReq(MsgAmbLiParamReq) returns (Null) {
0200:         option (rpc_id) = 105;
0201:         option (method_type) = METHOD;
0202:     }
0203: 
0204:     rpc AmbLiSceneReq(MsgAmbLiSceneReq) returns (Null) {
0205:         option (rpc_id) = 106;
0206:         option (method_type) = METHOD;
0207:         option (rpc_reliability) = RELIABLE;
0208:     }
0209: 
0210:     rpc AmbLiStsInfo(MsgAmbLiStsInfo) returns (Null) {
0211:         option (rpc_id) = 104;
0212:         option (method_type) = FIELD_READONLY;
0213:         option (update_policy) = ON_CHANGE;
0214:     }
0215: 
0216:     rpc AmbLiSwtSet(MsgAmbLiSwtSet) returns (Null) {
0217:         option (rpc_id) = 101;
0218:         option (method_type) = FIELD_WRITABLE;
0219:         option (update_policy) = ON_CHANGE;
0220:         option (rpc_reliability_field_set) = RELIABLE;
0221:     }
0222: }
```

## E06：WinMgr 同一服务含 FF 与 RR

材料：[srv.body.window.winmgr.proto](../evidence/platform_idl/srv.body.window.winmgr.proto)，第 201—234 行。

```text
0201: service WinMgr {
0202:     option(service_id) = 2007;
0203: 
0204:     rpc ReqWinTarPosn(WinTarPosnReq) returns (Null) {
0205:         option (rpc_id) = 101;
0206:         option (method_type) = METHOD;
0207:     }
0208: 
0209:     rpc ReqWinProhibit(ProhibitWinReq) returns (ProhibitWinReqResult) {
0210:         option (rpc_id) = 104;
0211:         option (method_type) = METHOD;
0212:     }
0213: 
0214:     rpc ReqWinSelfLearn(WinSelfLearnReq) returns (WinSelfLearnReqResult) {
0215:         option (rpc_id) = 105;
0216:         option (method_type) = METHOD;
0217:     }
0218: 
0219:     rpc ReqSideShdTarPosn(SideShdTarPosnReq) returns (Null) {
0220:         option (rpc_id) = 106;
0221:         option (method_type) = METHOD;
0222:     }
0223: 
0224:     rpc WinSts(WinStsInfo) returns (Null) {
0225:         option (rpc_id) = 103;
0226:         option (method_type) = FIELD_READONLY;
0227:         option (update_policy) = ON_CHANGE;
0228:         option (rpc_reliability_field_event) = RELIABLE;
0229:     }
0230: 
0231:     rpc SideShdSts(SideShdStsInfo) returns (Null) {
0232:         option (rpc_id) = 108;
0233:         option (method_type) = FIELD_READONLY;
0234:         option (update_policy) = ON_CHANGE;
```

## E07：AiCabinFuncMgr 含目标型参数

材料：[srv.thermal.hvac.aicabinfuncmgr.proto](../evidence/platform_idl/srv.thermal.hvac.aicabinfuncmgr.proto)，第 109—136 行。

```text
0109:     uint32 request_id                      = 9;
0110:     /**
0111:      * Comment: fan outlet temperature adjust
0112:      * Value  Description(EN)
0113:      * 0      no_request
0114:      * 1      warmer
0115:      * 2      much warmer
0116:      * -1     cooler
0117:      * -2     much cooler
0118:      */
0119:     int32 temp_adjust                     = 10;
0120:     /**
0121:      * Comment: same size as body_part if fandirection_adjust is requested (fan direction for each requested body part), otherwise 0 length
0122:      * Value  Description(EN)
0123:      * 0      no_request
0124:      * 1      direct facing
0125:      * -1     avoid facing
0126:      */
0127:     repeated int32 fandirection_adjust    = 11;
0128:     /**
0129:      * Value  Description(EN)
0130:      * 0      total or unknown
0131:      * 1      head
0132:      * 2      body up
0133:      * 3      body down
0134:      * 4      back rest
0135:      * 5      arm left
0136:      * 6      arm right
```

## E08：AiCabinFuncMgr 请求与状态

材料：[srv.thermal.hvac.aicabinfuncmgr.proto](../evidence/platform_idl/srv.thermal.hvac.aicabinfuncmgr.proto)，第 195—228 行。

```text
0195: service AiCabinFuncMgr {
0196:     option(service_id) = 3064;
0197: 
0198:     rpc SeatSpatialAutoMode(SeatSpatialAutoModeMsg) returns (AiCabinReqReturnMsg) {
0199:         option (rpc_id) = 1;
0200:         option (method_type) = METHOD;
0201:     }
0202: 
0203:     rpc ThmSceneMode(ThmSceneModeMsg) returns (AiCabinReqReturnMsg) {
0204:         option (rpc_id) = 2;
0205:         option (method_type) = METHOD;
0206:     }
0207: 
0208:     rpc ThmSceneModeRecommend(ThmSceneModeMsg) returns (Null) {
0209:         option (rpc_id) = 5;
0210:         option (method_type) = EVENT;
0211:         option (update_policy) = ON_CHANGE;
0212:         option (rpc_reliability) = RELIABLE;
0213:     }
0214: 
0215:     rpc SeatSpatialAutoModeSts(SeatSpatialAutoModeStsMsg) returns (Null) {
0216:         option (rpc_id) = 3;
0217:         option (method_type) = FIELD_READONLY;
0218:         option (update_policy) = ON_CHANGE;
0219:         option (rpc_reliability_field_event) = RELIABLE;
0220:     }
0221: 
0222:     rpc ThmSceneModeSts(ThmSceneModeStsMsg) returns (Null) {
0223:         option (rpc_id) = 4;
0224:         option (method_type) = FIELD_READONLY;
0225:         option (update_policy) = ON_CHANGE;
0226:         option (rpc_reliability_field_event) = RELIABLE;
0227:     }
0228: }
```

## E09：SmartSceneMgr 场景信息事件

材料：[srv.vehctl.scnmgr.smartscenemgr.proto](../evidence/platform_idl/srv.vehctl.scnmgr.smartscenemgr.proto)，第 50—59 行。

```text
0050: service SmartSceneMgr {
0051:     option(service_id) = 6051;
0052: 
0053:     rpc SmtSceneInfo(SmtSceneInfoDta) returns (Null) {
0054:         option (rpc_id) = 1;
0055:         option (method_type) = EVENT;
0056:         option (update_policy) = CYCLIC;
0057:         option (update_cycle_time) = 50;
0058:     }
0059: }
```

## E10：既有场景控制形式

材料：[srv.body.intrlight.ambliscenemgr.proto](../evidence/platform_idl/srv.body.intrlight.ambliscenemgr.proto)，第 92—113 行。

```text
0092: service AmbLiSceneMgr {
0093:     option(service_id) = 2188;
0094: 
0095:     rpc AmbLiSceneUpdate(AmbLiSceneUpdateMsg) returns (Null) {
0096:         option (rpc_id) = 1;
0097:         option (method_type) = METHOD;
0098:         option (rpc_reliability) = RELIABLE;
0099:     }
0100: 
0101:     rpc AmbLiSceneReq(AmbLiSceneReqMsg) returns (Null) {
0102:         option (rpc_id) = 2;
0103:         option (method_type) = METHOD;
0104:         option (rpc_reliability) = RELIABLE;
0105:     }
0106: 
0107:     rpc AmbLiSceneSts(AmbLiSceneStsMsg) returns (Null) {
0108:         option (rpc_id) = 3;
0109:         option (method_type) = FIELD_READONLY;
0110:         option (update_policy) = ON_CHANGE;
0111:         option (rpc_reliability_field_event) = RELIABLE;
0112:     }
0113: }
```

## E11：buffer 与新帧不能混同

材料：[README.md](../evidence/soa_adaptor/README.md)，第 9—20 行。

```text
0009: 当前九个订阅全部按无history queue的buffer模式，每个10ms周期各读取一次。SUCCESS只表示取得当前buffer值，不表示源端收到新帧；同值不去重，读取不消费buffer。
0010: 
0011: | 业务读取结果 | 业务值 | 独立读取信号 |
0012: | --- | --- | --- |
0013: | SUCCESS | 更新并转发本次值 | read_success=true，read_error=false |
0014: | 失败，已有历史值 | 转发最后一次成功读取值 | read_success=false，read_error=true |
0015: | 失败，无历史值 | 不制造默认值、不提供业务字段 | read_success=false，read_error=true |
0016: 
0017: 这里的历史成功值不要求E2E通过。adaptor不对成功读出的payload再做连接/E2E/超时门控，不加入业务debounce、安全值或关灯策略。业务读取失败原因不传给应用。ERR_NO_MSG=7表示本次没有可读取值，也不能使用输出参数。
0018: 
0019: `have_value`表示存在历史成功读取值；`data_valid`在此Demo与其同义，不表示源端新帧或E2E通过。`sample_seq/receive_time_ms`仅表示adaptor成功读取次数/最近成功读取时间，失败与重放不刷新。应用通过已有Snapshot状态通道、`AmbLiMgrVmbc_RxState(channel)`读取独立信号；此getter仅返回应用从SM取得的状态副本，不访问producer缓存。
0020: 
```

## E12：原始 E2E 与业务处理分离

材料：[README.md](../evidence/soa_adaptor/README.md)，第 32—39 行。

```text
0032: 状态仅来自第二路成功读取的原始值。0..6及未来状态值原样传递，不二次归类，不区分底座未提供的CRC细类；状态2是通用ERROR，4是NONEWDATA。状态读取失败不更新`e2e_state`，不推导OK或timeout。独立`e2e_read_success/e2e_read_error`表示该通路读取结果；关闭的通路两者均false。
0033: 
0034: Motion业务消息的两项业务字段及`e2e_state`采用proto3 optional；缺席表示本消息不更新该字段，0和false带presence时仍更新。首次只有状态时仅发送状态；已有历史业务值时可同时携带历史值与本次状态。应用只合并消息携带且本周期允许消费的字段，不增加实际灯光业务的E2E故障处理。两路最新快照不承诺逐帧关联，不保留E2E观测FIFO，不把轮询次数当作底座故障上报次数。
0035: 
0036: 静态配置位于`contract/amblimgr_state_config.json`的`e2e_state_used`。修改后执行：
0037: 
0038: ```sh
0039: python3 tools/configure_e2e.py
```

## E13：FF 发送不代表 Server 完成

材料：[README.md](../evidence/soa_adaptor/README.md)，第 62—64 行。

```text
0062: FF规则保持：每RPC核心队列深度4，跨RPC按观测到达顺序转发；满队列拒绝新请求，断连清旧命令，发送前复查连接epoch，每条请求只尝试一次、不自动重试。DynPrmSet.seg_node_pri恢复平台默认0。SM写成功不等于Server执行成功。
0063: 
0064: ## 部署与初始化
```

## E14：版本化架构与来源证据

材料：[source_evidence.py](../evidence/service_arch/backend/source_evidence.py)，第 8—19 行。

```text
0008: class SourceEvidence:
0009:     source_kind: str
0010:     repository_role: str | None = None
0011:     relative_path: str | None = None
0012:     locator: str | None = None
0013:     schema: str | None = None
0014:     vehicle_model: str | None = None
0015:     version: str | None = None
0016: 
0017:     def __post_init__(self) -> None:
0018:         values = asdict(self).values()
0019:         if any(value and any(ord(char) < 32 for char in value) for value in values):
```

## E15：服务实例及关系事实

材料：[platform_README.md](../evidence/service_arch/platform_README.md)，第 34—42 行。

```text
0034: - Service instance identity is:
0035:   `service_package + service_name + service_instance_name`.
0036: - Graph edges are built at method/event level.
0037: - `clients.method` maps to proto RPCs with `METHOD` or `FIELD` semantics.
0038: - `clients.event` maps to proto RPCs with `EVENT` or `FIELD` semantics.
0039: - If a provider is missing from the selected version configuration but the
0040:   service exists in proto, the graph uses an external-provider edge instead of
0041:   dropping the dependency.
0042: - If a module maps to multiple ECUs, normalization records a `multi_ecu_conflict`.
```

## E16：Event＋FF 样本统计边界

材料：[interface_scenario_survey.md](../references/soa_surveys/interface_scenario_survey.md)，第 18—21 行。

```text
0018: 通知、FF与Set合计1638/2033=80.6%；这是单向操作形态的占比，支持默认路线，不能当作已证明可无损转换率、CPU流量比例或全公司软件比例。未排除字面false分支时为1642/2082=78.9%。宏条件未解析，故2033不应称作已证明可达操作数。
0019: 
0020: 通知读取的1246项中，1238可匹配本地IDL：696 EVENT、476 FIELD_READONLY、66 FIELD_WRITABLE，8项未匹配。357 FF中356匹配；380 RR中374匹配且返回非Null；60 Get均匹配（59 RO、1 RO_NOSUB）；39 Set均匹配（30 RW、9 RW_NOSUB）。未匹配项保留未知，不依猜测补全。
0021: 
```

