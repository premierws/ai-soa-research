# 请求类接口字段使用与VMBC裁剪机会调研

## 结论

不能把AmbLiMgr的统计推广为“请求类接口很少能裁剪”。现有库已出现应用只表达请求消息部分独立业务意图，其余字段固定为NO_REQ/NA、固定来源ID或控制策略的明确案例。此前“发送全部字段都使用”的口径是完整构造并发送，并不等于每个字段都需要由应用动态维护。

## 扫描范围与局限

扫描soa_deployment/VDF与ZONE共669个C/C++文件，在120个模块目录中匹配826个C请求调用点，其中744个可匹配模块本地IDL并定位request_msg来源变量。该数字不能当作全库唯一接口数、完整业务使用统计或可裁剪比例。未覆盖全部C++ API、Field Set和非典型封装，未完成全程序指针/控制流/模型分析。

按模块自带Proto进行比对，不使用另一版本中央Proto替代。四个案例均核对两份车型配置的Client请求声明、请求IDL、实际构造与发送调用。

## 三种字段必须分开

1. 应用业务变量：当前模块实际变化的请求内容，通常保留在VMBC请求中。
2. 固定来源/模式/安全策略：有真实语义，可考虑配置化后由Adaptor注入，不能当成无用字段。
3. 不请求/无效/不适用字段：可作为内部IDL省略候选，Adaptor必须重建原有值，而非盲目清零或沿用其他Client缓存。

## 核实案例

| 模块 | 服务.RPC | 请求叶子字段 | 业务变量字段 | 固定字段 |
|---|---|---:|---:|---:|
| CRSDriveModeMgr | CbnClmtPenMgr.ReqPenHvac | 9 | 1（11.1%） | 8 |
| CbnAqiMgr | CbnClmtAssFuncMgr.ReqCabinHvacAdjust | 11 | 4（36.4%） | 7 |
| CbnAvcMgr | CabinAvcCmd.AvcCtl | 14 | 2（14.3%） | 12 |
| BDYmanSwtSeatApp | SeatMoveMgr.ReqSeatAdjEndur | 16 | 13（81.2%） | 3 |

## CRSDriveModeMgr → CbnClmtPenMgr.ReqPenHvac

- 业务变量：`hvac_eco_mod_pen`。
- 自动除雾和后吹风两个嵌套结构共4叶子字段固定；其余rear/airflow/temp/temp_level四项固定。仅ECO来自wk_Switch11。
- [源码构造](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/src/CRSDriveModeMgr.c:2719)；[发送调用](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/src/CRSDriveModeMgr.c:2763)；[IDL接口](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/proto/srv.thermal.hvac.cbnclmtpenmgr.proto:166)。
- 配置核对：[vdc-m7-a-main-leo](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/cfg/vdc-m7-a-main-leo/soa/soa_deployment.json)，实例=[None]；[vdc-m7-a2-main-dom](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/cfg/vdc-m7-a2-main-dom/soa/soa_deployment.json)，实例=[None]。

## CbnAqiMgr → CbnClmtAssFuncMgr.ReqCabinHvacAdjust

- 业务变量：`osa_ratio_req_type`, `osa_ratio_req`, `frnt_blw_spd_req_type`, `frnt_blw_spd_req`。
- req_src_id=1；booster/frnt_airflow/rear_airflow三组类型固定NO_REQ、值固定0；ConstB初始化在304行。
- [源码构造](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAqiMgr/src/CbnAqiMgr.c:949)；[发送调用](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAqiMgr/src/CbnAqiMgr.c:1025)；[IDL接口](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAqiMgr/proto/srv.thermal.hvac.cbnclmtassfuncmgr.proto:69)。
- 配置核对：[vdc-m7-a-main-leo](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAqiMgr/cfg/vdc-m7-a-main-leo/soa/soa_deployment.json)，实例=[None]；[vdc-m7-a2-main-dom](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAqiMgr/cfg/vdc-m7-a2-main-dom/soa/soa_deployment.json)，实例=[None]。

## CbnAvcMgr → CabinAvcCmd.AvcCtl

- 业务变量：`speed_spec`, `actuator_set_pos`。
- FLSH示例，其他15实例同样是14字段、12固定2业务变量。固定字段包含实际控制模式，不能直接按“不使用”删除平台字段。
- [源码构造](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAvcMgr/src/CbnAvcMgr.c:3199)；[发送调用](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAvcMgr/src/CbnAvcMgr.c:3248)；[IDL接口](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAvcMgr/proto/srv.thermal.hvac.cabinavccmd.proto:231)。
- 配置核对：[vdc-m7-a-main-leo](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAvcMgr/cfg/vdc-m7-a-main-leo/soa/soa_deployment.json)，实例=['FLMH', 'FLMV', 'FLSH', 'FLSV', 'FRMH', 'FRMV', 'FRSH', 'FRSV', 'MLMH', 'MLMV', 'MLSH', 'MLSV', 'MRMH', 'MRMV', 'MRSH', 'MRSV']；[vdc-m7-a2-main-dom](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnAvcMgr/cfg/vdc-m7-a2-main-dom/soa/soa_deployment.json)，实例=['FLMH', 'FLMV', 'FLSH', 'FLSV', 'FRMH', 'FRMV', 'FRSH', 'FRSV', 'MLMH', 'MLMV', 'MLSH', 'MLSV', 'MRMH', 'MRMV', 'MRSH', 'MRSV']。

## BDYmanSwtSeatApp → SeatMoveMgr.ReqSeatAdjEndur

- 业务变量：`cush_slide_req`, `back_rest_req`, `cush_hei_req`, `cush_len_req`, `front_cush_tilt_req`, `rear_cush_tilt_req`, `total_cush_tilt_req`, `uba_adj_req`, `headrest_adj_req`, `footrest_front_req`, `footrest_rear_req`, `leg_sup_len_req`, `leg_sup_tilt_req`。
- req_src_type固定；headfold_req、panodisp_filp_req固定MOVE_FB_NA（IDL值0）；FL/FR/RL/RR四实例同类构造。此接口为RR，响应语义仍需保留。
- [源码构造](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/src/BDYmanSwtSeatApp.c:597)；[发送调用](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/src/BDYmanSwtSeatApp.c:650)；[IDL接口](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/proto/srv.body.seat.seatmovemgr.proto:224)。
- 配置核对：[vdc-m7-a-main-leo](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/cfg/vdc-m7-a-main-leo/soa/soa_deployment.json)，实例=['SeatMoveMgr_FL', 'SeatMoveMgr_FR', 'SeatMoveMgr_RL', 'SeatMoveMgr_RR']；[vdc-m7-a2-main-dom](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/cfg/vdc-m7-a2-main-dom/soa/soa_deployment.json)，实例=['SeatMoveMgr_FL', 'SeatMoveMgr_FR', 'SeatMoveMgr_RL', 'SeatMoveMgr_RR']。

## 对AmbLiMgr统计的修正

当前POC参考版本Reference/AmbLiMgr/src/AmbLiMgr.c:11264中，DynPrmSet.seg_node_pri固定为DYN_AMBLI_PRI_NO_REQ。前期9/9统计表示9个字段被构造并发送，不等于9个独立变化的业务输入。这也说明即便是当前AmbLiMgr，仍可进一步区分固定策略和业务字段。VDF库中的AmbLiMgr是不同版本，不应把该版本固定字段数量套用到当前POC。

## 对Adaptor生成的具体要求

- 每条请求映射明确列出透传字段与补齐字段；补齐值需绑定Client/实例/版本，不可全局通用。
- 例如CRSDriveModeMgr可只传hvac_eco_mod_pen，Adaptor重建另外8个字段的原值，包括非0的INVALID；不是把其余字段一律置0。
- CbnAqiMgr可只传4个业务字段，由Adaptor补req_src_id=1，以及3组NO_REQ+0。
- CbnAvcMgr可评估只传speed_spec和actuator_set_pos，其余12字段由该Client的配置注入；固定模式仍是实际控制语义。
- BDYmanSwtSeatApp可评估由Adaptor补请求来源和2个NA字段，仍保留RR的请求关联、超时及响应。
- 不得因省略字段而把其他Client历史请求合入当前请求；仲裁继续由原Server承担，除非另有明确方案。
- 验证应对比改造前后平台请求的字段语义等价，并覆盖不同请求者、模式、实例和异常路径。业务语义等价后再评估实际RAM/CPU收益；默认值的线缆编码长度不等于C结构体大小。

## 证据边界

以上支持存在性结论：并非所有Client都需要动态表达请求接口全部字段。尚未形成全库可裁剪率，不声称固定字段均可无条件删除。没有修改原软件、配置、IDL或执行编译与目标测试。输入SHA-256与候选清单保存在同目录JSON。
