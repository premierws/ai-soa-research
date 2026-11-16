<callout emoji="loudspeaker" background-color="light-orange" border-color="light-orange">

- 本文档范围为VCC(Vehicle cabin control)功能的架构设计，<text underline="true">依赖系统能力实现端到端，一般不提供标准能力</text>。
- 从功能、性能要求出发，转化功能实现方案。以系统能力划分章节。
- 由FA撰写，与FO\SO握手架构设计。成为功能设计FDS，服务架构，软件架构的上游输出。
</callout>

# Document statement

## Change History
<lark-table rows="2" cols="4" header-row="true" column-widths="79,116,100,645">

  <lark-tr>
    <lark-td>
      Version
    </lark-td>
    <lark-td>
      Date
    </lark-td>
    <lark-td>
      Author
    </lark-td>
    <lark-td>
      Changes
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      0.0.1
    </lark-td>
    <lark-td>
      2026.08.25
    </lark-td>
    <lark-td>
      <mention-user id="ou_64ff4a7680642ca2fac4e21c692db4d0"/>
      <mention-user id="ou_2d9b1f7a324e67b7ea8156ae8e434fd9"/>
      <mention-user id="ou_f4283abfa902e705e981e9f67ddc3047"/>
      <mention-user id="ou_f6732dea6030f0a4ac85641723a029a7"/>
    </lark-td>
    <lark-td>
      初始版本
    </lark-td>
  </lark-tr>
</lark-table>

## Confidentiality

本文件受版权保护，所有权利均由蔚来保留。未经蔚来事先书面同意，不得全部或部分复制、影印或翻译本文件。本文件包含专有信息，未经蔚来事先书面同意，不得使用或向第三方披露。

This document is copyrighted, and all rights are reserved by NIO. This document may not, in whole or in part, be copied, photocopied, or translated without the prior written consent of NIO. This document contains proprietary information which is not to be used or brought to the knowledge of a third part without the prior written consent of NIO.

## Function List

## Review Record

## Summary Architecture

refer：

<mention-doc token="KBS7wWT6Qi3ThTkdpLVcjAbAnfY" type="wiki">02 NT3.5_VMBC Intelligent Function Architecture_0.0.4</mention-doc>

<mention-doc token="Vk5lwrCrsiDjIykcSXjc8SQ5nwc" type="wiki">VCC｜以 NCM 为技术底座的车端 Cabin Brain V1</mention-doc>

<quote-container>

**VCC 功能架构总览**

参照如下思路来规划 VCC 的功能架构

<image token="DRvIb7pbNo5S3BxreQTc2BCvnjc" width="1018" height="573" align="center"/>

</quote-container>

<whiteboard token="TSW3wGr8Khs4Ecb3N1tcgoljntY" width="820" height="313"/>

# Introduction

## Purpose

本文档从各系统的功能性能要求出发，转化架构要求，内容覆盖物理架构、功能分配和动态架构分析。

This document describes the VMBC function architecture of NT3.5 application project, including function list, function allocation diagram.

## Reference

## Scope

<lark-table rows="4" cols="3" header-row="true" column-widths="100,278,100">

  <lark-tr>
    <lark-td>
      Platform
    </lark-td>
    <lark-td>
      Project
    </lark-td>
    <lark-td>
      备注
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Entry
    </lark-td>
    <lark-td>
      Qinling（PRO/MAX）
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Entry+
    </lark-td>
    <lark-td>
      Qinling（ULTRA）
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Medium
    </lark-td>
    <lark-td>
      Pisces
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
</lark-table>

## Glossary

<lark-table rows="4" cols="2" header-row="true" column-widths="100,481">

  <lark-tr>
    <lark-td>
      Acronym
    </lark-td>
    <lark-td>
      Description
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
</lark-table>

# Function Architecture Diagram

## 3.0 VCC 场景对4项 KSF 的需求

<mention-doc token="DMSPwcx8aispt2kntvHcN2zNn8f" type="wiki">大body VCC 规划</mention-doc>

## Group-01 VCC-Lighting <mention-user id="ou_a49130a65b4e62a0a7779d18acb5b31c"/>

<whiteboard token="Sb3zwZx2ZhJ4r3bKsOSclmnWn6d"/>

## Group-02 VCC-Hvac <mention-user id="ou_497f5797e3df80f5346707af48ae07e3"/>

<mention-doc token="OwbHwRZ4Ui6HzHkSkB6cADoknwf" type="wiki">VCC_HAVC V0.1</mention-doc>

<whiteboard token="LVUiwKUA1hNDecbYKXOcWsa6nTe"/>

功能场景列表

<lark-table rows="14" cols="7" header-row="true" column-widths="94,132,210,203,197,145,223">

  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      **功能场景**
    </lark-td>
    <lark-td>
      **感知源（上游）**
    </lark-td>
    <lark-td>
      **座舱状态感知**
    </lark-td>
    <lark-td>
      **场景/意图识别**
    </lark-td>
    <lark-td>
      **任务**
    </lark-td>
    <lark-td>
      **规划&执行涉及系统（下游）**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      阳光直射场景
    </lark-td>
    <lark-td>
      - OMS乘客光斑
			- 日照强度
			- 乘员占位
			- 外界环境（隧道/地库/林荫/.....）
    </lark-td>
    <lark-td>
      - 热舒适
    </lark-td>
    <lark-td>
      局部阳光直射下热舒适需求
    </lark-td>
    <lark-td>
      联动电动出发口，进行局部精准送风
    </lark-td>
    <lark-td>
      - <text color="red">空调</text>
			- 电动出风口
			- <text color="red">遮阳帘</text>
			- <text color="red">变色玻璃</text>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      占位智能启停
      （离座/回座/沙发床/后排）
    </lark-td>
    <lark-td>
      - 乘员占位+类型（OMS）
			- 座椅位置（沙发床）
			- 门状态
    </lark-td>
    <lark-td>
      - 空间：占位/姿态
    </lark-td>
    <lark-td>
      离座/回座/沙发床切换/后排有人上车
    </lark-td>
    <lark-td>
      触发座椅通风加热/方向盘/后排空调智能启停任务
    </lark-td>
    <lark-td>
      - 座椅通风加热
			- 方向盘加热
			- 空调（后排开关）
			- 空调（单系模式）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      空间干涉避让
      （冰箱门/二排出风口与座椅）
    </lark-td>
    <lark-td>
      - 2排滑轨位置
			- 腿托长度/倾角
			- 座椅滑移进行中
			- 保险箱开闭
			- 占位
    </lark-td>
    <lark-td>
      - 空间：舱内几何关系
    </lark-td>
    <lark-td>
      座椅调节/开门取物/沙发床展开
    </lark-td>
    <lark-td>
      触发干涉避让任务（限冰箱门开度/出风口随动/随动关闭）
    </lark-td>
    <lark-td>
      - 冰箱（门开度）
			- 二排电动出风口
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      整车热舒适调节
      (Hot Start/Cold Start）
    </lark-td>
    <lark-td>
      - 外界场景（隧道/地库/......）
			- 人群画像（年龄/性别/老弱病残/......）
			- 车内温度
			- 环境温度
			- 日照强度
			- 乘员占位
			- HVAC运行状态
    </lark-td>
    <lark-td>
      - 热舒适：内温/环温/日照/占位融合为整舱分区热舒适状态
    </lark-td>
    <lark-td>
      多乘员差异化热舒适需求（常态行车/快速降温/静音）
    </lark-td>
    <lark-td>
      生成并下发整舱热舒适目标（分区温度、风量、出风、座椅/方向盘档位）
    </lark-td>
    <lark-td>
      - 空调+电动出风口
			- 座椅通风加热
			- 方向盘加热
			- <text color="gray">遮阳帘</text>
			- <text color="gray">隐私玻璃</text>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      预冷/预热预处理 + 快速升降温联动
    </lark-td>
    <lark-td>
      - APP远程请求
			- 钥匙遥感
			- 环温/内温/日照
			- 电量SOC
			- MaxHeat/MaxCool状态
			- PNC
    </lark-td>
    <lark-td>
      - 热舒适：内温/环温/日照
			- 安全：电量约束
    </lark-td>
    <lark-td>
      远程/预约/遥感上车预处理；极冷最大加热/暴晒最大降温；低电量降级
    </lark-td>
    <lark-td>
      触发预处理任务（空调+座椅3档+方向盘2档+冰箱快速温控联动）
    </lark-td>
    <lark-td>
      - 空调+电动出风口
			- 座椅通风加热
			- 方向盘加热
			- 冰箱
			- HLV
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      ECO+/ECO 节能仲裁
    </lark-td>
    <lark-td>
      - DriveModeMgr.EcoPlusModeInfo
    </lark-td>
    <lark-td>
      - 安全：能耗
    </lark-td>
    <lark-td>
      用户开启超级节能
    </lark-td>
    <lark-td>
      关AC及联动功能、座椅通风加热Auto Off、关香氛、限鼓风机、空调单席
    </lark-td>
    <lark-td>
      - 空调+电动出风口
			- 座椅热管理
			- 香氛
			- 冰箱
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      换电
    </lark-td>
    <lark-td>
      - veh_state_detailed
			- operator_state
			- power swap
    </lark-td>
    <lark-td>
      - 安全：整车状态机
    </lark-td>
    <lark-td>
      换电/SWUpdate/上下电
    </lark-td>
    <lark-td>
      关AC限风量、座椅加热Auto Off、冰箱关闭断电、退出恢复
    </lark-td>
    <lark-td>
      - 空调
			- 座椅热管理
			- 冰箱
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      自动除雾/除霜
    </lark-td>
    <lark-td>
      - 湿度+玻璃温度+露点
			- 环温
			- 外界场景模式（雨/雪/雾）
			- 雨刮状态
			- 占位状态
    </lark-td>
    <lark-td>
      - 安全：视野（起雾风险）
			- 热舒适：温湿度
    </lark-td>
    <lark-td>
      起雾风险/低温结霜/洗车·雨天
    </lark-td>
    <lark-td>
      触发自动除雾任务（前挡/后挡+加热丝+雨刮联动）
    </lark-td>
    <lark-td>
      - 空调（除雾/除霜）
			- 加热丝
			- 雨刮
			- 车窗
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      自动空气净化（PM2.5/AQS尾气防护/CO2通风）
    </lark-td>
    <lark-td>
      - 外界环境（扬尘/雾霾/...）
			- AQS等级
			- PM2.5
			- CO2（虚拟）
			- 车窗开度
			- 门/尾门
			- 车速
			- 新风量
    </lark-td>
    <lark-td>
      - 空气质量：空气新鲜度/整车环境
    </lark-td>
    <lark-td>
      空气差/尾气/隧道拥堵/CO2超标
    </lark-td>
    <lark-td>
      触发净化任务（内外循环+净化+风量+弹窗问询）
    </lark-td>
    <lark-td>
      - 空调（循环/风量）
			- 净化器
			- AVC出风口
			- 车窗
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      抽烟快速净化/智能除味杀菌（跨域编排）
    </lark-td>
    <lark-td>
      - 吸烟检测
			- 除味/杀菌请求
			- 占位
			- 车窗开度
    </lark-td>
    <lark-td>
      - 空气质量：空气新鲜度
			- 空间：占位
    </lark-td>
    <lark-td>
      抽烟/异味/离车自动净化
    </lark-td>
    <lark-td>
      触发快速净化任务（外循环+全吹面+出风口避人+车窗开度+负离子/SORM）
    </lark-td>
    <lark-td>
      - 空调
			- AVC出风口
			- 车窗
			- 负离子/SORM
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      香氛氛围场景联动
    </lark-td>
    <lark-td>
      - 场景模式（影院/露营/迎宾/休息）
			- 空气质量净化状态
			- 灯光氛围
    </lark-td>
    <lark-td>
      - 交互：场景氛围
    </lark-td>
    <lark-td>
      场景触发/净化进行中
    </lark-td>
    <lark-td>
      触发香氛释放/暂停/降浓度任务
    </lark-td>
    <lark-td>
      - 香氛
			- 空气质量（负离子）
			- 灯光
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      NVH 静音优化
    </lark-td>
    <lark-td>
      - 2排小桌板展开
			- 车辆加速状态
			- 舱温
			- 占位
    </lark-td>
    <lark-td>
      - 交互：静谧需求
			- 热舒适：舱温
    </lark-td>
    <lark-td>
      静谧需求（影音/小桌板/加速）
    </lark-td>
    <lark-td>
      触发NVH降转速任务
    </lark-td>
    <lark-td>
      - 冰箱（压缩机/风扇）
			- 空调（风扇）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-HVAC
    </lark-td>
    <lark-td>
      离车遗留守护/儿童遗留保护
    </lark-td>
    <lark-td>
      - 占位+类型（OMS）
			- operator_state
			- 门状态
    </lark-td>
    <lark-td>
      - 安全：遗留检测
			- 空间：占位
    </lark-td>
    <lark-td>
      离车时儿童/活体遗留
    </lark-td>
    <lark-td>
      触发遗留保护任务（请求空调、冰箱离车决策、关窗关遮阳帘提醒）
    </lark-td>
    <lark-td>
      - 空调
			- 冰箱
			- 车窗
			- 门锁
    </lark-td>
  </lark-tr>
</lark-table>

## Group-03 VCC-Seat <mention-user id="ou_2d9b1f7a324e67b7ea8156ae8e434fd9"/><mention-user id="ou_f6732dea6030f0a4ac85641723a029a7"/>

主驾自适应功能-涉及主驾座椅和方向盘的协同控制

Post-crash 功能-涉及门锁，空调系统，座舱舒适系统，内灯系统，高低压能量管理系统等多个系统的协同控制

### 功能架构示例

每个BU 可以参照下面的范本，以1~2个功能场景为示例绘制 VCC 的功能架构图

<whiteboard token="B3ljwLKCLhfn6tb6OLlc6vDhnoh" width="820" height="313"/>

Function Block

<whiteboard token="V6Y5wFNJhhrF5EbFtYCctU5Wngg" width="820" height="255"/>

被动安全VCC实例

<whiteboard token="AjEFwE66AhaqVWbPCDEcL48pnHf" width="820" height="313"/>

**智慧****安全VCC实例（优化版 · 分层流程）**

<whiteboard token="FeNMw8wxthYznybUt60cHPPVnne"/>

**VCC 分层融合 vs 分散调用：价值对比**

<whiteboard token="Ls7jwjSOHheqLxbFGiJcNgnpn8f"/>

### 功能场景列表

<lark-table rows="12" cols="7" column-widths="100,158,243,122,116,100,243">

  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      **功能场景**
    </lark-td>
    <lark-td>
      **感知源（上游）**
    </lark-td>
    <lark-td>
      **座舱状态感知**
    </lark-td>
    <lark-td>
      **场景/意图识别**
    </lark-td>
    <lark-td>
      **任务**
    </lark-td>
    <lark-td>
      **规划&执行涉及系统（下游）**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-Seat
    </lark-td>
    <lark-td>
      主驾自适应模式
    </lark-td>
    <lark-td>
      - 主驾眼点（骨骼点 ）位置
			- 用户账户记忆设置
			- HMI交互请求
			- 座椅/方向盘空间位置
			- 座椅占位状态
			- 车辆配置
			- 门状态
    </lark-td>
    <lark-td>
      - 空间：姿态-乘客体型/空间舒适分计算
			- 空间：舱内空间关系
    </lark-td>
    <lark-td>
      新用户上车场景（当前座舱空间不舒适）
    </lark-td>
    <lark-td>
      触发主驾自适应任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 方向盘控制
			- 后视镜控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      小憩模式
    </lark-td>
    <lark-td>
      HMI-用户通过 GUI或者 NOMI 发出需求指令
    </lark-td>
    <lark-td>
      - 空间
			- 热舒适
			- 光
			- 声场
    </lark-td>
    <lark-td>
      乘客希望车内提供安静舒适的休息环境
    </lark-td>
    <lark-td>
      触发车内小憩模式任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 空调控制
			- 车窗控制
			- 灯光控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      观影模式
    </lark-td>
    <lark-td>
      HMI-用户通过 GUI或者 NOMI 发出需求指令
    </lark-td>
    <lark-td>
      - 空间
			- 热舒适
			- 光
			- 声场
    </lark-td>
    <lark-td>
      用户希望获得舒适的2排观影环境
    </lark-td>
    <lark-td>
      触发车内观影模式任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 空调控制
			- 车窗控制
			- 灯光控制
			- 遮阳帘控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      办公模式
    </lark-td>
    <lark-td>
      HMI-用户通过 GUI或者 NOMI 发出需求指令
    </lark-td>
    <lark-td>
      - 空间
			- 热舒适
			- 光
    </lark-td>
    <lark-td>
      用户希望车内二排获得最大，最舒适的空间环境和热舒适状态，便于商务接待
    </lark-td>
    <lark-td>
      触发车内办公模式任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 空调控制
			- 车窗控制
			- 灯光控制
			- 遮阳帘控制
			- 天幕/变色玻璃控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      隐私模式
    </lark-td>
    <lark-td>
      HMI-用户通过 GUI或者 NOMI 发出需求指令
    </lark-td>
    <lark-td>
      - 空间
			- 光
    </lark-td>
    <lark-td>
      用户希望车内环境处于私密状态
    </lark-td>
    <lark-td>
      触发车内隐私模式任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 灯光控制
			- 车窗控制
			- 遮阳帘控制
			- 天幕/变色玻璃控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      露营模式
    </lark-td>
    <lark-td>
      HMI-用户通过 GUI或者 NOMI 发出需求指令
    </lark-td>
    <lark-td>
      - 空间
			- 光
			- 热舒适
    </lark-td>
    <lark-td>
      乘客希望保持在车周围露营的车内外用电，车内休息的需求
    </lark-td>
    <lark-td>
      触发露营模式任务
    </lark-td>
    <lark-td>
      - 座椅控制
			- 高低压电源控制
			- 天窗控制
			- 遮阳帘控制
			- 天幕控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      智能快捷场景（属于一个大的功能分类，无固定的功能场景）
    </lark-td>
    <lark-td>
      - 用户使用习惯
			- 车辆位置
			- 车辆行程状态
			- 车内外环境状态
    </lark-td>
    <lark-td>
      - 空间
			- 热舒适
			- 光
			- 声场
    </lark-td>
    <lark-td>
      根据用户习惯和场景定义，在当前场景下用户大概率有特定的车控功能需求
    </lark-td>
    <lark-td>
      触发符合用户使用习惯和当前场景需求的快捷场景推荐
    </lark-td>
    <lark-td>
      按需触发
      - 座椅控制
			- 空调控制
			- 车窗控制
			- 灯光控制
			- 遮阳帘控制
			- 天幕/变色玻璃控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      PreCrash保护
    </lark-td>
    <lark-td>
      - 主车(Ego)车速
			- 主车(Ego)和目标车(Target)相对车速
			- TTC-Time To Collision
    </lark-td>
    <lark-td>
      - 乘员约束状态
			- 乘员安全状态
    </lark-td>
    <lark-td>
      预碰撞场景，用户希望能在碰撞前车辆状态预先做一些调整，使发生碰撞后最大程度保证人员安全
    </lark-td>
    <lark-td>
      触发预碰撞保护任务
    </lark-td>
    <lark-td>
      - 主动安全带控制
			- 悬架高度控制
			- PTC，HVC高压控制（断空调系统高压）
			- PreMSD控制（关键车辆数据上传）
			- V2L控制（断前舱盖220V电源）
			- Hood前舱盖控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      PostCrash保护
    </lark-td>
    <lark-td>
      - crash状态
			- 翻滚状态
			- 安全带状态
			- 原始占位状态
			- 座椅融合占位状态
			- DMS占位状态
			- OMS占位状态
    </lark-td>
    <lark-td>
      - 乘员约束状态
			- 乘员安全状态
    </lark-td>
    <lark-td>
      1.碰撞场景，
      2.翻滚场景
      用户希望在这两种场景发生后有人身安全保护，便于救援，并受到关爱
    </lark-td>
    <lark-td>
      触发PostCrash（碰撞&翻滚）保护任务
    </lark-td>
    <lark-td>
      - 高压控制（下高压）
			- 动力切断，放电控制
			- 车门锁控制（包括四门和儿童锁）
			- 车门打开控制（禁用，解禁）
			- 尾门锁控制
			- 车窗控制
			- 双闪控制
			- 内灯控制
			- 空调控制
			- 座椅方向盘控制（禁用，解禁）
			- Ecall控制
			- 制动控制
			- 录像控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      低速碰撞保护
    </lark-td>
    <lark-td>
      - EDR锁存状态
			- 横纵向加速度
			- 车速
    </lark-td>
    <lark-td>
      - 乘员安全状态
    </lark-td>
    <lark-td>
      低速碰撞场景，用户希望获取向导来处置，并保证安全
    </lark-td>
    <lark-td>
      触发低速碰撞任务（保护和安抚）
    </lark-td>
    <lark-td>
      - 语音安全引导
			- 加速控制（MAI）
			- Ecall控制
			- 录像控制
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      热失控保护
    </lark-td>
    <lark-td>
      - 动力电池电芯温度
			- 动力电池单体电压
			- 动力电池单体电流
			- 绝缘电阻
    </lark-td>
    <lark-td>
      - 声场
			- 气味
			- 光
			- 热舒适
			- 乘员安全状态
    </lark-td>
    <lark-td>
      热失控场景，用户希望自身安全，能被快速营救或逃离
    </lark-td>
    <lark-td>
      触发热失控保护任务
    </lark-td>
    <lark-td>
      - 车门锁控制
			- 车窗控制
			- 双闪控制
			- 内灯控制
			- 空调控制
			- Ecall控制
			- HMI提醒控制
    </lark-td>
  </lark-tr>
</lark-table>

## Group-04 VCC-Body <mention-user id="ou_f4283abfa902e705e981e9f67ddc3047"/>

### VCC产品白皮书

<mention-doc token="F87JwsvPNipWpokQjFJcxZOyn6f" type="wiki">大Body / VCC 产品白皮书（V0.1）</mention-doc>

<mention-doc token="HtFCw8Lr8iftbSkng4ecXRLqnrf" type="wiki">阶段1指导与实例</mention-doc>

<view type="2">

  <file token="YyPPb9VBJoArWHxe9kici8ndnNg" name="body-vcc-overview-apple.html"/>

</view>

### 个人理解简述：VCC架构原则与接口演进

#### 核心判断

现有SOA开发方式能够完成单系统功能，但Use Case经过PRD、FR和SRD逐层分解后，场景目标、参与主体与整车完成条件容易被拆散。最终各系统可能均已完成本域实现，却缺少对“整车任务是否完成、是否降级以及为何失败”的统一判断。

VCC的核心价值不是替代现有SOA，也不是集中重写业务逻辑，而是以Mission为主线重新连接场景、需求、执行结果与端到端验收，形成可追踪的整车功能全景。

<image token="HWHubU0D5oftX1xIhiDcjUBQn8b" width="1672" height="941" align="center"/>

#### 职责边界

- **VCC：**管理Mission、跨域目标、约束、生命周期和整车完成条件。
- **目标适配层：**将Goal转化为本域策略，完成使能与安全判断并返回Result。
- **SOA能力层：**提供稳定的动作、状态、实时闭环、诊断和安全保护。

#### 非中央化设计准则

1. **明确功能归属。**仅将需要统一任务对象、跨域目标、共享生命周期、整车完成判定或统一降级协调的功能纳入VCC；单一系统可独立闭环的功能继续归属系统产品。
1. **升级交互契约。**VCC与系统产品之间由“动作命令 + 状态订阅”逐步升级为“Goal Contract + Result Contract”；Goal描述期望结果和约束，Result表达完成、降级、拒绝及其原因和证据。

<mention-doc token="T6pkdUPljozdLHxBD6mccW4zndh" type="docx">如何避免VCC成为中央脚本：功能边界、接口形式、优势与代价</mention-doc>

<lark-table rows="6" cols="3" header-row="true" column-widths="150,370,370">

  <lark-tr>
    <lark-td>
      **维度**
    </lark-td>
    <lark-td>
      **中央脚本：动作编排**
    </lark-td>
    <lark-td>
      **非中央脚本：目标契约**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **组织方式**
    </lark-td>
    <lark-td>
      VCC编排条件、动作、顺序和等待。
    </lark-td>
    <lark-td>
      VCC下发Goal，产品返回Result。
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **复杂度归属**
    </lark-td>
    <lark-td>
      跨域与域内逻辑集中在VCC。
    </lark-td>
    <lark-td>
      跨域协同在VCC；域内策略留在产品。
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **变更影响**
    </lark-td>
    <lark-td>
      场景差异形成IF/ELSE和脚本复制。
    </lark-td>
    <lark-td>
      通过constraints表达变体，双方可独立演进。
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **异常与验收**
    </lark-td>
    <lark-td>
      主要观察动作执行到哪一步。
    </lark-td>
    <lark-td>
      按mission_id汇聚状态、原因和证据。
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **成本与适用**
    </lark-td>
    <lark-td>
      首版快；适合固定、简单联动，长期维护成本高。
    </lark-td>
    <lark-td>
      前期需建设契约；适合多域、多变体和持续演进。
    </lark-td>
  </lark-tr>
</lark-table>

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

**结论：**动作接口可以保留，但不应承担整车场景编排；跨域协同采用Mission，域内实现保留在系统产品。
</callout>

#### 接口原则

**判断标准：**VCC是否侵入系统产品的实现细节。

- **中央脚本：**VCC判断条件、编排顺序并逐项调用动作。
- **目标契约：**VCC下发Goal，系统产品自主执行并返回Result。

#### SOA架构调整

不推翻现有SOA，仅增加两层：VCC侧的Mission Runtime，以及系统产品侧的目标适配层。

1. **VCC ↔ 系统产品：**使用Goal Contract向下传递目标，使用Result Contract向上返回结果。
1. **目标适配层 ↔ SOA能力层：**继续使用稳定的Capability Command、State和Event完成域内执行与反馈。
1. **执行原则：**VCC不直接调用硬件动作；域内时序、状态机、安全闭环和故障处理继续由系统产品负责。

<image token="GirWbuaCPonPPgxgUn6cWkcynzb" width="1672" height="941" align="center"/>

### 功能场景列表

<lark-table rows="5" cols="8" column-widths="100,100,220,122,116,132,217,103">

  <lark-tr>
    <lark-td>
    </lark-td>
    <lark-td>
      **功能场景**
    </lark-td>
    <lark-td>
      **感知源（上游）**
    </lark-td>
    <lark-td>
      **座舱状态感知**
    </lark-td>
    <lark-td>
      **场景/意图识别**
    </lark-td>
    <lark-td>
      **任务**
    </lark-td>
    <lark-td>
      **规划&执行涉及系统（下游）**
    </lark-td>
    <lark-td>
      附件
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-Body
    </lark-td>
    <lark-td>
      近车解锁开门
    </lark-td>
    <lark-td>
      - 蓝牙/UWB钥匙位置
			- 用户账户记忆设置
			- 车辆设置（近车自动解锁/车辆解锁模式）
			- 门锁状态
			- 防盗状态
    </lark-td>
    <lark-td>
      - 空间：用户位置
    </lark-td>
    <lark-td>
      乘员安全上车
      （乘员舒适 + 车辆安全）
    </lark-td>
    <lark-td>
      触发近车解锁任务（近车自动开门 + 后视镜展开 + 灯光闪烁/迎宾灯+ 踏板 + 座椅后移 + 方向盘控制）
    </lark-td>
    <lark-td>
      - 门锁控制
			- 门把手控制
			- 电动门控制
			- 后视镜控制
			- 灯光控制
			- 座椅控制
			- 方向盘控制
			- 踏板控制
    </lark-td>
    <lark-td>
      <image token="Jre9bCEcqofGqlxYHN7cpPjPnSb" width="931" height="1023" align="center"/>
      <mention-doc token="EW4qw99Sei9F02kILKmcIWpbnQg" type="wiki">E2E Latency Analysis Table</mention-doc>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-Body
    </lark-td>
    <lark-td>
      离车闭锁
    </lark-td>
    <lark-td>
      - 蓝牙/UWB钥匙位置
			- 车辆设置（离车自动上锁）
			- 门锁状态
			- 防盗状态
    </lark-td>
    <lark-td>
      - 空间：用户位置
    </lark-td>
    <lark-td>
      乘员安全离车（乘员舒适 + 车辆安全）
    </lark-td>
    <lark-td>
      触发离车闭锁任务
      （离车自动上锁 + 后视镜折叠 + 转向灯双闪 + 喇叭 + 自动关车窗 + 自动关遮阳帘）
    </lark-td>
    <lark-td>
      - 门锁控制
			- 后视镜控制
			- 灯光控制
			- 喇叭控制
			- 车窗控制
			- 遮阳帘控制
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-Body
    </lark-td>
    <lark-td>
      尾门自动避障
      （未实现）
    </lark-td>
    <lark-td>
      - 蓝牙/UWB钥匙位置
			- 尾门锁状态
			- PDS
			- 摄像头
			- 激光雷达
    </lark-td>
    <lark-td>
      - 空间：尾门障碍物相对位置
    </lark-td>
    <lark-td>
      乘员安全打开后备箱
      （乘员舒适 + 车辆安全）
    </lark-td>
    <lark-td>
      触发尾门自动避障任务（车辆前进 + 尾门打开 + 车辆后退归位）
    </lark-td>
    <lark-td>
      - AD（视觉+激光雷达）障碍物识别
			- PDS障碍物识别
			- 尾门控制
			- 灯光控制
    </lark-td>
    <lark-td>
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      VCC-Body
    </lark-td>
    <lark-td>
      视觉手势开启前舱盖
    </lark-td>
    <lark-td>
      - 用户手臂动作
			- 蓝牙/UWB钥匙位置
			- 车辆设置（前备箱手势开启）
			- 挡位/车速
    </lark-td>
    <lark-td>
      - 乘员状态：乘员手臂动作
    </lark-td>
    <lark-td>
      乘员安全打开前舱盖
      （乘员舒适 + 车辆安全）
    </lark-td>
    <lark-td>
      触发前舱盖打开任务
      （前舱盖打开 + 灯光闪烁）
    </lark-td>
    <lark-td>
      - DC手势识别
			- 前舱盖控制
			- 灯光控制
    </lark-td>
    <lark-td>
      <image token="WJ2wbpX0PokK7pxgnhXcHIIcnHf" width="969" height="690" align="center"/>
    </lark-td>
  </lark-tr>
</lark-table>

### 功能架构

- 当前近车解锁开发方式：

<whiteboard token="ZTAowmI2BhPW3Kbs5Spc9evUn9e"/>

- 预期近车解锁开发方式

<whiteboard token="Al53wrkm0hyxyRb8Ct2cUVS9nXb"/>

- 原分布式开发模式 -> VCC开发模式

<image token="YLnKbSvxiojiyXxahXKcDk8pnxd" width="1673" height="940" align="center"/>

<image token="Hvo5bftWooMus0xmwr7cSL8ynXg" width="1672" height="941" align="center"/>

### 技术包装

技术名称：

**VCC ACE三心坐标**

**A — Assurance：安心**

**C — Comfort：舒心**

**E — Ease：省心**

中文定义：

**安心、舒心、省心，是VCC管理乘员体验的三个基本维度。**

核心表达：

**VMC用XYZ管理车辆运动，VCC用ACE管理乘员体验。**

传播表达：

**车有XYZ，人有ACE。**

产品价值：

**安心是底线，舒心是目标，省心是体验。**

## Group-05 VCC-HLv <mention-user id="ou_b966ed72a8ebbe3083e166a99dd8639f"/>

## Function block

<whiteboard token="FBgmwQouhhnxeabif3TcCauvnJg" width="820" height="255"/>

### 功能块职责定义（Function Block Definition）

<lark-table rows="19" cols="4" header-row="true" column-widths="182,170,120,420">

  <lark-tr>
    <lark-td>
      层
    </lark-td>
    <lark-td>
      功能块
    </lark-td>
    <lark-td>
      缩写
    </lark-td>
    <lark-td>
      职责定义
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      基础感知能力（外部）
    </lark-td>
    <lark-td>
      基础感知能力 Base Perception
    </lark-td>
    <lark-td>
      —
    </lark-td>
    <lark-td>
      提供安全/空间/姿态/热舒适/光/声音等维度的原始传感器信号与融合信号，承载虚拟传感与置信度判断（已移出 VCC）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="3">
      ① 感知 Perception
    </lark-td>
    <lark-td>
      感知合理性校验
    </lark-td>
    <lark-td>
      VCC_PVAL
    </lark-td>
    <lark-td>
      对原始信号或融合结果做合理性校验（非强制），主路径校验 + 融合结果复检
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      多源感知融合
    </lark-td>
    <lark-td>
      VCC_PFUS
    </lark-td>
    <lark-td>
      同一物理量的多感知源在逻辑层面择优/融合（如座椅占位：SBR/OMS/UWB），输出仍为同一物理量
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      舱内统一状态表达
    </lark-td>
    <lark-td>
      VCC_PCTX
    </lark-td>
    <lark-td>
      结构化上下文处理（每座椅是否有人、乘客类型/体型、物品、热/光状态），供上层 agent 直接消费
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="4">
      ② 意图/场景识别 Cognition
    </lark-td>
    <lark-td>
      用户指令处理
    </lark-td>
    <lark-td>
      VCC_ICMD
    </lark-td>
    <lark-td>
      采集显性指令输入：HMI 开关、大屏操作、语音
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      特殊场景识别
    </lark-td>
    <lark-td>
      VCC_ISCN
    </lark-td>
    <lark-td>
      识别非指令性场景：舱外（碰撞等）、舱内（迎宾、午休、疲劳）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      意图冲突裁决
    </lark-td>
    <lark-td>
      VCC_IARB
    </lark-td>
    <lark-td>
      对「用户指令」与「特殊场景」两条通道做冲突裁决
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      意图/场景理解
    </lark-td>
    <lark-td>
      VCC_IUND
    </lark-td>
    <lark-td>
      将意图与场景转化为用户对座舱状态的需求（空间/安全/热/声/光）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="5">
      ③ 任务管理 Orchestration
    </lark-td>
    <lark-td>
      座舱级任务建立
    </lark-td>
    <lark-td>
      VCC_TCRE
    </lark-td>
    <lark-td>
      基于座舱状态需求建立座舱级任务（目标）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      子系统任务定义
    </lark-td>
    <lark-td>
      VCC_TDEF
    </lark-td>
    <lark-td>
      定义任务所涉及的子系统能力（座椅折叠、隐私玻璃、空调、净化等）
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      子系统任务仲裁
    </lark-td>
    <lark-td>
      VCC_TARB
    </lark-td>
    <lark-td>
      优先级/时序管理，解决与车辆工作状态冲突或资源抢占
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      正常流转
    </lark-td>
    <lark-td>
      VCC_TNRM
    </lark-td>
    <lark-td>
      根据各子系统完成状态更新座舱级任务状态
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      异常处理
    </lark-td>
    <lark-td>
      VCC_TABN
    </lark-td>
    <lark-td>
      依据仲裁结果/子系统超时/故障执行降级或异常响应
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="2">
      ④ 跨域目标规划 Planning
    </lark-td>
    <lark-td>
      跨域目标规划
    </lark-td>
    <lark-td>
      VCC_GPLN
    </lark-td>
    <lark-td>
      承接各子系统任务，完成具体控制目标与运动时序规划
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Seat / Door / Window / Thermal / Light
    </lark-td>
    <lark-td>
      VCC_SEAT 等
    </lark-td>
    <lark-td>
      各子系统的具体执行
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="3">
      支撑层  Support
    </lark-td>
    <lark-td>
      座舱状态模型 NCM
    </lark-td>
    <lark-td>
      VCC_NCM
    </lark-td>
    <lark-td>
      NIO Cabin Model，全局座舱状态模型，供各层共享
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      安全约束
    </lark-td>
    <lark-td>
      VCC_SAFE
    </lark-td>
    <lark-td>
      独立的安全约束，贯穿各层
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      UI 交互层
    </lark-td>
    <lark-td>
      VCC_UI
    </lark-td>
    <lark-td>
      横切交互层（输入+反馈+中断），反馈任务执行前/中/后状态
    </lark-td>
  </lark-tr>
</lark-table>
