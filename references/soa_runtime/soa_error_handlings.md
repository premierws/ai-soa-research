
<lark-table rows="9" cols="5" column-widths="151,197,134,384,213">

  <lark-tr>
    <lark-td>
      **Version**
    </lark-td>
    <lark-td>
      **Author**
    </lark-td>
    <lark-td>
      **Date**
    </lark-td>
    <lark-td>
      **Change History**
    </lark-td>
    <lark-td>
      **Note**
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v02.03.06
      SkyOS-S v01.03.06
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      Aug. 06 2026
    </lark-td>
    <lark-td>
      v0.7.5
      - Add recommended error handling for error `(9) kNotImplemented`
      v0.7.4
      - Add description of error code `(14) kDeprecatedItemUsed` and `(97) kFieldCacheNotInitialized`
      v0.7.3
      - Update `NRPC_SERDES_FAIL` and add one possible error handling related to NANO format
    </lark-td>
    <lark-td rowspan="8">
      This page always shows the latest version. 
      To view historical versions, click **...** > **查看已存****版本** on the top right.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v02.00.07
      SkyOS-S v01.00.07
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      Jan. 07 2025
    </lark-td>
    <lark-td>
      v0.7.2
      - Update Chapter 2 Error reporting path by removing all logs in TX/RX path according to <mention-doc token="WOajw7SUyihIr7kLQ8DcULp0nYg" type="wiki">Logging Level Strategy Design</mention-doc>
      v0.7.1
      - Update recommended error handling according to <mention-doc token="Bp11w0RTdiAvwXkHg5XcwMqFnPh" type="wiki">NT3 SOA Error Handling Best Practice—V1.0</mention-doc>
			- Added Chapter 5 TOX Error Code
      v0.7
      - Removed section 4.3.2 QoS Error
			- Move (11) NRPC_QOS_RELIABILITY_DROP_MESSAGE (12) NRPC_QOS_RELIABILITY_CLOSE_ON_ERROR (13) NRPC_QOS_RELIABILITY_MISMATCH_CFG to section 4.3.1.3 General Error Codes
      v0.6.3
      - Added (13) NRPC_TERMINATED_BY_USER to section 4.3.1.3 Error codes
			- Updated description for (2) NRPC_NOT_EXIST and (3) NRPC_ALREADY_EXIST
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v02.00.06
      SkyOS-S v01.00.06
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      Sept. 13, 2024
    </lark-td>
    <lark-td>
      v0.6.2  
      - QUERY_OVER_LIMIT become reason for DISCONNECTED instead of TERMINATED
			- Section 4.3.1.3 Error Codes: Added (12) kShapingQueueFull
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v02.00.04
      SkyOS-S v01.00.04
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      Aug. 12, 2024
    </lark-td>
    <lark-td>
      v0.6.1 Added additional handling for NRPC_BAD_PARAMETER.
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v01.16.08
      SkyOS-S v00.07.08
    </lark-td>
    <lark-td>
      <mention-user id="ou_242b58f2f4318a5f3f4553aa8a34db40"/>
    </lark-td>
    <lark-td>
      April 16, 2024
    </lark-td>
    <lark-td>
      v0.6 Add Section 3: App Framework Errors.
      v0.5: Update section 3.3.1.3 Error codes
      - Add a new error code NRPC_INIT_FAILED (11)
			- Add error messages to each error code
			- Deprecate error codes NRPC_NOT_EXIST (2) and NRPC_ALREADY_EXIST (3)
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      SkyOS-L v01.16.06
      SkyOS-S v00.07.06
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      March 05, 2024
    </lark-td>
    <lark-td>
      v0.4: Add QUERY_OVER_LIMIT (7) and KICKED_OFFLINE_BY_CLIENT_WITH_SAME_ID (8) to 3.2.2 Reasons
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v01.16.02
      v00.07.02
    </lark-td>
    <lark-td>
    </lark-td>
    <lark-td>
      Jan. 2, 2024
    </lark-td>
    <lark-td>
      v0.3: Add (6) NOT_MATCHED_SECURITY_CONFIG/kNotMatchedSecurityConfig in 3.2.2 Reasons
    </lark-td>
  </lark-tr>
  <lark-tr>
    <lark-td>
      v01.16.00
      v00.07.00
    </lark-td>
    <lark-td>
      <mention-user id="ou_41cd6d7ccb4b9eece7577f2447c6dbeb"/>
    </lark-td>
    <lark-td>
      Oct. 12, 2023
    </lark-td>
    <lark-td>
      v0.2: In 3.2 Connection States, add TERMINATED state and several reasons.
      v0.1: first draft
    </lark-td>
  </lark-tr>
</lark-table>

# Purpose

This document is to give an overview of end-to-end runtime error handling of SOA Framework. 

# Error reporting path

Each time an error happens, SOA Framework will report this by:

- Generate error code or error reply to application
- Increment internal counter is  with SOA Framework, which can be read out by [The Service Monitor Tool](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2FTqGAwoKnSiuna0kb36ecZa1Lnne). e.g. System busy and starts to drop unreliable messages

<callout emoji="exclamation" background-color="light-orange" border-color="light-orange">

If an error is related to send / receive message, no error log shall be printed. Please refer to <mention-doc token="WOajw7SUyihIr7kLQ8DcULp0nYg" type="wiki">Logging Level Strategy Design</mention-doc>for more info.
</callout>

## TX Direction

In general, SOA Framework provides error codes in 2 ways:

- Direct reporting: return code for sync APIs, or callback for aysnc APIs
- Indirect reporting: 
	- An error reply for request-reply 
	- An independent error event for others

### MRTOS

For MRTOS, almost all the error codes are indirectly reported, except those in the App Framework.

Also, when messages' processing runs into certain errors on the remote side, only Request-Reply can get an error code.

<diagram type="2"/>

### MPU

For MPU, the error detected outside TOX Core thread is reported directly. Errors detected inside TOX core thread is reported indirectly.

Also, when messages' processing runs into certain errors on the remote side, only Request-Reply can get an error code.

<diagram type="2"/>

## RX Direction

In RX direction, SOA Framework always provides error codes in "indirect reporting" way through an independent error callback. 

For incoming request of RR type, an additional error reply is sent back to remote side.

<diagram type="2"/>

# APP Framework Errors (MRTOS Only)

Before requests reaching SOA Framework, errors might happen in the App framework. Here are the error codes.

<reference-synced source-block-id="GlLvdpUi4sD0cjb3G3acfiGfngd" source-document-id="MwwBdi1dIoVNnzx3cBncmwP7nUe">

  <lark-table rows="11" cols="4" column-widths="241,100,300,633">

    <lark-tr>
      <lark-td>
        element_name
      </lark-td>
      <lark-td>
        value
      </lark-td>
      <lark-td>
        description
      </lark-td>
      <lark-td>
        usage example
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        SUCCESS
      </lark-td>
      <lark-td>
        0
      </lark-td>
      <lark-td>
        Success operation.
      </lark-td>
      <lark-td>
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_INTERNAL
      </lark-td>
      <lark-td>
        1
      </lark-td>
      <lark-td>
        Internal general error. Users are not expected to care about or handle this error.
      </lark-td>
      <lark-td>
        - Used to describe some users not cared general errors
					- Error cases in sm_send_resp_mc/sm_send_resp
					- Req has been canceled due to timeout,  on the server side when doing request receive or response send.
				- Used in some protective code to prevent code generator errors.
					- SM_IFACE_INST_ID_MAX <= iface_inst_id
					- NULL == p_sm_client_data
					- NULL == ph_request_list
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_INVALID_MSG
      </lark-td>
      <lark-td>
        2
      </lark-td>
      <lark-td>
        This error code indicates that user's input data is not within the limited range of defined messages from MDF
      </lark-td>
      <lark-td>
        - bool b_msg_valid = sm_validate_msg_${interface_request_def_name_lowercase}(p_${interface_request_def_name_lowercase});
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_OUTOF_RESOURSE
      </lark-td>
      <lark-td>
        3
      </lark-td>
      <lark-td>
        This error code indicates that the buffer for this interface owned by appfw is not available currently.
      </lark-td>
      <lark-td>
        - It maybe a request has been sent but not replyed or not timeout.
					- p_sm_client_data->request_sent 
				-  It may be a queue type interface's queue is full.
					- In sm_write_queued, os_fifo_enqueue(*ph_reader_queue, p_msg) returns OS_ERR_FIFO_FULL.
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_CODEC_MSG
      </lark-td>
      <lark-td>
        4
      </lark-td>
      <lark-td>
        This error code indicates that the encode/decode error for this message data.
      </lark-td>
      <lark-td>
        - Currently, this only occurs in SOA related message handling path. And it will be used by SOAM code gen tools.
					- bool   status = pb_decode(&stream, p_msg_desc, p_payload);
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_NOT_SUPPORTED
      </lark-td>
      <lark-td>
        5
      </lark-td>
      <lark-td>
        This error code indicates that  some functions/features are not internally supported.
      </lark-td>
      <lark-td>
        - It will be used by SOAM code gen tools.
					- NRPC API is not implemented in some SOA proxy/server.
				- It will be used in "DirectFunCall".
					- When the service's function is invoked in ISR context  by the client.
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_IPI_FAILED
      </lark-td>
      <lark-td>
        6
      </lark-td>
      <lark-td>
        This error code indicates that IPI usage in AppFw returns an error, probably because the underlying IPI queue is full.
      </lark-td>
      <lark-td>
        - Client sends request to server.
        ```c
        ipi.callback = ipi_sm_send_req_handler;
        ipi.param1 = (os_ipi_callback_param_t) p_sm_client_data;
        ipi.param2 = (os_ipi_callback_param_t) ((os_ubase_t)iface_inst_id);
        os_retval = os_ipi_send(target_core, &ipi);
        ```
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_NO_MSG
      </lark-td>
      <lark-td>
        7
      </lark-td>
      <lark-td>
        This error code indicates that the reading operation for list/queue/buffer fails for no data are waiting in the list/queue/buffer.
      </lark-td>
      <lark-td>
        - When server receives request from list, the list may be empty.
					- sm_list_remove(ph_request_list, &removed_item) returns OS_SM_LIST_IS_EMPTY
				- When reader reads data from queue but no data is waiting there.
				- For bufferred msg object, if user configured with an msg validation, this error code indicates that writer has not written to it.
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_UNCONNECTED
      </lark-td>
      <lark-td>
        8
      </lark-td>
      <lark-td>
        This error code indicates that an interface is instantiated in CDF but not connected to any component.
        - Original solution: 
        Return this error code for all interfaces that are not connected.
        - Updated solution after discussing <mention-user id="ou_6eb2740b387b78a5ec2b4f0038d2333b"/><mention-user id="ou_c795b1e4bfe39a9ee46b474737e2d40d"/><mention-user id="ou_9e4246cebd7d9bbe78ccaa6886efe473"/>
        Return this error code for unconnected interfaces of the reader, request response send/recv process (server ,client). Since these api will be stopped from using known data.
        Return SUCCESS for  unconnected interfaces of the writer. To minimize this change's affecting scope, and is reasonable.
      </lark-td>
      <lark-td>
        - ~~The writer's write interface has no reader connected to it.~~
				- The reader's read interface is not connected to any writer.
				- The server's receive req or send response has no client to connect to it.
				- The client's send request or receive resp  has no client to connect to it.
      </lark-td>
    </lark-tr>
    <lark-tr>
      <lark-td>
        ERR_PARTIAL_SUCCESS
      </lark-td>
      <lark-td>
        9
      </lark-td>
      <lark-td>
        This error code indicates that the writer on the *Signal_1_NQ* interface successfully sent signal data to some readers, but failed to send signal data to others.
      </lark-td>
      <lark-td>
        - The queue of some readers is full, and the queue of other readers is not full.
      </lark-td>
    </lark-tr>
  </lark-table>

  
</reference-synced>

# RPC Error codes and handling

## System level error

### TOX not able to initialize with 2000 ms after system start 

**Applied ****NVOS**** Product**: MRTOS

**Error Catching:**

- Error Log
  ```cpp
  Console log: "Failure! Waited too long (2000 ms) for TOX to initialize!"
  ```

**Recommended Error Handling:**System failure. Please check your network configuration and guarantee if network is up immediately after system boot.

## Connection States

Clients can get connection state and related reasons through SOA Framework APIs. 

<grid cols="2">

  <column width="50">
    MCU {align="center"}
    ```c
    static void on_connect_state_handler(const sm_comp_inst_id_t comp_id)
    {
        // receive server status
        connect_state_msg_com_nio_soafwk_testserviceremotetwo_t connect_state_msg;
        sm_read_test_client_two_on_connect_state_com_nio_soafwk_testserviceremotetwo(comp_id, &connect_state_msg);
        g_connect_state = connect_state_msg.connect_state;
        g_connect_state_reason = connect_state_msg.reason;
    }
    
    ```

  </column>
  <column width="50">
    MPU {align="center"}
    ```cpp
    NrpcConnectionState connect_result;
    NrpcConnectionReason connect_reason;
    proxy.GetNative()->ListenConnectState(
        [&connect_result, &connect_reason](const NrpcConnectionState& state, const NrpcConnectionReason& reason){
            LOG_I("NrpcConnectionState: %d, reason: %d", state, reason);
            connect_result = state;
            connect_reason = reason;
        });
    
    ```

  </column>

</grid>

### States

<reference-synced source-block-id="BhB6doxp3sBspmbhCHUcztcznnf" source-document-id="OdXvdoF9ooMju3x2XVfcBdy3nRf">

  <whiteboard token="Pi9Tw1ICQhxOFibqv0UcQ1Kynxg" width="717" height="338" align="center"/>

</reference-synced>

#### (0) STATE_DISCONNECTED / kDisconnected

**DESCRIPTION:**Not connected to server yet. Clients should not use server's API at this time. In this state, SOA Framework is still trying to connect to the server.

#### (1) STATE_CONNECTING / kConnecting

**DESCRIPTION:**Intermediate state when connecting to server yet. Clients should not use server's API at this time.

#### (2) STATE_CONNECTED / kConnected

**DESCRIPTION:**Successfully connected to server.

#### (3) STATE_TERMINATED / kTerminated

**DESCRIPTION:**Client is not connected to server, and SOA Framework will never try to connect to server anymore. This is usually caused by some unrecoverable failures. Please check the reason for more info.

### Reasons

<source-synced align="1">

  #### (0) NO_ADDITIONAL_INFO / kNoAdditionalInfo
  **DESCRIPTION:**This is the default value. No additional handling is needed. The connection is terminated gracefully.
  
  #### (1) INCOMPATIBLE_SERVER / kIncompatibleServer
  **DESCRIPTION:**Reason for TERMINATED. Client and server are incompatible, and can't be connected
  **Recommended Error Handling:**
  1. Please check DLT log to see if IDL version matches, reliability configuration matches.
  
  #### (2) AUTH_FAILED / kAuthFailed
  **DESCRIPTION:**Reason for TERMINATED**.**Authentication failed during client-server authentication handshake
  **Recommended Error Handling:**
  1. Please check DLT LOG to see which side has authentication issues: client or server. And change configuration to correct one.
  
  #### (3) PERMISSION_DENIED / kPermissionDenied
  **DESCRIPTION:**Reason for TERMINATED**.**Request/Set/Get/Subscription denied by server because of no permission.
  **Recommended Error Handling:**
  
  #### (4) RELIABLE_WINDOW_DIFF / kReliableWindowDiff
  **DESCRIPTION:**Reason for TERMINATED**.**Check inconsistent reliability during client-server recv data.
  **Recommended Error Handling:**
  
  #### (5) RELIABLE_WINDOW_FAIL / kReliableWindowFail
  **DESCRIPTION:**Reason for DISCONNECTED. Reliable queues are full and frozen for too long. SOA Framework decided to reset this connection.
  **Recommended Error Handling:**
  1. If this happens a lot, you need to check whether any side of this connection's processing capability is too low.
  
  #### (6) NOT_MATCHED_SECURITY_CONFIG / kNotMatchedSecurityConfig
  **DESCRIPTION:**Reason for DISCONNECTED. At the handshake stage, the client and the server exchanged their security configurations and found they did not match.
  **Recommended Error Handling:**
  1. Check security mode of the client and the server, and ensure they're the same.
  
  #### (7) QUERY_OVER_LIMIT / kQueryOverLimit
  **DESCRIPTION:**Reason for `DISCONNECTED (since v01.00.06)` / `TERMINATED (until v01.00.04)`. Client has sent QUERY too many times that reaches the quota configured in deployment file. 
  **Recommended Error Handling:**
  1. If you're running a test application, just restart the application.
	1. If not, please check why the service can't be discovered.
  
  #### (8) KICKED_OFFLINE_BY_CLIENT_WITH_SAME_ID / kKickedOfflineByClientWithSameId
  **DESCRIPTION:**Reason for TERMINATED. A new client with the same "client_id" is connected to the service, and this client is disconnected because a service can only support 1 connection to each non-zero "client_id".
  **Recommended Error Handling:**
  1. Please check if your client is configured with the correct "client_id" in deployment file.
	1. If your client is configured with correct "client_id", please check with service developer who has configured with wrong "client_id".

</source-synced>

## Messages errors

### General errors

#### Error catching - MCU

- Direct reporting: get return code from generated APIs. e.g.
  ```c
  static void send_method_one_request(void)
  {
      req_msg_xxx_requestmethodone_t methodOne = {};
  
      if (sm_send_req_xxx_request_xxx_requestmethodone( g_comp_id, &methodOne) != SUCCESS)
      {
          console_print("Send methodOne request error\n");
          return;
      }
  }
  ```

- Indirect reporting: 
	- Get error code from `on_soa_error_handler`
    ```cpp {wrap}
    static void app1_on_soa_error_helloworldmcu_handler(const sm_comp_inst_id_t comp_id)
    {
        soa_error_msg_t soa_error_msg;
        sm_read_app1_on_soa_error_helloworldmcu(comp_id, &soa_error_msg);
    
        console_print("=== HelloWorldMcu Base === app1 receives rpc id = %u, method_type = %u, soa error = %u, error msg = %s.\n",
                      soa_error_msg.rpc_id,
                      soa_error_msg.method_type,
                      soa_error_msg.error_code,
                      soa_error_msg.error_msg);
    }
    ```

  - For Request-reply, read error code from reply msg
    ```c
    static void on_methodone_response_arrived(const sm_comp_inst_id_t comp_id)
    {
        reply_msg_com_xxx_requestmethodone_t response;
        if ( sm_recv_resp_test_client_two_request_xxx_requestmethodone ( comp_id, &response) != SUCCESS)
        {
            return;
        }
    
        if (0 == response.error_code)
        {
            // Handle this response
        }
        else
        {
            console_print("recieved method one response with error, error_code: %d\n", 
                response.error_code);
        }
    }
    ```

#### Error catching - MPU

- Direct reporting: get return code from generated APIs. e.g.
	- For `async APIs`, error code returned in Callback
    ```cpp
    void SayHelloAsync(
        const ::nrpc::example::HelloRequest& request,
        const ::nio::nrpc::MethodCallInfo& info,
        const SayHelloAsyncCallback& callback,
        unsigned char group_index = 0,
        ::nio::nrpc::Priority prio = ::nio::nrpc::Priority::kNormal)
    ```

  - For `sync APIs` and `oneway APIs`, error code returned in return value.
    ```cpp
    ::nio::nrpc::NrpcErrorCode RequestMethodOneSync(
        const ::com::nio::soafwk::HelloRequest& request,
        const ::nio::nrpc::MethodCallInfo& info,
        ::com::nio::soafwk::HelloReply& reply,
        unsigned char group_index = 0,
        ::nio::nrpc::Priority prio = ::nio::nrpc::Priority::kNormal);
        
    ::nio::nrpc::NrpcErrorCode setHelloFieldOneWay(
        const ::nrpc::example::HelloRequest& request,
        unsigned char group_index = 0,
        ::nio::nrpc::Priority prio = ::nio::nrpc::Priority::kNormal)kTimeoutNoResponse
    ```

- Indirect reporting: 
	- Get error code from `ListenErrorEvent`
  ```cpp {wrap}
  service.GetNative()->ListenErrorEvent([&](const NrpcErrorEvent& err_event){
      int32_t rpc_id = err_event.rpc_id;
      NrpcErrorCode error_code = err_event.error_code;
      LOG_I("ListenErrorEvent Callback, rpc_id: %u, method_type: %u, error_code: %u, error_msg: %s",
          rpc_id, err_event.method_type, error_code, err_event.error_msg.c_str());
  });
  ```

  - For Request-reply, get error code from reply message
  ```cpp
  proxy.RequestMethodOneAsync(*request, info, [](NrpcErrorCode error, HelloReply*  reply) {
      if (error != nio::nrpc::NrpcErrorCode::kSuccess) {
          LOG_E("fail to RequestMethodOneAsync, error: %d", error);
          return;
      }
      // got reply
      LOG_I("Received methodone resp successfully, answer: %s, sum: %d", reply->answer().c_str(), reply->sum());
  });
  ```

#### Error codes

<source-synced align="1">

  ##### (0) NRPC_SUCCESS /  kSuccess
  **DESCRIPTION****: **Everything is OK.
  
  ##### (1) NRPC_INTERNAL_FAIL / kInternelFail
  **DESCRIPTION****: **A general failure
  **Error Message**:
  - TOX error code
	- App error code (<text color="green">MCU only</text>)
	- Received method_type is invalid
  **Recommended Error Handling:**
  1. Consult NVOS team for this.
  
  ##### (2) NRPC_NOT_EXIST / kNotExist 
  **DESCRIPTION:**The resource user trying to access doesn't exist, or this request is rejected for undisclosed reasons, e.g. access rights not granted.
  **Recommended Error Handling:**
  1. This should not happen. If it happens, please report to NVOS team.
  
  ##### (3) NRPC_ALREADY_EXIST / kAlreadyExist
  **DESCRIPTION:**The resource user trying to create already exists. 
  **Recommended Error Handling:**
  1. This error is not used yet.
  
  ##### (4) NRPC_OUT_OF_MEMORY / kOutOfMemory
  **DESCRIPTION:**SOA Framework has run out of memory
  **Error Message**: 
  - TOX error code
  **Recommended Error Handling:**
  1. Check** **TOX configuration according to <mention-doc token="wikcnslJXjSB86luOOH29r9VNyd" type="wiki">TOX Configuration Manual</mention-doc> 
	1. If this error can't recover, it might be a bug. Please report to NVOS team.
  #####  
  ##### (5) NRPC_SERDES_FAIL / kSerDesFail
  **DESCRIPTION****: **serialization or deserialization failure
  **Error Message**: 
  - Toxbind encode/decode failed (toxbind codec error code)
	- Nanopb error msg (<text color="green">MCU only</text>)
	- App error code: `ERR_CODEC_MSG` (<text color="green">MCU only</text>)
  **Recommended Error Handling:**
  1. (MPU only) NANO format related: the client / server tries to handle NANO format but failed. Please check:
		1. Check if the IDL has an .options file but not included during code generation.
		1. If all the var-length fields have corresponding options defined.
		1. If any unsupported protobuf types are used, e.g. OneOf, Group, Map...
	1. Deserialization: Check if client-server's IDL and <text underline="true">**options file**</text> match. Most cases are caused by unmatched <text underline="true">**options**</text> files.
	1. Serialization failure: this should not happen. If it happens, please report to NVOS team.
  
  ##### (6) NRPC_BAD_PARAMETER /  kBadParameter
  **Description:**User** **provided bad parameters
  **Possible causes**: 
  - Parameter validation failure by SOA Framework
	- Parameter validation failure by receiver (mostly in a reply sent back by server)
  **Error Message**: 
  - App error code: `ERR_INVALID_MSG` (<text color="green">MCU only</text>)
	- Request range is invalid
	- method_type is invalid (RR)
	- timeout_millis is invalid (RR)
	- Reply handler (ticket) is invalid (reply)
  **Recommended Error Handling:**
  1. Check if timeout parameter is set ( > 0). For detail: <mention-doc token="Kcdiw1NuQigFL6kntjBcoYVJn3e" type="wiki">SOA请求时timeout参数的设置说明</mention-doc> 
		- MPU side
      ```cpp
      MethodCallInfo info;
      info.time_out = 3000; // Default value 0 for time_out is unacceptable
      
      HelloRequest request;
      request1.set_greeting("hehehe");
      
      HelloReply reply1;
      
      // test request sync
      auto error = proxy.SayHelloSync(request1, info, reply1);
      ```

    - MCU side
      ```cpp
      req_msg_com_nio_soafwk_testserviceremotetwo_requestmethodone_t methodOne = {};
      methodOne.request_msg.a = 40;
      methodOne.timeout_millis = 3000; // Default value 0 for time_out is unacceptable
      
      if (sm_send_req_test_client_two_request_com_nio_soafwk_testserviceremotetwo_requestmethodone( g_comp_id, &methodOne) != SUCCESS)
      {
          console_print("Send methodOne request error\n");
          return;
      }
      ```

  1. Check if parameter value exceeded range set in IDL
    e.g. `float c` and `uint64 d` have preset range.
    ```protobuf
    message HelloRequest {
        string greeting = 1;
        int32 a = 2;
        int32 b = 3;
        float c = 4 [(float_max_value) = 16.5, (float_min_value) = 3.75];
        uint64 d = 5 [(integer_max_value) = 50, (integer_min_value) = -3];
    }
    ```

  1. If you directly use NRPC layer's API, please check if your input is correct. 
    e.g. method_type within defined range
    ```shell
    typedef enum nrpc_method_type
    {
        TYPE_NULL = 0,
        REQUEST_REPLY = 1,
        ONE_WAY = 2,
        SET_FIELD = 3,
        GET_FIELD = 4,
        SUB_PUB = 5,
        BUILD_IN_CHK_VER = 6
    } nrpc_method_type_t;
    ```

  1. (`Since SkyOS-S v01.00.04`) Check if your data size exceeds the `max_size`, `max_length`, `max_count` in `.options` file. Check <mention-doc token="ORMNwWtx2innGCkQZbEcajPlnab" type="wiki">SkyOS-S v01.00.04</mention-doc> for detailed info.
    ```protobuf {wrap}
    # myproto.proto
    message MyMessage {
        string name = 1;
        bytes  class= 3;
        repeated int32 ids = 2;
    }
    
    # myproto.options
    MyMessage.name         max_length:40
    MyMessage.class        max_size:20
    MyMessage.ids          max_count:5
    ```

  1. Others: please check DLT log for more info.
  
  ##### (7) NRPC_NO_RESPONSE / kTimeoutNoResponse
  **DESCRIPTION:**User's request is not replied within specified `timeout`  
  **Possible causes:**
  - The server did not receive the request in time.
	- The server received the request but didn't send back a reply in time.
	- The response returned too late.
  **Error Message**: 
  - TOX error code: `TOX_ERR_CLIENT_TIMEOUT`
  **Recommended Error Handling:**
  - If it's acceptable for a request to be discarded, then this error code can be ignored. In fact, the user shall consider using one-shot FF in this scenario. *But this is very unusual! You must be sure to understand what you're doing!*
	- If not, there are two recommended strategies:
		- Only pass the error messages to the upper layer
		- Retransmission
			- The prerequisite for retransmission is that the request is **idempotence**: even if the request is executed multiple times, the result is the same as when it is executed once
			- Finite retransmission: the total times depends on the message's lifespan. For example, it is acceptable for communication to be completed within `T` from a functional perspective. Then, `n` (typically 3 ~ 5) tries can be performed within `T`, with `RR timeout` = `T/n`. 
			- Infinite retransmissions: If the business wants a command to be delivered (retransmit the last timeout value), or the latest data to be delivered (retransmitting the latest value), it can also choose infinite retransmissions until no timeout occurs. It might be that the message has been delivered or the connection is down (NRPC_NOT_CONNECTED). Infinite retransmissions is equivalent to periodic sending in extreme cases.
  
  ##### (8) NRPC_NOT_CONNECTED / kNotConnected
  **DESCRIPTION:**Client's request is not sent because client is not connected to server.
  **Possible causes:**
  - The connection state is DISCONNECTED when calling the API.
	- When calling the API, the connection status is CONNECTED. However, the connection status changes to DISCONNECTED, before the RR or Non-ACKed Reliable message receives a reply.
  **Error Message**: 
  - TOX error code
  **Recommended Error Handling:**
  1. Please resend this request after the server is connected. 
  
  ##### (9) NRPC_NOT_IMPLEMENTED / kNotImplemented
  **DESCRIPTION:**The logic is not implemented / supported within SOA Framework. e.g. A RPC ID's callback is not generated.
  **Error Message**: 
  - SOAM callback is null
	- App error code: `ERR_NOT_SUPPORTED` (<text color="green">MCU only</text>)
  **Recommended Error Handling:**
  1. (**Since** NService 01.01.05) On MPU, if you use `ReadXXX` or `ReceiveXXX` interface, please ensure "disable callback" is configured for that `RPC Interface` in <app>.deployment.json. Check detail in <mention-doc token="KeUfwicvQi4DdQko9Z0ce3ydnXc" type="wiki">Support Read from Queue and Disable Callback on MPU</mention-doc>
	1. (**Since** NService 01.00.06) On MPU, check if you're using synchronization request within SOA Framework's callback. This is not allowed because callback is a kind of asynchronous interface and should not be mixed with synchronized request. In current implementation, it may result in:
		1. Disordered processing between async and sync response
		1. Blocking of SOA Framework callback thread for unpredictable time
	1. Otherwise, please check with NVOS team if this happens.
  
  ##### (10) NRPC_MESSAGE_DROPED / kMessageDropped
  **DESCRIPTION****: **The message is dropped within SOA Framework
  **Error Message**: 
  - TOX error code: `TOX_ERR_DROP`
  **Recommended Error Handling:**
  1. Check DLT log for reason of dropping. e.g. 
  ```cpp
  "err(1) drop invoke"
  ```

  ##### (11) NRPC_INIT_FAILED (MCU only)
  **DESCRIPTION:** SOA initialization failed
  **Error Message**: 
  - TOX init failed
	- Dispatch thread failed
	- Create broker failed
	- Create tox obj failed
	- Channel type not supported
	- Channel type invalid
	- Server backend is null (when publish)
	- Soam is initializing
  **Recommended Error Handling:**
  When this error occurs, the client or server cannot send any message. Please report to the NVOS team.
  
  ##### (12) kShapingQueueFull (MPU only)
  **DESCRIPTION:** The interface enables Shaping QoS, but sending frequency exceeds configured interval too much that the caching queue is full. And so a message is dropped.
  **Recommended Error Handling:**
  - Investigate why this queue is full: 
		- Is sending behavior faster than expected?
		- Or does the user just expect the Shaping QoS to work and drop some burst message?
  
  ##### (13) NRPC_TERMINATED_BY_USER / kTerminatedByUser
  **DESCRIPTION:**The message is not sent because the user terminates the proxy or server when SOA Framework is just about to handle this message.
  **Recommended Error Handling:**
  - If this message is not critical, just ignore this error.
	- If this message is critical, resend the message after proxy or server become online.
  
  ##### (14) kDeprecatedItemUsed (MPU only)
  <callout emoji="point_right" background-color="light-orange" border-color="light-orange">
  This error only reports to Cloud server. Users can never receive this error code.
  </callout>

  **DESCRIPTION:**A deprecated API is invoked by the user.
  
  ##### (31) NRPC_QOS_RELIABILITY_DROP_MESSAGE / kQosReliabilityDropMessage
  **DESCRIPTION:**Message is dropped because sending window is full or timeout waiting for the ACK
  **Recommended Error Handling:**
  - When sending window is full, retrying immediately is not recommended. The user can choose to
		- Delay a little while before retrying.
		- Report to upper layer about this error
  
  ##### (32) NRPC_QOS_RELIABILITY_CLOSE_ON_ERROR / kQosReliabilityCloseOnError
  **DESCRIPTION:**The reliability sliding window freeze time exceeds configured timeout. And SOA Framework decides to clear all the messages inside the sliding window.
  **Recommended Error Handling:**
  - Figure out the reason why the sliding window freezes:
		- If it is due to limited window size, try adjusting the max window size.
		- If it is due to a brief timeout, consider raising the transport's timeout value.
  
  ##### (33) NRPC_QOS_RELIABILITY_MISMATCH_CFG / kQosReliabilityMismatchCfg
  **DESCRIPTION:**The reliability setting in the received message does not match the local interface's configuration. This error occurs when the reliability setting of an interface is inconsistent between the server and the client.
  **Recommended Error Handling:**
  - Check if the reliability settings of the interface in the IDL file used by the server and the client are the same.
	- Check if interfaces are generated using the latest code generator.
	- Check if the SOA Framework version used by the server and client are compatible.
  
  ##### (92) NRPC_SERVER_INTERNAL_ERROR / kServerInternalError
  **DESCRIPTION****: **This error is set by server application, indicating internal error happened within server and can't process such request
  **Error Message**: N/A
  **Recommended Error Handling:**
  1. Check with server developer to see what is happening
  
  ##### (93) NRPC_VERSION_LOST / kVersionLost
  **DESCRIPTION****:** IDL Version problem
  **Error Message**: 
  - Version is invalid
	- Server version lost
  **Recommended Error Handling:**Check here: <mention-doc token="DyBsdMbhtoMTXExlDARcmmJvnad" type="docx">IDL Version Check User Guide</mention-doc> 
  
  ##### (94) NRPC_VERSION_CHECK_FAIL / kVersionCheckFail
  **DESCRIPTION:** IDL Version problem
  **Error Message**: 
  - Check server version min fail
	- Check server version max fail
	- Check client version min fail
	- Check client version max fail
  **Recommended Error Handling:**Check here: <mention-doc token="DyBsdMbhtoMTXExlDARcmmJvnad" type="docx">IDL Version Check User Guide</mention-doc> 
  
  ##### (95) NRPC_RCV_QUEUE_FULL / kRcvQueueFull
  **DESCRIPTION:**The queue on receiver side is full. For RR-Request, this error code is also included in reply. Refer to <mention-doc token="HbVTduU9KocJbzxRlEacQsX9nEf" type="docx">QoS Policy: History</mention-doc> for more info.
  **Possible Reason:**
  - The sending side's sending speed overwhelms receiving side's processing speed.
  **Error Message**: 
  - App error code: `ERR_OUTOF_RESOURSE` (request) (MCU only)
	- Recv queue is full (oneway/notify/reply)
  **Recommended Error Handling:**
  - Don't resend immediately: If the business requirements permit, please delay the retransmission.
	- Does the server have proper queue size?  Check [Recommended Settings](https%3A%2F%2Fnio.feishu.cn%2Fdocx%2FHbVTduU9KocJbzxRlEacQsX9nEf%23F3C3dEiDLonzlWxIMOjcUnTfned) here.
  
  ##### (96) NRPC_INTEGRITY_VERIFY_FAILED / kIntegrityVerifyFailed
  **DESCRIPTION:**Integrity verify failed for this request (RR type) because of:
  - MAC protection verification failed
  **Error Message**: N/A
  **Recommended Error Handling:**
  1. This shall recover after retrying. Otherwise, please report to NVOS team.
  
  ##### (97) NRPC_FIELD_CACHE_NOT_INITIALIZED / kFieldCacheNotInitialized
  **DESCRIPTION:**The field cache is not initialized yet but has already received a "GET" request or "GET on SUBSCRIBE" request. This only happens when field cache is enabled by setting "`replace_get_with_notification_cache`" to ON or "`field_cache_timeout`" to non-zero.
  **Error Message**: N/A
  **Recommended Error Handling:**
  1. Initialize the field cache at server startup.

</source-synced>

### E2E errors

E2E has special requirements, and has its own interfaces to handle errors. For detailed info, please refer to <mention-doc token="Iyl1db7vIoV2j7xinR6cKUAwnVd" type="docx">SOA E2E Communication Protection (MPU)</mention-doc>  <mention-doc token="XerVdFNqsobsq0xgasNcrjs5nSb" type="docx">SOA E2E Communication Protection (MCU)</mention-doc> 

#### Error Catching

##### Option 1: Only get the e2e state

<grid cols="2">

  <column width="55">
    MCU: Listen for the `xxx_on_e2e_state_xxx_handler` callback and call `sm_read_xxx_on_e2e_state_xxx`
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
            return;
        }
    
        // Log the received E2E state details.
        console_print("=== HelloWorldMcu Base === app2 receives [2b][E2E][EVENT] E2E state = %d\n",
                      e2e_state.status);
    }
    ```

  </column>
  <column width="44">
    MPU: Call the `ListenE2eEvent` interface to get the E2E state
    
    ```cpp
    service.ListenE2eEvent([&](const NrpcE2eEvent& event) {
        int32_t rpc_id = event.rpc_id;
        NrpcE2eStatus e2e_status = event.e2e_status;
        
        LOG_I("ListenE2eEvent Callback, rpc_id: %d, e2e_status: %d", 
            rpc_id, 
            e2e_status);
    });
    ```

    
  </column>

</grid>

##### Option 2: Read the E2E state along with the data

<grid cols="2">

  <column width="50">
    MCU: Listen for the `on_request_xxx_handler` callback and call `sm_read_e2e_xxx_on_notify_xxx` to read the E2E state with the data
    ```cpp
    static void
    on_request_helloworldmcu_sayhelloonewaymcu_handler(const sm_comp_inst_id_t comp_id)
    {
        // Initialize structures for the 'sayhellooneway' request and E2E state.
        req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t hello_request = {};
        sm_e2e_state_t                                         e2e_state     = {};
    
        // Read the 'sayhellooneway' request and the E2E state.
        if (sm_read_e2e_app1_on_request_helloworldmcu_sayhelloonewaymcu(
                comp_id, &hello_request, &e2e_state)
            != SUCCESS)
        {
            return;
        }
    
        // Log the received request details.
        console_print(
            "=== HelloWorldMcu Base === app1 receives [2a][METHOD_ONEWAY] oneway method sayhello "
            "request with greeting = \"%s\", a = %d, b = %d, E2E state = %d\n",
            hello_request.request_msg.greeting,
            hello_request.request_msg.a,
            hello_request.request_msg.b,
            e2e_state.status);
    }
    
    ```

  </column>
  <column width="50">
    MPU: Listen for the `registerxxxHandler` callback to read the E2E state with the data.
    
     
    ```cpp
    service.registerE2eRequestOneWayHandler([&](const ::nio::nrpc::NrpcSession& session,
                                                ::nio::nrpc::NrpcE2eStatus e2e_status,
                                                const ::nrpc::example::FuSaE2eRequest& request) {
        LOG_I("registerE2eRequestOneWayHandler, e2e_status = %d, greeting is %s", 
            e2e_status, 
            request.greeting().c_str());
    });
    ```

    
  </column>

</grid>

#### Error codes

##### (0) E2E_STATUS_OK / kE2eStatusOk

##### (1) E2E_STATUS_OK_SOME_LOST / kE2eStatusOkSomeLost

##### (2) E2E_STATUS_ERROR / kE2eStatusError

##### (3) E2E_STATUS_REPEATED / kE2eStatusRepeated

##### (4) E2E_STATUS_NONEWDATA / kE2eStatusNoNewData

##### (5) E2E_STATUS_WRONGSEQUENCE / kE2eStatusWrongSequence

Please check detailed info in  <mention-doc token="Iyl1db7vIoV2j7xinR6cKUAwnVd" type="docx">SOA E2E Communication Protection (MPU)</mention-doc>  <mention-doc token="XerVdFNqsobsq0xgasNcrjs5nSb" type="docx">SOA E2E Communication Protection (MCU)</mention-doc> 

# TOX Error Codes

<source-synced align="1">

  ### (0) TOX_ERR_OK
  - value 0, means no error
  
  ### (1) TOX_ERR_ARG
  - value 1, means illegal argument
	- usage scenarios
		-  The parameters passed in do not match the expected parameters, making the expected logic unexecuting
			- When calling tox_caller_complete, the parameters passed in do not match caller
			- When _tox_client_send_subscribe is called, the parameter client passed in is empty or does not have a subscribe id
			- There is no matching condition in switch or if
  
  ### (2) TOX_ERR_SEND_FAILED
  - value 2, request is rejected by server
	- usage scenarios
		- Call send failed 
  
  ### (3) TOX_ERR_CALLER_OUT
  - value 3, too many request
	- usage scenarios
		- Out of memory, caller allocation failed
  
  ### (4) TOX_ERR_BUFFER_OUT
  - value 4,  no more buffer
	- usage scenarios
		-  Failure to allocate memory, either object failure or buffer exhaustion
		-  Can be subdivided
    ```c
    bridge_out
    sender out
    buffer out
    poster out
    office out
    sagent out
    ragent out
    caller agent out
    cagent out
    seglnk out
    ```

  
  ### (5) TOX_ERR_STREAM_OUT
  - value 5,  server has no space for subscribing
	- usage scenarios
		- Out of memory, stream allocation failed
  
  ### (6) TOX_ERR_CLIENT_OFFLINE
  - value 6, client is offline
	- usage scenarios
		- heartbeat timeout
		- active disconnect
		-  The received message did not match to the client
  
  ### (7) TOX_ERR_CLIENT_TIMEOUT
  - value 7, response is timeout
	- usage scenarios
		- response timeout
		- <text bgcolor="light-purple">Can be changed to response timeout</text>
  
  ### (8) TOX_ERR_WINDOW_OUT
  - value 8, reliable window is full
	- usage scenarios
		- The local send window is full
		- The remote receive window is full
		- <text bgcolor="light-blue">Local txslot memory allocation failed </text>
			- <text bgcolor="light-purple">Enable the new error code TOX_ERR_TXSLOT_OUT</text>
  
  ### (9) TOX_ERR_SECURE_GEN
  - value 9,  gen sign/mac/encrpyt failed
	- usage scenarios
		- There is no sec_intrinsic callback function
			- <text bgcolor="light-blue">Enable the new error code TOX_ERR_NOT_SUPPORT_SECURITY</text>
		- There is no local callback function for security (similar to the first one)
			- <text bgcolor="light-blue">Enable the new error code TOX_ERR_NOT_SUPPORT_SECURITY</text>
		- <text bgcolor="light-blue">Security memory allocation failed, which can be attributed to buffer out: security_out</text>
			- Enable the new error code TOX_ERR_SECURITY_OUT
		- Encryption failed ---- to match
  
  ### (10) TOX_ERR_UNICAST_PORT_INVALID
  - value 10, unicast port is invalid
	- usage scenarios
		- The port for socket is not within the allowed range
  
  ### (11) TOX_ERR_PARAM_ENCODE_FAILED
  - value 11, param encode failed
	- usage scenarios
		- Serialization failed on send
  
  ### (20) TOX_ERR_NO_TIME_DOMAIN
  - value 20, domain state lost
	- usage scenarios
		- Lifespan failed to detect domain state
  
  ### (21) TOX_ERR_LIFESPAN_TIMEOUT
  - value 21, method call is received but expired
	- usage scenarios
		- Lifespan check timed out
  
  ### ~~(22) TOX_ERR_DISPATCH_BUFFER_OVER~~
  - value 22, dispatch err cause msg not receive
	- usage scenarios
		- Not used
  
  ### ~~(23) TOX_ERR_CRC~~
  - value 23, CRC verify failed
	- usage scenarios
		- Not used
  
  ### (24) TOX_ERR_DROP
  - value 24, drop message
	- usage scenarios
		- In the single-core scenario, the dispatch callback function returns a non-zero value
		- In a multicore scenario, when dispatching, poster creation fails with Reliable enabled
			- <text bgcolor="light-blue">Enable the new error code  TOX_ERR_POSTER_OUT_DROP</text>
		- In a multicore scenario, poster creation fails when client/server is removed
			- <text bgcolor="light-blue">enable the new error code  TOX_ERR_POSTER_OUT_DROP</text>
  
  ### (25) TOX_ERR_WINDOW_DROP
  - value 25, for client/server: drop the reliable sender during  tx window is full or  waiting for the ACK  timeout(reliable_cto). 
	- usage scenarios
		- When the application sends a reliable message, the sender message should be  join the tx window queue, the message will be dropped when window is full, and report the error of dropping sender is called TOX_ERR_WINDOW_DROP.
		- When reliable sender joins the tx window sucessfully，sender shall start a timer for the packet waiting for acknowledegment。The sender will clear the window after timeout(default:5000ms，configured by ToxRunnerConfig.reliable_cto).
  
  ### ~~(26) TOX_ERR_WINDOW_LOSS~~
  value 26, for client: reliable message dropped during publishing
  usage scenarios
  Not used
  
  ### (27) TOX_ERR_WINDOW_FAIL
  - value 27, service breaks due to reliable queue is frozen
	- usage scenarios
		- When the packet in the receive queue times out,
		- When recieve packet sn is over the window.  force moving and dropping the left recived packet
  
  This code has an alias as TOX_ERR_WINDOW_TX_TIMEOUT
  - Session gets timeout on sending reliable message
	- Usage scenarios
		- application will get this error when all following conditions are true:
			- Sum of reliable sender beyond risk level (see: reliable config)
			- The session has at least one sender beyond clear-timeout (see: reliable config)
			- The session is closed due to above two reasons
  
  ### (28) TOX_ERR_WINDOW_DIFF
  - value 28, service breaks due to inconsistent reliability
	- usage scenarios
		- An error occurred while checking inconsistently
  
  ### (29) TOX_ERR_PERMISSION_DENIED
  - value 29, Request/Set/Get/Subscription denied by server because of no permission
	- usage scenarios
		- The security auth check failed
  
  ### (30) TOX_ERR_AUTH_FAILED_CERT
  - value 30, Invalid cert
	- Usage scenarios
		- get role failed
			- <text bgcolor="light-blue">Enable the new error code TOX_ERR_AUTH_GET_ROLE_FAILED</text>
		- verify cert failed
  
  ### (31) TOX_ERR_AUTH_FAILED_SIGNATURE
  - value 31, Invalid signature in message
	- Usage scenarios
		- sign verify failed
  
  ### (32) TOX_ERR_AUTH_FAILED_NO_SUPPORTED_MAC_ALG
  - value 32, No supported MAC algorithms in received list
	- Usage scenarios
		- security consult ciphersuit failed and protection_type != encryption
  
  ### (33) TOX_ERR_AUTH_FAILED_NO_SUPPORTED_ENC_ALG
  - value 33, No supported encryption algorithms in received list
	- Usage scenarios
		- security consult ciphersuit failed and protection_type == encryption
  
  ### ~~(34) TOX_ERR_AUTH_FAILED_SERVICE_NOT_MATCH_CERT~~
  - value 34, Not matched information between server sand its certificate
	- Usage scenarios
		-   - Not used
  
  ### (35) TOX_ERR_AUTH_FAILED_HASH_LOGON_NOT_MATCH_GRANT
  - value 35
	- Usage scenarios
		- grant checking and secure_mode != AUTH_SERVER_ONLY
  ### (37) TOX_ERR_BRIDGE_OUT
  - value 37, too many request
	- usage scenarios
		- Out of memory and bridge allocation failed
  
  ### (38) TOX_ERR_SENDER_OUT
  - value 38, too many request
	- usage scenarios
		- Out of memory and sender allocation failed
  
  ### (39) TOX_ERR_POSTER_OUT
  - value 39, too many request
	- usage scenarios
		- Out of memory and poster allocation failed
  
  ### (40) TOX_ERR_OFFICE_OUT
  - value 40, too many request
	- usage scenarios
		- Out of memory and office allocation failed
  
  ### (41) TOX_ERR_SAGENT_OUT
  - value 41, too many request
	- usage scenarios
		- Out of memory and sagent allocation failed
  
  ### (42) TOX_ERR_RAGENT_OUT
  - value 42, too many request
	- usage scenarios
		- Out of memory and ragent allocation failed
  
  ### (43) TOX_ERR_CALLER_AGENT_OUT
  - value 43, too many request
	- usage scenarios
		- Out of memory and caller agent allocation failed
  
  ### (44) TOX_ERR_CAGENT_OUT
  - value 44, too many request
	- usage scenarios
		- Out of memory and cagent allocation failed
  
  ### (45) TOX_ERR_SEGLNK_OUT
  - value 45, too many request
	- usage scenarios
		- Out of memory and seglnk allocation failed
  
  ```c
  static void _tox_sender_output_bridge(tox_broker *broker, tox_bridge *bridge, char mc, char queue)
  {
      ...
              _tox_sender_drop_output(broker, sender, TOX_ERR_BUFFER_OUT);
      ...
  }
  ```

  ### (46) TOX_ERR_TXSLOT_OUT
  - value 46, too many request
	- usage scenarios
		- Out of memory and txslot allocation failed
  
  ### (47) TOX_ERR_SECURITY_OUT
  - value 47, too many request
	- usage scenarios
		- Out of memory and security allocation failed
  
  ### (48) TOX_ERR_POSTER_OUT_DROP
  - value 48,  create poster failed when dispatching
	- usage scenarios
		- In a multicore scenario, when dispatching, poster creation fails with Reliable enabled
		- In a multicore scenario, poster creation fails when client/server is removed
  
  ### (49) TOX_ERR_SEND_MSG_SIZE_INVALID
  - value 49, sender size or fragment size invalid
	- usage scenarios
		- The encoding before sending
  ### (50) TOX_ERR_NOT_SUPPORT
  - value 50, callback not set for client or server
	- usage scenarios
		- cls->on_removed not set
		- server_class->on_method not set
  ### (51) TOX_ERR_NOT_SUPPORT_SECURITY
  - value 51,  gen sign/mac/encrpyt failed
	- usage scenarios
		- There is no sec_intrinsic callback function
		- There is no local callback function that supports security
  
  ### (52) TOX_ERR_ENCODE_SECURITY_FAILED
  - value 52, Invalid cert
	- Usage scenarios
		- security failed
		- build security foot failed
    
  ### (53) TOX_ERR_AUTH_GET_ROLE_FAILED
  - value 53, Invalid cert
	- Usage scenarios
		- get role failed
  
  ### (54) TOX_ERR_REMOVE_BINDING
  [TOX internal]
  - value 54, unbinding. 
	- Usage scenarios
		- client/server unbinding
  ### (55) TOX_ERR_DISCONNECT
  [TOX internal]
  - value 55, remote disconnect. 
	- Usage scenarios
		- client/server disconnect
  ### (56) TOX_ERR_INCOMPATIBILITY_SDK_VERSION
  - value 56, version not match
	- Usage scenarios
		- Not matched SDK major version
  ### (57) TOX_ERR_INCOMPATIBILITY_IDL_VERSION
  - value 57, version not match
	- Usage scenarios
		- Not matched IDL major version
  ### (58) TOX_ERR_ILLEGAL_FRAME
  - value 58,  recv illegal frame
	- Usage scenarios
		- Received an illegal frame
  ### (59) TOX_ERR_AUTH_FAILED_SECURITY_MODE_NOT_MATCHED
  - Security mode of client and server don't match
	- Usage scenarios
		- At handshake stage, client and server will exchange their security mode. 
  ### (60) TOX_ERR_QUERY_OVER_LIMIT
  - Query times over limit
	- Usage scenarios
		- At handshake stage, The client keeps querying, but it never matches the service.
  ### (61) TOX_ERR_SAME_USER
  - The same service encounters multiple clients with the same instance id
	- Usage scenarios
		- An error is detected when the server receives the service.
  ### (62) TOX_ERR_CONFIG_NO_CA
  - Security ca is not provided
	- Usage scenarios
		- Security.
  ### (63) TOX_ERR_BRIDGE_TIMEOUT
  - Heartbeat timeout
	- Usage scenarios
		- After a connected endpoint is established, one endpoint does not receive peer messages for a long time.
  ### (64) TOX_ERR_BRIDGE_REBOOT
  - The peer has been detected
	- Usage scenarios
		- Connection detection: The local end finds that the corresponding remote end has been disconnected and restarted in the existing connection
  ### (65) TOX_ERR_ILLEGAL_CLIENT
  - remote client is not exist. not used yet
	- Usage scenarios
		- The local side finds a message that the client corresponding to the message has been closed, and the remote end has not been notified.
  ### (66) TOX_ERR_ILLEGAL_SHADOW
  - remote shaodow is not exist. not used yet
	- Usage scenarios
		- The local side finds a message that the server corresponding to the message has been closed, and the remote end has not been notified.
  ### (67) TOX_ERR_SAME_CONTEXT
  - api thread is same with tox loop thread
	- Usage scenarios
		- The RPC layer operates in the TOX main thread and is used in tox_remove_server and tox_remove_client calls to inform the RPC that TOX will handle the call operations synchronously. Used to distinguish between asynchronous processing.
  ### (68) TOX_ERR_SERVER_RESTART
  - detect server restart
	- Usage scenarios
		- Connection detection: The local end finds that the corresponding remote end has been disconnected and restarted in the existing connection
  ### (69) TOX_ERR_TX_FLUSH_TIMEOUT
  - tx flush over time limit in one loop
	- Usage scenarios
		- This time the message was sent too long and exceeded the maximum, leaving the unsent packets to be sent again on the next loop.
  ### (70) TOX_ERR_RCV_DECODE_SIZE_INVALID
  - ecode recv message failed
	- Usage scenarios
		- An error occurred when parsing the receiving packet.
  ### (71) TOX_ERR_ILLEGAL_BRIDGE
  - receive message decode bridge failed
	- Usage scenarios
		- The session packet received through the network cannot find the corresponding bridge locally.
  ### (72) TOX_ERR_UNKNOWN_MAGIC_ID
  - received message contains unknown magic id
	- Usage scenarios
		- The received package conforms to the tox protocol, but contains a pointer to the tox object that points to the actual object that is not legitimate.
  ### (73) TOX_ERR_DECODE_SECURITY_FAILED
  - decode received security message failed
	- Usage scenarios
		- decode the receiving packet failed
  ### (74) TOX_ERR_TAKER_OUT
  - create taker failed when receiving message
	- Usage scenarios
		- out of memory when receiving packet.
  ### (75) TOX_ERR_LINKER_OUT
  - create linker failed when sending packet
	- Usage scenarios
		- out of memory when sending packet..
  ### (76) TOX_ERR_BUDDY_DEVICE_NOT_WORKING
  - Tox buddy device failed to connect to agent 
	- Usage scenarios
		- Not Used
  ### (77) TOX_ERR_BUDDY_DEVICE_SEND_FAILED
  - Tox buddy device sent data to agent failed
	- Usage scenarios
		- Disconnect when sending data
  ### (78) TOX_ERR_BUDDY_DEVICE_SEND_BUFFER_OUT
  - Tox buddy device sent data to agent over 1.5K
	- Usage scenarios
		- When the size of query/claim frame is over 1.5K 
  ### (79) TOX_ERR_CLIENT_STOPPED
  - user call tox_client_stop api
	- Usage scenarios
		- After calls the tox_client_stop interface, tox completes the stop operation.
  ### (80) TOX_ERR_RX_FLUSH_TIMEOUT
  - rx flush over time limit in one loop
	- Usage scenarios
		- use for time driven strategy, not used yet.
  
  
</source-synced>

# Further Readings

- <mention-doc token="CIZIdCUdWolQUoxsWYGc42HZnRf" type="docx">NT3 SOA Error Handling Best Practice—V1.0</mention-doc> by <mention-user id="ou_f37979ece84a7496945677c6ccfc3bf1"/>
