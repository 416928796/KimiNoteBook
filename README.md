# KimiNoteBook

用于浏览和导出本地 Kimi Code CLI 会话的 Web 工具。

## 功能

- 读取 `~/.kimi-code/sessions/` 目录下的本地会话
- 列表展示所有会话，支持搜索
- 进入详情页查看用户与模型的问答对
- 勾选任意问答对，一键导出为 Markdown

## 技术栈

- 前端：Vue 3 + Element Plus + Vite
- 后端：Python + FastAPI

## 快速开始

### 1. 安装后端依赖

```bash
cd server
uv venv
source .venv/Scripts/activate  # Windows
# 或 source .venv/bin/activate  # Linux/macOS
uv pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd web
npm install
```

### 3. 同时启动前后端

```bash
# 在项目根目录
npm install
npm run dev
```

- 前端：http://localhost:5173
- 后端：http://localhost:8000

## 测试

```bash
# 后端测试
npm run test:server

# 前端测试
npm run test:web

# 全部测试
npm test
```

## 配置

后端默认读取 `~/.kimi-code/sessions/`。可通过环境变量修改：

```bash
SESSIONS_ROOT=/path/to/sessions npm run dev:server
```
