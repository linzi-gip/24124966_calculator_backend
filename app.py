# -*- coding: utf-8 -*-
"""
app.py - 前后端分离计算器系统 · 后端主程序
==========================================
基于 Flask 实现的 API 服务，提供以下接口：

  POST   /api/calculate      计算表达式（计算由后端完成）
  GET    /api/history        获取全部计算历史
  DELETE /api/history/<id>   按 id 删除一条历史记录
  DELETE /api/history        清空全部历史记录（附加功能）
  GET    /api/health         健康检查

启动方式：
    pip install -r requirements.txt
    python app.py
启动后服务运行在 http://127.0.0.1:5000
"""

from flask import Flask, jsonify, request

from calculator import ExpressionError, evaluate_expression
from database import Database

app = Flask(__name__)
db = Database()


# ---------------------------------------------------------------------------
# 跨域支持（CORS）：前端项目独立运行（例如直接双击打开 index.html）
# 时，浏览器会发起跨域请求，因此需要在后端允许跨域访问。
# ---------------------------------------------------------------------------
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    """处理浏览器发出的预检请求。"""
    return "", 204


# ---------------------------------------------------------------------------
# API 1：计算表达式
# 请求体示例: {"expression": "12+8"}
# 成功响应:   {"success": true, "id": 1, "expression": "12+8", "result": 20}
# 失败响应:   {"success": false, "message": "Invalid expression"}
# ---------------------------------------------------------------------------
@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return jsonify({"success": False, "message": "Missing expression"}), 400

    expression = data["expression"]
    if not isinstance(expression, str) or not expression.strip():
        return jsonify({"success": False, "message": "Invalid expression"}), 400

    try:
        result = evaluate_expression(expression)
    except ZeroDivisionError:
        return jsonify({"success": False, "message": "Division by zero"}), 400
    except ExpressionError:
        return jsonify({"success": False, "message": "Invalid expression"}), 400

    # 计算成功才写入历史记录
    record_id = db.insert_history(expression, result)
    return jsonify(
        {
            "success": True,
            "id": record_id,
            "expression": expression,
            "result": result,
        }
    ), 200


# ---------------------------------------------------------------------------
# API 2：获取全部计算历史
# 成功响应: {"success": true, "data": [{"id":1,"expression":"1+2","result":"3",
#           "created_at":"2026-10-01 10:20:00"}, ...]}
# ---------------------------------------------------------------------------
@app.route("/api/history", methods=["GET"])
def get_history():
    records = db.get_all_history()
    return jsonify({"success": True, "data": records}), 200


# ---------------------------------------------------------------------------
# API 3：按 id 删除一条历史记录
# ---------------------------------------------------------------------------
@app.route("/api/history/<int:record_id>", methods=["DELETE"])
def delete_history(record_id):
    deleted = db.delete_history(record_id)
    if not deleted:
        return jsonify({"success": False, "message": "Record not found"}), 404
    return jsonify({"success": True}), 200


# ---------------------------------------------------------------------------
# API 4（附加）：清空全部历史记录
# ---------------------------------------------------------------------------
@app.route("/api/history", methods=["DELETE"])
def clear_history():
    db.clear_history()
    return jsonify({"success": True}), 200


# ---------------------------------------------------------------------------
# 健康检查接口
# ---------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"success": True, "message": "OK"}), 200


if __name__ == "__main__":
    # host=0.0.0.0 表示允许局域网内其他设备访问，便于部署演示
    # debug=False 关闭调试模式，避免部署时暴露调试信息
    app.run(host="0.0.0.0", port=5000, debug=False)
