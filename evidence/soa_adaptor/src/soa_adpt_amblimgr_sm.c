#include "soa_adpt_amblimgr_sm.h"
#include "soa_adpt_amblimgr_af_api.h"
#include <string.h>
static int read_connection(void *ctx,SoaEndpoint id,SoaConnection *out) { SoaSmBindings *b=ctx; return b->read_connection(b->context,id,out); }
static int read_error(void *ctx,SoaEndpoint id,SoaBridgeError *out) { SoaSmBindings *b=ctx; return b->read_error(b->context,id,out); }
static int read_e2e_health(void *ctx,SoaRxChannel id,SoaSampleInfo *out) {
#if SOA_MOTION_E2E_STATE_USED
    SoaSmBindings *b=ctx;
    if (id!=SOA_RX_MOTIONCTRLINFO_IFCOMMINFO || !b->motion_e2e_report_supported) return SOA_IO_NOT_READY;
    sm_e2e_state_t state={0};
    int raw=sm_read_soa_adpt_amblimgr_on_e2e_state_srv_motion_drv_motionctrlinfo_motionctrlinfopri_ifcomminfo(b->component_id,&state);
    int result=b->classify(raw,true);out->raw_error=raw;
    if (result==SOA_IO_OK) {out->raw_e2e_known=true;out->raw_e2e=(int32_t)state.status;}
    return result;
#else
    (void)ctx;(void)id;(void)out;return SOA_IO_NOT_READY;
#endif
}
static int read_DriveModeMgr_DriveModeSts(void *ctx,srv_vehctl_scnmgr_DriveModeMgrDta *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_vehctl_scnmgr_drivemodemgr_drivemodests_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_vehctl_scnmgr_drivemodemgr_drivemodests(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_DriveModeMgr_EcoPlusModeInfo(void *ctx,srv_vehctl_scnmgr_EcoPlusModeInfoDta *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_vehctl_scnmgr_drivemodemgr_ecoplusmodeinfo_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_vehctl_scnmgr_drivemodemgr_ecoplusmodeinfo(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_DynAmbLiActu_DynAmbLiSts(void *ctx,srv_body_intrlight_MsgDynAmbLiSts *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_body_intrlight_dynambliactu_dynamblists_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_body_intrlight_dynambliactu_dynamblists(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(void *ctx,srv_motion_drv_MotionCommInfo *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_motion_drv_motionctrlinfo_motionctrlinfopri_ifcomminfo_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_motion_drv_motionctrlinfo_motionctrlinfopri_ifcomminfo(b->component_id,&msg);
    int result=b->classify(raw,true);meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_RlsInfo_LightSnrSts(void *ctx,srv_body_base_MsgLightSnrSts *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_body_base_rlsinfo_lightsnrsts_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_body_base_rlsinfo_lightsnrsts(b->component_id,&msg);
    int result=b->classify(raw,true);meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_SeatBasicSts_SeatBasicStsArray(void *ctx,srv_body_safety_SeatBasicStatus *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_body_safety_seatbasicsts_seatbasicstsarray_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_body_safety_seatbasicsts_seatbasicstsarray(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(void *ctx,srv_body_smtkey_SmtKeyUsrIntnDataStruct *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_body_smtkey_smtkeyusrintnmgr_smtkeyusrintnnotify_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_body_smtkey_smtkeyusrintnmgr_smtkeyusrintnnotify(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_VehConfig_IVcpVal_VehicleProject(void *ctx,srv_vehicle_plm_VcpVal *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_vehicle_plm_vehconfig_ivcpval_vehicleproject_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_vehicle_plm_vehconfig_ivcpval_vehicleproject(b->component_id,&msg);
    int result=b->classify(raw,true); meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int read_VehState_VehStateInfo(void *ctx,srv_infra_vehmoding_VehStateMsg *out,SoaSampleInfo *meta) {
    SoaSmBindings *b=ctx; evt_msg_srv_infra_vehmoding_vehstate_vehstateinfo_t msg={0};
    int raw=sm_read_soa_adpt_amblimgr_on_notify_srv_infra_vehmoding_vehstate_vehstateinfo(b->component_id,&msg);
    int result=b->classify(raw,true);meta->raw_error=raw;
    if (result==SOA_IO_OK) *out=msg.event_msg;
    return result;
}
static int send_DynAmbLiActu_DynEnaCtrl(void *ctx,const srv_body_intrlight_MsgDynEnaCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dynenactrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dynenactrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_DynAmbLiActu_DynSegCtrl(void *ctx,const srv_body_intrlight_MsgDynSegCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dynsegctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dynsegctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_DynAmbLiActu_DynNodeCtrl(void *ctx,const srv_body_intrlight_MsgDynNodeCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dynnodectrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dynnodectrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_DynAmbLiActu_DynGenBriCtrl(void *ctx,const srv_body_intrlight_MsgDynGenBriCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dyngenbrictrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dyngenbrictrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_DynAmbLiActu_DynPrmSet(void *ctx,const srv_body_intrlight_MsgDynPrmSet *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dynprmset_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dynprmset(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_DynAmbLiActu_DynSeqPilot(void *ctx,const srv_body_intrlight_MsgDynSeqPilot *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_dynambliactu_dynseqpilot_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_dynambliactu_dynseqpilot(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(void *ctx,const srv_body_intrlight_MsgStaEnaCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staenactrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliap_staenactrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(void *ctx,const srv_body_intrlight_MsgStaEnaCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staenactrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblifw_staenactrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(void *ctx,const srv_body_intrlight_MsgStaEnaCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staenactrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliip_staenactrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(void *ctx,const srv_body_intrlight_MsgStaEnaCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staenactrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblistorg_staenactrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(void *ctx,const srv_body_intrlight_MsgStaColorCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stacolorctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliap_stacolorctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(void *ctx,const srv_body_intrlight_MsgStaColorCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stacolorctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblifw_stacolorctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(void *ctx,const srv_body_intrlight_MsgStaColorCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stacolorctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliip_stacolorctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(void *ctx,const srv_body_intrlight_MsgStaColorCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stacolorctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblistorg_stacolorctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(void *ctx,const srv_body_intrlight_MsgStaGenBriCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stagenbrictrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblifw_stagenbrictrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(void *ctx,const srv_body_intrlight_MsgStaNodeBriCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stanodebrictrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliap_stanodebrictrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(void *ctx,const srv_body_intrlight_MsgStaNodeBriCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stanodebrictrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliip_stanodebrictrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(void *ctx,const srv_body_intrlight_MsgStaNodeBriCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_stanodebrictrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblistorg_stanodebrictrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(void *ctx,const srv_body_intrlight_MsgStaPrmCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staprmctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliap_staprmctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(void *ctx,const srv_body_intrlight_MsgStaPrmCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staprmctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblifw_staprmctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(void *ctx,const srv_body_intrlight_MsgStaPrmCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staprmctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staambliip_staprmctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
static int send_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(void *ctx,const srv_body_intrlight_MsgStaPrmCtrl *input) {
    SoaSmBindings *b=ctx; req_msg_srv_body_intrlight_staambliactu_staprmctrl_t msg={0}; msg.request_msg=*input;
    int raw=sm_write_soa_adpt_amblimgr_request_srv_body_intrlight_staambliactu_staamblistorg_staprmctrl(b->component_id,&msg);
    int result=b->classify(raw,false);
    return result==SOA_IO_OK ? SOA_IO_OK : (raw==0 ? SOA_IO_FAILURE : raw);
}
bool SoaAdaptorSm_MakePlatformPort(SoaSmBindings *b,SoaPlatformPort *p) {
    if (!b || !p || !b->classify || !b->read_connection || !b->read_error) return false;
    memset(p,0,sizeof(*p)); p->context=b;
    p->read_connection=read_connection; p->read_error=read_error; p->read_e2e_health=read_e2e_health;
    p->read_DriveModeMgr_DriveModeSts=read_DriveModeMgr_DriveModeSts;
    p->read_DriveModeMgr_EcoPlusModeInfo=read_DriveModeMgr_EcoPlusModeInfo;
    p->read_DynAmbLiActu_DynAmbLiSts=read_DynAmbLiActu_DynAmbLiSts;
    p->read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo=read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo;
    p->read_RlsInfo_LightSnrSts=read_RlsInfo_LightSnrSts;
    p->read_SeatBasicSts_SeatBasicStsArray=read_SeatBasicSts_SeatBasicStsArray;
    p->read_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify=read_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify;
    p->read_VehConfig_IVcpVal_VehicleProject=read_VehConfig_IVcpVal_VehicleProject;
    p->read_VehState_VehStateInfo=read_VehState_VehStateInfo;
    p->send_DynAmbLiActu_DynEnaCtrl=send_DynAmbLiActu_DynEnaCtrl;
    p->send_DynAmbLiActu_DynSegCtrl=send_DynAmbLiActu_DynSegCtrl;
    p->send_DynAmbLiActu_DynNodeCtrl=send_DynAmbLiActu_DynNodeCtrl;
    p->send_DynAmbLiActu_DynGenBriCtrl=send_DynAmbLiActu_DynGenBriCtrl;
    p->send_DynAmbLiActu_DynPrmSet=send_DynAmbLiActu_DynPrmSet;
    p->send_DynAmbLiActu_DynSeqPilot=send_DynAmbLiActu_DynSeqPilot;
    p->send_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl=send_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl;
    p->send_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl=send_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl;
    p->send_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl=send_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl;
    p->send_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl=send_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl;
    p->send_StaAmbLiActu_StaAmbLiAp_StaColorCtrl=send_StaAmbLiActu_StaAmbLiAp_StaColorCtrl;
    p->send_StaAmbLiActu_StaAmbLiFw_StaColorCtrl=send_StaAmbLiActu_StaAmbLiFw_StaColorCtrl;
    p->send_StaAmbLiActu_StaAmbLiIp_StaColorCtrl=send_StaAmbLiActu_StaAmbLiIp_StaColorCtrl;
    p->send_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl=send_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl;
    p->send_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl=send_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl;
    p->send_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl=send_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl;
    p->send_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl=send_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl;
    p->send_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl=send_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl;
    p->send_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl=send_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl;
    p->send_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl=send_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl;
    p->send_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl=send_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl;
    p->send_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl=send_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl;
    return true;
}
