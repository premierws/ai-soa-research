# AmbLiMgr Client 对服务 IDL 的覆盖统计

## 统计口径

- 接口按 proto 中显式 rpc 声明计数，不将 Field 隐式操作拆分计数。
- 信号按每个 RPC 的输入和非空输出的叶子字段计数；嵌套结构递归展开，enum计1个；同一类型被不同RPC使用时分别计数。
- 数组按叶子路径计一次，不乘元素数量；发送完整构造的常量和整包复制字段也计为使用。接收只读缓存但无业务字段引用的信号计0。
- 这是静态引用覆盖统计，字段数比例不代表内存、CPU或网络字节比例。

## 按 Client 实例统计

| Client / Instance | 配置接口/服务总接口 | 有调用接口/服务总接口 | 使用信号/服务总信号 | 使用信号/已配置接口信号 |
|---|---|---|---|---|
| RlsInfo（未指定实例） | 1/8（12.5%） | 1/8（12.5%） | 1/54（1.9%） | 1/12（8.3%） |
| DynAmbLiActu（未指定实例） | 7/8（87.5%） | 7/8（87.5%） | 23/28（82.1%） | 23/24（95.8%） |
| StaAmbLiActu/StaAmbLiAp | 4/6（66.7%） | 4/6（66.7%） | 9/15（60.0%） | 9/9（100.0%） |
| StaAmbLiActu/StaAmbLiFw | 5/6（83.3%） | 4/6（66.7%） | 9/15（60.0%） | 9/14（64.3%） |
| StaAmbLiActu/StaAmbLiIp | 4/6（66.7%） | 4/6（66.7%） | 9/15（60.0%） | 9/9（100.0%） |
| StaAmbLiActu/StaAmbLiStorg | 5/6（83.3%） | 4/6（66.7%） | 9/15（60.0%） | 9/14（64.3%） |
| SeatBasicSts（未指定实例） | 1/5（20.0%） | 1/5（20.0%） | 2/32（6.2%） | 2/5（40.0%） |
| SmtKeyUsrIntnMgr（未指定实例） | 1/1（100.0%） | 1/1（100.0%） | 1/7（14.3%） | 1/7（14.3%） |
| VehMode（未指定实例） | 2/4（50.0%） | 2/4（50.0%） | 0/13（0.0%） | 0/7（0.0%） |
| VehState（未指定实例） | 1/6（16.7%） | 1/6（16.7%） | 2/14（14.3%） | 2/4（50.0%） |
| MotionCtrlInfo/MotionCtrlInfoPri | 1/3（33.3%） | 1/3（33.3%） | 2/83（2.4%） | 2/58（3.4%） |
| DriveModeMgr（未指定实例） | 2/7（28.6%） | 2/7（28.6%） | 2/22（9.1%） | 2/12（16.7%） |
| VehConfig（未指定实例） | 2/77（2.6%） | 2/77（2.6%） | 1/77（1.3%） | 1/2（50.0%） |

## 结论

- 没有Client同时用全对应服务的接口和信号。SmtKeyUsrIntnMgr用全1个RPC，但只用1/7叶子字段。
- 按整个服务IDL的信号覆盖率，最多是DynAmbLiActu：23/28，82.1%；最少是VehMode：0/13，但存在读取缓存，不能直接删除。
- 排除无业务字段引用者，最少是VehConfig：1/77，1.3%。按接口覆盖，最多SmtKeyUsrIntnMgr（100%），最少VehConfig（2/77，2.6%）。
- DynAmbLiActu未选DynContrColorCtrl的4个字段，DynAmbLiSts只读ambli_sts、不读ambli_err。
- IfCommInfo内部用2/58字段；SeatBasicStsArray用2/5种叶子字段且只读9个位置中的7个，裁剪时不能破坏位置映射。
- 完整证据见同目录amblimgr_client_inventory.md/json；未找到字段引用不等于批准删除，需核实外部用途。

## RlsInfo / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| LightSnrSts | 1/12（8.3%） | `head_lamps_on` |

## DynAmbLiActu / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| DynAmbLiSts | 1/2（50.0%） | `ambli_sts.ambli_sts` |
| DynEnaCtrl | 1/1（100.0%） | `ena_ctrl` |
| DynGenBriCtrl | 1/1（100.0%） | `gen_bri_ctrl` |
| DynNodeCtrl | 3/3（100.0%） | `node_ctrl.color`、`node_ctrl.color_vld`、`node_ctrl.bri` |
| DynPrmSet | 9/9（100.0%） | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`seg_flow`、`seg_node_pri`、`disp_mod`、`color_mod`、`bri_mod` |
| DynSegCtrl | 7/7（100.0%） | `seg_ctrl.seg_start_posn`、`seg_ctrl.seg_nr`、`seg_ctrl.seg_color_vld`、`seg_ctrl.seg_start_color_h`、`seg_ctrl.seg_end_color_s`、`seg_ctrl.seg_start_bri`、`seg_ctrl.seg_end_bri` |
| DynSeqPilot | 1/1（100.0%） | `pilot_id` |

## StaAmbLiActu / StaAmbLiAp

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| StaColorCtrl | 2/2（100.0%） | `color_ctrl.color_or_h`、`color_ctrl.color_s` |
| StaEnaCtrl | 1/1（100.0%） | `ena_ctrl` |
| StaNodeBriCtrl | 1/1（100.0%） | `node_bri_ctrl` |
| StaPrmCtrl | 5/5（100.0%） | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod` |

## StaAmbLiActu / StaAmbLiFw

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| StaAmbLiSts | 0/5（0.0%） | configured_no_read_call |
| StaColorCtrl | 2/2（100.0%） | `color_ctrl.color_or_h`、`color_ctrl.color_s` |
| StaEnaCtrl | 1/1（100.0%） | `ena_ctrl` |
| StaGenBriCtrl | 1/1（100.0%） | `gen_bri_ctrl` |
| StaPrmCtrl | 5/5（100.0%） | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod` |

## StaAmbLiActu / StaAmbLiIp

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| StaColorCtrl | 2/2（100.0%） | `color_ctrl.color_or_h`、`color_ctrl.color_s` |
| StaEnaCtrl | 1/1（100.0%） | `ena_ctrl` |
| StaNodeBriCtrl | 1/1（100.0%） | `node_bri_ctrl` |
| StaPrmCtrl | 5/5（100.0%） | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod` |

## StaAmbLiActu / StaAmbLiStorg

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| StaAmbLiSts | 0/5（0.0%） | configured_no_read_call |
| StaColorCtrl | 2/2（100.0%） | `color_ctrl.color_or_h`、`color_ctrl.color_s` |
| StaEnaCtrl | 1/1（100.0%） | `ena_ctrl` |
| StaNodeBriCtrl | 1/1（100.0%） | `node_bri_ctrl` |
| StaPrmCtrl | 5/5（100.0%） | `fade_tim`、`fade_mod_cmd`、`nat_tran_mod`、`nat_tran_tim`、`breath_mod` |

## SeatBasicSts / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| SeatBasicStsArray | 2/5（40.0%） | `seat_basic_sts.occpnt_fail_sts`、`seat_basic_sts.occpnt_sensor_sts` |

## SmtKeyUsrIntnMgr / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| SmtKeyUsrIntnNotify | 1/7（14.3%） | `smt_key_drv_veh_intera_phase` |

## VehMode / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| VehModeInfo | 0/1（0.0%） | read_and_cached_no_business_field_reference |
| VehModeSettingInfo | 0/6（0.0%） | read_and_cached_no_business_field_reference |

## VehState / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| VehStateInfo | 2/4（50.0%） | `operator_state`、`veh_state_detailed` |

## MotionCtrlInfo / MotionCtrlInfoPri

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| IfCommInfo | 2/58（3.4%） | `accr_pedl_posn`、`accr_pedl_posn_vld` |

## DriveModeMgr / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| DriveModeSts | 1/10（10.0%） | `dm_type` |
| EcoPlusModeInfo | 1/2（50.0%） | `eco_plus_mode_sts` |

## VehConfig / 未指定实例

| RPC | 使用/该消息叶子字段 | 字段 |
|---|---|---|
| IVcpVal_InteriorBodyColor | 0/1（0.0%） | read_and_cached_no_business_field_reference |
| IVcpVal_VehicleProject | 1/1（100.0%） | `vcp_val` |
