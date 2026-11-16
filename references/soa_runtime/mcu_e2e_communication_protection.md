
<lark-table rows="5" cols="3" column-widths="84,91,668">

  <lark-tr>
    <lark-td>
      **Version**
    </lark-td>
    <lark-td>
      **Status**
    </lark-td>
    <lark-td>
      **History**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v02.00.06
    </lark-td>
    <lark-td>
      Done
    </lark-td>
    <lark-td>
      Add an E2E state code `E2E_STATUS_INITIAL` (see section 4.2)
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v01.16.06
    </lark-td>
    <lark-td>
      Done
    </lark-td>
    <lark-td>
      Update section 2.3.1 and section 3.1 as v01.16.06 supports multi-client E2E checking for one-way interface (see <mention-doc token="RzZSwm7Qtiad9Aky5uUcLz1enpf" type="wiki">SkyOS-L v01.16.06 [draft]</mention-doc> for the details of this change).
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v01.16.02
    </lark-td>
    <lark-td>
      Done
    </lark-td>
    <lark-td>
      Add [section 2.3.3](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2FUIWRwgOvMidN7ek0dR8cdvounod%23N91ydDB4hopxFUxTsscc8vr5n4c)
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v01.14.06
    </lark-td>
    <lark-td>
      Done
    </lark-td>
    <lark-td>
      Initial version
    </lark-td>
  </lark-tr>
</lark-table>

To meet the functional safety (FuSA) requirement, the SOA Framework implements the end-to-end (E2E) communication protection solution to protect safety-related data exchange against the effects of faults within the communication link at runtime.

This document describes how to enable the SOA E2E mechanism and how to obtain and handle E2E errors.

# Introduction

SOA E2E communuctaion protection works as follows:

<image token="C9l8bSwGQoxvXwxbnXmcvt2UnWg" width="1104" height="700" align="left"/>

When an SOA app calls an E2E-enabled interface to transmit data, the SOA Framework will apply E2E protection after data serialization at the sender side and perform the E2E check before data deserialization at the receiver side. E2E check results will be reported to the receiving SOA app via callbacks.

(Data integrity during the serialization and deserialization process is ensured by the Protobuf library.)

**Features****     **

- Reuse the existing E2E, CRC, and E2eT libraries
- Adopt E2E profile 4 to support the transfer of big data
- Secure MCU-MCU, MCU-MPU, and MPU-MPU communication
- Support [multi-instance ](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2FwikcnVenkKih8Y0RTQN9pUHhN3e)
- Support multicore 
- Detect multiple communication faults (see [Faults detectable](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23WmVGdjLoNo7ieCxYz6TcZUVRneb))
- Apply to the **periodic** event/field notifications and **periodic**Fire-Forget methods (see [Data protected](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23IYOjdx4xloewUxxA5AoccC0anr4))
- Tigger callbacks to report E2E check results (see [Result reporting](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23UGMNdZRz8oKgCVxUDp3cT4Zin8d))

**Limitations**

- <text color="red">**The**</text><text color="red">**SOA Framework**</text><text color="red">**is not responsible for executing the**</text><text color="red">**E2E**</text><text color="red">**FuSa-enabled interfaces periodically.**</text>
  Applications should implement a mechanism (e.g., timer) to ensure the interfaces are cyclically executed. 
- <text color="red">**SOA**</text><text color="red">** **</text><text color="red">**E2E**</text><text color="red">**can not be applied to a reliable interface.**</text>
  If you set reliability QoS to `RELIABLE` and enable SOA E2E for an interface at the same time, unexpected behavior can occur. (In the next release, code generation will stop with an error message in this case.)
- <text color="red">**E2E**</text><text color="red">**protection and checks are not implemented for local servers and clients.**</text>
  E2E state report APIs will always be generated, either in local or remote deployment, but they have some limitations in local deployment. See [E2E state report APIs](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23UGMNdZRz8oKgCVxUDp3cT4Zin8d) for details.

## Faults detectable 

Using E2E profile 4, SOA E2E can detect the following faults or effects of faults:

<lark-table rows="12" cols="3" column-widths="246,521,244">

  <lark-tr>
    <lark-td>
      **Fault**
    </lark-td>
    <lark-td>
      **Description**
    </lark-td>
    <lark-td>
      **Main**** safety mechanisms**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Repetition of information***** ***
    </lark-td>
    <lark-td>
      The information is received more than once.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Loss of information**
    </lark-td>
    <lark-td>
      Parts of your communication frame are missing.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Delay of information**
    </lark-td>
    <lark-td>
      The data frames are received later than expected.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Insertion of information**
    </lark-td>
    <lark-td>
      The frame contains more data than what is expected.
    </lark-td>
    <lark-td>
      Data ID
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Masquerading***** ***
    </lark-td>
    <lark-td>
      Non-authentic, possibly tampered information is received as valid.
    </lark-td>
    <lark-td>
      Data ID, CRC
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Incorrect addressing**
    </lark-td>
    <lark-td>
      The message is sent to the wrong receiver.
    </lark-td>
    <lark-td>
      Data ID
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Incorrect information sequence**
    </lark-td>
    <lark-td>
      The information stream sequence is different than expected.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Data corruption**
    </lark-td>
    <lark-td>
      Information is corrupted.
    </lark-td>
    <lark-td>
      CRC
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Asymmetric information**
    </lark-td>
    <lark-td>
      Happens when a message is sent from a sender to multiple receivers. The data received is different throughout the receivers.
    </lark-td>
    <lark-td>
      CRC
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Limited reception**
    </lark-td>
    <lark-td>
      Happens when a message is sent from a sender to multiple receivers. The message is only received by some of the receivers.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      **Blocking communication access**
    </lark-td>
    <lark-td>
      Access to a communication channel is blocked.
    </lark-td>
    <lark-td>
      Counter
    </lark-td>
  </lark-tr>
</lark-table>

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

From the table above, the SOA E2E mechanism provides functionalities of the Deadline and CRC (integrity) QoS policies and far more. 

Therefore, with the implementation of SOA E2E, the Deadline and CRC (integrity) QoS policies are officially deprecated. Use SOA E2E instead.
</callout>

## Data protected

E2E communication protection is limited to periodic or semi-periodic data communication paradigm, where the receiver (subscriber) has an expectancy on the regular reception of data and in case of communication loss/timeout or error, it performs an error handling.

Due to this limitation, the SOA E2E solution can protect data exchanged in the following types of interfaces:

- **Server to client**
	- Periodic event notifications
	- Periodic field notifications
- **Client to server**
	- Periodic set_field requests
	- Periodic one-way method requests

## E2E state report APIs

To allow receivers to flexibly get and handle E2E check results, the SOA E2E solution provides three pathways to deliver the data and report the E2E state:

<image token="DMdYbipt5ovqxgxO6pXcWdbXnEb" width="573" height="443" align="left"/>

When SOA E2E is enabled, the following new signal manager (sm) APIs will be generated on the receiver side:

<lark-table rows="4" cols="2" column-widths="218,608">

  <lark-tr>
    <lark-td>
      **Pathway**
    </lark-td>
    <lark-td>
      **APIs generated**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      State update path
    </lark-td>
    <lark-td>
      - `xxx_on_e2e_state_xxx_handler`
			- `sm_read_xxx_on_e2e_state_xxx`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Data & State update path
    </lark-td>
    <lark-td>
      - `sm_read_e2e_xxx_on_notify_xxx (const sm_comp_inst_id_t comp_id, evt_msg_xxx_t * const p_evt_msg_xxx, soa_e2e_state_message_t * p_e2e_state)`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Data only path (original)
    </lark-td>
    <lark-td>
      - `sm_read_xxx_on_notify_xxx (const sm_comp_inst_id_t comp_id, evt_msg_xxx_t * const p_evt_msg_xxx)`
    </lark-td>
  </lark-tr>
</lark-table>

The receiver can call the generated APIs to read only the E2E state, both the E2E state and data, or only data based on their needs.

<callout emoji="exclamation" background-color="light-orange" border-color="light-orange">

<text color="red">**E2E**</text><text color="red">**protection and checks are not implemented for local servers and clients.**</text>

When you enable E2E protection for a locally connected server and client, the above SM APIs will be generated but have some limitations:

- State update path: The `sm_read_xxx_on_e2e_state_xxx` API will always return `SUCCESS` but e2e_state is actually unknown because this API is not connected to any other interface. The `on_e2e_state_xxx_handler` callback will never be triggered. Users should initialize the app layer's e2e state value to `E2E_STATUS_OK`. The E2E state will not be updated via the e2e_state read API.
- Data & State update path: The e2e_state returned in the `sm_read_e2e_xxx_on_notify_xxx` API will always be `E2E_STATUS_OK` (implemented from v01.14.07).
- One-way E2E interface supporting multiple clients is available from v01.16.06, but limitations still exist for local clients in the same MCU as the server. The existence of local clients will make this API not work properly, meaning data (from **local clients** or **remote clients without e2e error**) will be uploaded to the server with only `E2E_STATUS_OK`, or data (from**remote clients with some e2e error detected**) will be dropped without error uploaded to the server.

🔆 **Tips**: If the server/client is not sure of their relative deployment (in the same ECU or not), it's recommended not to use the Data & State API. We recommend using the data API, as it remains unchanged whether the interface is E2E or non-E2E protected.
</callout>

# Configurations

## ECU config

In ECU configuration, ensure all SOA E2E-dependent modules are enabled.

1. In `ecus/${ecu_repo}/cmake-scripts/module-cfg.cmake`, add the following configuration to include and enable the E2E, CRC, and E2eT libraries in your ECU.
  ```cmake {wrap}
  nvos_include_module(NAME "bsw_crc_lib"      TYPE ${NVOS_MOD_TYPE_BSW} PATH "CrcLib")
  nvos_include_module(NAME "bsw_e2e_lib"      TYPE ${NVOS_MOD_TYPE_BSW} PATH "E2eLib" DEFINE "E2E_LIB_ENABLE")
  ```

1. In `ecus/${ecu_repo}/cfg/code_gen/${ecu_hardware}/modules/ecu_cfg.json`, add the following configuration to enable E2E profile 4 in your ECU.
  ```json
  {
      "ecu_config": {
          "e2e": {
              "enabled_profiles": [
                  "P01","P04","P05"
              ]
          }
      }
  }
  ```

## IDL config

Most SOA E2E configurations are done in the IDL (`.proto`) file of each service.

### Service option

In the `.proto` file, add the service-level option [`service_id`](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FDoLHdOdGvoOAdFxYtHPcEApCnZf%23WI4mdmkLho0CNTx3b6Mch8NZnKd) to uniquely identify the service. For example:
```protobuf
service HelloWorldMcu {
    option (service_id) = 123;
    ...
}
```

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

In real production, the `service_id` is generated by NTDC to ensure its global uniqueness.
</callout>

### Method option

As mentioned in [Data protected](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23IYOjdx4xloewUxxA5AoccC0anr4), SOA E2E FuSa applies to periodic event/filed notifications and periodic fire-forget methods.

To enable E2E FuSa for different types of methods, you need to set different E2E options in the IDL file.

#### Event/Field notification

To activate SOA E2E for periodic event or field notification, set the following method options in the IDL file:

<lark-table rows="9" cols="3" column-widths="250,154,418">

  <lark-tr>
    <lark-td>
      **Method options**
    </lark-td>
    <lark-td>
      **Required/Optional**
    </lark-td>
    <lark-td>
      **Value**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `method_type`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      - `EVENT`
			- `FIELD_READONLY`
			- `FIELD_WRITABLE`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `update_policy`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      `CYCLIC`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `update_cycle_time`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      An integer in [1, 32767]
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_s2c_enabled`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      `true`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_s2c_timeout`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      An integer in [1, 65535]
      The value should be greater than `update_cycle_time`.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_s2c_max_delta_counter`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [1, 65535]
      If undefined, the default value is 3.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_s2c_min_data_length`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [96, 32768]
      If undefined, the default value is 96.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_s2c_max_data_length`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [96, 32768]
      If undefined, the default value is 4096*8.
    </lark-td>
  </lark-tr>
</lark-table>

<callout emoji="exclamation" background-color="light-orange" border-color="light-orange">

You must adhere to the table above to enable E2E FuSa for an event/field; otherwise, errors will occur during compilation. See [Compilation errors](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23D10rdPKeaoGA63xRf6ncM1hKnBc) for details.
</callout>

#### Fire-Forget method

<lark-table rows="8" cols="3" column-widths="249,147,418">

  <lark-tr>
    <lark-td>
      **Method options**
    </lark-td>
    <lark-td>
      **Required/Optional**
    </lark-td>
    <lark-td>
      **Value**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `method_type`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      - `METHOD` (with the return value being `null`)
			- `FIELD_WRITABLE`
			- `FIELD_WRITABLE_NOSUB`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_cycle_time`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      An integer in [1, 32767]
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_enabled`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      `true`
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_timeout`
    </lark-td>
    <lark-td>
      Required
    </lark-td>
    <lark-td>
      An integer in [1, 65535]
      The value should be greater than `e2e_c2s_cycle_time`.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_max_delta_counter`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [1, 65535]
      If undefined, the default value is 2.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_min_data_length`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [96, 32768]
      If undefined, the default value is 96.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `e2e_c2s_max_data_length`
    </lark-td>
    <lark-td>
      Optional
    </lark-td>
    <lark-td>
      An integer in [96, 32768]
      If undefined, the default value is 4096*8.
    </lark-td>
  </lark-tr>
</lark-table>

<callout emoji="rainbow" background-color="light-green" border-color="light-green">

For the Fire-Forget method enabled with E2E FuSa, additional attributes (client ID) should be added in service and client deployment to identify the source of the request message. See [2.3 SOA deployment](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23E7Zqd0QzNop6dPxrDMrc0zcMnNb) for details.
</callout>

<callout emoji="exclamation" background-color="light-orange" border-color="light-orange">

You must adhere to the table above to enable E2E FuSa for a Fire-Forget method; otherwise, errors will occur during compilation. See [Compilation errors](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23D10rdPKeaoGA63xRf6ncM1hKnBc) for details.
</callout>

### Example

In this example, SOA E2E is enabled for the `SayHelloOneWayMcu` method and the `HiMcu` event.
```protobuf
service HelloWorldMcu {
    option (service_id) = 123;
    // define a method with "HelloRequestMcu" being input and "HelloReplyMcu" being output
    rpc SayHelloMcu(HelloRequestMcu) returns (HelloReplyMcu) {
        option (rpc_id) = 1;
        option (method_type) = METHOD;
    }

    // define a one way method with "HelloRequestMcu" being input
    rpc SayHelloOneWayMcu(HelloRequestMcu) returns (Null) {
        option (rpc_id) = 11;
        option (method_type) = METHOD;
        option (e2e_c2s_enabled) = true;
        option (e2e_c2s_cycle_time) = 1000;
        option (e2e_c2s_timeout) = 1500;
        option (e2e_c2s_max_delta_counter) = 3;
        option (e2e_c2s_min_data_length) = 128;
        option (e2e_c2s_max_data_length) = 4096;
    }

    // define an event with "HelloEventMcu" as data type
    rpc HiMcu(HelloEventMcu) returns (Null) {
        option (rpc_id) = 2;
        option (method_type) = EVENT;
        option (update_policy) = CYCLIC;
        option (update_cycle_time) = 1000;
        option (e2e_s2c_enabled) = true;
        option (e2e_s2c_timeout) = 1500;
        option (e2e_s2c_max_delta_counter) = 3;
        option (e2e_s2c_min_data_length) = 129;
        option (e2e_s2c_max_data_length) = 4097;
    }
    ...
}
```

## SOA deployment

### Client ID (<text color="green">Only required for C2S Fire-Forget methods</text>)

<text color="red">**When**</text><text color="red">**SOA**</text><text color="red">** **</text><text color="red">**E2E**</text><text color="red">** **</text><text color="red">**FuSa**</text><text color="red">**is enabled for a one-way interface (including FF method and set_field) in the**</text><text color="red">**IDL**</text><text color="red">**file, you must add a client ID to the client and service deployment to identify the source of the request message.**</text>

1. In the client's SOA deployment file, add a unique `client_id` to identify the client. 
  ```json
  {
      ...
      "clients": [
          {
              "component_instance_name": "app2",
              "service_name": "HelloWorldMcu",
              "service_package": "nvos.example",
              "client_id": 32
          }
      ]
  }
  ```

1. In the server's SOA deployment file, specify **a client** or **a list of clients** for which to perform the E2E check.
	- To perform E2E checking for a client, configure `e2e_client_id`:
  ```json
  {
      ...
      "services": [
          {
              "component_instance_name": "app1",
              "service_name": "HelloWorldMcu",
              "service_package": "nvos.example",
              "qos": {
                  "method": [
                      {
                          "request_name": "SayHelloOneWayMcu",
                          "e2e_client_id": 32
                      }
                  ]
              }
          }
      ]
  ```

  - To perform E2E checking for a list of clients, configure `e2e_client_ids` (supported from v01.16.06):
  ```json {wrap}
  "services": [
      {
          "component_instance_name": "app1",
          "service_name": "HelloWorldMcu",
          "service_package": "nvos.example",
          "qos": {
              "method": [
                  {
                      "request_name": "SayHelloOneWayMcu",
                      "e2e_client_ids": [
                          {
                              "client_id": 32
                          },
                          {
                              "client_id": 33
                          }
                      ]
                  }
              ]
          }
      }
  ]
  ```

  **Note**: For an E2E-enabled one-way interface, you must set either `e2e_client_id` or `e2e_client_ids` in service deployments; otherwise, a compilation error will be reported. If you set both, `e2e_client_ids` takes precedence. 

In SOA E2E communication, the client ID will be transmitted with the request message, and the server side will check if the received client ID is consistent with `e2e_client_id`/`e2e_client_ids` configured in deployment. If consistent, the server will perform the E2E check; if inconsistent, the SOA Framework will drop the request and report `E2E_STATUS_ERROR` to the server.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

- Only the client whose ID matches `e2e_client_id`/`e2e_client_ids` on the server side can access the E2E-enabled one-way interface; requests from all other clients will be dropped and `E2E_STATUS_ERROR` will be reported to the server.
- If a Fire-Forget method is enabled with E2E FuSa, but `e2e_client_id`/`e2e_client_ids` is not defined in service deployment, a compilation error will occur.
- If a Fire-Forget method is enabled with E2E FuSa and `e2e_client_id`/`e2e_client_ids` is defined, but `client_id` is not defined in client deployment, the SOA Framework will drop the request and report `E2E_STATUS_ERROR` to the server.
- From v0.16.06, for an E2E-enabled Fire-Forget method, if `client_id` is not defined in client deployment, a compilation error will occur.
</callout>

<callout emoji="exclamation" background-color="light-orange" border-color="light-orange">

**Limitations**

The current SOA Framework does not support a server with both local and remote clients where a client sometimes connects to the server intra-ECU and sometimes inter-ECU. In such cases, the SOA Framework will default to using the 'discard-e2e' approach. This means that E2E protection will not be provided for these alternating connections. Users should be aware of this limitation when designing their system architecture.

For an E2E protected one-way interface, if multiple clients invokes it, it has some limitations:

- The status upload API has only one buffer, which means the error status will overwrite each other if the client is not able to get scheduled to take this in time. 
- The status+data upload API is a queue (if history depth is > 1, default is 1 which is a buffer). When new status+data is put in queue, the data is stored there waiting to be consumed by user. However, when the queue is full, the new status+data will overwrite old data.
</callout>

### Service instance name (<text color="green">Optional</text>) 

If you want to use SOA E2E FuSa in the multi-instance scenario, you need to ensure:

1. The server and client use MRTOS V01.14.06_RC_04/Nservice v00.06.06_RC_04/SafeOS v00.06.06_RC_04 or later.
1. The `service_instance_name` in SOA deployment is unique. The SOA Framework will autogenerate `service_instance_id` based on `service_instance_name` to identify the service instance. For example:
	- Service deployment:
  ```json
  {
      "services": [
          {
              "component_instance_name": "app1",
              "service_name": "HelloWorldMcu",
              "service_package": "nvos.example"
          },
          {
              "component_instance_name": "app1",
              "service_name": "HelloWorldMcu",
              "service_instance_name": "Gen1",
              "service_package": "nvos.example"
          },
          {
              "component_instance_name": "app1",
              "service_name": "HelloWorldMcu",
              "service_instance_name": "Gen2",
              "service_package": "nvos.example"
          }
      ]
  }
  
  ```

  - Client deployment
  ```json
  {
      "clients": [
          {
              "component_instance_name": "app2",
              "service_name": "HelloWorldMcu",
              "service_package": "nvos.example"
          },
          {
              "component_instance_name": "app2_pro",
              "service_name": "HelloWorldMcu",
              "service_instance_name": "Gen1",
              "service_package": "nvos.example"
          },
          {
              "component_instance_name": "app2_pro_max",
              "service_name": "HelloWorldMcu",
              "service_instance_name": "Gen2",
              "service_package": "nvos.example"
          }
      ]
  }
  ```

### Disable E2E for an individual event interface per client (<text color="green">Optional</text>) (<text color="green">Client only</text>)

When E2E checking is activated in an IDL file, it becomes a mandatory feature for all clients that use the IDL file. However, some scenarios require disabling E2E checking on a per-client basis. In this case, you can add `disable_e2e` in `soa_deployment.json` to disable E2E checking for a specified event interface for a client.

For example:
```json
{
    "$schema": "../../../../../platform/BSW/soa/schema/default.deployment.schema.json",
    "$target": "MCU",
    "services": [],
    "clients": [
        {
            "component_instance_name": "app21",
            "service_name": "HelloWorldMcu",
            "service_package": "nvos.example",
            "client_id": 33,
            "qos": {
                "event": [
                    {
                        "request_name": "HiMcu",
                        "disable_e2e": true
                    }
                ]
            }
        }
    ]
}
```

In this example, E2E checking is disabled for the `HiMcu` event notification interface for the client (app21), and the E2E state report APIs will not be generated.

# App implementation

After SOA E2E FuSa is enabled, app developers need to modify their apps' source code to handle E2E check results.

## Server

1. Implement a timer to periodically publish the E2E-enabled event or field.
1. Read the E2E state of an E2E-enabled one-way request from the client.
  **Option 1**: Listen for the `xxx_on_e2e_state_xxx_handler` callback and call `sm_read_xxx_on_e2e_state_xxx` to get the E2E state. For example:
  ```cpp {wrap}
  // Callback to handle the E2E state of the client's 'sayhelloonewaymcu' one-way method.
  static void app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu_handler(
      const sm_comp_inst_id_t comp_id)
  {
      // Initialize structure to capture the e2e state of the one-way method.
      sm_e2e_state_t e2e_state = {};
  
      // Read the e2e state for the 'sayhelloonewaymcu' method from client.
      if (sm_read_app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu(comp_id, &e2e_state) != SUCCESS)
      {
          // Early exit on read failure.
          return;
      }
  
      // Log the received e2e state.
      console_print(
          "=== HelloWorldMcu Base === app1 receives [11][METHOD_ONEWAY] E2E state = %d, E2E "
          "client_id = %d\n",
          e2e_state.status,
          e2e_state.client_id);
  }
  
  app1_ifaces_t app1_ifaces =
  {
      .app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu_handler = app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu_handler,
  };
  ```

  **Option 2**: Listen for the `on_request_xxx_handler` callback and call `sm_read_e2e_xxx_on_request_xxx` to read the E2E state with the data. For example:
  ```cpp {wrap}
  // Callback to process client's 'sayhellooneway' method request.
  static void on_request_helloworldmcu_sayhelloonewaymcu_handler(const sm_comp_inst_id_t comp_id)
  {
      // Initialize structures for 'sayhellooneway' request and end-to-end state.
      req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t hello_request = {};
      sm_e2e_state_t                                         e2e_state     = {};
  
      // Read the 'sayhellooneway' request from client.
      if (sm_read_e2e_app1_on_request_helloworldmcu_sayhelloonewaymcu(
              comp_id, &hello_request, &e2e_state)
          != SUCCESS)
      {
          // Early exit on read failure.
          return;
      }
  
      // Log the received request details.
      console_print(
          "=== HelloWorldMcu Base === app1 receives [11][METHOD_ONEWAY] oneway method sayhello "
          "request with greeting = \"%s\", a = %d, b = %d, E2E state = %d, E2E client_id = %d\n",
          hello_request.request_msg.greeting,
          hello_request.request_msg.a,
          hello_request.request_msg.b,
          e2e_state.status,
          e2e_state.client_id);
  
      // ====== [2] EVENT ======
      // send event to all clients
      // note: sending event in helloworldmcu_sayhellomcu_handler is just an example
      // the real timing of sending event depends on your logic
      evt_msg_nvos_example_helloworldmcu_himcu_t hello_event = {};
      hello_event.event_msg.index                            = g_event_index++;
      strcpy(hello_event.event_msg.place, "This is the way");
  
      // Dispatch the event.
      if (sm_write_app1_notify_helloworldmcu_himcu(comp_id, &hello_event) != SUCCESS)
      {
          // Handle dispatch failure.
          return;
      }
  }
  
  // ====== [11][E2E] ONEWAY METHOD ======
  // Callback to handle the e2e state for client's 'sayhelloonewaymcu' one-way method.
  static void app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu_handler(
      const sm_comp_inst_id_t comp_id)
  {
      // Initialize structure to capture the e2e state of the one-way method.
      sm_e2e_state_t e2e_state = {};
  
      // Read the e2e state for the 'sayhelloonewaymcu' method from client.
      if (sm_read_app1_on_e2e_state_helloworldmcu_sayhelloonewaymcu(comp_id, &e2e_state) != SUCCESS)
      {
          // Early exit on read failure.
          return;
      }
  
      // Log the received e2e state.
      console_print(
          "=== HelloWorldMcu Base === app1 receives [11][METHOD_ONEWAY] E2E state = %d, E2E "
          "client_id = %d\n",
          e2e_state.status,
          e2e_state.client_id);
  }
  
  app1_ifaces_t app1_ifaces =
  {
      .app1_on_request_helloworldmcu_sayhelloonewaymcu_request_arrived = &on_request_helloworldmcu_sayhelloonewaymcu_handler,
  };
  ```

## Client

1. Implement a timer to periodically send one-way requests.
1. Read the E2E state of an E2E-enabled event or field notification.
  **Option 1**: Listen for the `xxx_on_e2e_state_xxx_handler` callback and call `sm_read_xxx_on_e2e_state_xxx` to get the E2E state. For example:
  ```c
  // Callback to handle the E2E state from server's 'helloevent' notification.
  static void
  app2_on_e2e_state_helloworldmcu_himcu_handler(const sm_comp_inst_id_t comp_id)
  {
      // Initialize the E2E state structure.
      sm_e2e_state_t e2e_state = {};
  
      // Read the E2E state.
      if (sm_read_app2_on_e2e_state_helloworldmcu_himcu(comp_id, &e2e_state) != SUCCESS)
      {
          // Early exit on read failure.
          return;
      }
  
      // Log the received E2E state details.
      console_print("=== HelloWorldMcu Base === app2 receives [2b][E2E][EVENT] E2E state = %d\n",
                    e2e_state.status);
  }
  
  app2_ifaces_t app2_ifaces = {
      .app2_on_e2e_state_helloworldmcu_himcu_handler = app2_on_e2e_state_helloworldmcu_himcu_handler,
  };
  ```

  **Option 2**: Listen for the `xxx_on_notify_xxx_handler` callback and call `sm_read_e2e_xxx_on_notify_xxx` to read the E2E state with the data. For example:
  ```c
  // Callback to handle the 'helloevent' notification from the server.
  static void
  app2_on_notify_helloworldmcu_helloevent_handler(const sm_comp_inst_id_t comp_id)
  {
      // Initialize event message and E2E state structures.
      evt_msg_nvos_example_helloworldmcu_himcu_t hello_event_msg = {};
      sm_e2e_state_t                             e2e_state       = {};
  
      // Read the event and E2E state.
      if (sm_read_e2e_app2_on_notify_helloworldmcu_himcu(comp_id, &hello_event_msg, &e2e_state)
          != SUCCESS)
      {
          // Early exit on read failure.
          return;
      }
  
      // Log the received event details.
      console_print(
          "=== HelloWorldMcu Base === app2 receives [2b][EVENT] hello event with index = %d, place = "
          "\"%s\" E2E state = %d\n",
          hello_event_msg.event_msg.index,
          hello_event_msg.event_msg.place,
          e2e_state.status);
  }
  
  app2_ifaces_t app2_ifaces = {
      .app2_on_notify_helloworldmcu_himcu_handler = app2_on_notify_helloworldmcu_helloevent_handler,
  };
  ```

# Error handling

Errors can occur during compilation and runtime due to misconfiguration or incorrect code.

This section lists all errors associated with SOA E2E FuSa and troubleshooting tips.

## Compilation errors

<lark-table rows="7" cols="3" column-widths="290,382,372">

  <lark-tr>
    <lark-td>
      **Error message**
    </lark-td>
    <lark-td>
      **Cause**
    </lark-td>
    <lark-td>
      **Tips**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      'Service "{wrappedService.full_name} - Method "{method.name}": **E2E**** is enabled but service ID is not set**.'
    </lark-td>
    <lark-td>
      `service_id` is not set while `e2e_c2s_enabled` or `e2e_s2c_enabled` is true in the IDL file.
    </lark-td>
    <lark-td>
      To enable E2E FuSa, `service_id` must be set in the IDL file.
      See [Service option](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23RoiydQ5uRoMQkvxMUV7c1SMmnbc) for details.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      'Method "{method.name}" **has ****e2e**** enabled but update_cycle_time is not set, exit!!**'
    </lark-td>
    <lark-td>
      `update_cycle_time` is not set while `e2e_s2c_enabled` is true in the IDL file.
    </lark-td>
    <lark-td>
      To enable E2E FuSa for an event/filed, the following options must also be set:
      - `update_policy` = `CYCLIC`
			- `update_cycle_time` = integer in [1, 32767]
      See [Event/Field notification](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23B9N5dB3aKovr2hxWmwccUZ1dnge) for details.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      'Method "{method.name}" **has ****e2e**** enabled but e2e_c2s_cycle_time is not set, exit**!!'
    </lark-td>
    <lark-td>
      `e2e_c2s_cycle_time` is not set while `e2e_c2s_enabled` is true in the IDL file.
    </lark-td>
    <lark-td>
      To enable E2E FuSa for a Fire-Forget method, the `e2e_c2s_cycle_time` option must also be set.
      See [Fire-Forget method](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23SF1fdOv0IoRJ2qxOZvkcMRUOnAX) for details.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      'Method "{method.name}" **does not have valid e2e_timeout while e2e_enabled is turned on, exit!!**'
    </lark-td>
    <lark-td>
      - `e2e_s2c_timeout`  is not set while `e2e_s2c_enabled` is true in the IDL file.
			- `e2e_c2s_timeout`is not set while `e2e_c2s_enabled` is true in the IDL file.
    </lark-td>
    <lark-td>
      - To enable E2E FuSa for an event/filed, the `e2e_s2c_timeout` option must also be set. See [Event/Field notification](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23B9N5dB3aKovr2hxWmwccUZ1dnge) for details.
			- To enable E2E FuSa for a Fire-Forget method, the `e2e_c2s_enabled` option must also be set. See [Fire-Forget method](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23SF1fdOv0IoRJ2qxOZvkcMRUOnAX) for details.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      Unsupported e2e configuration type.
    </lark-td>
    <lark-td>
      Use `e2e_s2c_xxx` or `e2e_c2s_xxx` options for wrong method types.
    </lark-td>
    <lark-td>
      - Ensure you use `e2e_s2c_xxx` options for an event/field (method_type = `EVENT`/`FIELD_READONLY`/`FIELD_WRITABLE`).
			- Ensure you use `e2e_c2s_xxx` options for a Fire-Forget method (method_type = oneway `METHOD` /`FIELD_WRITABLE`/`FIELD_WRITABLE_NOSUB`).
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      <service_name> - <method_name> **has ****e2e**** enabled but the "e2e_client_id" is not set in the ****deployment**** file, exit**!!
    </lark-td>
    <lark-td>
      `e2e_c2s_enabled` is enabled for the Fire-Forget method in the IDL file, but `e2e_client_id` is not set for the service in the SOA deployment file.
    </lark-td>
    <lark-td>
      To enable E2E FuSa for a Fire-Forget method, you must set `e2e_client_id` for service and set `client_id` for client in SOA deployment. 
      See [SOA deployment](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23E7Zqd0QzNop6dPxrDMrc0zcMnNb) for details.
    </lark-td>
  </lark-tr>
</lark-table>

## Runtime errors

During runtime, E2E status code will be reported via [the State update path and the Data & State Update path](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FXerVdFNqsobsq0xgasNcrjs5nSb%23UGMNdZRz8oKgCVxUDp3cT4Zin8d):

<lark-table rows="13" cols="5" column-widths="239,100,216,453,336">

  <lark-tr>
    <lark-td>
      **State code**
    </lark-td>
    <lark-td>
      **Enum Value**
    </lark-td>
    <lark-td>
      **Fault**
    </lark-td>
    <lark-td>
      **Description**
    </lark-td>
    <lark-td>
      **Tips**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_OK`
    </lark-td>
    <lark-td>
      0
    </lark-td>
    <lark-td>
      -
    </lark-td>
    <lark-td>
      No error occurs.
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_OK_SOME_LOST`
    </lark-td>
    <lark-td>
      1
    </lark-td>
    <lark-td>
      1 < delta ounter <= configured max_delta_counter
      (delta counter = current received counter - last received counter)
    </lark-td>
    <lark-td>
      Some data in the sequence has been probably lost since the last correct/initial reception, but this is within the configured tolerance range.
    </lark-td>
    <lark-td>
      Users can decide to discard or use the data.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td rowspan="6">
      `E2E_STATUS_ERROR`
    </lark-td>
    <lark-td rowspan="6">
      2
    </lark-td>
    <lark-td rowspan="6">
      - Wrong CRC
			- Wrong data ID
			- Wrong data length
			- Configuration errors
    </lark-td>
    <lark-td>
      The E2E check fails due to one of the following reasons:
    </lark-td>
    <lark-td>
      -
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      - Wrong CRC
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      - Wrong data ID
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      - Wrong data length
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      - For a Fire-Forget method enabled with E2E FuSa, the server receives a request message in which `**client_id**`**is not set** or **inconsistent with**`**e2e_client_id**`.
    </lark-td>
    <lark-td>
      For a Fire-Forget method enabled with E2E FuSa, ensure the following:
      - `client_id` is set for the client in SOA deployment.
			- `client_id` must be unique.
			- Only the client whose `client_id` is the same as `e2e_client_id` access the service interface. (All other clients should avoid calling service interface; otherwise, their requests will be denied with `E2E_STATUS_ERROR`.)
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      - E2E FuSa is enabled on the receiver side, but it receives a message that doesn't have E2eProtect information
    </lark-td>
    <lark-td>
      This could be a compatibility issue where a newer version of a service is communicating with an older version that doesn't expect E2eProtect information.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_REPEATED`
    </lark-td>
    <lark-td>
      3
    </lark-td>
    <lark-td>
      delta counter == 0
    </lark-td>
    <lark-td>
      The counter is identical to the most recent data received.
    </lark-td>
    <lark-td>
      Users can decide to discard or use the data.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_NONEWDATA`
    </lark-td>
    <lark-td>
      4
    </lark-td>
    <lark-td>
      timeout
    </lark-td>
    <lark-td>
      No E2E checks of data have been consequently executed.
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_WRONGSEQUENCE`
    </lark-td>
    <lark-td>
      5
    </lark-td>
    <lark-td>
      delta_counter > configured max_delta_counter
    </lark-td>
    <lark-td>
      Too much data in the sequence has probably been lost since the last correct/initial reception.
    </lark-td>
    <lark-td>
      Users can decide to discard or use the data.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      `E2E_STATUS_INITIAL`
    </lark-td>
    <lark-td>
      6
    </lark-td>
    <lark-td>
      -
    </lark-td>
    <lark-td>
      The initial frame in the E2E publication process.
    </lark-td>
    <lark-td>
      NA
    </lark-td>
  </lark-tr>
</lark-table>

<callout emoji="rainbow" background-color="light-blue" border-color="light-blue">

- e2e state 非0都是或大或小的异常。
- 其中2和4，不会有数据到应用：
	- 2代表严重错误，数据会丢掉，只有e2e state给到应用。
	- 4超时，压根没有数据来，所以也只有e2e state给到应用。
- 其他状态，数据和e2e state都给到应用，由应用自己决定。
</callout>

## Notes on E2E Status Update

From v01.16.06 MRTOS supports multiple clients sending methods one-way to one server's E2E interface. This is not intended to be used unless you know the cost of it well.  One of the costs is that the E2E status update will be changed from "Modified" to "Updated",  meaning if no new date arrives for some time, the `E2E_STATUS_NONEWDATA` error code will be continuously reported to the user at each timeout checking. And  each time the received data is checked OK, then `E2E_STATUS_OK` is reported to the user too.

Server side shall pay attention to this and filter out the repeated message. Be careful not burning the CPU

# Demo app

We have a demo app that implements the FuSa E2E feature for your reference: [`nvos-platform/tools/code_gen/soa/examples/fusa-e2e`](https%3A%2F%2Fgit.nevint.com%2Fds%2Fnvos-platform%2F-%2Ftree%2Fdevelop%2Ftools%2Fcode_gen%2Fsoa%2Fexamples%2Ffusa-e2e)

You can follow `README.md` in the directory to run the demo app.

# References

To learn details of the whole architecture and design, see the following documents:

- <mention-doc token="M3vWwYCrYimWvJkKARZcNKGGnhh" type="wiki">SOA Framework: FuSa Arch Design</mention-doc> 
- <mention-doc token="KMmnw1zMHi3Qo8k016zc45HpnUf" type="wiki">SOA E2E Strategy on MCU</mention-doc> 
- <mention-doc token="Du65d1lzYoALuHx6n3cc6Vu0nee" type="docx">[E2E] Support E2E FuSa on MCU for SOA</mention-doc> 
