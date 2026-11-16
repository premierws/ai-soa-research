# Embedded Architecture Platform

Web platform for building software-module and service-interface relationship
graphs from a shared proto repository, multiple code repositories, and an Excel
deployment table.

## Current Scope

- Configure one shared proto repository, one Excel repository, multiple code
  repositories, and saved version configurations that bind branches together.
- Parse shared `proto + .options` inputs into service, rpc, and field-constraint facts.
- Parse `cfg/soa/soa_deployment.json` files into provider and client facts.
- Parse the deployment Excel table into software-module, ECU, and Server deployment facts.
- Normalize modules, service instances, and method/event edges with anomaly detection.
- Expose graph build and compare APIs over the sample data set.
- Render a frontend workspace for repository management, graph build, graph view, and inline compare.
- Project a build quality report for every graph build version, including Server deployment metrics, Client matching metrics, missing classifications, and Module Board location targets.

## Input Model

- Shared proto repository:
  `proto` files define services and RPCs; matching `.options` files define field constraints.
- Code repositories:
  each software directory contains `cfg/soa/soa_deployment.json`.
  Some repositories add an optional vehicle-variant directory above the software directory.
- Excel deployment table:
  maps software modules to a single ECU.

## Core Rules

- Software module identity is based on `component_instance_name`.
- `component_instance_name` and Excel `CompName` are treated as the same module name
  with case-insensitive matching only.
- Service instance identity is:
  `service_package + service_name + service_instance_name`.
- Graph edges are built at method/event level.
- `clients.method` maps to proto RPCs with `METHOD` or `FIELD` semantics.
- `clients.event` maps to proto RPCs with `EVENT` or `FIELD` semantics.
- If a provider is missing from the selected version configuration but the
  service exists in proto, the graph uses an external-provider edge instead of
  dropping the dependency.
- If a module maps to multiple ECUs, normalization records a `multi_ecu_conflict`.

## Layout

- `frontend/`: React + Vite shell for the UI.
- `backend/`: FastAPI service, parsers, normalization logic, and graph APIs.
- `docker-compose.yml`: Local bootstrap for the frontend and backend scaffold services.

## Frontend

- `npm run dev` starts the Vite app.
- `VITE_DEV_PROXY_TARGET=http://127.0.0.1:18000 npm run dev` starts Vite
  with `/api` and `/health` proxied to a non-default backend.
- `VITE_API_BASE_URL=http://127.0.0.1:18000 npm run dev` makes the
  frontend call that backend directly instead of same-origin proxy paths.
- `npm test -- --run` runs the frontend tests.
- `npm run build` type-checks and builds the app.
- `Repositories` lets you maintain Proto, Excel, code repositories, and version configurations.
- `Build Graph` lets you request a graph build for a version configuration and inspect returned fact counts.
- `Graph` loads the sample graph payload and keeps compare as an inline secondary action.
- `Compare` lets you compare two version configurations and inspect added/removed edge keys.

## Backend

- `python -m pytest -q` runs the backend tests.
- `/health/live` returns the process liveness result; `/health/ready` checks the
  database, Redis, `git`, `ssh`, and `query-cli`; `/health` remains the
  compatibility readiness endpoint.
- `/api/repositories/proto` creates the unique proto repository config.
- `/api/repositories/excel` creates the unique Excel repository config.
- `/api/repositories/code` creates a code repository config.
- `/api/version-configurations` creates a branch-binding analysis configuration.
- `/api/graphs/build` returns graph applications, service instances, edges, and anomalies.
- `/api/compare` returns added and removed edge keys between two refs.
- `/api/graph-build-versions/{id}/quality-report` returns the read-only quality projection for a graph build version. Running and failed builds return their status; current snapshots return full issue details; legacy snapshots without `missing_dependencies` return summary-only data.

## 构建质量报告

版本配置中的每个图构建版本都提供“构建质量”入口。报告使用两组独立口径：

- `Server 部署数`统计 Local SOA、Excel、NXTC 中的部署记录；`唯一 Server 数`按 `service_package + service_name + service_instance_name` 去重，不包含 ECU。
- `已匹配的 Clients`统计成功匹配到 Server 的有效 Client；`未匹配 Clients`按 Server 未部署、Server 实例不匹配、Client 所在 ECU 缺少 Server 部署分类。

报告由后端从 snapshot 动态投影，不修改原始构建数据。问题明细可以切换到报告所属 snapshot，并定位到受影响 Client 软件模块的 Focus 页面。完整设计见 `docs/superpowers/specs/2026-07-13-build-quality-report-design.md`。

报告总览固定为`构建质量流`、`问题矩阵`、`服务影响地图`、`实例差异`和`构建信息`五个分栏。五个分栏覆盖单次构建的整体结果、ECU 分布、服务影响、实例专项诊断和输入溯源；每次只显示一个总览视图，下方问题明细始终保留并独立滚动。

## 容器运行与真实构建

Backend 和 Worker 共用 `service-arch-backend:dev` 镜像。镜像内固定安装
`query-cli 0.1.0` 并校验 SHA-256，同时包含 Git 和 OpenSSH；运行时不再通过
`pip install` 临时补依赖。

```bash
docker compose --env-file "$HOME/.config/service-arch/sso-dev.env" build backend worker
docker compose --env-file "$HOME/.config/service-arch/sso-dev.env" \
  up -d --wait redis backend worker frontend
docker compose --env-file "$HOME/.config/service-arch/sso-dev.env" \
  exec -T backend curl -fsS http://127.0.0.1:8000/health/ready
```

Compose 以只读方式挂载宿主机 `$HOME/.ssh`。容器内 Git 忽略宿主
`~/.ssh/config`，使用默认 SSH identity 和 `known_hosts`，避免绑定挂载后的属主
不符合 OpenSSH 检查；因此默认 identity 必须已具备输入仓库的读取权限。Git 只对
当前 checkout 的规范化路径设置 `safe.directory`，不会全局信任任意仓库。
Frontend 的 `/app/node_modules` 使用独立 Docker Volume，容器执行 `npm ci` 不会
改写宿主仓库的依赖目录权限。

Frontend 默认为真实数据模式：请求失败会显示错误与重试入口，不再回退到 Mock
数据。仅在演示时显式设置 `VITE_ENABLE_DEMO_DATA=true`，界面会显示 Demo 标识。

## 来源证据与 Golden Snapshot

Module Focus、服务实例、外部 Provider 和缺失 Provider 会显示来源证据。证据只保存
仓库角色、仓库内相对路径、JSON/Excel 定位信息及 NXTC 查询上下文，不保存绝对
checkout 路径、仓库 URL 或凭据。缺失 Provider 的证据表示“哪个 Consumer 声明了
依赖”，不代表缺失服务部署在该 Consumer 所在 ECU。

Golden Snapshot 是脱敏后的真实构建基线，只记录输入版本、来源 commit、实体计数、
缺失原因分布、质量哈希和证据覆盖率。以成功构建生成的新 Snapshot ID 为参数：

```bash
docker compose --env-file "$HOME/.config/service-arch/sso-dev.env" exec -T backend \
  python -m app.commands.write_golden_snapshot \
  --snapshot-id <SNAPSHOT_ID> \
  --output golden/pisces-v02-rl312-bl0310.json

docker compose --env-file "$HOME/.config/service-arch/sso-dev.env" exec -T backend \
  python -m app.commands.verify_golden_snapshot \
  --manifest golden/pisces-v02-rl312-bl0310.json \
  --snapshot-id <SNAPSHOT_ID>
```

当前基线来自 PISCES `V02_RL312_BL0310`、SOA deployment `V2.4.0`。

## Verification

Run these commands from the platform directories:

- `cd backend && python -m pytest -q`
- `cd frontend && npm test -- --run`
- `cd frontend && npm run build`
- `cd .. && docker-compose config`

## NIO SSO 与权限配置

本项目只使用 Laputa/IAM 的“仅身份验证”能力。业务授权由本项目的 `User`、`Admin` 角色和 Permission Matrix 管理，不从 IAM Group 推导角色。

在 NIO SSO DEV 为本地开发申请独立 Client，并登记精确回调地址，例如 `http://localhost:5173/api/auth/callback`；该路径由 Vite 代理到 Backend，确保 Callback 完成后的 `/` 回到前端。DEV、TEST、STG、PROD 的 Client、Secret、Issuer 和回调地址必须相互隔离。

启动前通过仓库外环境变量或部署平台 Secret 注入以下配置：

- `ARCH_PLATFORM_ENVIRONMENT`：`development`、`test`、`staging` 或 `production`。
- `ARCH_PLATFORM_OIDC_ISSUER_URL`、`ARCH_PLATFORM_OIDC_CLIENT_ID`。
- `ARCH_PLATFORM_OIDC_CLIENT_SECRET`：敏感值，不写入 Compose 或 Git。
- `ARCH_PLATFORM_OIDC_REDIRECT_URI`。
- `ARCH_PLATFORM_SESSION_ENCRYPTION_KEY`：Fernet Key，敏感值，不与 OIDC Secret 复用。
- `ARCH_PLATFORM_SESSION_COOKIE_SECURE`：本地纯 HTTP 调试可设为 `false`；非 Development 必须为 `true`。
- `ARCH_PLATFORM_BOOTSTRAP_ADMIN_USERNAME`：仅用于干净数据库的首个 Admin 引导，不提供仓库内默认账号。

本地启动顺序：

```bash
docker compose up -d --wait redis backend worker frontend
```

Redis 不映射宿主机端口，只允许 Compose 内部网络访问。Backend 启动前执行 Alembic，Frontend 的 `/api` 和 `/health` 通过 Vite 代理访问 Backend。

退出登录只删除 Service Arch 的 Redis Session 并清除 HttpOnly Cookie，不结束 LAPUTA 全局 SSO 会话。再次登录时，LAPUTA 可以复用现有全局会话完成自动认证。

首个 Bootstrap Admin 登录后，应在“用户与权限”中配置至少第二个 Admin。若管理入口不可用，可在 Backend 容器内按精确用户名恢复 Admin：

```bash
docker compose exec backend python -m app.commands.grant_admin <username>
```

不得把 `.env`、真实账号、Client Secret、Session Encryption Key、Token、Cookie、Redis 数据或包含这些内容的日志和截图提交到 Git。浏览器只保存 HttpOnly Session Cookie；OIDC Token 不进入 Local Storage、Session Storage 或业务数据库。

非 Development 环境缺少任一 OIDC 必填项、加密 Key，或关闭 Secure Cookie 时，Backend 和 Worker 会在启动期拒绝运行。
