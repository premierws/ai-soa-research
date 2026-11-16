#include "soa_adpt_amblimgr.h"
#include "soa_adpt_amblimgr_vmbc.h"
#include "mock_ports.h"
#include <assert.h>
#include <stdio.h>
static unsigned deliveries;
static bool fail_read;
static int read_motion(void *ctx,srv_motion_drv_MotionCommInfo *msg,SoaSampleInfo *meta) {
    (void)ctx;msg->accr_pedl_posn=fail_read?999.0f:19.0f;
    meta->raw_e2e_known=true;meta->raw_e2e=2;
    return fail_read?SOA_IO_FAILURE:SOA_IO_OK;
}
static int publish(void *ctx,const vmbc_drv_MotionCommInfo *msg,const SoaRxState *state) {
    (void)ctx;assert(state->have_value);assert(msg->accr_pedl_posn==19.0f);
    ++deliveries;return SOA_IO_OK;
}
int main(void) {
    SoaPlatformPort p;SoaApplicationPort a;
    SoaTest_DefaultPlatform(&p);SoaAdaptorVmbc_MakePort(20,&a);
    p.read_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo=read_motion;
    a.publish_MotionCtrlInfo_MotionCtrlInfoPri_IfCommInfo=publish;
    assert(SoaAdaptor_Init(&p,&a));SoaTest_ConnectAll();
    SoaAdaptor_Input10ms(10);
    assert(deliveries==1);
    /* 连接状态不替代实际SM结果；失败不使用被污染的输出参数。 */
    SoaConnection disconnected={0};disconnected.raw_known=true;
    SoaAdaptor_ObserveConnection(SOA_EP_MOTIONCTRLINFO_MOTIONCTRLINFOPRI,&disconnected);
    SoaAdaptor_Input10ms(10000);
    assert(deliveries==2 && SoaAdaptor_GetRxState(SOA_RX_MOTIONCTRLINFO_IFCOMMINFO)->read_success);
    fail_read=true;SoaAdaptor_Input10ms(10010);
    assert(deliveries==3 && SoaAdaptor_GetRxState(SOA_RX_MOTIONCTRLINFO_IFCOMMINFO)->read_error);
    assert(SoaAdaptor_GetDiagnostics().error_events==0);
    puts("PASS: SDK payload forwarded regardless of E2E quality");
    return 0;
}
