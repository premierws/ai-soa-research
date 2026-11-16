# 服务架构矩阵

## 工作界面

<whiteboard token="OAduwg4qPhjJ6ib9pgKcuGlUned"/>

## 运作流程

<whiteboard token="Mnfxw7azBhVNlKb24RpcW8DInRc"/>

# 技术规划概览

<whiteboard token="XnwmwcMashruH0bE7t0clInmnVd"/>

# 详细技术规划

<lark-table rows="14" cols="8" header-row="true" header-column="true" column-widths="76,106,266,130,272,203,100,149">

  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      分类
    </lark-td>
    <lark-td>
      现状及痛点
    </lark-td>
    <lark-td>
      专项攻关
    </lark-td>
    <lark-td>
      攻关收益
    </lark-td>
    <lark-td>
      前瞻技术研究
    </lark-td>
    <lark-td>
      时间计划
    </lark-td>
    <lark-td>
      所属BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="4">
      发现问题
    </lark-td>
    <lark-td>
      SOA资源占用
    </lark-td>
    <lark-td>
      1. 同一个功能系统的不同服务软件，存在若干重复的服务接口调用，造成可观的存储资源和CPU性能开销
    </lark-td>
    <lark-td>
      优化SOA整体（应用+SkyOS）资源占用
    </lark-td>
    <lark-td>
      - 消除部署在同一个MCU上的重复服务接口调用
			- 降低SOA存储资源和CPU性能开销
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      DLT
    </lark-td>
    <lark-td>
      2. 排查问题所需的关键时刻DLT信息缺失；DLT无序使用引起VDF等ECU频繁抱怨；部分可替代代价更高的上云数据
    </lark-td>
    <lark-td>
      管控治理应用软件DLT
    </lark-td>
    <lark-td>
      - 提升问题排查效率
			- 降低DLT的CPU占用
			- 减少上云流量费用
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC基础功能子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      平台型服务
    </lark-td>
    <lark-td>
      4. PNC、Vehicle config、Dtc等平台型服务与业务功能密切相关，但其变更经常没有与所有相关方进行评审和影响评估，导致应用软件返工或功能异常
    </lark-td>
    <lark-td>
      统一管理平台型服务
    </lark-td>
    <lark-td>
      - 评估平台型服务变更对业务的影响
			- 规避不合理的服务变更
			- 确保SOA优化方案实施的一致性
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      S2S
    </lark-td>
    <lark-td>
      3. S2S仍存在初始值、validity等影响功能的关键问题，另外由于原子服务与逻辑服务/APP异地部署，造成TOX资源开销
    </lark-td>
    <lark-td>
      优化S2S实现和部署方案
    </lark-td>
    <lark-td>
      - 规避S2S软件实现引起的问题bug
			- 支持ZONE MCU降本等VAVE方案
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年12月
    </lark-td>
    <lark-td>
      DE：Jerry.JIN
      COME&AS：伍锦
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="4">
      提升效率
    </lark-td>
    <lark-td>
      SDS
    </lark-td>
    <lark-td>
      7. 原子服务内容简单，但因数量较多，每个原子服务维护一份，人均SDS维护量大、效率低
    </lark-td>
    <lark-td>
      合并优化原子服务SDS
    </lark-td>
    <lark-td>
      - 减少SDS维护工作量
			- 提高版本迭代效率，节省人时
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      服务架构看板
    </lark-td>
    <lark-td>
      8. 没有实时服务架构信息，缺乏服务架构每天的演进信息；
    </lark-td>
    <lark-td>
      SOA服务、服务接口监控
    </lark-td>
    <lark-td>
      - 通过对各版本SOA服务及接口的监控逐步形成VMBC服务架构信息基线
			- 通过网页上“监控-度量-看护”的方式形成SOA服务架构信息的看板大屏；
			- 帮助大家了解服务架构实时状态支持后续服务架构需求合入；
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      服务测试
    </lark-td>
    <lark-td>
      5. 服务连通性、响应性、性能（通信、启动时延等）、稳定性等问题在VAS内部缺乏闭环，引起功能bug后再进行排查，周期长、效率低
    </lark-td>
    <lark-td>
      建立服务架构闭环测试能力
    </lark-td>
    <lark-td>
      - 降低SOA定义/配置等问题的流出率
			- 避免因SOA定义、配置、部署等问题引起功能bug
			- 减少问题bug排查定位人时
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年12月
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SOA代码开发
    </lark-td>
    <lark-td>
      6. SOA通信框架代码由SWE基于模型开发，理解成本高，易出现重复错误，架构优化方案落地拉通工作量大，易遗漏
    </lark-td>
    <lark-td>
      提升SOA框架代码开发效率
    </lark-td>
    <lark-td>
      - 应用软件不需要适配SOA框架的变更
			- 软件逻辑和SOA框架可进行单独测试，提高软件质量
			- 进行SOA接口合并，可节省资源
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年12月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="2">
      拓展业务
    </lark-td>
    <lark-td>
      A核部署
    </lark-td>
    <lark-td>
      9. 由于SkyOS在MCU和MPU侧SOA功能实现的差异，使得VAS应用软件移植至A核，无法得到同样的功能和性能表现
    </lark-td>
    <lark-td>
      服务软件无缝迁移至VDF-ACore
    </lark-td>
    <lark-td>
      - 实现VAS软件在VDF A核的灵活部署
			- 避免因SOA实现的差异，引入软件变更工作量
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      信号路由
    </lark-td>
    <lark-td>
      10. 随着越来越多的业务上移A核，结合ZONE降本需求，考虑部分原子服务上移至VDF-M/A，需要考虑实现信号的上下行路由
    </lark-td>
    <lark-td>
      支持S2S软件上移的信号路由方案
    </lark-td>
    <lark-td>
      - 支持S2S原子服务灵活部署
			- 支持ZONE MCU降本
			- 减少同一功能系统的SOA流量
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      精神面貌
    </lark-td>
    <lark-td>
      技术导向业务驱动
    </lark-td>
    <lark-td>
      历史技术债务累积；服务通信开销比较大（在VDF A核上）；
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="2">
      持续领先
    </lark-td>
    <lark-td>
      AI+SOA
    </lark-td>
    <lark-td>
      10. SOA问题分析定位通常人力、资源消耗较大，同时问题分析和潜在失效风险预测缺乏确定性的规则
			1. AI Cabin/AI Motion对于轻量化训练模型在端侧（嵌入式系统）部署的需求，对于训练数据的要求，可能会不同于当前的SOA数据提供方式（高频周期或低频onchange等），需要针对嵌入式AI模型的数据需求进行匹配
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      SOA异常检测与分析：
      基于时序数据的AI模型（如LSTM+Attention）可实时监测服务调用链异常，定位故障源（如以太网延迟激增或某个ECU服务超时），并触发备份服务或降级策略
    </lark-td>
    <lark-td>
      26年
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      灵活部署
    </lark-td>
    <lark-td>
      12. 按功能融合趋势发展，灯光、座椅、空调等车身功能的仲裁、决策可就近部署至CDF；NAD相关的横向、纵向控制功能的仲裁、决策可就近部署至ADF。以尽可能实现ZONE MCU降级、VDF SOC降本、减少SOA通信
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      服务软件在CDF、ADF等的灵活部署：
      识别CDF、ADF在SOA框架能力上的差异点，推进SkyOS、CDF、ADF等相关方进行能力适配
    </lark-td>
    <lark-td>
      26年
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
</lark-table>

<lark-table rows="5" cols="8" header-row="true" header-column="true" column-widths="76,106,266,130,272,203,100,149">

  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      分类
    </lark-td>
    <lark-td>
      现状及痛点
    </lark-td>
    <lark-td>
      专项攻关
    </lark-td>
    <lark-td>
      攻关收益
    </lark-td>
    <lark-td>
      前瞻技术研究
    </lark-td>
    <lark-td>
      时间计划
    </lark-td>
    <lark-td>
      所属BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      发现问题
    </lark-td>
    <lark-td>
      SOA资源占用
    </lark-td>
    <lark-td>
      1. 同一个功能系统的不同服务软件，存在若干重复的服务接口调用，造成可观的存储资源和CPU性能开销
    </lark-td>
    <lark-td>
      优化SOA整体（应用+SkyOS）资源占用
    </lark-td>
    <lark-td>
      - 消除部署在同一个MCU上的重复服务接口调用
			- 降低SOA存储资源和CPU性能开销
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      SOA代码开发
    </lark-td>
    <lark-td>
      6. SOA通信框架代码由SWE基于模型开发，理解成本高，易出现重复错误，架构优化方案落地拉通工作量大，易遗漏
    </lark-td>
    <lark-td>
      提升SOA框架代码开发效率
    </lark-td>
    <lark-td>
      - 应用软件不需要适配SOA框架的变更
			- 软件逻辑和SOA框架可进行单独测试，提高软件质量
			- 进行SOA接口合并，可节省资源
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年12月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="2">
      拓展业务
    </lark-td>
    <lark-td>
      A核部署
    </lark-td>
    <lark-td>
      9. 由于SkyOS在MCU和MPU侧SOA功能实现的差异，使得VAS应用软件移植至A核，无法得到同样的功能和性能表现
    </lark-td>
    <lark-td>
      服务软件无缝迁移至VDF-ACore
    </lark-td>
    <lark-td>
      - 实现VAS软件在VDF A核的灵活部署
			- 避免因SOA实现的差异，引入软件变更工作量
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      信号路由
    </lark-td>
    <lark-td>
      10. 随着越来越多的业务上移A核，结合ZONE降本需求，考虑部分原子服务上移至VDF-M/A，需要考虑实现信号的上下行路由
    </lark-td>
    <lark-td>
      支持S2S软件上移的信号路由方案
    </lark-td>
    <lark-td>
      - 支持S2S原子服务灵活部署
			- 支持ZONE MCU降本
			- 减少同一功能系统的SOA流量
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      2025年9月
    </lark-td>
    <lark-td>
      VMBC算力子系统BU
    </lark-td>
  </lark-tr>
</lark-table>

# 2025年6-9月VAU

### V1：识别业务服务的关键问题，制定方案并跟踪闭环

#### A1：

通过服务代理、依赖项合并等措施进一步优化VMBC业务服务化引入的ECU资源占用，单client优化RAM 28bytes，优化Flash 1KB以上，同时确保业务功能不降级 <text bgcolor="light-yellow">**@软件架构矩阵**</text><text bgcolor="light-yellow">** **</text><text bgcolor="light-yellow">**<mention-user id="ou_0ed39e4c2b8ef8fdaebeef34bb41a2ea"/>**</text>

- 初步讨论
	- 应用层优化：优化资源占用，优化效果大，涉及业务修改
	- skyos优化：优化流量、服务启动阶段的蜂拥，优化效果小，不涉及业务修改
- 2025/6/25：
	- 已经纳入ZONE降387的系统优化方案，因涉及业务软件变更，当前优先级较低，8/13的387软件包不包含此优化 <mention-doc token="UYpRdE4tPo9MrvxYd9hcvNeunbd" type="docx">Q3V1A1-服务架构优化(服务合并) V1.0</mention-doc>
	- 在SOA战队，形成了一个方案决策，由SkyOS的tox团队，在MCU/MPU侧进行client的整体合并，可以接近应用层优化的效果<mention-doc token="RSDZdHCoOo0pfFxBqqhctLQgnGb" type="docx">对"Client去重方案"OKTG的决策</mention-doc>
  第一次讨论结论：按skyos的tox优化方案推进
- 2025/7/23：
	- SkyOS更新了交付节点，计划在V02.02.08交付；
- 2025/8/8：
	- SkyOS优先级调整，在MCU降本方案实施后再评估收益；

#### A2：

制定DLT平台化管理方案，管控VMBC业务DLT使用，SOA问题定位时间减少1人天，SOA error数据上云减少4万条/车/天 <text bgcolor="light-yellow">**@系统架构矩阵**</text><text bgcolor="light-yellow">**<mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/>**</text>

- 2025/6/25：
	- 已经上过SkyOS的CCB，但需要有明确的code，skyos才开始实施
- 2025/7/23：
	- 目前还没有明确由哪个BU CODE支持实施
	- 在7月底前再沟通协调
- 2025/8/8：
	- skyos已经实施并释放，接下来3季度完成应用软件DLT管控

#### A3：

建立平台型服务统一管理平台，管控并评估服务变更影响范围，提升变更效率，规避变更引入的问题 <text bgcolor="light-yellow">**<mention-user id="ou_1d5398622291e193775c4f26c8d9a2e9"/>**</text><text bgcolor="light-yellow">** **</text><text bgcolor="light-yellow">**<mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/>**</text>

- 2025/6/25：
	- 全部平台服务都已经纳入NDTC平台管理，管理效率

### V2：识别业务服务交付过程低效点，制定提效方案并跟踪闭环

#### A1：

在RL240（DRACO PP1），梳理原子服务设计现状，按功能系统进行原子服务聚合，减少SDS文档数量，提升原子服务更新维护效率 <text bgcolor="light-yellow">**@系统架构矩阵**</text><text bgcolor="light-yellow">**<mention-user id="ou_d5b7df716ff0b2d60f41250ab32ca5a1"/>**</text>

- 2025/6/25：
	- 基于座椅系统形成了初步服务合并分析，下一步跟SO沟通是否可行<mention-doc token="DL8ididdzoI01Ex3DxzcTph4nEd" type="docx">服务SDS整合 - 座椅（示例）</mention-doc>
- 2025/7/23：
	- 针对body和seat当前FDS/SDS中存在功能逻辑描述不完整、分散等问题进行了梳理
	- 针对seat系统，计划对FDS整改，方向是在FDS里完整的描述子系统需求和功能，逻辑服务SDS主要定义服务接口和参数
	- seat座椅SDS整改版本，预计8月15前形成初版
- 2025/8/8：
	- 已经形成方案proposal，并在服务架构矩阵和系统架构矩阵征求意见<mention-doc token="HFcjdgozDoNSPLx2Gowc3bU3nPc" type="docx">SDS和FDS文档优化方案</mention-doc>

#### A2：

在VEDAP建立服务架构数据看板，按平台、车型版本进行自动更新维护，为服务架构优化治理提供数据基础 <text bgcolor="light-yellow">**<mention-user id="ou_3717a60d1741746c7cecb8b6f908336c"/>**</text><text bgcolor="light-yellow">** **</text><text bgcolor="light-yellow">**<mention-user id="ou_0ed39e4c2b8ef8fdaebeef34bb41a2ea"/>**</text>

- 2025/6/25：
	- 已形成初步方案 
- 2025/7/9：
	- <mention-doc token="RDPcdeF16oEt0Nxf4Syc2RJinCc" type="docx">Q3V2A2-服务架构数据看板搭建V1.0</mention-doc> 初稿完成，下一步与 达宸 讨论对齐；
- 2025/7/23：
	- 已经与<mention-user id="ou_3717a60d1741746c7cecb8b6f908336c"/>沟通需求，预计8月上旬能够有资源支持开发
- 2025/8/8：
	- 已经与 达宸 确定时间，8月11日下午15:00会和 达宸、杜勇、李俊帅 对齐需求；

#### A3：

完善各ECU节点服务连通性、响应性测试能力，初步具备SOA性能（通信、启动时延等）、稳定性等测试能力，降低SOA问题流出率，减少问题排查人时 <text bgcolor="light-yellow">**<mention-user id="ou_a57a9a3fbd93271ae385965a9f503c02"/>**</text><text bgcolor="light-yellow">**<mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/>**</text>

- 2025/6/25：
	- 已完成服务架构测试项梳理<mention-doc token="TJlkdstO2ojsKjxdnvsce9wen4e" type="docx">服务架构测试需求</mention-doc>
	- 下一步进行测试用例编写
- 2025/7/23：
	- https://jira.nioint.com/browse/NT3VIMS-58557
	- 已经建票开始实施
- 2025/8/8：
	- P0优先级的测试能力已经构建完成

### V3：关键技术能力积累提升

#### A1：

制定MPU侧VMBC服务架构方案，跟踪SkyOS优化A核SOA技术底座，目标是业务软件迁移A核后，SOA性能无明显降级 <text bgcolor="light-yellow">**@SOA架构战队**</text><text bgcolor="light-yellow">**<mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/>**</text>

- 2025/6/25：
	- SOA战队A核部署正常推进中
- 2025/7/23：
	- A核当前采用hypervisor+skyos_L的实现方案，SOA架构层面与MCU实现机制一致
	- 但是由于A核上SOA通信无法独占核，可能会带来通信时延和吞吐量性能的降级
- 2025/8/8：
	- 因平台整体方案调整，需评估soa lite技术方案的可行性及对VMBC业务的影响

#### A2：

制定S2S原子服务上移技术方案，明确S2S原子服务可上移范围，推动SkyOS优化ETH PDU等技术底座，实现S2S原子服务灵活部署，支持ZONE MCU降本 <text bgcolor="light-yellow">**@系统架构矩阵 @软件架构矩阵 @SOA架构战队**</text><text bgcolor="light-yellow">**<mention-user id="ou_d5b7df716ff0b2d60f41250ab32ca5a1"/>**</text>

- 2025/6/25：
	- 在ZONE MCU降本BU推进，第一阶段以方案分析为主，实施优先级较低
- 2025/7/23：
	- 服务架构矩阵方案分析工作已完成并交付给算力BU
	- 接下来算力BU会基于方案与DA&SKYOS确认具体实施方案和功能性能需求
- 2025/8/8：
	- 作为ZONE MCU降本储备方案继续跟进细化

# 2025年Q3 VAU

### V1：识别业务服务的关键问题，制定解决方案并跟踪闭环

#### A1：

提升端到端问题分析能力，解决CETUS量产前后休眠唤醒等场景下由SOA通信导致的P1、P2功能bug ≥ 5项，制定VMBC平台通用方案，在各系统BU横展后，完成问题闭环 <mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/><mention-user id="ou_1d5398622291e193775c4f26c8d9a2e9"/>

#### A2：

梳理VMBC应用软件中SOA数据接收、数据初始化、QoS配置、Error handling等薄弱点，制定统一的平台化方案≥5项，协同效能工具团队，完成方案落地实施 <mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/><mention-user id="ou_8f05c67f61516607d74df3219024dd0d"/>

#### A3：

持续完善服务架构规范，在此基础上，优化AI Cabin、表显里程等服务架构方案≥5项，管控IDL变更，每个大版本服务变更量最大不超过5% <mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/><mention-user id="ou_d5b7df716ff0b2d60f41250ab32ca5a1"/><mention-user id="ou_0ed39e4c2b8ef8fdaebeef34bb41a2ea"/>

### V2：识别业务服务交付过程低效点，制定提效方案并跟踪闭环

#### A1：

在RL240（DRACO PP1），梳理逻辑+原子服务设计现状，按功能系统进行服务SDS文档治理，优化SDS文档内容及结构，提升SDS文档可读性及更新维护效率 <mention-user id="ou_d5b7df716ff0b2d60f41250ab32ca5a1"/>

#### A2：

在VEDAP建立服务架构数据看板，按平台、车型版本进行自动更新维护，为服务架构优化治理提供数据基础 <mention-user id="ou_0ed39e4c2b8ef8fdaebeef34bb41a2ea"/><mention-user id="ou_3717a60d1741746c7cecb8b6f908336c"/>

#### A3：

建立VMBC服务架构测试闭环能力，覆盖服务连通性、响应性、SOA性能（通信、启动时延等）、稳定性等测试项，降低SOA问题流出率，减少问题排查人时 <mention-user id="ou_a57a9a3fbd93271ae385965a9f503c02"/><mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/>

### V3：服务架构矩阵关键技术能力积累提升

#### A1：

制定VM-L平台VMBC服务架构方案，确保VM-L SOA基础功能性能满足业务功能需求，目标是业务软件迁移VM-L后，SOA功能性能无降级 <mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/><mention-user id="ou_e270895783ea3754bd16433af7a259f6"/>

#### A2：

细化S2S原子服务上移技术方案，确定S2S原子服务可上移范围，推动SkyOS优化ETH PDU等技术底座，实现S2S原子服务灵活部署，支持ZONE MCU降本 <mention-user id="ou_d5b7df716ff0b2d60f41250ab32ca5a1"/><mention-user id="ou_0ed39e4c2b8ef8fdaebeef34bb41a2ea"/>

#### A3：

Entry&NPF平台SOA lite方案技术评估，确保其功能、性能（时延、丢包、吞吐量等）满足VMBC业务需求 <mention-user id="ou_1b7654f99b3ce7d6e5c7b0a84ee09dfb"/><mention-user id="ou_f37979ece84a7496945677c6ccfc3bf1"/>

SOA技术限制和规范
