from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(slots=True)
class ProtoRpc:
    name: str
    request_message: str
    response_message: str
    rpc_id: str | None
    method_type: str | None
    rpc_reliability: str | None
    rpc_reliability_field_event: str | None
    update_policy: str | None
    request_has_fields: bool = True
    response_has_fields: bool = True


@dataclass(slots=True)
class ProtoServiceModel:
    package: str
    idl_version: str | None
    service_name: str
    service_id: str | None
    rpcs: list[ProtoRpc]


def _extract_option(block: str, option_name: str) -> str | None:
    pattern = rf"option\s*\({re.escape(option_name)}\)\s*=\s*([^;]+);"
    match = re.search(pattern, block)
    if not match:
        return None
    return match.group(1).strip().strip('"')


def _extract_named_blocks(text: str, keyword: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for match in re.finditer(rf"\b{keyword}\s+(\w+)\s*\{{", text):
        name = match.group(1)
        body_start = match.end()
        depth = 1
        index = body_start
        while index < len(text) and depth > 0:
            char = text[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            index += 1
        if depth == 0:
            blocks[name] = text[body_start : index - 1]
    return blocks


def _strip_comments(text: str) -> str:
    text = re.sub(r"//.*", "", text)
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def _message_has_fields(message_name: str, message_blocks: dict[str, str]) -> bool:
    short_name = message_name.rsplit(".", 1)[-1]
    if short_name in {"Empty", "Null", "Void"}:
        return False
    block = message_blocks.get(short_name)
    if block is None:
        return True
    return bool(
        re.search(
            r"^\s*(?:repeated\s+|optional\s+)?(?:map<[^>]+>|[\w.]+)\s+\w+\s*=\s*\d+",
            _strip_comments(block),
            flags=re.M,
        )
    )


def parse_proto_file(path: Path) -> ProtoServiceModel:
    text = path.read_text(encoding="utf-8")
    message_blocks = _extract_named_blocks(text, "message")

    package_match = re.search(r"package\s+([\w.]+);", text)
    service_match = re.search(
        r"service\s+(\w+)\s*\{(?P<body>.*)\}\s*$",
        text,
        re.S,
    )
    if not package_match or not service_match:
        raise ValueError(f"Unsupported proto file format: {path}")

    service_body = service_match.group("body")
    rpc_matches = re.finditer(
        r"rpc\s+(\w+)\(([\w.]+)\)\s+returns\s+\(([\w.]+)\)\s*\{(?P<body>.*?)\}",
        service_body,
        re.S,
    )

    rpcs: list[ProtoRpc] = []
    for match in rpc_matches:
        rpc_body = match.group("body")
        rpcs.append(
            ProtoRpc(
                name=match.group(1),
                request_message=match.group(2),
                response_message=match.group(3),
                rpc_id=_extract_option(rpc_body, "rpc_id"),
                method_type=_extract_option(rpc_body, "method_type"),
                rpc_reliability=_extract_option(rpc_body, "rpc_reliability"),
                rpc_reliability_field_event=_extract_option(
                    rpc_body, "rpc_reliability_field_event"
                ),
                update_policy=_extract_option(rpc_body, "update_policy"),
                request_has_fields=_message_has_fields(match.group(2), message_blocks),
                response_has_fields=_message_has_fields(match.group(3), message_blocks),
            )
        )

    return ProtoServiceModel(
        package=package_match.group(1),
        idl_version=_extract_option(text, "idl_version"),
        service_name=service_match.group(1),
        service_id=_extract_option(service_body, "service_id"),
        rpcs=rpcs,
    )
