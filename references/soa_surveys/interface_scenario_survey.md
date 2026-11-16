# Client实际使用场景与Event+FF归一评估

日期：2026-11-02。结论：有条件通过。现有MCU样本支持以Event+FF作为默认内部接口形态；按实际业务依赖保留查询和事务型例外。不能按平台RPC类型机械转换。

## 统计方法与范围

扫描VDF/ZONE的669个C文件（该库无.cpp），140个模块目录存在匹配到的Client操作。操作按模块目录+端点（含实例）+操作去重；不把同一RR的响应读取再次计入入口操作总数。平台IDL匹配基于模块本地Proto。另定性抽查MPU参考CabinHumEthMgr。

| 操作 | 去重语法项 | 所有调用点均位于字面false分支的项 | 排除这些项后 |
|---|---:|---:|---:|
| 通知读取（Event或Field Notify） | 1246 | 0 | 1246 |
| FF请求发送 | 357 | 4 | 353 |
| Field Set发送 | 39 | 0 | 39 |
| RR请求发送 | 380 | 15 | 365 |
| Field Get发送 | 60 | 30 | 30 |
| 合计 | 2082 | 49 | 2033 |

通知、FF与Set合计1638/2033=80.6%；这是单向操作形态的占比，支持默认路线，不能当作已证明可无损转换率、CPU流量比例或全公司软件比例。未排除字面false分支时为1642/2082=78.9%。宏条件未解析，故2033不应称作已证明可达操作数。

通知读取的1246项中，1238可匹配本地IDL：696 EVENT、476 FIELD_READONLY、66 FIELD_WRITABLE，8项未匹配。357 FF中356匹配；380 RR中374匹配且返回非Null；60 Get均匹配（59 RO、1 RO_NOSUB）；39 Set均匹配（30 RW、9 RW_NOSUB）。未匹配项保留未知，不依猜测补全。

## 1. 状态消费：周期读缓存与回调写缓存

AmbLiMgr的IfCommInfo先调用sm_read_on_notify，成功后写DW缓存，业务周期任务再读信号；BDYmanSwtSeatApp在on_notify回调更新缓存。应用只需要最新有效状态时，两者均可由内部Event提供，不要求改变原业务执行线程。必须保留首次有效值、freshness、连接/E2E状态和数据交付策略。
证据：[AmbLiMgr](/home/shaun/soa_adaptor/Reference/AmbLiMgr/src/AmbLiMgr.c:9020)；[回调式消费](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/src/BDYmanSwtSeatApp.c:178)。

## 2. 单向控制：FF与Field Set

CRSDriveModeMgr.ReqPenHvac属于业务意图发送，业务不等待专属返回值；内部FF传业务字段，Adaptor补齐固定项并保持平台FF。Field Set在当前API中同样是单向写，可映射内部FF，但其订阅、Notify状态和失败上报仍需单独保留，不能将Set当成RR成功确认。
证据：[ReqPenHvac](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSDriveModeMgr/src/CRSDriveModeMgr.c:2763)；[MCU Set规范](/home/shaun/soa_adaptor/SOA_API/MCU_SOA_Glue_Code_C_API.md:358)。

## 3. 平台RR但未发现业务消费响应：内部FF候选

380个RR请求端点中370有对应响应读取。370个响应端点中349可通过简单赋值追踪reply_msg/error_code到缓存；其中329未发现这些缓存符号的其他直接C源码引用。21项未被该追踪模式覆盖，另20项至少存在负载或错误缓存的其他引用。这里不是自动删除结论，也不是继承现有异常处理缺失。

BDYmanSwtSeatApp四个ReqSeatAdjEndur请求的回调将reply_msg/error_code写入DW，所提供C源码中未发现后续直接引用；SeatMoveMgr_FL的目标位置/自学习RR也出现此模式。可评估内部FF，由Adaptor继续执行平台RR并消费响应、处理超时、上报必要通信状态。原Server仍收到RR，不把Adaptor接收成功当作Server执行成功。
证据：[座椅开关响应](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/BDYmanSwtSeatApp/src/BDYmanSwtSeatApp.c:202)；[SeatMoveMgr_FL响应](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/SeatMoveMgr_FL/src/SeatMoveMgr_FL.c:240)。

## 4. Get只是初始化/刷新：可评估移入Adaptor

SeatMoveMgr_FL的显式Get位于if(false)，不能当成实际主动查询需求。SeatMoveMgr_RL在Initialize Function中按SEATMGR_RL_FIELD_TRIGGER发起Get，且已有Notify回调；这类首次填充/订阅建立可由Adaptor承担，再给应用发送首个有效快照。宏值不在本模块材料中，不能认定其启用或禁用。若应用要求本次查询的专属结果，则不能用任意旧缓存替代。
证据：[FL关闭的Get](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/SeatMoveMgr_FL/src/SeatMoveMgr_FL.c:6123)；[RL初始化Get](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/SeatMoveMgr_RL/src/SeatMoveMgr_RL.c:8507)；[RL通知](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/SeatMoveMgr_RL/src/SeatMoveMgr_RL.c:1231)。

## 5. 主动获取配置数据：查询例外需保留

MOTlsv对Imu.GetLeverArm（RO_NOSUB）显式发Get并消费offset_x/y/z与rotation等响应字段。业务可能只要一份刷新后的外参快照，适合进一步评估由Adaptor获取后Event发布；但该接口无Notify，无法直接改成订阅。获取时机、刷新周期和新鲜度未确认前，保留查询机制或显式Query FF+专属Result Event。
证据：[获取请求](/home/shaun/projects/ai-demo/service_arch/soa_deployment/ZONE/Motion_Longitudinal_Service_CETUS_Code-V37_Zone_RL250_BL157/LogicService/MOTlsv/src/MOTlsv.c:43800)；[实际消费响应字段](/home/shaun/projects/ai-demo/service_arch/soa_deployment/ZONE/Motion_Longitudinal_Service_CETUS_Code-V37_Zone_RL250_BL157/LogicService/MOTlsv/src/MOTlsv.c:43830)。

## 6. 请求结果参与状态机：必须保留事务语义

OdoInfoMgr.CloudServiceReq实际检查ack_code和error_code，推进成功/失败状态并保存response.request_id；CRSSmtKeyPosnNmCtrl.RequestBta/Adf等把result与错误码用于计数和READY/FAIL状态。CbnFrdgMgr.EfuseStatusInquiry也实际消费诊断查询结果。它们不能简化为只发FF且吞掉响应。可以保留内部RR；若选择FF+Result Event，则必须实现请求关联、结果投递、超时/并发/迟到结果，语义并未因此简化。
证据：[里程云请求结果](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/OdoInfoMgr/src/OdoInfoMgr.c:536)；[网络唤醒结果判定](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CRSSmtKeyPosnNmCtrl/src/CRSSmtKeyPosnNmCtrl.c:100)；[Efuse结果](/home/shaun/projects/ai-demo/service_arch/soa_deployment/VDF/CbnFrdgMgr/src/CbnFrdgMgr.c:1613)。

## 7. MPU定性抽查

CabinHumEthMgr在100ms任务内ReadTempSts并转换到本地缓存，后续读取in_car_val，符合周期消费状态的模式。这支持同类设计思路，但单个MPU样例不参与MCU量化比例，也不能推出MPU全部调用可简化。
证据：[CabinHumEthMgr](/home/shaun/soa_adaptor/Reference/CabinHumEthMgr/src/CabinHumEthMgr.cpp:531)。

## 设计结论

1. 默认状态通道使用Event，默认命令通道使用FF，符合当前样本主要形态。
2. 平台接口类型只决定Adaptor外侧实现；内部类型由该Client对结果、时效和事务的真实依赖决定。
3. 对RR未用响应、Get仅用于首次填充的场景，允许按需简化，但逐项确认失败处理和初始化语义，不能只按“生成了缓存”判断。
4. 结果状态机、查询返回、请求关联是明确例外；保留RR/Get，或显式配置带关联的FF+Event协议，不把协议搬家误当作语义消失。
5. Event消费保持可选择周期读缓存或调度事件触发；不能统一把业务逻辑放进通信回调。
6. 下一阶段映射表至少包含：平台RPC和实际操作、响应负载/错误依赖、初始化/刷新需求、内部Event/FF/RR/Get选择、首值/队列/E2E/超时策略和验证用例。

## 验证边界

对操作计数、RR/Get配对、IDL类别和关键样例做静态交叉核查。未修改源库，未执行编译/目标测试。未进行完整AST、宏展开、指针别名、反射/诊断读取或时序验证。所有“未发现后续引用”只作为人工评审候选。源码位置、候选追踪结果及输入SHA-256存于同目录JSON。
