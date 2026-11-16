# 版本记录

      Version

      Date

      Author

      Changes

      0.0.1

      2026.02.04

      初稿

      0.0.2

      2026.08.21

      补充SkyOS进程间通信IPC通道实现进展和release情况

# 背景

## 目标

设计VMBC应用软件与SOA解耦详细POC方案，验证：

- 技术可行性
- 观测对MCU/MPU性能和资源的影响
- 测试对关键功能的影响

## 参考

VMBC应用软件与SOA解耦方案

## 范围

      车型

      版本

      控制器

      软件

      相关方

      Draco

      V33 RC03

      VDF_M Core2

      BDYsunroofMgr
      TurnLiMgr
      BDYpersonDetectInfo
      SeatMassgMgr_RR
      BDYdoorHndlSnsrMgr
      SeatMassgMgr_RL
      LoBeamMgr
      CRSVehSpdLimMgr
      BDYrainAutoClsApp
      BDYmanChrgrGateApp
      ThermalOutOfControlApp
      AdLiMgr
      HLVwtiCaller
      BDYprofileSettingApp
      CRSSmtChrgMgr
      BDYcarpetLiMgr
      BDYafsControlAdbApp
      AntiTheftMgr
      DayRunLiMgr
      UserVirtualGear
      CRSChargingMgr
      ReadLiMgr
      SpdInfoMgr
      BDYbackLiMgr
      IntSideDoorlockApp
      SeatMoveMgr
      LightingWelcomeMgr
      BDYhoodOpenGearCtrlApp
      UserVirtualAccr
      EntrySetting
      BDYdoorHndlAutoCtrlApp
      BDYdoorOpenCloseApp
      AmbLiMgr
      CRSanimationLiAdvApp
      BDYdoorHndlLiMgr
      BDYrcpMoveMgr
      MOTUsrVrtl
      PowerPedalMgr
      BDYloBeamLevelMgr
      BDYautoMirrApp
      DimGlassMgr
      BDYmanSwtSeatApp
      DoorLockMgr
      ExtrLiSetting
      BDYloBeamApp
      OdoInfoMgr
      BDYbackLiCtrlApp
      BDYrearShadeMgr
      UserVirtualSteer
      SteerColAdjMgr
      MirrFoldMgr
      WinMgr
      BDYseatAutoModeApp
      ChrgrGateMgr
      PosnLiMgr_LEO
      DoorOpenMgr
      SeatMassgMgr_FL
      SeatMassgMgr_FR
      BDYrdlCtrlApp
      FrontWiperMgr
      BDYadbMgr
      BDYmanoeuvreLiMgr
      HiBeamMgr
      HLVdsplCore
      UserVirtualBrk
      BDYpeLockApp
      BDYAutoChrgrGateApp
      BDYswtLiCtrlApp
      CrashApp
      SeatBasicSts
      DoorHndlMgr
      CRSDriveModeMgr
      CRSAnimatLiMgr

      Draco

      V33 RC03

      VDF_A vmbc_body进程

      BDYantilockOutApp
      BDYautoLeveling4senApp
      BDYblindSpotDetLiMgr
      BDYcornerLiApp
      BDYfrntWiprSwtApp
      BDYlockWinAutoClsCtrlApp
      BDYoneKeyComfortApp
      BDYroofShadeManApp
      BDYsafeBoxFront
      BDYsafeBoxRear
      BDYseatProductionModeApp
      BDYseatSelfDefApp
      BDYtransportModAutoClsCtrlApp
      CbnFragMgr
      CornerLiMgr
      CRSproductionModeLiApp
      FogLiMgr
      GearPUnlckApp
      Ls_CabinSolarRadiatJud
      MirrAdjustMgr
      RvrsLiMgr
      SpeedUpApp

      Draco

      V33 RC03

      ZONE_REM Core2

      MOTlsv

# 方案设计

## 软件架构

## 接口文件

### 概念

这里的接口文件，是指VMBC软件开发所使用到的接口文件，形式为IDL文件。

采用IDL文件的目的，是其可以维持VMBC应用软件开发模式不变。

### 设计思路

应用软件可能包含client端实现和service端实现。

作为service端，应用软件需要实现service提供的所有服务接口和所有信号。

作为client端，应用软件按需使用service所提供的部分服务接口中的部分信号。

#### client端

- 根据软件模块实际使用的接口信号，对平台服务IDL进行裁剪
- 相比平台服务，只改域名，域名按照.格式，如vmbc.dooropenmgr
- 不改服务名、接口名、信号名
- Service ID按照私有服务规则编排
- 删除接口中的TOX相关配置，包括E2E、reliability等
- RPC接口类型均采用简单接口类型，具体映射关系如下：
	- FIELD_READONLY → EVENT
	- FIELD_WRITABLE → EVENT + FF_METHOD
	- RR_METHOD → FF_METHOD（如需response，特殊处理）
	- FF_METHOD → FF_METHOD
	- EVENT → EVENT

    ```protobuf
    syntax = "proto3";
    package srv.motion.drv;
    import "nrpc.option.proto";
    option (idl_version) = "1.10";
    
    message MotionCommInfo {
        float accr_pedl_posn                                 = 1; // Unit: %
        bool accr_pedl_posn_vld                              = 2;
        EnumMotionCtrlInfoActGear act_gear                   = 3;
        bool act_gear_vld                                    = 4;
        bool brk_pedl_prsd                                   = 5;
        bool brk_pedl_prsd_vld                               = 6;
        float brk_pedl_trvl                                  = 7; // Unit: %
        bool brk_trvl_vld                                    = 8;
        float veh_spd_asild                                  = 9; // Unit: km/h
        bool veh_spd_asild_vld                              = 10;
        float peuf_mot_spd                                  = 11; // Unit: rpm
        bool peuf_mot_spd_vld                               = 12;
        float peuf_mot_act_tq                               = 13; // Unit: Nm
        bool peuf_mot_act_tq_vld                            = 14;
        float peur_mot_spd                                  = 15; // Unit: rpm
        bool peur_mot_spd_vld                               = 16;
        float peur_mot_act_tq                               = 17; // Unit: Nm
        bool peur_mot_act_tq_vld                            = 18;
        bool veh_rdy                                        = 19;
        float whl_spd_fl                                    = 20; // Unit: km/h
        float whl_spd_fr                                    = 21; // Unit: km/h
        float whl_spd_rl                                    = 22; // Unit: km/h
        float whl_spd_rr                                    = 23; // Unit: km/h
        EnumWhlSpdDir whl_spd_dir_fl                        = 24;
        EnumWhlSpdDir whl_spd_dir_fr                        = 25;
        EnumWhlSpdDir whl_spd_dir_rl                        = 26;
        EnumWhlSpdDir whl_spd_dir_rr                        = 27;
        EnumMotionCtrlInfoWhlSpdStsFl whl_spd_sts_fl        = 28;
        EnumMotionCtrlInfoWhlSpdStsFr whl_spd_sts_fr        = 29;
        EnumMotionCtrlInfoWhlSpdStsRl whl_spd_sts_rl        = 30;
        EnumMotionCtrlInfoWhlSpdStsRr whl_spd_sts_rr        = 31;
        float whl_pls_cntr_fl                               = 32; // Unit: NA
        bool whl_pls_cntr_fl_vld                            = 33;
        float whl_pls_cntr_fr                               = 34; // Unit: NA
        bool whl_pls_cntr_fr_vld                            = 35;
        float whl_pls_cntr_rl                               = 36; // Unit: NA
        bool whl_pls_cntr_rl_vld                            = 37; //  
        float whl_pls_cntr_rr                               = 38; // Comment:    Unit: NA
        bool whl_pls_cntr_rr_vld                            = 39; //  
        EnumMotionCtrlInfoShifterPostnSts shifter_postn_sts = 40; //  
        bool shifter_postn_sts_vld                          = 41; //  
        bool arb_prk_butn_sts                               = 42; // 0: ARBPRKBUTNSTS_NOT_PRESSED 1: ARBPRKBUTNSTS_PRESSED
        bool arb_prk_butn_sts_vld                           = 43;
        float bcu_veh_spd                                   = 44; // Comment:    Unit: km/h
        bool bcu_veh_spd_sts                                = 45; //  
        EnumVehMovDir veh_mov_dir                           = 46; //  
        uint64 vehspd_asild_tv_ns                           = 59; // Comment:    Unit: km/h
        uint64 whlspd_tv_ns                                 = 60; // Comment:     Unit: km/h
        uint64 tv_ns                                        = 61; // Comment:    Unit: km/h
        bool spin_sts_fl                                    = 62; // false-无打滑；true-打滑
        bool spin_sts_fr                                    = 63; // false-无打滑；true-打滑
        bool spin_sts_rl                                    = 64; // false-无打滑；true-打滑
        bool spin_sts_rr                                    = 65; // false-无打滑；true-打滑
        bool spin_sts_fl_validity                           = 66; // spin_sts_fl信号有效性
        bool spin_sts_fr_validity                           = 67; // spin_sts_fr信号有效性
        bool spin_sts_rl_validity                           = 68; // spin_sts_rl信号有效性
        bool spin_sts_rr_validity                           = 69; // spin_sts_rr信号有效
        float peuf_bearing_temp_calc                        = 70; // Unit: ℃
    }
    
    enum EnumMotionCtrlInfoAvhSts {
        MCIAVHSTS_FAILURE      = 0;
        MCIAVHSTS_STANDBY      = 1;
        MCIAVHSTS_ACTIVE       = 2;
        MCIAVHSTS_OFF          = 3;
    }
    
    enum EnumMotionCtrlInfoEpbSts {
        MCIEPBSTS_UNKNOW        = 0;
        MCIEPBSTS_EPB_APPLIED   = 1;
        MCIEPBSTS_EPB_RELEASING = 2;
        MCIEPBSTS_EPB_RELEASED  = 3;
        MCIEPBSTS_EPB_APPLYING  = 4;
    }
    
    enum EnumMotionCtrlInfoActGear {
        MCIACTGEAR_PARKING      = 0;
        MCIACTGEAR_REVERSE      = 1;
        MCIACTGEAR_NEUTRAL      = 2;
        MCIACTGEAR_DRIVE        = 3;
    }
    
    enum EnumVehMovDir {
        VEHMOVDIR_STANDSTILL = 0;
        VEHMOVDIR_FORWARD    = 1;
        VEHMOVDIR_BACKWARD   = 2;
        VEHMOVDIR_INVALID    = 3;
    }
    
    enum EnumWhlSpdDir {
        WHLSPDDIR_STANDSTILL = 0;
        WHLSPDDIR_FORWARD    = 1;
        WHLSPDDIR_BACKWARD   = 2;
        WHLSPDDIR_INVALID    = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFl {
        MCIWHLSPDSTSFL_INITIALIZATION = 0;
        MCIWHLSPDSTSFL_VALID          = 1;
        MCIWHLSPDSTSFL_INVALID        = 2;
        MCIWHLSPDSTSFL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFr {
        MCIWHLSPDSTSFR_INITIALIZATION = 0;
        MCIWHLSPDSTSFR_VALID          = 1;
        MCIWHLSPDSTSFR_INVALID        = 2;
        MCIWHLSPDSTSFR_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRl {
        MCIWHLSPDSTSRL_INITIALIZATION = 0;
        MCIWHLSPDSTSRL_VALID          = 1;
        MCIWHLSPDSTSRL_INVALID        = 2;
        MCIWHLSPDSTSRL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRr {
        MCIWHLSPDSTSRR_INITIALIZATION = 0;
        MCIWHLSPDSTSRR_VALID          = 1;
        MCIWHLSPDSTSRR_INVALID        = 2;
        MCIWHLSPDSTSRR_RESERVED       = 3;
    }

    enum EnumMotionCtrlInfoShifterPostnSts {
        MCISHIFTERPOSTNSTS_NO_REQUEST      = 0;
        MCISHIFTERPOSTNSTS_GEAR_R_REQUEST  = 1;
        MCISHIFTERPOSTNSTS_GEAR_NR_REQUEST = 2;
        MCISHIFTERPOSTNSTS_GEAR_ND_REQUEST = 3;
        MCISHIFTERPOSTNSTS_GEAR_D_REQUEST  = 4;
    }
    
    enum EnumMotionCtrlInfoHdcSts {
        MCIHDCSTS_OFF          = 0;
        MCIHDCSTS_FAILURE      = 1;
        MCIHDCSTS_STANDBY      = 2;
        MCIHDCSTS_ACTIVE       = 3;
    }
    
    message VafInfo {
        bool abs_actv                    = 1;
        bool tcs_vdc_actv                = 2;
        EnumMotionCtrlInfoAvhSts avh_sts = 3;
        EnumMotionCtrlInfoEpbSts epb_sts = 4;
        bool abs_fail_sts                = 5;
        bool epb_fail_sts                = 6;
        EnumMotionCtrlInfoHdcSts hdc_sts = 7;
        bool cdp_actv                    = 8;
        bool dtc_actv                    = 9;
        bool arp_actv                   = 10;
        bool over_heat_sts              = 11;
        bool tcs_vdc_fail_sts           = 12;
        bool tcs_mod_sts                = 13;
        bool vdc_mod_sts                = 14;
        bool dtc_avl                    = 15;
        bool cdp_avl                    = 16;
        uint64 tv_ns                    = 17;
        bool vdc_actv                   = 18;
    }
    
    message MotionInfoMonitorType {
        float tq_cmd_fa          = 1; // Unit: NA
        float brk_fx_trq_total   = 2; // Unit: NA
        uint32 brk_fx_mod_total  = 3;
        uint32 brk_fx_type_total = 4;
        uint32 rbu_brk_fx_sts    = 5;
        uint32 brk_fx_sts_main   = 6;
        uint32 brk_fx_sts_rdnt   = 7;
    }
    
    service MotionCtrlInfo {
        option(service_id) = 5003;
    
        rpc IfCommInfo(MotionCommInfo) returns (Null) {
            option (rpc_id) = 100;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
            option (e2e_s2c_enabled) = true;
            option (e2e_s2c_timeout) = 100;
            option (e2e_s2c_max_delta_counter) = 5;
            option (e2e_s2c_min_data_length) = 96;
            option (e2e_s2c_max_data_length) = 32768;
        }
    
        rpc IfVafInfo(VafInfo) returns (Null) {
            option (rpc_id) = 101;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
            option (e2e_s2c_enabled) = true;
            option (e2e_s2c_timeout) = 100;
            option (e2e_s2c_max_delta_counter) = 5;
            option (e2e_s2c_min_data_length) = 96;
            option (e2e_s2c_max_data_length) = 32768;
        }
    
        rpc MotionInfoMonitor(MotionInfoMonitorType) returns (Null) {
            option (rpc_id) = 102;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
        }
    }
    ```

    ```protobuf
    syntax = "proto3";
    package vmbc.dooropenmgr;
    import "nrpc.option.proto";
    option (idl_version) = "1.10";
    
    message MotionCommInfo {
            float bcu_veh_spd  = 44; // Comment:    Unit: km/h
    }
    
    service MotionCtrlInfo {
        option(service_id) = 50003;
        
        rpc IfCommInfo(MotionCommInfo) returns (Null) {
            option (rpc_id) = 100;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
        }
    ```

#### service端

- service端需要实现所有的接口及信号，只对平台服务IDL进行配置属性裁剪
- 相比平台服务，只改域名，域名按照.格式，如vmbc.motiony
- 不改服务名、接口名、信号名
- Service ID按照私有服务规则编排
- 删除接口中的TOX相关配置，包括E2E、reliability等
- RPC接口类型均采用简单接口类型，具体映射关系如下：
	- FIELD_READONLY → EVENT
	- FIELD_WRITABLE → EVENT + FF_METHOD
	- RR_METHOD → FF_METHOD（如需response，特殊处理）
	- FF_METHOD → FF_METHOD
	- EVENT → EVENT

    ```protobuf
    syntax = "proto3";
    package srv.motion.drv;
    import "nrpc.option.proto";
    option (idl_version) = "1.10";
    
    message MotionCommInfo {
        float accr_pedl_posn                                 = 1; // Unit: %
        bool accr_pedl_posn_vld                              = 2;
        EnumMotionCtrlInfoActGear act_gear                   = 3;
        bool act_gear_vld                                    = 4;
        bool brk_pedl_prsd                                   = 5;
        bool brk_pedl_prsd_vld                               = 6;
        float brk_pedl_trvl                                  = 7; // Unit: %
        bool brk_trvl_vld                                    = 8;
        float veh_spd_asild                                  = 9; // Unit: km/h
        bool veh_spd_asild_vld                              = 10;
        float peuf_mot_spd                                  = 11; // Unit: rpm
        bool peuf_mot_spd_vld                               = 12;
        float peuf_mot_act_tq                               = 13; // Unit: Nm
        bool peuf_mot_act_tq_vld                            = 14;
        float peur_mot_spd                                  = 15; // Unit: rpm
        bool peur_mot_spd_vld                               = 16;
        float peur_mot_act_tq                               = 17; // Unit: Nm
        bool peur_mot_act_tq_vld                            = 18;
        bool veh_rdy                                        = 19;
        float whl_spd_fl                                    = 20; // Unit: km/h
        float whl_spd_fr                                    = 21; // Unit: km/h
        float whl_spd_rl                                    = 22; // Unit: km/h
        float whl_spd_rr                                    = 23; // Unit: km/h
        EnumWhlSpdDir whl_spd_dir_fl                        = 24;
        EnumWhlSpdDir whl_spd_dir_fr                        = 25;
        EnumWhlSpdDir whl_spd_dir_rl                        = 26;
        EnumWhlSpdDir whl_spd_dir_rr                        = 27;
        EnumMotionCtrlInfoWhlSpdStsFl whl_spd_sts_fl        = 28;
        EnumMotionCtrlInfoWhlSpdStsFr whl_spd_sts_fr        = 29;
        EnumMotionCtrlInfoWhlSpdStsRl whl_spd_sts_rl        = 30;
        EnumMotionCtrlInfoWhlSpdStsRr whl_spd_sts_rr        = 31;
        float whl_pls_cntr_fl                               = 32; // Unit: NA
        bool whl_pls_cntr_fl_vld                            = 33;
        float whl_pls_cntr_fr                               = 34; // Unit: NA
        bool whl_pls_cntr_fr_vld                            = 35;
        float whl_pls_cntr_rl                               = 36; // Unit: NA
        bool whl_pls_cntr_rl_vld                            = 37; //  
        float whl_pls_cntr_rr                               = 38; // Comment:    Unit: NA
        bool whl_pls_cntr_rr_vld                            = 39; //  
        EnumMotionCtrlInfoShifterPostnSts shifter_postn_sts = 40; //  
        bool shifter_postn_sts_vld                          = 41; //  
        bool arb_prk_butn_sts                               = 42; // 0: ARBPRKBUTNSTS_NOT_PRESSED 1: ARBPRKBUTNSTS_PRESSED
        bool arb_prk_butn_sts_vld                           = 43;
        float bcu_veh_spd                                   = 44; // Comment:    Unit: km/h
        bool bcu_veh_spd_sts                                = 45; //  
        EnumVehMovDir veh_mov_dir                           = 46; //  
        uint64 vehspd_asild_tv_ns                           = 59; // Comment:    Unit: km/h
        uint64 whlspd_tv_ns                                 = 60; // Comment:     Unit: km/h
        uint64 tv_ns                                        = 61; // Comment:    Unit: km/h
        bool spin_sts_fl                                    = 62; // false-无打滑；true-打滑
        bool spin_sts_fr                                    = 63; // false-无打滑；true-打滑
        bool spin_sts_rl                                    = 64; // false-无打滑；true-打滑
        bool spin_sts_rr                                    = 65; // false-无打滑；true-打滑
        bool spin_sts_fl_validity                           = 66; // spin_sts_fl信号有效性
        bool spin_sts_fr_validity                           = 67; // spin_sts_fr信号有效性
        bool spin_sts_rl_validity                           = 68; // spin_sts_rl信号有效性
        bool spin_sts_rr_validity                           = 69; // spin_sts_rr信号有效
        float peuf_bearing_temp_calc                        = 70; // Unit: ℃
    }
    
    enum EnumMotionCtrlInfoAvhSts {
        MCIAVHSTS_FAILURE      = 0;
        MCIAVHSTS_STANDBY      = 1;
        MCIAVHSTS_ACTIVE       = 2;
        MCIAVHSTS_OFF          = 3;
    }
    
    enum EnumMotionCtrlInfoEpbSts {
        MCIEPBSTS_UNKNOW        = 0;
        MCIEPBSTS_EPB_APPLIED   = 1;
        MCIEPBSTS_EPB_RELEASING = 2;
        MCIEPBSTS_EPB_RELEASED  = 3;
        MCIEPBSTS_EPB_APPLYING  = 4;
    }
    
    enum EnumMotionCtrlInfoActGear {
        MCIACTGEAR_PARKING      = 0;
        MCIACTGEAR_REVERSE      = 1;
        MCIACTGEAR_NEUTRAL      = 2;
        MCIACTGEAR_DRIVE        = 3;
    }
    
    enum EnumVehMovDir {
        VEHMOVDIR_STANDSTILL = 0;
        VEHMOVDIR_FORWARD    = 1;
        VEHMOVDIR_BACKWARD   = 2;
        VEHMOVDIR_INVALID    = 3;
    }
    
    enum EnumWhlSpdDir {
        WHLSPDDIR_STANDSTILL = 0;
        WHLSPDDIR_FORWARD    = 1;
        WHLSPDDIR_BACKWARD   = 2;
        WHLSPDDIR_INVALID    = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFl {
        MCIWHLSPDSTSFL_INITIALIZATION = 0;
        MCIWHLSPDSTSFL_VALID          = 1;
        MCIWHLSPDSTSFL_INVALID        = 2;
        MCIWHLSPDSTSFL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFr {
        MCIWHLSPDSTSFR_INITIALIZATION = 0;
        MCIWHLSPDSTSFR_VALID          = 1;
        MCIWHLSPDSTSFR_INVALID        = 2;
        MCIWHLSPDSTSFR_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRl {
        MCIWHLSPDSTSRL_INITIALIZATION = 0;
        MCIWHLSPDSTSRL_VALID          = 1;
        MCIWHLSPDSTSRL_INVALID        = 2;
        MCIWHLSPDSTSRL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRr {
        MCIWHLSPDSTSRR_INITIALIZATION = 0;
        MCIWHLSPDSTSRR_VALID          = 1;
        MCIWHLSPDSTSRR_INVALID        = 2;
        MCIWHLSPDSTSRR_RESERVED       = 3;
    }

    enum EnumMotionCtrlInfoShifterPostnSts {
        MCISHIFTERPOSTNSTS_NO_REQUEST      = 0;
        MCISHIFTERPOSTNSTS_GEAR_R_REQUEST  = 1;
        MCISHIFTERPOSTNSTS_GEAR_NR_REQUEST = 2;
        MCISHIFTERPOSTNSTS_GEAR_ND_REQUEST = 3;
        MCISHIFTERPOSTNSTS_GEAR_D_REQUEST  = 4;
    }
    
    enum EnumMotionCtrlInfoHdcSts {
        MCIHDCSTS_OFF          = 0;
        MCIHDCSTS_FAILURE      = 1;
        MCIHDCSTS_STANDBY      = 2;
        MCIHDCSTS_ACTIVE       = 3;
    }
    
    message VafInfo {
        bool abs_actv                    = 1;
        bool tcs_vdc_actv                = 2;
        EnumMotionCtrlInfoAvhSts avh_sts = 3;
        EnumMotionCtrlInfoEpbSts epb_sts = 4;
        bool abs_fail_sts                = 5;
        bool epb_fail_sts                = 6;
        EnumMotionCtrlInfoHdcSts hdc_sts = 7;
        bool cdp_actv                    = 8;
        bool dtc_actv                    = 9;
        bool arp_actv                   = 10;
        bool over_heat_sts              = 11;
        bool tcs_vdc_fail_sts           = 12;
        bool tcs_mod_sts                = 13;
        bool vdc_mod_sts                = 14;
        bool dtc_avl                    = 15;
        bool cdp_avl                    = 16;
        uint64 tv_ns                    = 17;
        bool vdc_actv                   = 18;
    }
    
    message MotionInfoMonitorType {
        float tq_cmd_fa          = 1; // Unit: NA
        float brk_fx_trq_total   = 2; // Unit: NA
        uint32 brk_fx_mod_total  = 3;
        uint32 brk_fx_type_total = 4;
        uint32 rbu_brk_fx_sts    = 5;
        uint32 brk_fx_sts_main   = 6;
        uint32 brk_fx_sts_rdnt   = 7;
    }
    
    service MotionCtrlInfo {
        option(service_id) = 5003;
    
        rpc IfCommInfo(MotionCommInfo) returns (Null) {
            option (rpc_id) = 100;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
            option (e2e_s2c_enabled) = true;
            option (e2e_s2c_timeout) = 100;
            option (e2e_s2c_max_delta_counter) = 5;
            option (e2e_s2c_min_data_length) = 96;
            option (e2e_s2c_max_data_length) = 32768;
        }
    
        rpc IfVafInfo(VafInfo) returns (Null) {
            option (rpc_id) = 101;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
            option (e2e_s2c_enabled) = true;
            option (e2e_s2c_timeout) = 100;
            option (e2e_s2c_max_delta_counter) = 5;
            option (e2e_s2c_min_data_length) = 96;
            option (e2e_s2c_max_data_length) = 32768;
        }
    
        rpc MotionInfoMonitor(MotionInfoMonitorType) returns (Null) {
            option (rpc_id) = 102;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
        }
    }
    ```

    ```protobuf
    syntax = "proto3";
    package vmbc.motiony;
    import "nrpc.option.proto";
    option (idl_version) = "1.10";
    
    message MotionCommInfo {
        float accr_pedl_posn                                 = 1; // Unit: %
        bool accr_pedl_posn_vld                              = 2;
        EnumMotionCtrlInfoActGear act_gear                   = 3;
        bool act_gear_vld                                    = 4;
        bool brk_pedl_prsd                                   = 5;
        bool brk_pedl_prsd_vld                               = 6;
        float brk_pedl_trvl                                  = 7; // Unit: %
        bool brk_trvl_vld                                    = 8;
        float veh_spd_asild                                  = 9; // Unit: km/h
        bool veh_spd_asild_vld                              = 10;
        float peuf_mot_spd                                  = 11; // Unit: rpm
        bool peuf_mot_spd_vld                               = 12;
        float peuf_mot_act_tq                               = 13; // Unit: Nm
        bool peuf_mot_act_tq_vld                            = 14;
        float peur_mot_spd                                  = 15; // Unit: rpm
        bool peur_mot_spd_vld                               = 16;
        float peur_mot_act_tq                               = 17; // Unit: Nm
        bool peur_mot_act_tq_vld                            = 18;
        bool veh_rdy                                        = 19;
        float whl_spd_fl                                    = 20; // Unit: km/h
        float whl_spd_fr                                    = 21; // Unit: km/h
        float whl_spd_rl                                    = 22; // Unit: km/h
        float whl_spd_rr                                    = 23; // Unit: km/h
        EnumWhlSpdDir whl_spd_dir_fl                        = 24;
        EnumWhlSpdDir whl_spd_dir_fr                        = 25;
        EnumWhlSpdDir whl_spd_dir_rl                        = 26;
        EnumWhlSpdDir whl_spd_dir_rr                        = 27;
        EnumMotionCtrlInfoWhlSpdStsFl whl_spd_sts_fl        = 28;
        EnumMotionCtrlInfoWhlSpdStsFr whl_spd_sts_fr        = 29;
        EnumMotionCtrlInfoWhlSpdStsRl whl_spd_sts_rl        = 30;
        EnumMotionCtrlInfoWhlSpdStsRr whl_spd_sts_rr        = 31;
        float whl_pls_cntr_fl                               = 32; // Unit: NA
        bool whl_pls_cntr_fl_vld                            = 33;
        float whl_pls_cntr_fr                               = 34; // Unit: NA
        bool whl_pls_cntr_fr_vld                            = 35;
        float whl_pls_cntr_rl                               = 36; // Unit: NA
        bool whl_pls_cntr_rl_vld                            = 37; //  
        float whl_pls_cntr_rr                               = 38; // Comment:    Unit: NA
        bool whl_pls_cntr_rr_vld                            = 39; //  
        EnumMotionCtrlInfoShifterPostnSts shifter_postn_sts = 40; //  
        bool shifter_postn_sts_vld                          = 41; //  
        bool arb_prk_butn_sts                               = 42; // 0: ARBPRKBUTNSTS_NOT_PRESSED 1: ARBPRKBUTNSTS_PRESSED
        bool arb_prk_butn_sts_vld                           = 43;
        float bcu_veh_spd                                   = 44; // Comment:    Unit: km/h
        bool bcu_veh_spd_sts                                = 45; //  
        EnumVehMovDir veh_mov_dir                           = 46; //  
        uint64 vehspd_asild_tv_ns                           = 59; // Comment:    Unit: km/h
        uint64 whlspd_tv_ns                                 = 60; // Comment:     Unit: km/h
        uint64 tv_ns                                        = 61; // Comment:    Unit: km/h
        bool spin_sts_fl                                    = 62; // false-无打滑；true-打滑
        bool spin_sts_fr                                    = 63; // false-无打滑；true-打滑
        bool spin_sts_rl                                    = 64; // false-无打滑；true-打滑
        bool spin_sts_rr                                    = 65; // false-无打滑；true-打滑
        bool spin_sts_fl_validity                           = 66; // spin_sts_fl信号有效性
        bool spin_sts_fr_validity                           = 67; // spin_sts_fr信号有效性
        bool spin_sts_rl_validity                           = 68; // spin_sts_rl信号有效性
        bool spin_sts_rr_validity                           = 69; // spin_sts_rr信号有效
        float peuf_bearing_temp_calc                        = 70; // Unit: ℃
    }
    
    enum EnumMotionCtrlInfoAvhSts {
        MCIAVHSTS_FAILURE      = 0;
        MCIAVHSTS_STANDBY      = 1;
        MCIAVHSTS_ACTIVE       = 2;
        MCIAVHSTS_OFF          = 3;
    }
    
    enum EnumMotionCtrlInfoEpbSts {
        MCIEPBSTS_UNKNOW        = 0;
        MCIEPBSTS_EPB_APPLIED   = 1;
        MCIEPBSTS_EPB_RELEASING = 2;
        MCIEPBSTS_EPB_RELEASED  = 3;
        MCIEPBSTS_EPB_APPLYING  = 4;
    }
    
    enum EnumMotionCtrlInfoActGear {
        MCIACTGEAR_PARKING      = 0;
        MCIACTGEAR_REVERSE      = 1;
        MCIACTGEAR_NEUTRAL      = 2;
        MCIACTGEAR_DRIVE        = 3;
    }
    
    enum EnumVehMovDir {
        VEHMOVDIR_STANDSTILL = 0;
        VEHMOVDIR_FORWARD    = 1;
        VEHMOVDIR_BACKWARD   = 2;
        VEHMOVDIR_INVALID    = 3;
    }
    
    enum EnumWhlSpdDir {
        WHLSPDDIR_STANDSTILL = 0;
        WHLSPDDIR_FORWARD    = 1;
        WHLSPDDIR_BACKWARD   = 2;
        WHLSPDDIR_INVALID    = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFl {
        MCIWHLSPDSTSFL_INITIALIZATION = 0;
        MCIWHLSPDSTSFL_VALID          = 1;
        MCIWHLSPDSTSFL_INVALID        = 2;
        MCIWHLSPDSTSFL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsFr {
        MCIWHLSPDSTSFR_INITIALIZATION = 0;
        MCIWHLSPDSTSFR_VALID          = 1;
        MCIWHLSPDSTSFR_INVALID        = 2;
        MCIWHLSPDSTSFR_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRl {
        MCIWHLSPDSTSRL_INITIALIZATION = 0;
        MCIWHLSPDSTSRL_VALID          = 1;
        MCIWHLSPDSTSRL_INVALID        = 2;
        MCIWHLSPDSTSRL_RESERVED       = 3;
    }
    
    enum EnumMotionCtrlInfoWhlSpdStsRr {
        MCIWHLSPDSTSRR_INITIALIZATION = 0;
        MCIWHLSPDSTSRR_VALID          = 1;
        MCIWHLSPDSTSRR_INVALID        = 2;
        MCIWHLSPDSTSRR_RESERVED       = 3;
    }

    enum EnumMotionCtrlInfoShifterPostnSts {
        MCISHIFTERPOSTNSTS_NO_REQUEST      = 0;
        MCISHIFTERPOSTNSTS_GEAR_R_REQUEST  = 1;
        MCISHIFTERPOSTNSTS_GEAR_NR_REQUEST = 2;
        MCISHIFTERPOSTNSTS_GEAR_ND_REQUEST = 3;
        MCISHIFTERPOSTNSTS_GEAR_D_REQUEST  = 4;
    }
    
    enum EnumMotionCtrlInfoHdcSts {
        MCIHDCSTS_OFF          = 0;
        MCIHDCSTS_FAILURE      = 1;
        MCIHDCSTS_STANDBY      = 2;
        MCIHDCSTS_ACTIVE       = 3;
    }
    
    message VafInfo {
        bool abs_actv                    = 1;
        bool tcs_vdc_actv                = 2;
        EnumMotionCtrlInfoAvhSts avh_sts = 3;
        EnumMotionCtrlInfoEpbSts epb_sts = 4;
        bool abs_fail_sts                = 5;
        bool epb_fail_sts                = 6;
        EnumMotionCtrlInfoHdcSts hdc_sts = 7;
        bool cdp_actv                    = 8;
        bool dtc_actv                    = 9;
        bool arp_actv                   = 10;
        bool over_heat_sts              = 11;
        bool tcs_vdc_fail_sts           = 12;
        bool tcs_mod_sts                = 13;
        bool vdc_mod_sts                = 14;
        bool dtc_avl                    = 15;
        bool cdp_avl                    = 16;
        uint64 tv_ns                    = 17;
        bool vdc_actv                   = 18;
    }
    
    message MotionInfoMonitorType {
        float tq_cmd_fa          = 1; // Unit: NA
        float brk_fx_trq_total   = 2; // Unit: NA
        uint32 brk_fx_mod_total  = 3;
        uint32 brk_fx_type_total = 4;
        uint32 rbu_brk_fx_sts    = 5;
        uint32 brk_fx_sts_main   = 6;
        uint32 brk_fx_sts_rdnt   = 7;
    }
    
    service MotionCtrlInfo {
        option(service_id) = 50004;
    
        rpc IfCommInfo(MotionCommInfo) returns (Null) {
            option (rpc_id) = 100;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
        }
    
        rpc IfVafInfo(VafInfo) returns (Null) {
            option (rpc_id) = 101;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
        }
    
        rpc MotionInfoMonitor(MotionInfoMonitorType) returns (Null) {
            option (rpc_id) = 102;
            option (method_type) = EVENT;
            option (update_policy) = CYCLIC;
            option (update_cycle_time) = 20;
        }
    }
    ```

### 实现方案

- Step1：开发脚本，扫描出软件模块中使用到的所有服务接口信号，按照接口类型分类。具体内容包含：
	- 域名：package_name
	- 服务名：service_name
	- 实例名：instance_name
	- 接口名：rpc_name
	- 接口类型：interface_type
		- event_sub
		- FF_REQ
		- RR_REQ
		- field_set
	- 信号名：signal_name
		- 结构体嵌套：仅保留第一层信号
		- 数组：仅保留信号名，无索引信息
- Step2：提取完成后，基于原生的平台服务IDL，自动生成client端的VMBC接口IDL文件，映射关系如下：

        软件模块

        role

        package_name

        service_id

        service_name

        instance_name

        rpc_name

        signal_type

        signal_name

        嵌套数据类型

        平台服务IDL

        DoorOpenMgr

        client

        srv.motion.drv

        5003

        相同

        相同

        相同

        相同

        相同

        相同

        VMBC接口IDL

        DoorOpenMgr

        client

        vmbc.dooropenmgr

        12200

        E2E配置

        reliable配置

        平台服务IDL

        有/无

        有/无

        VMBC接口IDL

        无

        无

        e2e_state

        connect_state

        VMBC接口IDL

        新增接口的element

        新增接口的element

- Step3：基于QoS部署配置信息，生成service端的VMBC接口IDL文件，映射关系如下：

        软件模块

        role

        package_name

        service_id

        service_name

        instance_name

        rpc_name

        signal_type

        signal_name

        嵌套数据类型

        平台服务IDL

        DoorOpenMgr

        service

        srv.body.entry

        5003

        相同

        相同

        相同

        相同

        相同

        相同

        VMBC接口IDL

        DoorOpenMgr

        service

        vmbc.entry

        12200

        E2E配置

        reliable配置

        平台服务IDL

        有/无

        有/无

        VMBC接口IDL

        无

        无

        无queue配置

        有queue配置

        VMBC接口IDL

        message

        message[queue_size]

- Step4：生成的service和client端的VMBC接口IDL，按平台软件版本推送至VAS proto仓库对应的分支

## 全局变量（motion域）

### 概念

motion域应用软件与SOA完全解耦，应用软件使用全局变量与SOA Adaptor交互。

- SOA Adaptor将应用软件依赖的外部服务接口信号转成全局变量，motion软件去读
- motion软件写入全局变量的数据，通过SOA Adaptor转发为服务接口，供其他域软件调用

对于S2S mapping场景，中间件支持CAN/LIN/DE信号与全局变量双向转发。

### 设计思路

应用软件的实现没有client或service的概念，只有数据接收和数据发送的概念。

应用软件通过读全局变量实现数据接收，通过写全局变量实现数据发送。

### 实现方案

基于共享内存的全局变量解决方案，需要考虑以下几个关键点：

- 每个全局变量只能有一个写者：两个不同的软件模块不能同时写同一个全局变量
- 全局变量不使用结构体或数组：确保原子读写，避免写到一半被读、没有一致性保证

SOA Adaptor根据应用软件中各个runnable使用全局变量的情况，把接收到的SOA接口信号转发成全局变量给应用软件使用，把应用软件写入的全局变量转发成SOA接口发送出去。

对于S2S mapping场景，按照业务需求，除了实现CAN/LIN信号与全局变量的双向转发外，也需要支持转成服务接口，具体使用场景如下：

- 仅转成全局变量：信号只有本控制器内的motion软件模块使用
- 同时转成全局变量和服务接口：信号除转成全局变量供本地motion软件模块用外，还要被其他域软件模块使用
- 仅转成服务接口：信号只有其他域软件模块使用，如uss信号

#### G2S mapping

**G2S：Global variable to Service mapping**

通过表格形式维护模块全局变量和服务接口信号之间的mapping关系。**每个软件模块一个表格**，表格模板如下：

      package_name

      service_name

      instance_name

      rpc_name

      rpc_type

      trigger_type

      message_in

      message_out

      schedule

      ASIL

      message_signal

      signal_type

      signal_order

      property

      variables

      variable_type

      srv.motion.drv

      WhlSpdSnsr

      IfWhlSpdVal

      EVENT

      sub

      WhlSpdVal

      5ms

      QM

      WhlSpdVal.hspr_vwhlflpulse

      uint8

      3

      output

      LSV_hspr_vwhlflpulse

      uint8

      srv.motion.drv

      VehSpdBrdcst

      VehSpdBrdcstPri

      IfVehSpdSrlData

      FIELD_WRITABLE

      set

      VehSpdSrlData

      10ms

      C

      VehSpdSrlData.veh_spd_slp

      float

      5

      input

      VME_vVehSpdSlp

      single

      srv.motion.drv

      UserVirtualBrk

      IfBrkCtrlModArb

      FIELD_WRITABLE

      sub

      BrkSrvParArrayType

      10ms

      QM

      BrkSrvParArrayType.brk_pedl_mod_req

      EnumBrkPedlModReq

      11

      output

      LSV_brk_pedl_mod_req

      uint8

根据软件模块在各个控制器core的部署情况，G2S mapping表格，生成SOA adaptor代码，完成服务接口信号和全局变量互转。

G2S mapping表中字段信息如下：

- 服务信息
	- 包含package_name、service_name、instance_name、rpc_name、rpc_type、message_in、message_out、message_signal、signa_type、signal_order等
	- 这些信息都可以从平台服务IDL文件中获取，所有信号平铺
- 扩展服务信息
	- trigger_type：消息触发类型
		- sub：作为client订阅某个服务信号
		- pub：作为server发布某个服务信号
		- set：作为client去set某个服务信号
		- get：作为client去get某个服务信号
		- req：作为client去请求某个服务信号
		- on_req：作为server接收某个服务请求信号
		- on_set：作为server接收某个服务set信号
		- on_get：作为server接收某个服务get信号
	- schedule：信号使用方的调度周期
	- ASIL：信号的功能安全信息
- 全局变量信息
	- property：对SOA Adaptor来说，全局变量是读还是写
		- input：软件模块写，SOA Adaptor读
		- output：SOA Adaptor写，软件模块读
	- variables：全局变量名
	- variable_type：全局变量数据类型

**全局变量定义方**：

- SOA Adaptor写，软件模块读的全局变量，由SOA Adaptor定义，软件模块引用；
- 软件模块写，SOA Adaptor读的全局变量，由软件模块定义，SOA Adaptor引用。

#### Sig2G mapping

**Sig2G：Signal to Global variable mapping**

通过表格形式维护全局变量和CAN/LIN/DE信号间的mapping关系。

**全局变量维护颗粒度**：

- 如果该信号已有原子服务mapping，则以原子服务颗粒度进行全局变量定义；
- 如果该信号无原子服务mapping，则以使用相关信号的软件模块的颗粒度进行全局变量定义。

Sig2G mapping表在现有S2S mapping表的基础上进行扩展。主要扩展字段如下：

- Sig2G_req：信号属性
	- 需要转全局变量：Y
	- 不需要转全局变量：N（默认）
- Variables：全局变量名
- Variable_type：全局变量类型
- Property：全局变量读写方向
	- input：应用软件写，Sig2G软件读
	- output：Sig2G软件写，应用软件读
- Schedule：对于未mapping服务的信号，需要在全局变量侧，标记全局变量使用的调度周期需求
	- xx ms：表示该全局变量需要被xx ms的runnable调度或使用
- SW_module：使用全局变量的软件模块名称
	- 仅在信号未mapping服务的场景下，需要填写该字段

**全局变量定义方**：

- Sig2G写，软件模块读的全局变量，由Sig2G定义，软件模块引用；
- 软件模块写，Sig2G读的全局变量，由软件模块定义，Sig2G引用。

#### 功能安全设计

在同安全等级的两个软件模块间共享全局变量，是符合安全规范的。

在不同安全等级的两个软件模块间共享全局变量，需要遵循跨安全等级通信规范：

- 高安全等级软件模块可以读写低安全等级软件模块定义的全局变量
- 低安全等级软件模块只能读高安全等级软件模块定义的全局变量，不能写入

      请求方等级

      可写入目标等级

      限制条件

      ASILD

      ASILD, ASILB, QM

      无特殊限制

      ASILB

      ASILB, QM

      禁止写ASILD的全局变量

      QM

      QM

      禁止写ASILB/ASILD资源

## SOA Adaptor

### 概念

SOA Adaptor是实现VMBC应用软件间、VMBC应用软件与外域软件间SOA通信的平台中间件。

SOA Adaptor实现两类功能：

- 实现平台服务与VMBC接口之间的互转
- 实现平台服务与全局变量之间的互转

### 设计思路

SOA Adaptor的设计约束：

- 需要兼容ZONE、VDF-M、VDF-A等部署场景
- 需要兼容ECU内部通信、ECU间tox通信等通信场景
- 需要兼容基于IDL和基于全局变量的数据输入输出需求
- 支持不同功能安全等级的软件模块的数据通信和访问隔离
- 支持应用软件灵活部署
- 支持应用软件与SOA框架、配置和平台服务IDL基线解耦

ZONE上部署形态:

- 每个core都部署soa_adpt软件模块
- 按QM、ASIL-B、ASIL-D部署三个soa_adpt软件模块，满足同安全等级应用软件数据访问和混合调度需求

VDF MCore部署形态：

- 每个core都部署soa_adpt软件模块
- 按QM、ASIL-B部署两个soa_adpt软件模块，满足同安全等级应用软件数据访问和混合调度需求

VDF ACore部署形态：

- soa_adpt作为独立的进程部署
- 部署normal和urgent两个进程，urgent进程为强实时、功能安全E2E通信需求单独设计，进程优先级高

在应用软件灵活部署、SOA框架隔离、全局变量&IDL混合通信等需求下：

- 应用软件间交互，不论ECU内还是ECU间，都经过SOA Adaptor转发
- server端的一些特殊情况，可以不经过SOA Adaptor转发
	- 仅local本地通信的原子服务，例如所有sd服务
	- 基于S2S mapping自动生成代码的所有原子服务

### 实施方案

#### ZONE部署的soa_adpt

##### 基于IDL通信交互

###### 软件架构

###### 配置管理

通过表格管理平台服务IDL与VMBC接口IDL间的映射关系，结合部署、调度信息，生成soa_adpt软件代码。

需要管理的配置信息包括：

- 平台服务IDL信息
- 软件模块部署配置信息
- 软件调度信息
- 软件模块信号使用信息
- 是否判断服务连接状态
- 是否处理soa error
- 是否关心e2e state
- 是否超时重传
	- 超时时间
	- 重传次数

具体配置信息表应如下：

      配置信息类

      字段

      含义

      配置选项

      软件模块信息

      component_name

      service_package

      service_name

      service_instance_name

      role

      client_id

      qos_method_request_name

      qos_method_e2e_client_ids

      qos_method_history_depth_request

      qos_method_history_depth_set

      qos_event_request_name

      qos_event_history_depth

      rpc_custom_method_request_name

      rpc_custom_method_disable_callback

      rpc_custom_method_generate_get

      rpc_custom_method_generate_set

      rpc_custom_method_generate_request

      rpc_custom_event_request_name

      rpc_custom_event_subscribe

      rpc_custom_event_disable_callback

      ECU

      Core

      ASIL_Level

      软件调度信息

      Runnable_Name

      Schedule

      平台服务IDL信息

      InterfaceType

      DataTypeName

      DataType

      StructMemberPosition

      SubDataTypeName

      SubDataType

      StrMemName

      SubStrMemName

      SubStrElemtType

      服务连接状态

      connection_state_used

      soa error处理策略

      soa_error_used

      e2e state处理策略

      e2e_state_used

      RR retry策略

      RR_timeout

      retry_count

基于上述维护的信息，需要自动生成下列文件：

- VMBC接口文件IDL，详细参考2.2节
- soa_adpt软件代码
- soa_adpt软件的SOA deployment文件
- soa_adpt的调度配置信息

###### 代码生成

####### 代码结构

soa_adpt软件代码结构为：

- soa_adpt_qm
	- a2l
	- cfg
	- inc
		- soa_adpt_qm.h
	- lib
	- proto
	- src
		- soa_adpt_qm_adaptor.c
		- soa_adpt_qm.c
	- CMakelists.txt
	- app.json
	- ntxpkg.yml
	- swc_runnable.json
  
- soa_adpt_asilb
	- 同上
  
- soa_adpt_asild
	- 同上

####### 代码生成规则

需要考虑所有RPC接口类型的所有使用场景，具体场景穷举如下：

      role

      rpc类型

      API

      数据流向

      soa_adpt client

      soa_adpt server

      应用软件

      client

      EVENT

      sm_read_on_notify

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      sm_read_on_e2e_state

      E2E

      Y

      optional

      sm_get_queue_num

      History queue

      Y

      optional

      RR_METHOD

      sm_send_req

      发送

      Y

      sm_read_on_request

      sm_write_request

      sm_recv_resp

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      optional

      FF_METHOD

      sm_write_request

      发送

      Y

      sm_read_on_request

      sm_write_request

      FIELD_READONLY

      sm_read_on_notify

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      sm_read_on_e2e_state

      E2E

      Y

      optional

      sm_get_queue_num

      History queue

      Y

      optional

      sm_send_req_get

      发送

      Y

      trigger

      optional

      sm_recv_resp_get

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      optional

      FIELD_WRITABLE

      sm_read_on_notify

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      sm_read_on_e2e_state

      E2E

      Y

      optional

      sm_get_queue_num

      History queue

      Y

      optional

      sm_write_set

      发送

      Y

      sm_read_on_request

      sm_write_request

      sm_send_req_get

      发送

      Y

      trigger

      optional

      sm_recv_resp_get

      接收

      Y

      sm_write_notify

      sm_read_on_notify

      optional

      sm_read_on_connect_state

      Connection state

      Y

      sm_write_notify

      sm_read_on_notify

      optional

      sm_read_on_soa_error

      SOA error

      Y

      sm_write_notify

      sm_read_on_notify

      optional

      service

      EVENT

      sm_write_notify

      发送

      sm_read_on_notify

      Y

      sm_write_notify

      RR_METHOD

      sm_recv_on_req

      接收

      sm_write_request

      Y

      sm_read_on_request

      sm_get_queue_num

      History queue

      Y

      optional

      sm_send_resp

      发送

      sm_read_on_notify

      Y

      sm_write_notify

      FF_METHOD

      sm_read_on_request

      接收

      sm_write_request

      Y

      sm_read_on_request

      sm_read_on_e2e_state

      E2E

      Y

      optional

      sm_get_queue_num

      History queue

      Y

      optional

      FIELD_READONLY

      sm_write_notify

      发送

      sm_read_on_notify

      Y

      sm_write_notify

      sm_recv_req_on_get

      接收

      replace_get_with_cache
      初始化时notify一次

      optional

      sm_send_resp_on_get

      发送

      optional

      FIELD_WRITABLE

      sm_write_notify

      发送

      sm_read_on_notify

      Y

      sm_write_notify

      sm_read_on_set

      接收

      sm_write_request

      Y

      sm_read_on_request

      sm_read_on_e2e_state

      E2E

      Y

      optional

      sm_get_queue_num

      History queue

      Y

      optional

      sm_recv_on_get

      接收

      replace_get_with_cache
      初始化时notify一次

      optional

      sm_send_resp_on_get

      发送

      optional

      sm_read_on_soa_error

      SOA error

      sm_write_notify

      Y

      sm_read_on_notify

      optional

代码生成规则：

- 由soa_adpt替代实现原应用软件client的所有接口（对外，使用平台IDL生成）
- 由soa_adpt替代实现原应用软件server的所有接口（对外，使用平台IDL生成）
- soa_adpt与应用软件间基于VMBC自定义接口IDL生成相应接口

###### 软件调度

在通信时延不恶化的前提下，为确保不同功能安全等级应用软件的数据收发需求，需要在soa_adpt软件代码中：

- 按照数据接收和数据发送分别生成runnable函数
- 数据收和数据发的runnable函数调度周期与应用软件runnable保持一致
- 根据应用软件的ASIL等级，相应数据收和数据发的runnable函数生成在对应ASIL等级的soa_adpt软件模块
- soa_adaptor_xxx.c代码中，引用应用软件的头文件

为了不增加调度配置的复杂度，在soa_adpt软件模块中对runnable进行二次封装（如下图中的方案2），将数据收、应用软件处理、数据发的runnable封装在一个runnable函数里，封装后的runnable函数作为调度配置管理的最小颗粒度。

举例说明：

- 应用软件有10ms runnable：`MOTsrcctrl_task_10ms`
- MOTsrcCtrl软件的功能安全为QM
- soa_adpt_qm软件模块中根据`MOTsrcctrl_task_10ms`的数据收发需求，生成`motsrcctrl_10ms_in`和`motsrcctrl_10ms_out`两个runnable函数
- soa_adpt_qm软件代码中，生成`motsrcctrl_10ms`函数，在函数中依次调用`motsrcctrl_10ms_in`、`MOTsrcctrl_task_10ms`和`motsrcctrl_10ms_out`
- soa_adpt_qm.c引用MotsrcCtrl的头文件
- `motsrcctrl_10ms`作为调度配置的输入

##### 基于全局变量通信交互

###### 软件架构

###### 配置管理

通过表格管理平台服务IDL与全局变量间的映射关系（DD表），结合部署、调度等信息，生成soa_adpt软件代码。

需要管理的配置信息包括：

- 平台服务IDL信息
- 软件模块部署配置信息
- 软件调度信息
- 软件模块信号使用信息
- 全局变量信息
- 是否判断服务连接状态
- 是否处理soa error
- 是否关心e2e state
- 是否超时重传
	- 超时时间
	- 重传次数

具体配置信息表应如下：

      配置信息类

      字段

      含义

      配置选项

      软件模块信息

      component_name

      service_package

      service_name

      service_instance_name

      role

      client_id

      qos_method_request_name

      qos_method_e2e_client_ids

      qos_method_history_depth_request

      qos_method_history_depth_set

      qos_event_request_name

      qos_event_history_depth

      rpc_custom_method_request_name

      rpc_custom_method_disable_callback

      rpc_custom_method_generate_get

      rpc_custom_method_generate_set

      rpc_custom_method_generate_request

      rpc_custom_event_request_name

      rpc_custom_event_subscribe

      rpc_custom_event_disable_callback

      ECU

      Core

      ASIL_Level

      软件调度信息

      Runnable_Name

      Schedule

      平台服务IDL信息

      InterfaceType

      DataTypeName

      DataType

      StructMemberPosition

      SubDataTypeName

      SubDataType

      StrMemName

      SubStrMemName

      SubStrElemtType

      全局变量信息

      Variables

      全局变量名

      Property

      流向

      input/output/Mapping

      Attribute

      变量类型

      基础数据类型
      非结构体

      ASIL_Level

      服务连接状态

      connection_state_used

      soa error处理策略

      soa_error_used

      e2e state处理策略

      e2e_state_used

      RR retry策略

      RR_timeout

      retry_count

基于上述维护的信息，需要自动生成下列文件：

- soa_adpt软件代码
- soa_adpt软件的SOA deployment文件
- soa_adpt的调度配置信息

###### 代码生成

####### 代码结构

soa_adpt软件代码结构同2.4.3.1.1.3.1节。

####### 代码生成规则

需要考虑所有RPC接口类型的所有使用场景，具体场景穷举如下：

      role

      rpc类型

      API

      数据流向

      soa_adpt

      应用软件

      client

      EVENT

      sm_read_on_notify

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_read_on_e2e_state

      E2E状态接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      RR_METHOD

      sm_send_req

      发送

      - 引用应用软件头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      sm_recv_resp

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      FF_METHOD

      sm_write_request

      发送

      - 引用应用软件头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      FIELD_READONLY

      sm_read_on_notify

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_read_on_e2e_state

      E2E状态接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_send_req_get

      发送

      - 引用应用软件头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      optional

      sm_recv_resp_get

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      FIELD_WRITABLE

      sm_read_on_notify

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_read_on_e2e_state

      E2E状态接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_write_set

      发送

      - 引用应用软件头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      sm_send_req_get

      发送

      - 引用应用软件头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      optional

      sm_recv_resp_get

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_read_on_connect_state

      Connection state接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_read_on_soa_error

      SOA error接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      service

      EVENT

      sm_write_notify

      发送

      - 引用soa_adpt头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      RR_METHOD

      sm_recv_on_req

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_send_resp

      发送

      - 引用soa_adpt头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      optional

      FF_METHOD

      sm_read_on_request

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_read_on_e2e_state

      E2E状态接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      FIELD_READONLY

      sm_write_notify

      发送

      - 引用soa_adpt头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      sm_recv_req_on_get

      接收

      replace_get_with_cache
      初始化时notify一次

      optional

      sm_send_resp_on_get

      发送

      optional

      FIELD_WRITABLE

      sm_write_notify

      发送

      - 引用soa_adpt头文件
			- 全局变量只读

      - 定义全局变量
			- 写入全局变量

      sm_read_on_set

      接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      sm_read_on_e2e_state

      E2E状态接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_get_queue_num

      History queue接收

      - 定义全局变量，每个维度对应一个全局变量，确保原子操作
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

      sm_recv_on_get

      接收

      replace_get_with_cache
      初始化时notify一次

      optional

      sm_send_resp_on_get

      发送

      optional

      sm_read_on_soa_error

      SOA error接收

      - 定义全局变量
			- 写入全局变量

      - 引用soa_adpt头文件
			- 全局变量只读

      optional

代码生成规则：

- 由soa_adpt替代实现原应用软件client的所有接口（对外，使用平台IDL生成）
- 由soa_adpt替代实现原应用软件server的所有接口（对外，使用平台IDL生成）
- soa_adpt与应用软件间基于全局变量通信，基于配置表生成相应代码

###### 软件调度

在通信时延不恶化的前提下，为确保不同功能安全等级应用软件的数据收发需求，需要在soa_adpt软件代码中：

- 按照数据接收和数据发送分别生成runnable函数
- 数据收和数据发的runnable函数调度周期与应用软件runnable保持一致
- 根据应用软件的ASIL等级，相应数据收和数据发的runnable函数生成在对应ASIL等级的soa_adpt软件模块
- soa_adaptor_xxx.c代码中，引用应用软件的头文件，反之亦然

为了不增加调度配置的复杂度，在soa_adpt软件模块中对runnable进行二次封装（如下图中的方案2），将数据收、应用软件处理、数据发的runnable封装在一个runnable函数里，封装后的runnable函数作为调度配置管理的最小颗粒度。

举例说明：

- 应用软件有10ms runnable：`MOTsrcctrl_task_10ms`
- MOTsrcCtrl软件的功能安全为QM
- soa_adpt_qm软件模块中根据`MOTsrcctrl_task_10ms`的数据收发需求，生成`motsrcctrl_10ms_in`和`motsrcctrl_10ms_out`两个runnable函数
- soa_adpt_qm软件代码中，生成`motsrcctrl_10ms`函数，在函数中依次调用`motsrcctrl_10ms_in`、`MOTsrcctrl_task_10ms`和`motsrcctrl_10ms_out`
- soa_adpt_qm.c引用MotsrcCtrl的头文件
- `motsrcctrl_10ms`作为调度配置的输入

#### VDF MCore部署的soa_adpt

在VDF MCore部署的soa_adpt与在ZONE部署的基于IDL通信交互的soa_adpt，在实现上保持一致。

具体参考2.4.3.1.1的实现方案。

#### VDF ACore部署的soa_adpt

##### 软件架构

VDF ACore的soa_adpt进程实现及软件架构，强依赖于高效率的进程间通信IPC框架，以实现TOX通信domain与进程间通信domain的隔离。

soa_adpt作为独立进程，同时接入TOX通信domain与进程间通信domain。

- 在TOX通信domain，基于平台基线IDL通信；
- 在进程间通信domain，基于VMBC自定义IDL通信。

在进程间通信domain，soa_adpt进程与vmbc业务进程，采用进程间通信IPC框架通信；

在TOX通信domain，soa_adpt进程与其他业务进程采用TOX通信，与其他ECU上的应用软件采用TOX通信。

强依赖高效率的进程间通信IPC框架，否则失去了soa adaptor的意义

A核原生软件开发模式：NT3.5对软件开发模式进行重构，目标是优化整体cpu占用

CPU效率高的应用，核心原则是：

- 事件驱动
- 避免忙等
- 减少不必要的上下文切换

##### 配置管理

##### 代码生成

###### 代码结构

###### 代码生成规则

##### 软件调度

## Sig2G实现

从实施层面，Sig2G就是要将应用软件需要的所有信息，从上行信号转为全局变量；或将应用软件产生的数据写入全局变量后，转为下行信号。具体包括：

- 上行
	- CAN/LIN报文信号转换为全局变量
	- DE信号转换为全局变量
	- CAN/LIN冗余报文信号转换为全局变量
	- 信号有效性标志位转换为全局变量
- 下行
	- 全局变量转换为CAN/LIN报文信号
	- 全局变量转换为DE信号
	- 全局变量转换为CAN/LIN冗余报文信号

对于信号转成的全局变量，全部采用单一数据类型（非结构体）形式，以确保所有全局变量的写入都是原子操作。

- 上行的全局变量，在中间件侧定义，由中间件写入，应用软件只读；
- 下行的全局变量，由应用软件定义并写入，中间件只读。

具体Sig2G配置管理表见2.3.3.2节。

Sig2G mapping在维护过程中，需要针对具体情况具体分析，相比于使用VMBC自定义服务，主要的风险是要确保全局变量无竞争（仅有一个写者），具体可以有多种实现方案。
