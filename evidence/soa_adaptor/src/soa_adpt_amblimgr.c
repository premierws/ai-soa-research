#include "soa_adpt_amblimgr.h"
#include <stddef.h>
#include <string.h>
static SoaPlatformPort g_platform;
static SoaApplicationPort g_application;
static bool g_ready, g_running;
static uint32_t g_now;
#if SOA_MOTION_E2E_STATE_USED
static uint32_t g_motion_e2e_code;
#endif
static uint64_t g_command_sequence;
static SoaEndpointState g_endpoints[SOA_EP_COUNT];
static SoaRxState g_rx[SOA_RX_COUNT];
static bool g_endpoint_dirty[SOA_EP_COUNT], g_rx_dirty[SOA_RX_COUNT];
static SoaBridgeError g_errors[SOA_ERROR_DEPTH];
static unsigned g_error_head, g_error_count;
static SoaDiagnostics g_diagnostics;
static const SoaEndpoint k_rx_endpoint[SOA_RX_COUNT] = { SOA_EP_DRIVEMODEMGR, SOA_EP_DRIVEMODEMGR, SOA_EP_DYNAMBLIACTU, SOA_EP_MOTIONCTRLINFO_MOTIONCTRLINFOPRI, SOA_EP_RLSINFO, SOA_EP_SEATBASICSTS, SOA_EP_SMTKEYUSRINTNMGR, SOA_EP_VEHCONFIG, SOA_EP_VEHSTATE };
static vmbc_scnmgr_DriveModeMgrDta g_cache_DriveModeMgr_DriveModeSts;
static vmbc_scnmgr_EcoPlusModeInfoDta g_cache_DriveModeMgr_EcoPlusModeInfo;
static vmbc_intrlight_MsgDynAmbLiSts g_cache_DynAmbLiActu_DynAmbLiSts;
static vmbc_drv_MotionCommInfo g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo;
static vmbc_base_MsgLightSnrSts g_cache_RlsInfo_LightSnrSts;
static vmbc_safety_SeatBasicStatus g_cache_SeatBasicSts_SeatBasicStsArray;
static vmbc_smtkey_SmtKeyUsrIntnDataStruct g_cache_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify;
static vmbc_plm_VcpVal g_cache_VehConfig_IVcpVal_VehicleProject;
static vmbc_vehmoding_VehStateMsg g_cache_VehState_VehStateInfo;
static struct { vmbc_intrlight_MsgDynEnaCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynEnaCtrl;
static struct { vmbc_intrlight_MsgDynSegCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynSegCtrl;
static struct { vmbc_intrlight_MsgDynNodeCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynNodeCtrl;
static struct { vmbc_intrlight_MsgDynGenBriCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynGenBriCtrl;
static struct { vmbc_intrlight_MsgDynPrmSet data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynPrmSet;
static struct { vmbc_intrlight_MsgDynSeqPilot data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_DynAmbLiActu_DynSeqPilot;
static struct { vmbc_intrlight_MsgStaEnaCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl;
static struct { vmbc_intrlight_MsgStaEnaCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl;
static struct { vmbc_intrlight_MsgStaEnaCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl;
static struct { vmbc_intrlight_MsgStaEnaCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl;
static struct { vmbc_intrlight_MsgStaColorCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl;
static struct { vmbc_intrlight_MsgStaColorCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl;
static struct { vmbc_intrlight_MsgStaColorCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl;
static struct { vmbc_intrlight_MsgStaColorCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl;
static struct { vmbc_intrlight_MsgStaGenBriCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl;
static struct { vmbc_intrlight_MsgStaNodeBriCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl;
static struct { vmbc_intrlight_MsgStaNodeBriCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl;
static struct { vmbc_intrlight_MsgStaNodeBriCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl;
static struct { vmbc_intrlight_MsgStaPrmCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl;
static struct { vmbc_intrlight_MsgStaPrmCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl;
static struct { vmbc_intrlight_MsgStaPrmCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl;
static struct { vmbc_intrlight_MsgStaPrmCtrl data[SOA_COMMAND_DEPTH]; uint32_t epoch[SOA_COMMAND_DEPTH]; uint64_t order[SOA_COMMAND_DEPTH]; unsigned head, count; } g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl;
static bool emit_error(SoaEndpoint ep, unsigned rpc, SoaErrorStage stage, int32_t code) {
    SoaBridgeError e = {0};
    e.endpoint=ep; e.rpc_id=rpc; e.stage=stage; e.error_code=code;
    e.sequence=++g_diagnostics.error_events; e.connection_epoch=g_endpoints[ep].connection_epoch; e.time_ms=g_now;
    if (g_error_count==SOA_ERROR_DEPTH) { ++g_diagnostics.dropped_error_events; return false; }
    g_errors[(g_error_head+g_error_count)%SOA_ERROR_DEPTH]=e; ++g_error_count; return true;
}
static void flush_errors(void) {
    unsigned budget=SOA_ERROR_DEPTH;
    while (g_error_count && budget--) {
        if (g_application.report_error(g_application.context,&g_errors[g_error_head])!=SOA_IO_OK) break;
        g_error_head=(g_error_head+1u)%SOA_ERROR_DEPTH; --g_error_count;
    }
}
static void flush_commands(SoaEndpoint ep) {
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynEnaCtrl.count; g_queue_DynAmbLiActu_DynEnaCtrl.head=0; g_queue_DynAmbLiActu_DynEnaCtrl.count=0; }
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynSegCtrl.count; g_queue_DynAmbLiActu_DynSegCtrl.head=0; g_queue_DynAmbLiActu_DynSegCtrl.count=0; }
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynNodeCtrl.count; g_queue_DynAmbLiActu_DynNodeCtrl.head=0; g_queue_DynAmbLiActu_DynNodeCtrl.count=0; }
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynGenBriCtrl.count; g_queue_DynAmbLiActu_DynGenBriCtrl.head=0; g_queue_DynAmbLiActu_DynGenBriCtrl.count=0; }
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynPrmSet.count; g_queue_DynAmbLiActu_DynPrmSet.head=0; g_queue_DynAmbLiActu_DynPrmSet.count=0; }
    if (ep==SOA_EP_DYNAMBLIACTU) { g_diagnostics.discarded_commands+=g_queue_DynAmbLiActu_DynSeqPilot.count; g_queue_DynAmbLiActu_DynSeqPilot.head=0; g_queue_DynAmbLiActu_DynSeqPilot.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIAP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count; g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIFW) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count; g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIIP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count; g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLISTORG) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count; g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIAP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count; g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIFW) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count; g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIIP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count; g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLISTORG) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count; g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIFW) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count; g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIAP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count; g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIIP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count; g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLISTORG) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count; g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIAP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count; g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIFW) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count; g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLIIP) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count; g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count=0; }
    if (ep==SOA_EP_STAAMBLIACTU_STAAMBLISTORG) { g_diagnostics.discarded_commands+=g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count; g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head=0; g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count=0; }
}
void SoaAdaptor_ObserveConnection(SoaEndpoint ep, const SoaConnection *input) {
    if (!g_ready || !input || (unsigned)ep>=SOA_EP_COUNT) return;
    SoaEndpointState *s=&g_endpoints[ep];
    bool next=input->raw_known && input->connected;
    bool changed=s->known!=input->raw_known || s->connected!=next || s->raw_state!=input->raw_state || s->reason!=input->reason;
    if (!changed) return;
    bool new_epoch=next && !s->connected;
    if (new_epoch) ++s->connection_epoch;
    s->known=input->raw_known; s->connected=next; s->raw_state=input->raw_state; s->reason=input->reason;
    g_endpoint_dirty[ep]=true;
    if (!next || new_epoch) {
        flush_commands(ep);
    }
}
static void refresh_connection(SoaEndpoint id) {
        for (unsigned n=0;n<SOA_SOURCE_ERROR_BUDGET;++n) {
            SoaConnection c={0}; int result=g_platform.read_connection(g_platform.context,id,&c);
            if (result==SOA_IO_EMPTY) break;
            if (result!=SOA_IO_OK) { emit_error(id,0,SOA_STAGE_STATE_MAPPING,result); c.raw_known=false; SoaAdaptor_ObserveConnection(id,&c); break; }
            SoaAdaptor_ObserveConnection(id,&c);
        }
}
static bool accept_sample(SoaRxChannel id, const SoaSampleInfo *meta) {
    SoaRxState *s=&g_rx[id]; (void)meta;
    s->have_value=true; s->data_valid=true;
    s->source_epoch=g_endpoints[k_rx_endpoint[id]].connection_epoch;
    /* 仅为成功读取次数/时间；buffer没有新帧标识。 */
    ++s->sample_seq; s->receive_time_ms=g_now;
    return true;
}
static void deliver_states(void) {
    for (unsigned i=0;i<SOA_EP_COUNT;++i) if (g_endpoint_dirty[i]) {
        if (g_application.report_connection(g_application.context,(SoaEndpoint)i,&g_endpoints[i])==SOA_IO_OK) g_endpoint_dirty[i]=false;
    }
    for (unsigned i=0;i<SOA_RX_COUNT;++i) if (g_rx_dirty[i]) {
        if (g_application.report_rx_state(g_application.context,(SoaRxChannel)i,&g_rx[i])==SOA_IO_OK) g_rx_dirty[i]=false;
    }
}
static void crop_DriveModeMgr_DriveModeSts(vmbc_scnmgr_DriveModeMgrDta *out, const srv_vehctl_scnmgr_DriveModeMgrDta *in) {
    (*out).dm_type = (vmbc_scnmgr_DriveModType)(*in).dm_type;
}
static void deliver_DriveModeMgr_DriveModeSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_DriveModeMgr_DriveModeSts(g_application.context,&g_cache_DriveModeMgr_DriveModeSts,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS]=true; }
        else emit_error(SOA_EP_DRIVEMODEMGR,100u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_DriveModeMgr_DriveModeSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS];
    srv_vehctl_scnmgr_DriveModeMgrDta input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_DriveModeMgr_DriveModeSts(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_DRIVEMODEMGR_DRIVEMODESTS,&meta))
        crop_DriveModeMgr_DriveModeSts(&g_cache_DriveModeMgr_DriveModeSts,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS]=true;
    deliver_DriveModeMgr_DriveModeSts();
}
static void crop_DriveModeMgr_EcoPlusModeInfo(vmbc_scnmgr_EcoPlusModeInfoDta *out, const srv_vehctl_scnmgr_EcoPlusModeInfoDta *in) {
    (*out).eco_plus_mode_sts = (vmbc_scnmgr_EcoPlusModType)(*in).eco_plus_mode_sts;
}
static void deliver_DriveModeMgr_EcoPlusModeInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_DriveModeMgr_EcoPlusModeInfo(g_application.context,&g_cache_DriveModeMgr_EcoPlusModeInfo,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO]=true; }
        else emit_error(SOA_EP_DRIVEMODEMGR,103u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_DriveModeMgr_EcoPlusModeInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO];
    srv_vehctl_scnmgr_EcoPlusModeInfoDta input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_DriveModeMgr_EcoPlusModeInfo(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO,&meta))
        crop_DriveModeMgr_EcoPlusModeInfo(&g_cache_DriveModeMgr_EcoPlusModeInfo,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO]=true;
    deliver_DriveModeMgr_EcoPlusModeInfo();
}
static void crop_DynAmbLiActu_DynAmbLiSts(vmbc_intrlight_MsgDynAmbLiSts *out, const srv_body_intrlight_MsgDynAmbLiSts *in) {
    for (unsigned i0=0; i0<7u; ++i0) {
        (*out).ambli_sts[i0].ambli_sts = (vmbc_intrlight_DynOnOffType)(*in).ambli_sts[i0].ambli_sts;
    }
}
static void deliver_DynAmbLiActu_DynAmbLiSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_DynAmbLiActu_DynAmbLiSts(g_application.context,&g_cache_DynAmbLiActu_DynAmbLiSts,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS]=true; }
        else emit_error(SOA_EP_DYNAMBLIACTU,107u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_DynAmbLiActu_DynAmbLiSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS];
    srv_body_intrlight_MsgDynAmbLiSts input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_DynAmbLiActu_DynAmbLiSts(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_DYNAMBLIACTU_DYNAMBLISTS,&meta))
        crop_DynAmbLiActu_DynAmbLiSts(&g_cache_DynAmbLiActu_DynAmbLiSts,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS]=true;
    deliver_DynAmbLiActu_DynAmbLiSts();
}
static void crop_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(vmbc_drv_MotionCommInfo *out, const srv_motion_drv_MotionCommInfo *in) {
    (*out).accr_pedl_posn = (*in).accr_pedl_posn;
    (*out).accr_pedl_posn_vld = (*in).accr_pedl_posn_vld;
}
static void deliver_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO];
    if (s->delivery_pending && (s->have_value || s->e2e_read_success)) {
        if (g_application.publish_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(g_application.context,&g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO]=true; }
        else emit_error(SOA_EP_MOTIONCTRLINFO_MOTIONCTRLINFOPRI,100u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO];
    srv_motion_drv_MotionCommInfo input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_MOTIONCTRLINFO_IFCOMMINFO,&meta))
        crop_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(&g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo,&input);
    g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo.has_accr_pedl_posn=s->have_value;
    g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo.has_accr_pedl_posn_vld=s->have_value;
#if SOA_MOTION_E2E_STATE_USED
    g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo.has_e2e_state=s->e2e_read_success;
    if (s->e2e_read_success) g_cache_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo.e2e_state=g_motion_e2e_code;
#endif
    s->data_valid=s->have_value;
    s->delivery_pending=(s->have_value || s->e2e_read_success); g_rx_dirty[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO]=true;
    deliver_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo();
}
static void crop_RlsInfo_LightSnrSts(vmbc_base_MsgLightSnrSts *out, const srv_body_base_MsgLightSnrSts *in) {
    (*out).head_lamps_on = (vmbc_base_RlsFcnOnOff)(*in).head_lamps_on;
}
static void deliver_RlsInfo_LightSnrSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_RLSINFO_LIGHTSNRSTS];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_RlsInfo_LightSnrSts(g_application.context,&g_cache_RlsInfo_LightSnrSts,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_RLSINFO_LIGHTSNRSTS]=true; }
        else emit_error(SOA_EP_RLSINFO,100u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_RlsInfo_LightSnrSts(void) {
    SoaRxState *s=&g_rx[SOA_RX_RLSINFO_LIGHTSNRSTS];
    srv_body_base_MsgLightSnrSts input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_RlsInfo_LightSnrSts(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_RLSINFO_LIGHTSNRSTS,&meta))
        crop_RlsInfo_LightSnrSts(&g_cache_RlsInfo_LightSnrSts,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_RLSINFO_LIGHTSNRSTS]=true;
    deliver_RlsInfo_LightSnrSts();
}
static void crop_SeatBasicSts_SeatBasicStsArray(vmbc_safety_SeatBasicStatus *out, const srv_body_safety_SeatBasicStatus *in) {
    for (unsigned i0=0; i0<9u; ++i0) {
        (*out).seat_basic_sts[i0].occpnt_sensor_sts = (vmbc_safety_OccpntStsType)(*in).seat_basic_sts[i0].occpnt_sensor_sts;
        (*out).seat_basic_sts[i0].occpnt_fail_sts = (*in).seat_basic_sts[i0].occpnt_fail_sts;
    }
}
static void deliver_SeatBasicSts_SeatBasicStsArray(void) {
    SoaRxState *s=&g_rx[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_SeatBasicSts_SeatBasicStsArray(g_application.context,&g_cache_SeatBasicSts_SeatBasicStsArray,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY]=true; }
        else emit_error(SOA_EP_SEATBASICSTS,100u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_SeatBasicSts_SeatBasicStsArray(void) {
    SoaRxState *s=&g_rx[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY];
    srv_body_safety_SeatBasicStatus input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_SeatBasicSts_SeatBasicStsArray(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY,&meta))
        crop_SeatBasicSts_SeatBasicStsArray(&g_cache_SeatBasicSts_SeatBasicStsArray,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY]=true;
    deliver_SeatBasicSts_SeatBasicStsArray();
}
static void crop_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(vmbc_smtkey_SmtKeyUsrIntnDataStruct *out, const srv_body_smtkey_SmtKeyUsrIntnDataStruct *in) {
    (*out).smt_key_drv_veh_intera_phase = (vmbc_smtkey_SmtKeyDrvVehInteraPhase)(*in).smt_key_drv_veh_intera_phase;
}
static void deliver_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(void) {
    SoaRxState *s=&g_rx[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(g_application.context,&g_cache_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY]=true; }
        else emit_error(SOA_EP_SMTKEYUSRINTNMGR,100u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(void) {
    SoaRxState *s=&g_rx[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY];
    srv_body_smtkey_SmtKeyUsrIntnDataStruct input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY,&meta))
        crop_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(&g_cache_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY]=true;
    deliver_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify();
}
static void crop_VehConfig_IVcpVal_VehicleProject(vmbc_plm_VcpVal *out, const srv_vehicle_plm_VcpVal *in) {
    (*out).vcp_val = (*in).vcp_val;
}
static void deliver_VehConfig_IVcpVal_VehicleProject(void) {
    SoaRxState *s=&g_rx[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_VehConfig_IVcpVal_VehicleProject(g_application.context,&g_cache_VehConfig_IVcpVal_VehicleProject,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT]=true; }
        else emit_error(SOA_EP_VEHCONFIG,2u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_VehConfig_IVcpVal_VehicleProject(void) {
    SoaRxState *s=&g_rx[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT];
    srv_vehicle_plm_VcpVal input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_VehConfig_IVcpVal_VehicleProject(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT,&meta))
        crop_VehConfig_IVcpVal_VehicleProject(&g_cache_VehConfig_IVcpVal_VehicleProject,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT]=true;
    deliver_VehConfig_IVcpVal_VehicleProject();
}
static void crop_VehState_VehStateInfo(vmbc_vehmoding_VehStateMsg *out, const srv_infra_vehmoding_VehStateMsg *in) {
    (*out).veh_state_detailed = (vmbc_vehmoding_VehStateDetailed)(*in).veh_state_detailed;
    (*out).operator_state = (vmbc_vehmoding_OperatorState)(*in).operator_state;
}
static void deliver_VehState_VehStateInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_VEHSTATE_VEHSTATEINFO];
    if (s->delivery_pending && s->data_valid) {
        if (g_application.publish_VehState_VehStateInfo(g_application.context,&g_cache_VehState_VehStateInfo,s)==SOA_IO_OK) { s->delivery_pending=false; g_rx_dirty[SOA_RX_VEHSTATE_VEHSTATEINFO]=true; }
        else emit_error(SOA_EP_VEHSTATE,101u,SOA_STAGE_INTERNAL_DELIVERY,SOA_IO_FAILURE);
    }
}
static void input_VehState_VehStateInfo(void) {
    SoaRxState *s=&g_rx[SOA_RX_VEHSTATE_VEHSTATEINFO];
    srv_infra_vehmoding_VehStateMsg input={0}; SoaSampleInfo meta={0};
    int result=g_platform.read_VehState_VehStateInfo(g_platform.context,&input,&meta);
    s->read_success=result==SOA_IO_OK; s->read_error=!s->read_success;
    if (result==SOA_IO_OK && accept_sample(SOA_RX_VEHSTATE_VEHSTATEINFO,&meta))
        crop_VehState_VehStateInfo(&g_cache_VehState_VehStateInfo,&input);
    s->data_valid=s->have_value;
    s->delivery_pending=s->have_value; g_rx_dirty[SOA_RX_VEHSTATE_VEHSTATEINFO]=true;
    deliver_VehState_VehStateInfo();
}
static void expand_DynAmbLiActu_DynEnaCtrl(srv_body_intrlight_MsgDynEnaCtrl *out, const vmbc_intrlight_MsgDynEnaCtrl *in) {
    for (unsigned i0=0; i0<7u; ++i0) {
        (*out).ena_ctrl[i0] = (*in).ena_ctrl[i0];
    }
}
int SoaAdaptor_Submit_DynAmbLiActu_DynEnaCtrl(const vmbc_intrlight_MsgDynEnaCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,100u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynEnaCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,100u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynEnaCtrl.head+g_queue_DynAmbLiActu_DynEnaCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynEnaCtrl.data[tail]=*input; g_queue_DynAmbLiActu_DynEnaCtrl.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynEnaCtrl.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynEnaCtrl.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynEnaCtrl(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynEnaCtrl.count) {
        unsigned head=g_queue_DynAmbLiActu_DynEnaCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynEnaCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynEnaCtrl msg={0}; expand_DynAmbLiActu_DynEnaCtrl(&msg,&g_queue_DynAmbLiActu_DynEnaCtrl.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynEnaCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,100u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynEnaCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynEnaCtrl.count;
    }
}
static void expand_DynAmbLiActu_DynSegCtrl(srv_body_intrlight_MsgDynSegCtrl *out, const vmbc_intrlight_MsgDynSegCtrl *in) {
    for (unsigned i0=0; i0<12u; ++i0) {
        (*out).seg_ctrl[i0].seg_start_posn = (*in).seg_ctrl[i0].seg_start_posn;
        (*out).seg_ctrl[i0].seg_nr = (*in).seg_ctrl[i0].seg_nr;
        (*out).seg_ctrl[i0].seg_color_vld = (*in).seg_ctrl[i0].seg_color_vld;
        (*out).seg_ctrl[i0].seg_start_color_h = (*in).seg_ctrl[i0].seg_start_color_h;
        (*out).seg_ctrl[i0].seg_end_color_s = (*in).seg_ctrl[i0].seg_end_color_s;
        (*out).seg_ctrl[i0].seg_start_bri = (*in).seg_ctrl[i0].seg_start_bri;
        (*out).seg_ctrl[i0].seg_end_bri = (*in).seg_ctrl[i0].seg_end_bri;
    }
}
int SoaAdaptor_Submit_DynAmbLiActu_DynSegCtrl(const vmbc_intrlight_MsgDynSegCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,101u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynSegCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,101u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynSegCtrl.head+g_queue_DynAmbLiActu_DynSegCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynSegCtrl.data[tail]=*input; g_queue_DynAmbLiActu_DynSegCtrl.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynSegCtrl.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynSegCtrl.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynSegCtrl(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynSegCtrl.count) {
        unsigned head=g_queue_DynAmbLiActu_DynSegCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynSegCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynSegCtrl msg={0}; expand_DynAmbLiActu_DynSegCtrl(&msg,&g_queue_DynAmbLiActu_DynSegCtrl.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynSegCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,101u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynSegCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynSegCtrl.count;
    }
}
static void expand_DynAmbLiActu_DynNodeCtrl(srv_body_intrlight_MsgDynNodeCtrl *out, const vmbc_intrlight_MsgDynNodeCtrl *in) {
    for (unsigned i0=0; i0<207u; ++i0) {
        (*out).node_ctrl[i0].color = (*in).node_ctrl[i0].color;
        (*out).node_ctrl[i0].color_vld = (*in).node_ctrl[i0].color_vld;
        (*out).node_ctrl[i0].bri = (*in).node_ctrl[i0].bri;
    }
}
int SoaAdaptor_Submit_DynAmbLiActu_DynNodeCtrl(const vmbc_intrlight_MsgDynNodeCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,102u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynNodeCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,102u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynNodeCtrl.head+g_queue_DynAmbLiActu_DynNodeCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynNodeCtrl.data[tail]=*input; g_queue_DynAmbLiActu_DynNodeCtrl.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynNodeCtrl.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynNodeCtrl.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynNodeCtrl(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynNodeCtrl.count) {
        unsigned head=g_queue_DynAmbLiActu_DynNodeCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynNodeCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynNodeCtrl msg={0}; expand_DynAmbLiActu_DynNodeCtrl(&msg,&g_queue_DynAmbLiActu_DynNodeCtrl.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynNodeCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,102u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynNodeCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynNodeCtrl.count;
    }
}
static void expand_DynAmbLiActu_DynGenBriCtrl(srv_body_intrlight_MsgDynGenBriCtrl *out, const vmbc_intrlight_MsgDynGenBriCtrl *in) {
    (*out).gen_bri_ctrl = (*in).gen_bri_ctrl;
}
int SoaAdaptor_Submit_DynAmbLiActu_DynGenBriCtrl(const vmbc_intrlight_MsgDynGenBriCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,104u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynGenBriCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,104u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynGenBriCtrl.head+g_queue_DynAmbLiActu_DynGenBriCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynGenBriCtrl.data[tail]=*input; g_queue_DynAmbLiActu_DynGenBriCtrl.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynGenBriCtrl.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynGenBriCtrl.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynGenBriCtrl(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynGenBriCtrl.count) {
        unsigned head=g_queue_DynAmbLiActu_DynGenBriCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynGenBriCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynGenBriCtrl msg={0}; expand_DynAmbLiActu_DynGenBriCtrl(&msg,&g_queue_DynAmbLiActu_DynGenBriCtrl.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynGenBriCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,104u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynGenBriCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynGenBriCtrl.count;
    }
}
static void expand_DynAmbLiActu_DynPrmSet(srv_body_intrlight_MsgDynPrmSet *out, const vmbc_intrlight_MsgDynPrmSet *in) {
    (*out).fade_tim = (*in).fade_tim;
    (*out).fade_mod_cmd = (srv_body_intrlight_DynSwtType)(*in).fade_mod_cmd;
    (*out).nat_tran_mod = (srv_body_intrlight_DynSwtType)(*in).nat_tran_mod;
    (*out).nat_tran_tim = (*in).nat_tran_tim;
    (*out).seg_flow = (srv_body_intrlight_DynSegFlowType)(*in).seg_flow;
    (*out).disp_mod = (srv_body_intrlight_DynDispModType)(*in).disp_mod;
    (*out).color_mod = (srv_body_intrlight_DynColorModType)(*in).color_mod;
    (*out).bri_mod = (srv_body_intrlight_DynBriModType)(*in).bri_mod;
    out->seg_node_pri = srv_body_intrlight_DynPriType_DYN_AMBLI_PRI_NO_REQ;
}
int SoaAdaptor_Submit_DynAmbLiActu_DynPrmSet(const vmbc_intrlight_MsgDynPrmSet *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,105u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynPrmSet.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,105u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynPrmSet.head+g_queue_DynAmbLiActu_DynPrmSet.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynPrmSet.data[tail]=*input; g_queue_DynAmbLiActu_DynPrmSet.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynPrmSet.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynPrmSet.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynPrmSet(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynPrmSet.count) {
        unsigned head=g_queue_DynAmbLiActu_DynPrmSet.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynPrmSet.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynPrmSet msg={0}; expand_DynAmbLiActu_DynPrmSet(&msg,&g_queue_DynAmbLiActu_DynPrmSet.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynPrmSet(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,105u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynPrmSet.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynPrmSet.count;
    }
}
static void expand_DynAmbLiActu_DynSeqPilot(srv_body_intrlight_MsgDynSeqPilot *out, const vmbc_intrlight_MsgDynSeqPilot *in) {
    (*out).pilot_id = (*in).pilot_id;
}
int SoaAdaptor_Submit_DynAmbLiActu_DynSeqPilot(const vmbc_intrlight_MsgDynSeqPilot *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_DYNAMBLIACTU,106u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_DynAmbLiActu_DynSeqPilot.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_DYNAMBLIACTU,106u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_DynAmbLiActu_DynSeqPilot.head+g_queue_DynAmbLiActu_DynSeqPilot.count)%SOA_COMMAND_DEPTH;
    g_queue_DynAmbLiActu_DynSeqPilot.data[tail]=*input; g_queue_DynAmbLiActu_DynSeqPilot.epoch[tail]=ep->connection_epoch; g_queue_DynAmbLiActu_DynSeqPilot.order[tail]=++g_command_sequence; ++g_queue_DynAmbLiActu_DynSeqPilot.count;
    return SOA_IO_OK;
}
static void output_DynAmbLiActu_DynSeqPilot(void) {
    refresh_connection(SOA_EP_DYNAMBLIACTU);
    if (g_queue_DynAmbLiActu_DynSeqPilot.count) {
        unsigned head=g_queue_DynAmbLiActu_DynSeqPilot.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_DYNAMBLIACTU];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_DynAmbLiActu_DynSeqPilot.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgDynSeqPilot msg={0}; expand_DynAmbLiActu_DynSeqPilot(&msg,&g_queue_DynAmbLiActu_DynSeqPilot.data[head]);
            int result=g_platform.send_DynAmbLiActu_DynSeqPilot(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_DYNAMBLIACTU,106u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_DynAmbLiActu_DynSeqPilot.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_DynAmbLiActu_DynSeqPilot.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(srv_body_intrlight_MsgStaEnaCtrl *out, const vmbc_intrlight_MsgStaEnaCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).ena_ctrl[i0] = (*in).ena_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(const vmbc_intrlight_MsgStaEnaCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,100u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,100u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head+g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIAP);
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaEnaCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,100u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(srv_body_intrlight_MsgStaEnaCtrl *out, const vmbc_intrlight_MsgStaEnaCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).ena_ctrl[i0] = (*in).ena_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(const vmbc_intrlight_MsgStaEnaCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,100u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,100u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head+g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIFW);
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaEnaCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,100u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(srv_body_intrlight_MsgStaEnaCtrl *out, const vmbc_intrlight_MsgStaEnaCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).ena_ctrl[i0] = (*in).ena_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(const vmbc_intrlight_MsgStaEnaCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,100u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,100u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head+g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIIP);
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaEnaCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,100u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(srv_body_intrlight_MsgStaEnaCtrl *out, const vmbc_intrlight_MsgStaEnaCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).ena_ctrl[i0] = (*in).ena_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(const vmbc_intrlight_MsgStaEnaCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,100u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,100u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head+g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLISTORG);
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaEnaCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,100u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(srv_body_intrlight_MsgStaColorCtrl *out, const vmbc_intrlight_MsgStaColorCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).color_ctrl[i0].color_or_h = (*in).color_ctrl[i0].color_or_h;
        (*out).color_ctrl[i0].color_s = (*in).color_ctrl[i0].color_s;
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(const vmbc_intrlight_MsgStaColorCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,101u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,101u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head+g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIAP);
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaColorCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,101u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(srv_body_intrlight_MsgStaColorCtrl *out, const vmbc_intrlight_MsgStaColorCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).color_ctrl[i0].color_or_h = (*in).color_ctrl[i0].color_or_h;
        (*out).color_ctrl[i0].color_s = (*in).color_ctrl[i0].color_s;
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(const vmbc_intrlight_MsgStaColorCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,101u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,101u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head+g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIFW);
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaColorCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,101u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(srv_body_intrlight_MsgStaColorCtrl *out, const vmbc_intrlight_MsgStaColorCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).color_ctrl[i0].color_or_h = (*in).color_ctrl[i0].color_or_h;
        (*out).color_ctrl[i0].color_s = (*in).color_ctrl[i0].color_s;
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(const vmbc_intrlight_MsgStaColorCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,101u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,101u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head+g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIIP);
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaColorCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,101u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(srv_body_intrlight_MsgStaColorCtrl *out, const vmbc_intrlight_MsgStaColorCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).color_ctrl[i0].color_or_h = (*in).color_ctrl[i0].color_or_h;
        (*out).color_ctrl[i0].color_s = (*in).color_ctrl[i0].color_s;
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(const vmbc_intrlight_MsgStaColorCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,101u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,101u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head+g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLISTORG);
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaColorCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,101u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(srv_body_intrlight_MsgStaGenBriCtrl *out, const vmbc_intrlight_MsgStaGenBriCtrl *in) {
    (*out).gen_bri_ctrl = (*in).gen_bri_ctrl;
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(const vmbc_intrlight_MsgStaGenBriCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,102u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,102u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head+g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIFW);
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaGenBriCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,102u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(srv_body_intrlight_MsgStaNodeBriCtrl *out, const vmbc_intrlight_MsgStaNodeBriCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).node_bri_ctrl[i0] = (*in).node_bri_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(const vmbc_intrlight_MsgStaNodeBriCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,103u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,103u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head+g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIAP);
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaNodeBriCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,103u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(srv_body_intrlight_MsgStaNodeBriCtrl *out, const vmbc_intrlight_MsgStaNodeBriCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).node_bri_ctrl[i0] = (*in).node_bri_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(const vmbc_intrlight_MsgStaNodeBriCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,103u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,103u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head+g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIIP);
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaNodeBriCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,103u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(srv_body_intrlight_MsgStaNodeBriCtrl *out, const vmbc_intrlight_MsgStaNodeBriCtrl *in) {
    for (unsigned i0=0; i0<17u; ++i0) {
        (*out).node_bri_ctrl[i0] = (*in).node_bri_ctrl[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(const vmbc_intrlight_MsgStaNodeBriCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,103u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,103u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head+g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLISTORG);
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaNodeBriCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,103u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(srv_body_intrlight_MsgStaPrmCtrl *out, const vmbc_intrlight_MsgStaPrmCtrl *in) {
    (*out).fade_tim = (*in).fade_tim;
    (*out).fade_mod_cmd = (srv_body_intrlight_StaSwtType)(*in).fade_mod_cmd;
    (*out).nat_tran_mod = (srv_body_intrlight_StaSwtType)(*in).nat_tran_mod;
    (*out).nat_tran_tim = (*in).nat_tran_tim;
    for (unsigned i0=0; i0<3u; ++i0) {
        (*out).breath_mod[i0] = (srv_body_intrlight_StaBreathModType)(*in).breath_mod[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(const vmbc_intrlight_MsgStaPrmCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,104u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,104u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head+g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIAP);
    if (g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIAP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaPrmCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIAP,104u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(srv_body_intrlight_MsgStaPrmCtrl *out, const vmbc_intrlight_MsgStaPrmCtrl *in) {
    (*out).fade_tim = (*in).fade_tim;
    (*out).fade_mod_cmd = (srv_body_intrlight_StaSwtType)(*in).fade_mod_cmd;
    (*out).nat_tran_mod = (srv_body_intrlight_StaSwtType)(*in).nat_tran_mod;
    (*out).nat_tran_tim = (*in).nat_tran_tim;
    for (unsigned i0=0; i0<3u; ++i0) {
        (*out).breath_mod[i0] = (srv_body_intrlight_StaBreathModType)(*in).breath_mod[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(const vmbc_intrlight_MsgStaPrmCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,104u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,104u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head+g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIFW);
    if (g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIFW];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaPrmCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIFW,104u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(srv_body_intrlight_MsgStaPrmCtrl *out, const vmbc_intrlight_MsgStaPrmCtrl *in) {
    (*out).fade_tim = (*in).fade_tim;
    (*out).fade_mod_cmd = (srv_body_intrlight_StaSwtType)(*in).fade_mod_cmd;
    (*out).nat_tran_mod = (srv_body_intrlight_StaSwtType)(*in).nat_tran_mod;
    (*out).nat_tran_tim = (*in).nat_tran_tim;
    for (unsigned i0=0; i0<3u; ++i0) {
        (*out).breath_mod[i0] = (srv_body_intrlight_StaBreathModType)(*in).breath_mod[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(const vmbc_intrlight_MsgStaPrmCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,104u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,104u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head+g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLIIP);
    if (g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLIIP];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaPrmCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLIIP,104u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count;
    }
}
static void expand_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(srv_body_intrlight_MsgStaPrmCtrl *out, const vmbc_intrlight_MsgStaPrmCtrl *in) {
    (*out).fade_tim = (*in).fade_tim;
    (*out).fade_mod_cmd = (srv_body_intrlight_StaSwtType)(*in).fade_mod_cmd;
    (*out).nat_tran_mod = (srv_body_intrlight_StaSwtType)(*in).nat_tran_mod;
    (*out).nat_tran_tim = (*in).nat_tran_tim;
    for (unsigned i0=0; i0<3u; ++i0) {
        (*out).breath_mod[i0] = (srv_body_intrlight_StaBreathModType)(*in).breath_mod[i0];
    }
}
int SoaAdaptor_Submit_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(const vmbc_intrlight_MsgStaPrmCtrl *input) {
    if (!g_ready) return SOA_IO_NOT_READY;
    if (!input) return SOA_IO_FAILURE;
    SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
    if (!ep->known || !ep->connected) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,104u,SOA_STAGE_PLATFORM_TX,SOA_ERROR_DISCONNECTED); return SOA_IO_OFFLINE; }
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count==SOA_COMMAND_DEPTH) { emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,104u,SOA_STAGE_QUEUE,SOA_ERROR_QUEUE_FULL); return SOA_IO_FULL; }
    unsigned tail=(g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head+g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count)%SOA_COMMAND_DEPTH;
    g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.data[tail]=*input; g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.epoch[tail]=ep->connection_epoch; g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.order[tail]=++g_command_sequence; ++g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count;
    return SOA_IO_OK;
}
static void output_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(void) {
    refresh_connection(SOA_EP_STAAMBLIACTU_STAAMBLISTORG);
    if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count) {
        unsigned head=g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head; SoaEndpointState *ep=&g_endpoints[SOA_EP_STAAMBLIACTU_STAAMBLISTORG];
        if (!ep->connected || !ep->known || ep->connection_epoch!=g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.epoch[head]) ++g_diagnostics.discarded_commands;
        else {
            srv_body_intrlight_MsgStaPrmCtrl msg={0}; expand_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(&msg,&g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.data[head]);
            int result=g_platform.send_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(g_platform.context,&msg);
            if (result!=SOA_IO_OK) emit_error(SOA_EP_STAAMBLIACTU_STAAMBLISTORG,104u,SOA_STAGE_PLATFORM_TX,result);
        }
        g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head=(head+1u)%SOA_COMMAND_DEPTH; --g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count;
    }
}
bool SoaAdaptor_Init(const SoaPlatformPort *p, const SoaApplicationPort *a) {
    if (!p || !a || !p->read_connection || !p->read_error || !a->report_connection || !a->report_rx_state || !a->report_error) return false;
    if (!p->read_DriveModeMgr_DriveModeSts || !a->publish_DriveModeMgr_DriveModeSts) return false;
    if (!p->read_DriveModeMgr_EcoPlusModeInfo || !a->publish_DriveModeMgr_EcoPlusModeInfo) return false;
    if (!p->read_DynAmbLiActu_DynAmbLiSts || !a->publish_DynAmbLiActu_DynAmbLiSts) return false;
    if (!p->read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo || !a->publish_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo) return false;
    if (!p->read_RlsInfo_LightSnrSts || !a->publish_RlsInfo_LightSnrSts) return false;
    if (!p->read_SeatBasicSts_SeatBasicStsArray || !a->publish_SeatBasicSts_SeatBasicStsArray) return false;
    if (!p->read_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify || !a->publish_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify) return false;
    if (!p->read_VehConfig_IVcpVal_VehicleProject || !a->publish_VehConfig_IVcpVal_VehicleProject) return false;
    if (!p->read_VehState_VehStateInfo || !a->publish_VehState_VehStateInfo) return false;
    if (!p->send_DynAmbLiActu_DynEnaCtrl) return false;
    if (!p->send_DynAmbLiActu_DynSegCtrl) return false;
    if (!p->send_DynAmbLiActu_DynNodeCtrl) return false;
    if (!p->send_DynAmbLiActu_DynGenBriCtrl) return false;
    if (!p->send_DynAmbLiActu_DynPrmSet) return false;
    if (!p->send_DynAmbLiActu_DynSeqPilot) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiAp_StaColorCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiFw_StaColorCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiIp_StaColorCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl) return false;
    if (!p->send_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl) return false;
    g_platform=*p; g_application=*a; g_ready=false; g_running=false; g_now=0; g_command_sequence=0;
    memset(g_endpoints,0,sizeof(g_endpoints)); memset(g_rx,0,sizeof(g_rx)); memset(&g_diagnostics,0,sizeof(g_diagnostics));
    g_error_count=g_error_head=0; memset(g_endpoint_dirty,1,sizeof(g_endpoint_dirty)); memset(g_rx_dirty,1,sizeof(g_rx_dirty));
    for (unsigned i=0;i<SOA_EP_COUNT;++i) flush_commands((SoaEndpoint)i);
    g_diagnostics.discarded_commands=0;
    g_ready=true; return true;
}
void SoaAdaptor_Input10ms(uint32_t now_ms) {
    if (!g_ready) return;
    g_now=now_ms;
    for (unsigned i=0;i<SOA_EP_COUNT;++i) {
        refresh_connection((SoaEndpoint)i);
        for (unsigned n=0;n<SOA_SOURCE_ERROR_BUDGET;++n) {
            SoaBridgeError e={0}; int result=g_platform.read_error(g_platform.context,(SoaEndpoint)i,&e);
            if (result==SOA_IO_EMPTY) break;
            if (result!=SOA_IO_OK) { emit_error((SoaEndpoint)i,0,SOA_STAGE_PLATFORM_ASYNC,result); break; }
            if (emit_error((SoaEndpoint)i,e.rpc_id,SOA_STAGE_PLATFORM_ASYNC,e.error_code)) g_errors[(g_error_head+g_error_count-1u)%SOA_ERROR_DEPTH].method_type=e.method_type;
        }
    }
#if SOA_MOTION_E2E_STATE_USED
    {
        SoaRxState *s=&g_rx[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO];
        SoaSampleInfo meta={0};
        int result=g_platform.read_e2e_health ?
            g_platform.read_e2e_health(g_platform.context,SOA_RX_MOTIONCTRLINFO_IFCOMMINFO,&meta) : SOA_IO_NOT_READY;
        s->e2e_read_success=result==SOA_IO_OK && meta.raw_e2e_known;
        s->e2e_read_error=!s->e2e_read_success;
        if (s->e2e_read_success) g_motion_e2e_code=(uint32_t)meta.raw_e2e;
    }
#endif
    input_DriveModeMgr_DriveModeSts();
    input_DriveModeMgr_EcoPlusModeInfo();
    input_DynAmbLiActu_DynAmbLiSts();
    input_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo();
    input_RlsInfo_LightSnrSts();
    input_SeatBasicSts_SeatBasicStsArray();
    input_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify();
    input_VehConfig_IVcpVal_VehicleProject();
    input_VehState_VehStateInfo();
    deliver_states(); flush_errors();
}
void SoaAdaptor_Output10ms(uint32_t now_ms) {
    if (!g_ready) return;
    g_now=now_ms;
    /* 跨RPC保留应用实际提交顺序；每轮只取最早的队首。 */
    for (unsigned budget=0;budget<22u*SOA_COMMAND_DEPTH;++budget) {
        uint64_t earliest=UINT64_MAX; int selected=-1;
        if (g_queue_DynAmbLiActu_DynEnaCtrl.count && g_queue_DynAmbLiActu_DynEnaCtrl.order[g_queue_DynAmbLiActu_DynEnaCtrl.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynEnaCtrl.order[g_queue_DynAmbLiActu_DynEnaCtrl.head]; selected=0; }
        if (g_queue_DynAmbLiActu_DynSegCtrl.count && g_queue_DynAmbLiActu_DynSegCtrl.order[g_queue_DynAmbLiActu_DynSegCtrl.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynSegCtrl.order[g_queue_DynAmbLiActu_DynSegCtrl.head]; selected=1; }
        if (g_queue_DynAmbLiActu_DynNodeCtrl.count && g_queue_DynAmbLiActu_DynNodeCtrl.order[g_queue_DynAmbLiActu_DynNodeCtrl.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynNodeCtrl.order[g_queue_DynAmbLiActu_DynNodeCtrl.head]; selected=2; }
        if (g_queue_DynAmbLiActu_DynGenBriCtrl.count && g_queue_DynAmbLiActu_DynGenBriCtrl.order[g_queue_DynAmbLiActu_DynGenBriCtrl.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynGenBriCtrl.order[g_queue_DynAmbLiActu_DynGenBriCtrl.head]; selected=3; }
        if (g_queue_DynAmbLiActu_DynPrmSet.count && g_queue_DynAmbLiActu_DynPrmSet.order[g_queue_DynAmbLiActu_DynPrmSet.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynPrmSet.order[g_queue_DynAmbLiActu_DynPrmSet.head]; selected=4; }
        if (g_queue_DynAmbLiActu_DynSeqPilot.count && g_queue_DynAmbLiActu_DynSeqPilot.order[g_queue_DynAmbLiActu_DynSeqPilot.head]<earliest) { earliest=g_queue_DynAmbLiActu_DynSeqPilot.order[g_queue_DynAmbLiActu_DynSeqPilot.head]; selected=5; }
        if (g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.count && g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl.head]; selected=6; }
        if (g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.count && g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl.head]; selected=7; }
        if (g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.count && g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl.head]; selected=8; }
        if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.count && g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl.head]; selected=9; }
        if (g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.count && g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaColorCtrl.head]; selected=10; }
        if (g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.count && g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaColorCtrl.head]; selected=11; }
        if (g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.count && g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaColorCtrl.head]; selected=12; }
        if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.count && g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl.head]; selected=13; }
        if (g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.count && g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl.head]; selected=14; }
        if (g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.count && g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl.head]; selected=15; }
        if (g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.count && g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl.head]; selected=16; }
        if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.count && g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl.head]; selected=17; }
        if (g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.count && g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl.head]; selected=18; }
        if (g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.count && g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl.head]; selected=19; }
        if (g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.count && g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl.head]; selected=20; }
        if (g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.count && g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head]<earliest) { earliest=g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.order[g_queue_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl.head]; selected=21; }
        switch (selected) {
            case 0: output_DynAmbLiActu_DynEnaCtrl(); break;
            case 1: output_DynAmbLiActu_DynSegCtrl(); break;
            case 2: output_DynAmbLiActu_DynNodeCtrl(); break;
            case 3: output_DynAmbLiActu_DynGenBriCtrl(); break;
            case 4: output_DynAmbLiActu_DynPrmSet(); break;
            case 5: output_DynAmbLiActu_DynSeqPilot(); break;
            case 6: output_StaAmbLiActu_StaAmbLiAp_StaEnaCtrl(); break;
            case 7: output_StaAmbLiActu_StaAmbLiFw_StaEnaCtrl(); break;
            case 8: output_StaAmbLiActu_StaAmbLiIp_StaEnaCtrl(); break;
            case 9: output_StaAmbLiActu_StaAmbLiStorg_StaEnaCtrl(); break;
            case 10: output_StaAmbLiActu_StaAmbLiAp_StaColorCtrl(); break;
            case 11: output_StaAmbLiActu_StaAmbLiFw_StaColorCtrl(); break;
            case 12: output_StaAmbLiActu_StaAmbLiIp_StaColorCtrl(); break;
            case 13: output_StaAmbLiActu_StaAmbLiStorg_StaColorCtrl(); break;
            case 14: output_StaAmbLiActu_StaAmbLiFw_StaGenBriCtrl(); break;
            case 15: output_StaAmbLiActu_StaAmbLiAp_StaNodeBriCtrl(); break;
            case 16: output_StaAmbLiActu_StaAmbLiIp_StaNodeBriCtrl(); break;
            case 17: output_StaAmbLiActu_StaAmbLiStorg_StaNodeBriCtrl(); break;
            case 18: output_StaAmbLiActu_StaAmbLiAp_StaPrmCtrl(); break;
            case 19: output_StaAmbLiActu_StaAmbLiFw_StaPrmCtrl(); break;
            case 20: output_StaAmbLiActu_StaAmbLiIp_StaPrmCtrl(); break;
            case 21: output_StaAmbLiActu_StaAmbLiStorg_StaPrmCtrl(); break;
            default: flush_errors(); return;
        }
        flush_errors();
    }
    flush_errors();
}
void SoaAdaptor_Run10ms(uint32_t now_ms, void (*application)(void)) {
    if (!g_ready || g_running || !application) return;
    g_running=true; SoaAdaptor_Input10ms(now_ms); application(); SoaAdaptor_Output10ms(now_ms); g_running=false;
}
void SoaAdaptor_ReplayCurrent(void) {
    if (!g_ready) return;
    memset(g_endpoint_dirty,1,sizeof(g_endpoint_dirty)); memset(g_rx_dirty,1,sizeof(g_rx_dirty));
    if (g_rx[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS].data_valid) { g_rx[SOA_RX_DRIVEMODEMGR_DRIVEMODESTS].delivery_pending=true; deliver_DriveModeMgr_DriveModeSts(); }
    if (g_rx[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO].data_valid) { g_rx[SOA_RX_DRIVEMODEMGR_ECOPLUSMODEINFO].delivery_pending=true; deliver_DriveModeMgr_EcoPlusModeInfo(); }
    if (g_rx[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS].data_valid) { g_rx[SOA_RX_DYNAMBLIACTU_DYNAMBLISTS].delivery_pending=true; deliver_DynAmbLiActu_DynAmbLiSts(); }
    if (g_rx[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO].data_valid) { g_rx[SOA_RX_MOTIONCTRLINFO_IFCOMMINFO].delivery_pending=true; deliver_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo(); }
    if (g_rx[SOA_RX_RLSINFO_LIGHTSNRSTS].data_valid) { g_rx[SOA_RX_RLSINFO_LIGHTSNRSTS].delivery_pending=true; deliver_RlsInfo_LightSnrSts(); }
    if (g_rx[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY].data_valid) { g_rx[SOA_RX_SEATBASICSTS_SEATBASICSTSARRAY].delivery_pending=true; deliver_SeatBasicSts_SeatBasicStsArray(); }
    if (g_rx[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY].data_valid) { g_rx[SOA_RX_SMTKEYUSRINTNMGR_SMTKEYUSRINTNNOTIFY].delivery_pending=true; deliver_SmtKeyUsrIntnMgr_SmtKeyUsrIntnNotify(); }
    if (g_rx[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT].data_valid) { g_rx[SOA_RX_VEHCONFIG_IVCPVAL_VEHICLEPROJECT].delivery_pending=true; deliver_VehConfig_IVcpVal_VehicleProject(); }
    if (g_rx[SOA_RX_VEHSTATE_VEHSTATEINFO].data_valid) { g_rx[SOA_RX_VEHSTATE_VEHSTATEINFO].delivery_pending=true; deliver_VehState_VehStateInfo(); }
    deliver_states();
}
void SoaAdaptor_ReportTransportError(SoaEndpoint ep,unsigned rpc,int32_t code) {
    if (g_ready && (unsigned)ep<SOA_EP_COUNT) emit_error(ep,rpc,SOA_STAGE_INTERNAL_DELIVERY,code);
}
void SoaAdaptor_DiscardCommands(void) {
    if (!g_ready) return;
    for (unsigned i=0;i<SOA_EP_COUNT;++i) flush_commands((SoaEndpoint)i);
}
void SoaAdaptor_DeInit(void) {
    if (!g_ready) return;
    for (unsigned i=0;i<SOA_EP_COUNT;++i) { SoaConnection c={0}; SoaAdaptor_ObserveConnection((SoaEndpoint)i,&c); }
    deliver_states(); flush_errors(); g_ready=false;
}
const SoaEndpointState *SoaAdaptor_GetEndpoint(SoaEndpoint id) { return (unsigned)id<SOA_EP_COUNT ? &g_endpoints[id] : NULL; }
const SoaRxState *SoaAdaptor_GetRxState(SoaRxChannel id) { return (unsigned)id<SOA_RX_COUNT ? &g_rx[id] : NULL; }
SoaDiagnostics SoaAdaptor_GetDiagnostics(void) { return g_diagnostics; }
