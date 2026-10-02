# 24124966_calculator_backend

前后端分离计算器系统 —— **后端项目**

## 项目介绍

本项目是《软件工程》第一次作业"前后端分离计算器系统"的后端部分。

后端负责：
- 接收前端发来的计算请求（HTTP API）
- 校验输入、解析数学表达式
- 完成表达式计算（支持四则运算、括号、一元正负号、小数）
- 处理异常（非法表达式、除零）
- 将计算历史持久化到 SQLite 数据库
- 提供历史记录的查询、删除接口
- 返回标准化的 JSON API 响应

计算逻辑完全在后端完成，**不依赖前端计算结果**，满足作业对"前后端分离"的要求。

## 技术栈

| 模块       | 技术                     |
| ---------- | ------------------------ |
| 后端框架   | Python 3 + Flask         |
| 数据库     | SQLite（Python 内置）    |
| 表达式计算 | 自研递归下降解析器（不使用 eval） |

## 运行环境

- Python 3.8 及以上（本项目在 Python 3.14 下开发测试）
- 操作系统：Windows / macOS / Linux 均可

## 安装方法

```bash
# 进入后端项目目录
cd 24124966_calculator_backend

# （建议）创建虚拟环境
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate
# macOS / Linux 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 启动方法

```bash
python app.py
```

启动成功后，服务运行在 `http://127.0.0.1:5000`，控制台会输出：
`Running on http://0.0.0.0:5000`

## 配置说明

所有配置均在 `app.py` 顶部，可通过修改 `app.run()` 的参数调整：
- `port=5000`：服务端口
- `host="0.0.0.0"`：允许局域网访问（如需仅本机访问可改为 `127.0.0.1`）

## 数据库初始化方法

无需手动初始化。项目首次启动时，`database.py` 会自动在项目目录下创建
`calculator.db` 数据库文件及 `calculation_history` 表，表结构如下：

```sql
CREATE TABLE calculation_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    expression  TEXT    NOT NULL,   -- 计算表达式
    result      TEXT    NOT NULL,   -- 计算结果
    created_at  TEXT    NOT NULL    -- 计算时间
);
```

如需清空数据库，删除 `calculator.db` 文件后重启服务即可。

## 前后端连接方法

前端通过 HTTP 请求访问后端接口，前端项目见
`24124966_calculator_frontend` 仓库。前端配置的后端地址默认是：

```
http://127.0.0.1:5000
```

## API 文档

### 1. 计算表达式

```
POST /api/calculate
Content-Type: application/json
```

请求体：

```json
{
  "expression": "12+8"
}
```

成功响应（HTTP 200）：

```json
{
  "success": true,
  "id": 1,
  "expression": "12+8",
  "result": 20
}
```

失败响应（HTTP 400，非法表达式）：

```json
{
  "success": false,
  "message": "Invalid expression"
}
```

失败响应（HTTP 400，除零）：

```json
{
  "success": false,
  "message": "Division by zero"
}
```

### 2. 获取全部计算历史

```
GET /api/history
```

成功响应（HTTP 200）：

```json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "expression": "(2+3)*4",
      "result": "20",
      "created_at": "2026-10-01 10:22:00"
    }
  ]
}
```

### 3. 按 id 删除一条历史记录

```
DELETE /api/history/{id}
```

成功响应（HTTP 200）：

```json
{
  "success": true
}
```

记录不存在（HTTP 404）：

```json
{
  "success": false,
  "message": "Record not found"
}
```

### 4. 清空全部历史记录（附加功能）

```
DELETE /api/history
```

成功响应（HTTP 200）：

```json
{
  "success": true
}
```

### 5. 健康检查

```
GET /api/health
```

## 目录结构

```
24124966_calculator_backend/
├── app.py            # Flask 主程序，定义全部 API 接口
├── calculator.py     # 表达式解析与计算模块（递归下降解析器）
├── database.py       # SQLite 数据库操作模块
├── requirements.txt  # Python 依赖清单
├── README.md         # 项目说明
└── codestyle.md      # 代码规范
```

## 代码规范

代码遵循 [PEP 8](https://peps.python.org/pep-0008/)，详见 [codestyle.md](codestyle.md)。
