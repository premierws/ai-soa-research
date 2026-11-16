# 车控 Agent 与服务架构矩阵汇报材料

日期：2026-11-16。两份独立 HTML 纵向演示稿，共用离线 CSS／JS，入口为 `index.html`。

- `agent.html`：20 页，业务价值、必要性决策、目标、整体方案、演进、实施和完整案例。
- `matrix.html`：18 页，SOA 核心基础、COE 规划、角色、边界、流程、资源和演进。
- `sources.html`：来源与证据边界。
- `deck_content.json`：正文与逐页讲述提示。
- `build_decks.py`：正文与 HTML 生成源，执行后生成两份演示稿。
- `assets/`：共用样式和翻页逻辑，无 CDN 依赖。

## 演示

支持滚动、向上／向下、PageUp／PageDown、Home／End；O 打开目录，N 显示讲述提示，F 请求全屏。也可使用右下角按钮和右侧导航。文件 URL 与 HTTP 均可打开，手机按纵向内容排列。

浏览器打印可保存横向 PDF，讲述提示不进入打印。

## 内容约束

本矩阵以 SOA 为最重要基础设施和核心 know-how，向能力与交互延伸，不接管独立软件架构矩阵。VCC 业务责任、系统产品执行、COE 技术赋能及工程交付分别明确。

跨入口协调缺口只证明共同职责的需求，独立边界、Agent 规划和大模型仍需分别论证。资源测算是容量示例，不是新增编制或实施承诺。

## 本地预览

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory /home/shaun/projects/soa_matrix
```

## 目标部署

用户指定服务器 `10.110.169.217`，目录 `/workspace/soa_matrix`。只部署本目录的静态材料，不修改已有应用或 Web 服务配置。SSH 接入与实际发布路径以部署验证结果为准。
