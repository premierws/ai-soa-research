from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from app.services.source_evidence import SourceEvidence


@dataclass(slots=True)
class SoaRpcRequest:
    request_name: str
    generate_get: bool = False
    generate_set: bool = False


@dataclass(slots=True)
class SoaEndpointFact:
    component_instance_name: str
    service_name: str
    service_package: str
    service_instance_name: str | None
    domain_id: int | None
    use_full_service_name: bool | None
    always_include_instance_name: bool | None
    protocol: str | None
    participant: str | None
    realms: list[dict[str, str]]
    method_requests: list[str]
    event_requests: list[str]
    method_request_configs: list[SoaRpcRequest] = field(default_factory=list)
    evidence: list[SourceEvidence] = field(default_factory=list)


@dataclass(slots=True)
class SoaDeploymentModel:
    component_instance_name: str
    providers: list[SoaEndpointFact]
    clients: list[SoaEndpointFact]
    evidence: list[SourceEvidence] = field(default_factory=list)


def _extract_method_request_configs(item: dict) -> list[SoaRpcRequest]:
    rpc_custom = item.get("rpc_behavior_customization", {})
    return [
        SoaRpcRequest(
            request_name=entry["request_name"],
            generate_get=entry.get("generate_get") is True,
            generate_set=entry.get("generate_set") is True,
        )
        for entry in rpc_custom.get("method", [])
    ]


def _extract_event_requests(item: dict) -> list[str]:
    rpc_custom = item.get("rpc_behavior_customization", {})
    return [entry["request_name"] for entry in rpc_custom.get("event", [])]


def _extract_realms(item: dict) -> list[dict[str, str]]:
    return [
        {
            "protocol": realm.get("protocol", ""),
            "participant": realm.get("participant", ""),
        }
        for realm in item.get("realms", [])
    ]


def _build_endpoint_fact(item: dict, evidence: SourceEvidence) -> SoaEndpointFact:
    realms = _extract_realms(item)
    method_request_configs = _extract_method_request_configs(item)
    return SoaEndpointFact(
        component_instance_name=item["component_instance_name"],
        service_name=item["service_name"],
        service_package=item["service_package"],
        service_instance_name=item.get("service_instance_name"),
        domain_id=item.get("domain_id"),
        use_full_service_name=item.get("use_full_service_name"),
        always_include_instance_name=item.get("always_include_instance_name"),
        protocol=item.get("protocol") or (realms[0]["protocol"] if realms else None),
        participant=item.get("participant") or (realms[0]["participant"] if realms else None),
        realms=realms,
        method_requests=[entry.request_name for entry in method_request_configs],
        method_request_configs=method_request_configs,
        event_requests=_extract_event_requests(item),
        evidence=[evidence],
    )


def parse_soa_deployment(
    path: Path,
    *,
    source_root: Path | None = None,
    repository_role: str = "code",
) -> SoaDeploymentModel:
    payload = json.loads(path.read_text(encoding="utf-8"))
    component_instances = payload.get("system", {}).get("component_instances", [])
    if component_instances:
        component_instance_name = component_instances[0]["component_instance_name"]
    else:
        services = payload.get("services") or []
        clients = payload.get("clients") or []
        component_instance_name = None
        if services:
            component_instance_name = services[0].get("component_instance_name")
        if component_instance_name is None and clients:
            component_instance_name = clients[0].get("component_instance_name")
        if component_instance_name is None:
            raise KeyError("component_instance_name")
    evidence_root = source_root or path.parent
    def evidence(locator: str) -> SourceEvidence:
        return SourceEvidence.from_path(
            source_kind="local",
            repository_role=repository_role,
            path=path,
            source_root=evidence_root,
            locator=locator,
        )
    providers = [
        _build_endpoint_fact(item, evidence(f"services[{index}]"))
        for index, item in enumerate(payload.get("services", []))
    ]
    clients = [
        _build_endpoint_fact(item, evidence(f"clients[{index}]"))
        for index, item in enumerate(payload.get("clients", []))
    ]
    return SoaDeploymentModel(
        component_instance_name=component_instance_name,
        providers=providers,
        clients=clients,
        evidence=[evidence("system.component_instances[0]")],
    )
