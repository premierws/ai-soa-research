Based on the SOA Framework, all application developers need to do is define their services in IDL files and use auto-generated glue code APIs to code their applications' logic. During runtime, auto-created SoaManagers will interact with underlying components to enable communications between the applications. 

This document explains the glue code APIs generated based on the HelloWorld service IDL file (`HelloWorldMcu.proto`). The glue code APIs generated from other service IDL files are similar; you can refer to this document to understand them.FIELD_READONLY

`HelloWorldMcu.proto`
```protobuf {wrap}
syntax = "proto3";

import "nrpc.option.proto";

package nvos.example;

//====================== message definition ==========================
message HelloRequestMcu {
    string greeting = 1;
    int32 a = 2;
    int32 b = 3 [(integer_min_value) = -128, (integer_max_value) = 128];
    float c = 4 [(float_min_value) = -128.0, (float_max_value) = 128.0];
}

message HelloReplyMcu {
    string answer = 1;
    int32 sum = 2;
}

message HelloEventMcu {
    int32 index = 1;
    string place = 3;
}

message FieldVehSpdMcu {
    int32 speed = 1;
}

message FieldAccMcu {
    float acceleration = 1;
}

// ==================== Service definition ==========================
service HelloWorldMcu {
    option (service_id) = 12345; // A unique service ID must be supplied by NDTC.

    //Define a method with "HelloRequestMcu" being input and "HelloReplyMcu" being output
    rpc SayHelloMcu(HelloRequestMcu) returns (HelloReplyMcu) {
        option (rpc_id) = 1;
        option (method_type) = METHOD;
    }

    //Define a one-way method with "HelloRequestMcu" being input
    rpc SayHelloOneWayMcu(HelloRequestMcu) returns (Null) {
        option (rpc_id) = 11;
        option (method_type) = METHOD;
    }

    //Define an event with "HelloEventMcu" as the data type
    rpc HiMcu(HelloEventMcu) returns (Null) {
        option (rpc_id) = 2;
        option (method_type) = EVENT;
    }

    //Define a read-only field named "FieldSpeed" with "FieldVehSpdMcu" as the data type
    rpc FieldSpeed(FieldVehSpdMcu) returns (Null) {
        option (rpc_id) = 3;
        option (method_type) = FIELD_READONLY;
    }

    //Define a read-only field (without subscription) named "FieldSpeedNoSub" with "FieldVehSpdMcu" as the data type
    rpc FieldSpeedNoSub(FieldVehSpdMcu) returns (Null) {
        option (rpc_id) = 31;
        option (method_type) = FIELD_READONLY_NOSUB;
    }

    //Define a read-only field named "FieldAcceleration" with "FieldAccMcu" as the data type
    rpc FieldAcceleration(FieldAccMcu) returns (Null) {
        option (rpc_id) = 4;
        option (method_type) = FIELD_WRITABLE;
    }

    //Define a read-only field (without subscription) named "FieldAcceleration" with "FieldAccMcu" as the data type
    rpc FieldAccelerationNoSub(FieldAccMcu) returns (Null) {
        option (rpc_id) = 41;
        option (method_type) = FIELD_WRITABLE_NOSUB;
    }
}
```

# Server APIs

When generating glue code APIs for a server, the code generator reads the SOA deployment file for the service name, package name, and component name to create API names. For the HelloWorld service, the service deployment information is as follows:
```json {wrap}
{
    "$schema": "../../../../../platform/BSW/soa/schema/default.deployment.schema.json",
    "$target": "MCU",
    "services": [
        {
            "component_instance_name": "app1",
            "service_name": "HelloWorldMcu",
            "service_package": "nvos.example"
        }
    ],
    "clients": []
}
```

Based on the `HelloWorldMcu.proto` file and service deployment information above, the auto-generated glue code server APIs are as follows:

## Built-in interfaces

The following built-interfaces will be auto-generated for each service instance:

- `lifecycle_init`
- `lifecycle_deinit`
- `connect_state` (<text color="red">for local deployment only</text>)
- `session_changed` 
- `soa_error`
- `qos_event`

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

The SOA Framework supports customization of the `session_changed`, `soa_error`, and `qos_event` build-in interfaces. 

See `rpc_behavior_customization` > `builtin-interface` in [section 2.2 Service deployment](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2Fwikcnp19h76IlJpy57uMBA2Yr8d%23doxcniAoaaM6SYWq6szC6sVNwWd) for details.
</callout>

### Component initialization
```c
sched_cb_fn app1_lifecycle_init_handler;
```

This callback is triggered when the server component is initialized.

When receiving the callback, the server should call the `sm_write_app1_notify_connect_state_helloworldmcu` method to notify the client that the server is active.

### Component destruction
```c
sched_cb_fn app1_lifecycle_deinit_handler;
```

This callback is triggered when the server component is destroyed.

After receiving the callback, the server should call the `sm_write_app1_notify_connect_state_nvos_example_helloworld` method to notify the client that the server is inactive.

### Connection state

#### Send connection state to a client
```cpp {wrap}
sm_api_retval_t sm_write_app1_notify_connect_state_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    const connect_state_msg_t *const p_connect_state_msg);
```

After receiving the `app1_lifecycle_init_handler` callback, the server should call this method to notify the client that its status is active; when receiving the `app1_lifecycle_deinit_handler`** **callback, the server should call this method to notify the client that its status is inactive.

**Note**

<text color="red">**This function works for local clients only**</text>. For remote clients, Tox will trigger a server status notifier upon connection to the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_connect_state_msg`: Pointer to the connection state, including the `connect_state` and `reason` fields. See `connect_state_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

**Example**
```cpp {wrap}
static void lifecycle_init_handler(const sm_comp_inst_id_t comp_id)
{
    // Notify server status: This function works for local clients only.
    // For remote clients, the client-side Tox will trigger a server status notifier upon connection to this server.
    connect_state_msg_t status_msg = {};
    status_msg.connect_state = NRPC_CONNECT_STATE_CONNECTED;
    if (sm_write_app1_notify_connect_state_helloworldmcu(comp_id, &status_msg) != SUCCESS) {
        // error
    }
}
```

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.2) to troubleshoot connection issues.
</callout>

### Session state

#### Receive the session state
```c {wrap}
sched_cb_fn app1_on_session_changed_helloworldmcu_handler;
```

This callback is triggered when the session state changes.

#### Read the session state
```c {wrap}
sm_api_retval_t sm_read_app1_on_session_changed_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    session_changed_msg_t *const p_session_changed_msg);
```

After receiving the `app1_on_session_changed_helloworldmcu_handler` callback, the server should call this method to read the current session state and the reason that has caused the state change.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_session_changed_msg`: Pointer to the session changed message, including the `client_id`, `session_state`, and `reason` fields. See `session_changed_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

**Example**
```c {wrap}
// This function is called when the session state changes. It reads the new session state
// and prints a message to the console indicating whether the session was connected or disconnected.
static void app1_on_session_changed_helloworldmcu_handler(const sm_comp_inst_id_t comp_id)
{
    // receive session changed
    session_changed_msg_t session_changed_msg;
    sm_read_app1_on_session_changed_helloworldmcu(comp_id, &session_changed_msg);
    if (session_changed_msg.session_state == NRPC_SESSION_CREATED)
    {
        // session is connected
        console_print(
            "=== HelloWorldMcu Base === app1 receives session changed [connected] with client_id = %d.\n",
            session_changed_msg.client_id);
    }
    else if (session_changed_msg.session_state == NRPC_SESSION_DESTORIED)
    {
        // session is disconnected
        console_print(
            "=== HelloWorldMcu Base === app1 receives session changed [disconnected] with client_id = %d reason = %d.\n",
            session_changed_msg.client_id,
            session_changed_msg.reason);
    }
}
```

### SOA error

#### Receive the SOA error
```c {wrap}
sched_cb_fn app1_on_soa_error_helloworldmcu_handler;
```

This callback is triggered when an SOA error occurs.

#### Read the SOA error
```c {wrap}
sm_api_retval_t sm_read_app1_on_soa_error_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    soa_error_msg_t *const  p_soa_error_msg)
```

After receiving the `app1_on_soa_error_helloworldmcu_handler` callback, the server should call this method to read the SOA error code and message.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_soa_error_msg`: Pointer to the session changed message, including the `error_code`, `rpc_id`, and `method_type` fields. See `soa_error_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.3.1) to handle the general errors.
</callout>

### QoS event (Deprecated)

<source-synced align="1">

  <callout emoji="exclamation" background-color="light-blue" border-color="light-blue" text-color="blue">
  The QoS event APIs have been deprecated since v02.00.07 RC 15 & v02.01.02, as the QoS errors are merged into SOA error.
  These APIs are still auto-generated, but do not take effect. 
  If you have used these APIs and implemented error handling logic, you need to:
  - Use SOA error reporting API instead and move the QoS error handling logic there.
	- (Optional) Use [`builtin-interface`](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2Fwikcnp19h76IlJpy57uMBA2Yr8d%23share-QoDNdxbe7oAA1zxYiVtceBM4nbh) > `generate` in SOA deployment to disable the generation of `on_qos_event_xxx_handler` and remove the error handling logic in your code.
  You can check <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 4.3.1.1) for information on how to catch SOA error.
  </callout>

</source-synced>

#### Receive the QoS event
```c {wrap}
sched_cb_fn app1_on_qos_event_helloworldmcu_handler;
```

This callback is triggered when a QoS event occurs.

#### Read the QoS event
```c {wrap}
sm_api_retval_t sm_read_app1_on_qos_event_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    qos_event_msg_t *const  p_qos_event_msg);
```

After receiving the `app1_on_soa_error_helloworldmcu_handler` callback, the server should call this method to read the QoS event message.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_qos_event_msg`: Pointer to the session changed message, including the `rpc_id`, `qos_type`, and `error_code` fields. See `qos_event_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

## Custom RPC interfaces

The following methods and callbacks will be auto-generated for the server side based on the RPC interfaces defined in your `.proto` file:

### RR method

#### Receive a `sayhellomcu` request
```cpp
sched_cb_fn app1_on_request_helloworldmcu_sayhellomcu_request_arrived;
```

This callback is triggered when a `sayhellomcu` request arrives at the server.

#### Read data of the `sayhellomcu` request
```cpp
sm_api_retval_t sm_recv_req_app1_on_request_helloworldmcu_sayhellomcu(
    const sm_comp_inst_id_t comp_id,
    req_msg_nvos_example_helloworldmcu_sayhellomcu_t *const p_req_msg_nvos_example_helloworldmcu_sayhellomcu);
```

After receiving the `app1_on_request_helloworldmcu_sayhellomcu_request_arrived` callback, the server should call this method to read the request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_req_msg_nvos_example_helloworldmcu_sayhellomcu`: Pointer to the request message. See `req_msg_nvos_example_helloworldmcu_sayhellomcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Reply to the `sayhellomcu` request
```cpp
sm_api_retval_t sm_send_resp_app1_on_request_helloworldmcu_sayhellomcu(
    const sm_comp_inst_id_t comp_id,
    const reply_msg_nvos_example_helloworldmcu_sayhellomcu_t *const p_reply_msg_nvos_example_helloworldmcu_sayhellomcu);
```

When completing processing the `sayhellomcu` request internally, the server should call this method to send a response to the client.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_nvos_example_helloworldmcu_sayhellomcu`: Ponter to the response message. See `reply_msg_nvos_example_helloworldmcu_sayhellomcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### One-way method

#### Receive a `sayhelloonewaymcu` request
```cpp
sched_cb_fn app1_on_request_helloworldmcu_sayhelloonewaymcu_request_arrived;
```

This callback is triggered when a `sayhelloonewaymcu` request arrives at the server.

#### Read data of the `sayhelloonewaymcu` request
```cpp
sm_api_retval_t sm_read_app1_on_request_helloworldmcu_sayhelloonewaymcu(
    const sm_comp_inst_id_t comp_id,
    req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t *const p_req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu);
```

After receiving the `app1_on_request_helloworldmcu_sayhelloonewaymcu_request_arrived` callback , the server should call this method to read the data of the `sayhellooneway`request.

**Notes**

The server does not send a response to a one-way call.

**Parameters**** **

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu`: Pointer to the request message. See `req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Event

#### Send a notification when the `himcu` event occurs
```cpp
sm_api_retval_t sm_write_app1_notify_helloworldmcu_himcu(
    const sm_comp_inst_id_t comp_id,
    const evt_msg_nvos_example_helloworldmcu_himcu_t *const p_evt_msg_nvos_example_helloworldmcu_himcu);
```

When the `himcu` event occurs, the server should call this method to send event notifications to clients that subscribe to the event.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_himcu`: Pointer to the event message. See `evt_msg_nvos_example_helloworldmcu_himcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_readonly

#### Receive a `get_fieldspeed` request
```cpp
sched_cb_fn app1_on_get_helloworldmcu_fieldspeed_request_arrived;
```

This callback is triggered when a `get_fieldspeed` request arrives at the server.

After receiving the callback, the server should do the following:

1. Call the `sm_recv_req_app1_on_get_helloworldmcu_fieldspeed` method to read the data of the `get_fieldspeed` request.
1. Call the `sm_send_resp_app1_on_get_helloworldmcu_fieldspeed` method to send a response after processing the request.
1. Call the `sm_write_app1_notify_helloworldmcu_fieldspeed` method to notify the client when the `fieldspeed` field is updated.

#### Read data of the `get_fieldspeed` request
```cpp
sm_api_retval_t sm_recv_req_app1_on_get_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    get_msg_nvos_example_helloworldmcu_fieldspeed_t *const p_get_msg_nvos_example_helloworldmcu_fieldspeed);
```

After receiving the `app1_on_get_helloworldmcu_fieldspeed_request_arrived` callback, the server should call this method to read the data of the `get_fieldspeed` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldspeed`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Reply to the `get_fieldspeed` request
```cpp
sm_api_retval_t sm_send_resp_app1_on_get_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    const reply_msg_get_nvos_example_helloworldmcu_fieldspeed_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldspeed);
```

When completing processing the `get_fieldspeed` request internally, the server should call this method to send a response to the client.

**Notes**

The `get_fieldspeed` call requests to get and subscribe to the `fieldspeed` field. Therefore, if the request succeeds, the server should call `sm_write_app1_notify_helloworldmcu_fieldspeed` to notify the subscriber every time when the field is updated.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldspeed`: Ponter to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Send a notification when the `fieldspeed` field is updated
```cpp
sm_api_retval_t sm_write_app1_notify_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    const evt_msg_nvos_example_helloworldmcu_fieldspeed_t *const p_evt_msg_nvos_example_helloworldmcu_fieldspeed);
```

When the `fieldspeed` field is updated, the server should call this method to send notifications to clients that have subscribed to the field by sending the `get_fieldspeed` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_fieldspeed`: Pointer to the event message. See `evt_msg_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Filed_readonly_nosub

#### Receive a `get_fieldroonenosub` request
```cpp
sched_cb_fn app1_on_get_helloworldmcu_fieldspeednosub_request_arrived;
```

This callback is triggered when a `get_fieldspeednosub` request arrives at the server.

After receiving the callback, the server should do the following:

1. Call the `sm_recv_req_app1_on_get_helloworldmcu_fieldspeednosub` method to read the data of the `get_fieldspeednosub` request.
1. Call the `sm_send_resp_app1_on_get_helloworldmcu_fieldspeednosub` method to send a response after processing the request.

**Notes**

The server does not need to notify the client when the `fieldspeednosub` field is updated because the `get_fieldspeednosub` call does not request to subscribe to the field.

#### Read data of the `get_fieldspeednosub` request
```cpp
sm_api_retval_t sm_recv_req_app1_on_get_helloworldmcu_fieldspeednosub(
    const sm_comp_inst_id_t comp_id,
    get_msg_nvos_example_helloworldmcu_fieldspeednosub_t *const p_get_msg_nvos_example_helloworldmcu_fieldspeednosub);
```

After receiving the `app1_on_get_helloworldmcu_fieldspeednosub_request_arrived` callback, the server should call this method to read the data of the `get_fieldspeednosub` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldspeednosub`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldspeednosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Reply to the `get_fieldspeednosub` request
```cpp
sm_api_retval_t sm_send_resp_app1_on_get_helloworldmcu_fieldspeednosub(
    const sm_comp_inst_id_t comp_id,
    const reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub);
```

When completing processing the `get_fieldspeednosub` request internally, the server should call this method to send a response to the client.

**Notes**

The `get_fieldspeednosub` call only requests to get the filed once. After sending the response, the server does not send notifications to the client when the `fieldspeednosubfield` changes. 

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub`: Ponter to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_writable

#### Receive a `get_fieldacceleration` request
```c {wrap}
sched_cb_fn app1_on_get_helloworldmcu_fieldacceleration_request_arrived;
```

This callback is triggered when a new `get_fieldacceleration` request arrives at the server.

#### Read data of the `get_fieldacceleration` request
```c
sm_api_retval_t sm_recv_req_app1_on_get_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    get_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_get_msg_nvos_example_helloworldmcu_fieldacceleration);
```

After receiving the `app1_on_get_helloworldmcu_fieldacceleration_request_arrived``** **``callback`, the server should call the method to read the data of the `get_fieldacceleration` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the event message. See `get_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Reply to the `get_fieldacceleration` request
```c
sm_api_retval_t sm_send_resp_app1_on_get_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    const reply_msg_get_nvos_example_helloworldmcu_fieldacceleration_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldacceleration);
```

When completing processing the `get_fieldacceleration` request internally, the server should call this method to send a response to the client.

**Notes**

The `get_fieldacceleration` call only requests to get the filed once. After sending the response, the server does not send notifications to the client when the `fieldacceleration` changes. 

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldacceleration`: Ponter to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive a `set_fieldacceleration` request
```cpp
sched_cb_fn app1_on_set_helloworldmcu_fieldacceleration_request_arrived;
```

This callback is triggered when a new `set_fieldacceleration` request arrives at the server.

#### Read data of the `set_fieldacceleration` request
```cpp
sm_api_retval_t sm_read_app1_on_set_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    set_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_set_msg_nvos_example_helloworldmcu_fieldacceleration);
```

After receiving the `app1_on_set_helloworldmcu_fieldacceleration_request_arrived`** **callback , the server should call the method to read the data of the `set_fieldacceleration` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_set_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the event message. See `set_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Send a notification when the `fieldacceleration` field is updated
```cpp
sm_api_retval_t sm_write_app1_notify_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    const evt_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_evt_msg_nvos_example_helloworldmcu_fieldacceleration);
```

When the `fieldacceleration` field is updated, the server should call this method to send notifications to clients that have subscribed to the field by sending the `set_fieldacceleration` request.

**Parameters**

- `comp_id `: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the event message. See `evt_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_writable_nosub

#### Receive a `get_fieldaccelerationnosub` request
```c
sched_cb_fn app1_on_get_helloworldmcu_fieldaccelerationnosub_request_arrived;
```

This callback is triggered when a new `get_fieldaccelerationnosub` request arrives at the server.

#### Read data of the `get_fieldaccelerationnosub` request
```c
sm_api_retval_t sm_recv_req_app1_on_get_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

After receiving the `app1_on_get_helloworldmcu_fieldaccelerationnosub_request_arrived` callback, the server should call the method to read the data of the `get_fieldaccelerationnosub` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub`: Pointer to the event message. See `get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Reply to the `get_fieldaccelerationnosub` request
```c
sm_api_retval_t sm_send_resp_app1_on_get_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    const reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

When completing processing the `get_fieldaccelerationnosub` request internally, the server should call this method to send a response to the client.

**Notes**

The `get_fieldaccelerationnosub` call only requests to get the filed once. After sending the response, the server does not send notifications to the client when the `fieldaccelerationnosub` changes. 

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub`: Ponter to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive a `set_fieldaccelerationnosub` request
```cpp
app1_on_set_helloworldmcu_fieldaccelerationnosub_request_arrived;
```

This callback is triggered when a `set_fieldwritfournosub` request arrives at the server.

**Notes**

The server does not need to notify the client when the `fieldaccelerationnosub` field is updated because the `set_fieldaccelerationnosub` call does not request to subscribe to the field.

#### Read data of the `set_fieldaccelerationnosub` request
```cpp
sm_api_retval_t sm_read_app1_on_set_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

After receiving the `app1_on_set_helloworldmcu_fieldaccelerationnosub_request_arrived` callback, the server should call this method to read the data of the `set_fieldaccelerationnosub` request.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub`: Pointer to the request message. See `set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

# Client APIs

When generating glue code APIs for a client, the code generator reads the SOA deployment file for the service name, package name, and component name to create API names. For the client of the HelloWorld service, the client deployment information is as follows:
```json {wrap}
{
    "$schema": "../../../../../platform/BSW/soa/schema/default.deployment.schema.json",
    "$target": "MCU",
    "services": [],
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

Based on the `HelloWorldMcu.proto` file and client deployment information above, the auto-generated glue code server APIs are as follows:

## Built-in interfaces

The following built-interfaces will be auto-generated for each client instance:

- `lifecycle_init`
- `lifecycle_deinit`
- `connect_state`
- `soa_error`
- `qos_event`
- `check_version` (**Note**: Different from other built-in interfaces, the check_version interface is generated when the IDL version check feature is enabled. In this example, the IDL version check feature is not enabled. To enable the feature, see <mention-doc token="wikcnSD4cSp3oNHmTrLqjrGZtsf" type="wiki">IDL Version Check User Guide</mention-doc> for details.)

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

The SOA Framework supports customization of the `connect_state`, `soa_error`, and `qos_event`, `check_version` build-in interfaces. 

See `rpc_behavior_customization` > `builtin-interface` in [section 2.3 Client deployment](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2Fwikcnp19h76IlJpy57uMBA2Yr8d%23doxcn4Q6Uyusc2OSAMpiDTfG7Pg) for details.
</callout>

### Component initialization
```c
sched_cb_fn app2_lifecycle_init_handler;
```

This callback is triggered when the client component is initialized.

### Component destruction
```c
sched_cb_fn app1_lifecycle_deinit_handler;
```

This callback is triggered when the client component is destroyed.

### Connection state

#### Receive the connection state
```c {wrap}
sched_cb_fn app2_on_connect_state_helloworldmcu_handler;
```

This callback is triggered when the connection state to a server changes.

#### Read the connection state
```cpp {wrap}
sm_api_retval_t sm_read_app2_on_connect_state_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    connect_state_msg_t *const p_connect_state_msg);
```

After receiving the `app2_on_connect_state_helloworldmcu_handler` callback, the client should call this method to get the connection state to the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_connect_state_msg`: Pointer to the connection state, including the `connect_state` and `reason` fields. See `connect_state_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.2) to troubleshoot connection issues.
</callout>

### SOA error

#### Receive the SOA error
```c {wrap}
sched_cb_fn app2_on_soa_error_helloworldmcu_handler;
```

This callback is triggered when an SOA error occurs.

#### Read the SOA error
```c
sm_api_retval_t sm_read_app2_on_soa_error_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    soa_error_msg_t *const  p_soa_error_msg);
```

After receiving the `app2_on_soa_error_helloworldmcu_handler` callback, the client should call this method to read the SOA error code and message.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_soa_error_msg`: Pointer to the session changed message, including the `error_code`, `rpc_id`, and `method_type` fields. See `soa_error_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### QoS event (Deprecated)

<reference-synced source-block-id="O9jbdRXFCszk2RbiiHycHmYHnC3" source-document-id="doxcn6fGZY5B0fUDulJimKB6eSg">

  <callout emoji="exclamation" background-color="light-blue" border-color="light-blue" text-color="blue">
  The QoS event APIs have been deprecated since v02.00.07 RC 15 & v02.01.02, as the QoS errors are merged into SOA error.
  These APIs are still auto-generated, but do not take effect. 
  If you have used these APIs and implemented error handling logic, you need to:
  - Use SOA error reporting API instead and move the QoS error handling logic there.
	- (Optional) Use [`builtin-interface`](https%3A%2F%2Fnio.feishu.cn%2Fwiki%2Fwikcnp19h76IlJpy57uMBA2Yr8d%23share-QoDNdxbe7oAA1zxYiVtceBM4nbh) > `generate` in SOA deployment to disable the generation of `on_qos_event_xxx_handler` and remove the error handling logic in your code.
  You can check <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 4.3.1.1) for information on how to catch SOA error.
  </callout>

</reference-synced>

#### Receive the QoS event
```c
sched_cb_fn app2_on_qos_event_helloworldmcu_handler;
```

This callback is triggered when a QoS event occurs.

#### Read the QoS event
```c
sm_api_retval_t sm_read_app2_on_qos_event_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    qos_event_msg_t *const  p_qos_event_msg);
```

After receiving the `app2_on_qos_event_helloworldmcu_handler` callback, the client should call this method to read the QoS event message.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_qos_event_msg`: Pointer to the session changed message, including the `rpc_id`, `qos_type`, and `error_code` fields. See `qos_event_msg_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.3.2) to handle the QoS errors.
</callout>

### Gets QoS event
```c {wrap}
sm_api_retval_t sm_read_app1_on_qos_event_helloworldmcu(
    const sm_comp_inst_id_t comp_id,
    qos_event_msg_t *const  p_qos_event_msg);
```

After receiving the `app1_on_soa_error_helloworldmcu_handler` callback, the server should call this method to read the QoS event message.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_qos_event_msg`: Pointer to the session changed message, including the `rpc_id`, `qos_type`, and `error_code` fields. See `qos_event_msg_t` for the data type.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.3.1) to handle the general errors.
</callout>

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

<callout emoji="💡" background-color="light-blue" border-color="light-blue">

Users can refer to <mention-doc token="KTO4wSw7ziHAvJkTr6bcgG00ncb" type="wiki">SOA Framework: Error Handlings</mention-doc> (section 3.3.2) to handle the QoS errors.
</callout>

## Custom RPC interfaces

The following methods and callbacks will be auto-generated for the client side based on the RPC interfaces defined in your `.proto` file:

### RR method

#### Send a `sayhellomcu` request
```c
sm_api_retval_t sm_send_req_app2_request_helloworldmcu_sayhellomcu(
    const sm_comp_inst_id_t comp_id,
    const req_msg_nvos_example_helloworldmcu_sayhellomcu_t *const p_req_msg_nvos_example_helloworldmcu_sayhellomcu);
```

The client calls this method to send a `sayhellomcu` request to the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_req_msg_nvos_example_helloworldmcu_sayhellomcu`: Ponter to the request message. See `req_msg_nvos_example_helloworldmcu_sayhellomcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `sayhellomcu` response
```c
sched_cb_fn app2_request_helloworldmcu_sayhellomcu_response_arrived;
```

This callback is triggered when the `sayhellomcu` response sent by the server arrives at the client.

#### Read data of the `sayhellomcu` response
```c
sm_api_retval_t sm_recv_resp_app2_request_helloworldmcu_sayhellomcu(
    const sm_comp_inst_id_t comp_id,
    reply_msg_nvos_example_helloworldmcu_sayhellomcu_t *const p_reply_msg_nvos_example_helloworldmcu_sayhellomcu);
```

After receiving the `app2_request_helloworldmcu_sayhellomcu_response_arrived` callback, the client can call this method to read the data of the `sayhellomcu` response sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_nvos_example_helloworldmcu_sayhellomcu`: Pointer to the response message. See `reply_msg_nvos_example_helloworldmcu_sayhellomcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### One-way method

#### Sends a `sayhelloonewaymcu` request
```c
sm_api_retval_t sm_write_app2_request_helloworldmcu_sayhelloonewaymcu(
    const sm_comp_inst_id_t comp_id,
    const req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t
        *const p_req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu);
```

The client calls this method to send a `sayhelloonewaymcu` request to the server.

**Notes**

This method is a one-way call and does not expect a response from the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu`: Ponter to the request message. See `req_msg_nvos_example_helloworldmcu_sayhelloonewaymcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Event

#### Receive the `himcu` event notification
```c
sched_cb_fn app2_on_notify_helloworldmcu_himcu_handler;
```

This callback is triggered when the `himcu` event notification sent by the server arrives at the client.

#### Reads data of the `himcu` event notification
```c
sm_api_retval_t sm_read_app2_on_notify_helloworldmcu_himcu(
    const sm_comp_inst_id_t comp_id,
    evt_msg_nvos_example_helloworldmcu_himcu_t *const p_evt_msg_nvos_example_helloworldmcu_himcu);
```

After receiving the `app2_on_notify_helloworldmcu_himcu_handler` callback, the client can call this method to read the data of the `himcu` event notification sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_himcu`: Pointer to the event notification. See `evt_msg_nvos_example_helloworldmcu_himcu_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field-readonly

#### Send a `get_fieldspeed` request
```c
sm_api_retval_t sm_send_req_app2_get_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    const get_msg_nvos_example_helloworldmcu_fieldspeed_t *const p_get_msg_nvos_example_helloworldmcu_fieldspeed);
```

The client can call this method to send a `get_fieldspeed` request to the server to get and subscribe to the data of the `fieldspeed` field. 

**Notes**

When the request succeeds, the server calls `sm_send_resp_app1_on_get_helloworldmcu_fieldspeed` to send the current data of the `fieldspeed` field immediately; when the `fieldspeed` field is updated, the server calls `sm_write_app1_notify_helloworldmcu_fieldspeed` to notify the client.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldspeed`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `get_fieldspeed` reponse
```c
sched_cb_fn app2_get_helloworldmcu_fieldspeed_response_arrived;
```

This callback is triggered when the `get_fieldspeed` response sent by the server arrives at the client.

#### Reads data of the `get_fieldspeed` response
```c
sm_api_retval_t sm_recv_resp_app2_get_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    reply_msg_get_nvos_example_helloworldmcu_fieldspeed_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldspeed);
```

After receiving the `app2_get_helloworldmcu_fieldspeed_response_arrived callback`, the client can call this method to read the data of the `get_fieldspeed` response sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldspeed`: Pointer to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `fieldspeed` notification
```c
sched_cb_fn app2_on_notify_helloworldmcu_fieldspeed_handler;
```

This callback is triggered when the `fieldspeed` update notification sent by the server arrives at the client.

#### Reads data of the `fieldspeed` notification
```c
sm_api_retval_t sm_read_app2_on_notify_helloworldmcu_fieldspeed(
    const sm_comp_inst_id_t comp_id,
    evt_msg_nvos_example_helloworldmcu_fieldspeed_t *const p_evt_msg_nvos_example_helloworldmcu_fieldspeed);
```

After receiving the `app2_on_notify_helloworldmcu_fieldspeed_handler` callback, the client can call this method to read the data of the `fieldspeed` notification sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_fieldspeed`: Pointer to the notification message. See `evt_msg_nvos_example_helloworldmcu_fieldspeed_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_readonly_nosub

#### Send a `get_fieldspeednosub` request
```c
sm_api_retval_t sm_send_req_app2_get_helloworldmcu_fieldspeednosub(
    const sm_comp_inst_id_t comp_id,
    const get_msg_nvos_example_helloworldmcu_fieldspeednosub_t *const p_get_msg_nvos_example_helloworldmcu_fieldspeednosub);
```

The client can call this method to send a `get_fieldspeednosub` request to the server to get the `fieldspeednosub` field. 

**Notes**

This method requests to get the `fieldspeednosub` field only once and does not subscribe to the field. Therefore, the server does not send notifications when the field changes.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldspeednosub`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldspeednosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `get_fieldspeednosub` response
```c
sched_cb_fn app2_get_helloworldmcu_fieldspeednosub_response_arrived;
```

This callback is triggered when the `fieldspeednosub` update notification sent by the server arrives at the client.

#### Read data of the `get_fieldspeednosub` response
```c
sm_api_retval_t sm_recv_resp_app2_get_helloworldmcu_fieldspeednosub(
    const sm_comp_inst_id_t comp_id,
    reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub);
```

After receiving the `app2_get_helloworldmcu_fieldspeednosub_response_arrived` callback, the client can call this method to read the data of the `get_fieldspeednosub` response sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub`: Pointer to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldspeednosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_writable

#### Send a `get_fieldacceleration` request
```c
sm_api_retval_t sm_send_req_app2_get_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    const get_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_get_msg_nvos_example_helloworldmcu_fieldacceleration);
```

The client can call this method to send a `get_fieldacceleration` request to the server to get the `fieldacceleration` field. 

**Notes**

This method requests to get the `fieldacceleration` field only once and does not subscribe to the field. Therefore, the server does not send notifications when the field changes.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `get_fieldacceleration` response
```c
sched_cb_fn app2_get_helloworldmcu_fieldacceleration_response_arrived;
```

This callback is triggered when the `get_fieldacceleration` response sent by the server arrives at the client.

#### Read data of the `get_fieldacceleration` response
```c
sm_api_retval_t sm_recv_resp_app2_get_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    reply_msg_get_nvos_example_helloworldmcu_fieldacceleration_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldacceleration);
```

After receiving the `app2_get_helloworldmcu_fieldacceleration_response_arrived` callback, the client can call this method to read the data of the `get_fieldacceleration` response sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Send a `set_fieldacceleration` request
```c
sm_api_retval_t sm_write_app2_set_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    const set_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_set_msg_nvos_example_helloworldmcu_fieldacceleration);
```

The client can call this method to send a `set_fieldacceleration` request to the server to set and subscribe to the value of the `fieldacceleration` field.

**Notes**

This method is a fire-forget call and does not expect a response from the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_set_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the request message. See `set_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `fieldacceleration` notification
```c
sched_cb_fn app2_on_notify_helloworldmcu_fieldacceleration_handler;
```

This callback is triggered when the `fieldacceleration` update notification sent by the server arrives at the client.

#### Reads data of the `fieldacceleration` notification
```c
sm_api_retval_t sm_read_app2_on_notify_helloworldmcu_fieldacceleration(
    const sm_comp_inst_id_t comp_id,
    evt_msg_nvos_example_helloworldmcu_fieldacceleration_t *const p_evt_msg_nvos_example_helloworldmcu_fieldacceleration);
```

After receiving the `app2_on_notify_helloworldmcu_fieldacceleration_handler` callback, the client calls this method to read the data of the `fieldacceleration` notification sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_evt_msg_nvos_example_helloworldmcu_fieldacceleration`: Pointer to the notification message. See `evt_msg_nvos_example_helloworldmcu_fieldacceleration_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

### Field_writable_nosub

#### Send a `get_fieldaccelerationnosub` request
```c
sm_api_retval_t sm_send_req_app2_get_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    const get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

The client can call this method to send a `get_fieldaccelerationnosub` request to the server to get the `fieldaccelerationnosub` field. 

**Notes**

This method requests to get the `fieldaccelerationnosub` field only once and does not subscribe to the field. Therefore, the server does not send notifications when the field changes.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub`: Pointer to the request message. See `get_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Receive the `get_fieldaccelerationnosub` response
```c
sched_cb_fn app2_get_helloworldmcu_fieldaccelerationnosub_response_arrived;
```

This callback is triggered when the `get_fieldaccelerationnosub` response sent by the server arrives at the client.

#### Read data of the `get_fieldaccelerationnosub` response
```c
sm_api_retval_t sm_recv_resp_app2_get_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

After receiving the `app2_get_helloworldmcu_fieldaccelerationnosub_response_arrived` callback, the client can call this method to read the data of the `get_fieldaccelerationnosub` response sent by the server.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub`: Pointer to the response message. See `reply_msg_get_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.

#### Send a `set_fieldaccelerationnosub` request
```c
sm_api_retval_t sm_write_app2_set_helloworldmcu_fieldaccelerationnosub(
    const sm_comp_inst_id_t comp_id,
    const set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t *const p_set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub);
```

The client can call this method to send a `set_fieldaccelerationnosub` request to the server to set the data of the `fieldaccelerationnosub` field. 

**Notes**

This method is a fire-forget call and does not expect a response from the server.

This method requests to set the `fieldaccelerationnosub` field only once and does not subscribe to the field. Therefore, the server does not send notifications when the field changes.

**Parameters**

- `comp_id`: The component instance ID, which is automatically generated by the App Framework code generator and will be passed in as `comp_id` to the App framework callbacks. When you call this method within a callback, you can use `comp_id` reported by the callback.
- `p_set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub`: Pointer to the request message. See `set_msg_nvos_example_helloworldmcu_fieldaccelerationnosub_t` for the data type.

**Returns**

- `0` if the method call succeeded.
- An error message if the method call failed.
