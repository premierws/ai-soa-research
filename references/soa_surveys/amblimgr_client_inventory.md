# AmbLiMgr Client 消费与桥接分析

分析日期：2026-10-30。仅新增分析产物，未修改参考软件、IDL 和部署配置。

## 1. 结论与证据范围

配置包含 13 个 Client 条目、10 种服务、36 个业务接口实例项：14 个接收项、22 个 FF Method 发送项。这里按服务实例计数，不包含连接状态和错误接口。源码找到 12 个接收调用、22 个请求发送调用；其中 9 个接收项存在明确业务字段引用，3 个只读取缓存，另有 2 个配置订阅但未找到读取调用。

配置中的实际字段为 `rpc_behavior_customization`，不是 `rpc_custom`；实例字段为 `service_instance_name`。未指定实例时只记录“未指定”，不推断平台实例名。配置里的 `event` 分类不能代替 IDL 的 method_type：14 个接收项实际为 5 个 EVENT、8 个 FIELD_READONLY、1 个 FIELD_WRITABLE；本模块对该 writable Field 只发现接收调用。

分析覆盖提供的 src/、lib/、inc/、app.json、deployment、Proto 与 .options。未执行编译或运行测试；静态无引用不是删除批准，字段引用也不是运行时可达性证明。

## 2. Client 与实例总表

| Package | Service | Instance | 接收接口 | 请求发送接口 |
|---|---|---|---|---|
| srv.body.base | RlsInfo | 未指定 | LightSnrSts | — |
| srv.body.intrlight | DynAmbLiActu | 未指定 | DynAmbLiSts | DynEnaCtrl、DynGenBriCtrl、DynNodeCtrl、DynPrmSet、DynSegCtrl、DynSeqPilot |
| srv.body.intrlight | StaAmbLiActu | StaAmbLiAp | — | StaColorCtrl、StaEnaCtrl、StaNodeBriCtrl、StaPrmCtrl |
| srv.body.intrlight | StaAmbLiActu | StaAmbLiFw | StaAmbLiSts | StaColorCtrl、StaEnaCtrl、StaGenBriCtrl、StaPrmCtrl |
| srv.body.intrlight | StaAmbLiActu | StaAmbLiIp | — | StaColorCtrl、StaEnaCtrl、StaNodeBriCtrl、StaPrmCtrl |
| srv.body.intrlight | StaAmbLiActu | StaAmbLiStorg | StaAmbLiSts | StaColorCtrl、StaEnaCtrl、StaNodeBriCtrl、StaPrmCtrl |
| srv.body.safety | SeatBasicSts | 未指定 | SeatBasicStsArray | — |
| srv.body.smtkey | SmtKeyUsrIntnMgr | 未指定 | SmtKeyUsrIntnNotify | — |
| srv.infra.vehmoding | VehMode | 未指定 | VehModeInfo、VehModeSettingInfo | — |
| srv.infra.vehmoding | VehState | 未指定 | VehStateInfo | — |
| srv.motion.drv | MotionCtrlInfo | MotionCtrlInfoPri | IfCommInfo | — |
| srv.vehctl.scnmgr | DriveModeMgr | 未指定 | DriveModeSts、EcoPlusModeInfo | — |
| srv.vehicle.plm | VehConfig | 未指定 | IVcpVal_InteriorBodyColor、IVcpVal_VehicleProject | — |

## 3. 接收信号与代码实际使用

| Service / Instance | RPC / IDL 类型 | 实际业务字段 | 证据 |
|---|---|---|---|
| RlsInfo / 未指定 | LightSnrSts / EVENT | `head_lamps_on` | [AmbLiMgr.c:8177](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:8177)；字段 [AmbLiMgr.c:8219](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:8219) |
| DynAmbLiActu / 未指定 | DynAmbLiSts / FIELD_READONLY | `ambli_sts[0].ambli_sts`、`ambli_sts[1].ambli_sts`、`ambli_sts[2].ambli_sts`、`ambli_sts[3].ambli_sts`、`ambli_sts[4].ambli_sts`、`ambli_sts[5].ambli_sts`、`ambli_sts[6].ambli_sts` | [AmbLiMgr.c:30241](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:30241)；字段 [AmbLiMgr.c:30315](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:30315) |
| StaAmbLiActu / StaAmbLiFw | StaAmbLiSts / FIELD_READONLY | 配置订阅，未找到读取调用 | 配置声明；全目录检索未找到读取调用 |
| StaAmbLiActu / StaAmbLiStorg | StaAmbLiSts / FIELD_READONLY | 配置订阅，未找到读取调用 | 配置声明；全目录检索未找到读取调用 |
| SeatBasicSts / 未指定 | SeatBasicStsArray / FIELD_READONLY | `seat_basic_sts[7].occpnt_sensor_sts`、`seat_basic_sts[0].occpnt_sensor_sts`、`seat_basic_sts[1].occpnt_sensor_sts`、`seat_basic_sts[2].occpnt_sensor_sts`、`seat_basic_sts[3].occpnt_sensor_sts`、`seat_basic_sts[4].occpnt_sensor_sts`、`seat_basic_sts[8].occpnt_sensor_sts`、`seat_basic_sts[0].occpnt_fail_sts`、`seat_basic_sts[1].occpnt_fail_sts`、`seat_basic_sts[2].occpnt_fail_sts`、`seat_basic_sts[3].occpnt_fail_sts`、`seat_basic_sts[4].occpnt_fail_sts`、`seat_basic_sts[7].occpnt_fail_sts`、`seat_basic_sts[8].occpnt_fail_sts` | [AmbLiMgr.c:21444](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:21444)；字段 [AmbLiMgr.c:21485](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:21485) |
| SmtKeyUsrIntnMgr / 未指定 | SmtKeyUsrIntnNotify / EVENT | `smt_key_drv_veh_intera_phase` | [AmbLiMgr.c:7570](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:7570)；字段 [AmbLiMgr.c:7644](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:7644) |
| VehMode / 未指定 | VehModeInfo / FIELD_READONLY | 已读取并缓存，未找到业务字段引用 | [AmbLiMgr.c:30370](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:30370) |
| VehMode / 未指定 | VehModeSettingInfo / FIELD_READONLY | 已读取并缓存，未找到业务字段引用 | [AmbLiMgr.c:30411](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:30411) |
| VehState / 未指定 | VehStateInfo / FIELD_READONLY | `operator_state`、`veh_state_detailed` | [AmbLiMgr.c:8099](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:8099)；字段 [AmbLiMgr.c:8153](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:8153) |
| MotionCtrlInfo / MotionCtrlInfoPri | IfCommInfo / EVENT | `accr_pedl_posn_vld`、`accr_pedl_posn` | [AmbLiMgr.c:9020](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:9020)；字段 [AmbLiMgr.c:9091](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:9091) |
| DriveModeMgr / 未指定 | DriveModeSts / FIELD_WRITABLE | `dm_type` | [AmbLiMgr.c:16621](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:16621)；字段 [AmbLiMgr.c:16672](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:16672) |
| DriveModeMgr / 未指定 | EcoPlusModeInfo / FIELD_READONLY | `eco_plus_mode_sts` | [AmbLiMgr.c:7788](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:7788)；字段 [AmbLiMgr.c:7896](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:7896) |
| VehConfig / 未指定 | IVcpVal_InteriorBodyColor / EVENT | 已读取并缓存，未找到业务字段引用 | [AmbLiMgr.c:30191](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:30191) |
| VehConfig / 未指定 | IVcpVal_VehicleProject / EVENT | `vcp_val` | [AmbLiMgr.c:12826](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:12826)；字段 [AmbLiMgr.c:12865](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:12865) |

### 可明确评估的裁剪机会

- `LightSnrSts`：12 个顶层字段中只发现 `head_lamps_on` 的业务引用；有效性/Alive 字段虽未引用，是否随桥接补充状态需单独决策。
- `SmtKeyUsrIntnNotify`：5 个顶层字段中只引用 `smt_key_drv_veh_intera_phase`。
- `VehStateInfo`：4 个顶层字段中引用 `operator_state`、`veh_state_detailed`。
- `IfCommInfo`：58 个顶层字段中只引用 `accr_pedl_posn`、`accr_pedl_posn_vld`，这是清晰的裁剪试点。
- `DriveModeSts`：10 个顶层字段中只引用 `dm_type`；虽然 IDL 是 FIELD_WRITABLE，本模块没有发现 Setter 调用，不应据此新增写能力。
- `EcoPlusModeInfo`：2 个字段中只引用 `eco_plus_mode_sts`。
- `DynAmbLiSts`：固定 7 项，业务读取每项的 `ambli_sts`，未发现 `ambli_err` 业务引用。
- `SeatBasicStsArray`：固定 9 项，仅引用索引 0、1、2、3、4、7、8 的 `occpnt_sensor_sts` 和 `occpnt_fail_sts`；不能直接压缩为 7 项并沿用旧索引。优先保留 9 项位置、裁剪元素字段，或显式设计索引映射。

## 4. 请求发送字段

22 个发送项的 IDL 均为 METHOD + Null（FF Method），本配置没有 Client RR、主动 Getter 或 Setter 的显式业务调用。发送数据也是 Client 改造范围，不属于需要保留直连的应用 Server 侧。第一版保留全部请求字段和数组形状，不把常量当作未使用字段。

| Service / Instance | RPC | 请求类型 | 直接构造路径 | API 证据 |
|---|---|---|---|---|
| DynAmbLiActu / 未指定 | DynEnaCtrl | MsgDynEnaCtrl | `ena_ctrl[wk_i32_i]` | [AmbLiMgr.c:8925](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:8925) |
| DynAmbLiActu / 未指定 | DynGenBriCtrl | MsgDynGenBriCtrl | `gen_bri_ctrl` | [AmbLiMgr.c:9700](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:9700) |
| DynAmbLiActu / 未指定 | DynNodeCtrl | MsgDynNodeCtrl | `node_ctrl[0]` | [AmbLiMgr.c:9798](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:9798) |
| DynAmbLiActu / 未指定 | DynPrmSet | MsgDynPrmSet | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`seg_flow`、`seg_node_pri`、`disp_mod`、`color_mod`、`bri_mod` | [AmbLiMgr.c:11299](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:11299) |
| DynAmbLiActu / 未指定 | DynSegCtrl | MsgDynSegCtrl | `seg_ctrl[0]` | [AmbLiMgr.c:12025](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:12025) |
| DynAmbLiActu / 未指定 | DynSeqPilot | MsgDynSeqPilot | `pilot_id` | [AmbLiMgr.c:12133](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:12133) |
| StaAmbLiActu / StaAmbLiAp | StaColorCtrl | MsgStaColorCtrl | `color_ctrl[wk_i32_i]` | [AmbLiMgr.c:19576](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:19576) |
| StaAmbLiActu / StaAmbLiAp | StaEnaCtrl | MsgStaEnaCtrl | `ena_ctrl[wk_i32_i]` | [AmbLiMgr.c:23217](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:23217) |
| StaAmbLiActu / StaAmbLiAp | StaNodeBriCtrl | MsgStaNodeBriCtrl | `node_bri_ctrl[wk_i32_i]` | [AmbLiMgr.c:25655](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:25655) |
| StaAmbLiActu / StaAmbLiAp | StaPrmCtrl | MsgStaPrmCtrl | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod[0]`、`breath_mod[1]`、`breath_mod[2]` | [AmbLiMgr.c:27848](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:27848) |
| StaAmbLiActu / StaAmbLiFw | StaColorCtrl | MsgStaColorCtrl | `color_ctrl[wk_i32_i]` | [AmbLiMgr.c:19007](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:19007) |
| StaAmbLiActu / StaAmbLiFw | StaEnaCtrl | MsgStaEnaCtrl | `ena_ctrl[wk_i32_i]` | [AmbLiMgr.c:22486](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:22486) |
| StaAmbLiActu / StaAmbLiFw | StaGenBriCtrl | MsgStaGenBriCtrl | `gen_bri_ctrl` | [AmbLiMgr.c:23518](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:23518) |
| StaAmbLiActu / StaAmbLiFw | StaPrmCtrl | MsgStaPrmCtrl | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod[0]`、`breath_mod[1]`、`breath_mod[2]` | [AmbLiMgr.c:27254](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:27254) |
| StaAmbLiActu / StaAmbLiIp | StaColorCtrl | MsgStaColorCtrl | `color_ctrl[wk_i32_i]` | [AmbLiMgr.c:22286](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:22286) |
| StaAmbLiActu / StaAmbLiIp | StaEnaCtrl | MsgStaEnaCtrl | `ena_ctrl[wk_i32_i]` | [AmbLiMgr.c:23016](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:23016) |
| StaAmbLiActu / StaAmbLiIp | StaNodeBriCtrl | MsgStaNodeBriCtrl | `node_bri_ctrl[wk_i32_i]` | [AmbLiMgr.c:25421](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:25421) |
| StaAmbLiActu / StaAmbLiIp | StaPrmCtrl | MsgStaPrmCtrl | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod[0]`、`breath_mod[1]`、`breath_mod[2]` | [AmbLiMgr.c:28751](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:28751) |
| StaAmbLiActu / StaAmbLiStorg | StaColorCtrl | MsgStaColorCtrl | `color_ctrl[wk_i32_i]` | [AmbLiMgr.c:17645](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:17645) |
| StaAmbLiActu / StaAmbLiStorg | StaEnaCtrl | MsgStaEnaCtrl | `ena_ctrl[wk_i32_i]` | [AmbLiMgr.c:22750](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:22750) |
| StaAmbLiActu / StaAmbLiStorg | StaNodeBriCtrl | MsgStaNodeBriCtrl | `node_bri_ctrl[wk_i32_i]` | [AmbLiMgr.c:24529](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:24529) |
| StaAmbLiActu / StaAmbLiStorg | StaPrmCtrl | MsgStaPrmCtrl | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod[0]`、`breath_mod[1]`、`breath_mod[2]` | [AmbLiMgr.c:26590](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:26590) |

### 必须保留的数组与嵌套语义

- `DynEnaCtrl.ena_ctrl`：7 项；`DynNodeCtrl.node_ctrl`：207 项，每项含 color/color_vld/bri。源码在 9735 行附近构造数组，9765/9772 行通过 memcpy 拷贝全部 207 项，不能把 `[0]` 误判为只用第一个元素。
- `DynSegCtrl.seg_ctrl`：12 项，每项 7 个字段；12001 行起拷贝完整数组。11338 行起可见完整段结构赋值，部分值为常量，但仍参与实际消息。
- `StaColorCtrl.color_ctrl`、`StaEnaCtrl.ena_ctrl`、`StaNodeBriCtrl.node_bri_ctrl`：均固定 17 项。颜色元素含 color_or_h/color_s，后者可为显式常量 0，也应保留原行为。
- `StaPrmCtrl`：fade_tim/fade_mod_cmd/nat_tran_mod/nat_tran_tim/breath_mod[3]，各实例均有实际构造。
- `.options` 规定的 max_count、fixed_count、int_size 是契约组成部分，不能只读 .proto。

## 5. 不一致与待核实项

1. `StaAmbLiFw.StaAmbLiSts`、`StaAmbLiStorg.StaAmbLiSts` 配置已订阅，但在提供的全部 C 源码中未找到对应读取调用。先作为取消订阅候选，不能自动删除。
2. `VehModeInfo`、`VehModeSettingInfo`、`IVcpVal_InteriorBodyColor` 有读取和整包缓存，但未找到业务字段读取或整包进一步传递；需要确认是否生成残留、诊断/标定依赖或遗漏的外部用途。
3. `LightSnrSts`、`VehModeInfo`、`VehStateInfo`、`IfCommInfo` 在平台 IDL 中启用了 E2E。当前显式业务路径主要判断 sm_* 返回值 SUCCESS，未发现显式 E2E 状态分支；需核对框架返回契约，不能认定现有软件没有 E2E 检查，也不能认定桥接天然保留端到端保护。
4. 13 个 Client 均生成 soa_error；其中 DynAmbLiActu 和四个 StaAmbLiActu 实例生成 connect_state，且业务代码实际读取连接状态并影响请求触发。迁移时必须保留这些输入的等效语义。
5. 模块本地 20 个 .proto/.options 与 Reference/Proto 对应文件逐字节一致，当前没有发现这两份输入的版本分歧。

## 6. Server 保留边界与部署信息

- 应用提供 `srv.body.intrlight.AmbLiMgr`，平台 service_id=2095；保留 AmbLiParamReq、AmbLiSceneReq、AmbLiStsInfo、AmbLiSwtSet 四个 RPC。Server Getter/Setter、事件通知和处理回调不能被 Client 批量替换误伤。
- deployment：$target=MCU；component_instance_name=amblimgr；object_id=951；Client protocol 均为 TOX，domain_id=1。
- cfg/instance.json 声明 CoreId=2；swc_runnable.json 定义 AmbLiMgr_timer_10ms，周期 10ms，并包含四个 Server 事件 Runnable。当前文件不足以确认最终 ECU、ASIL、Offset 和集成调度顺序。
- instance.json 的 CDF 引用指向 cfg/amblimgr_cdf.json，但当前参考文件位于 cfg/user/amblimgr_cdf.json；可能由底座处理，集成前需核实，不直接修正参考输入。
- CMakeLists.txt 挂接外部 ECU_TARGET_NAME，源码依赖底座生成的 amblimgr_af_api.h；当前资料不是独立可构建工程。

## 7. 对 Demo 范围的建议

先建立36项映射清单并冻结字段契约，再分批实现：接收裁剪链路、22项FF请求转发、连接状态与错误映射、应用适配和集成。首次功能等价验证保留争议项，不把订阅清理与桥接迁移混成一次收益；可以另做清理对照组。

VMBC IDL 第一版对接收项按确认的字段定义裁剪类型，对请求项保守保留完整字段。不同实例可共享消息类型，但不得合并实例身份。Service ID/namespace、本地部署协议、E2E状态契约和最终调度需在集成前确认。

## 8. 验证与追踪

- 36 个配置业务项均匹配模块本地 Proto 的 RPC、消息类型及 options。
- 全部提供的 C 文件中找到的34种 Client 业务 API，与清单中的12种接收API和22种发送API集合一致，无额外未归档业务API。
- 直接字段路径逐级匹配 Proto 类型；嵌套整包和 memcpy 另作人工核查，未声称完成完整程序数据流证明。
- 20 个 Proto/.options 副本逐字节一致；输入文件 SHA-256、原始配置、路径行号及类型链存于同目录 JSON。
- 未运行编译、刷写、通信测试或资源测量；本报告不作为功能通过或性能收益证据。
