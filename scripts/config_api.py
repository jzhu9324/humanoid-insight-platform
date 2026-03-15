#!/usr/bin/env python3
"""
配置管理 API 服务器

提供 REST API 接口用于读写 config/sources.json 文件
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs


# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config" / "sources.json"


class ConfigAPIHandler(BaseHTTPRequestHandler):
    """处理配置 API 请求"""

    def _set_headers(self, status=200, content_type='application/json'):
        """设置响应头"""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self._set_headers()

    def do_GET(self):
        """处理 GET 请求 - 读取配置"""
        if self.path == '/api/config':
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                self._set_headers()
                self.wfile.write(json.dumps(config, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({
                    'error': str(e)
                }).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({
                'error': 'Not found'
            }).encode('utf-8'))

    def do_POST(self):
        """处理 POST 请求 - 保存配置"""
        if self.path == '/api/config':
            try:
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                config = json.loads(post_data.decode('utf-8'))

                # 验证配置格式
                if not isinstance(config, dict):
                    raise ValueError('配置必须是一个对象')

                if 'companies' not in config or 'paper_keywords' not in config or 'wechat_accounts' not in config:
                    raise ValueError('配置缺少必要字段')

                # 保存到文件
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)

                self._set_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': '配置已保存'
                }, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({
                    'error': str(e)
                }, ensure_ascii=False).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({
                'error': 'Not found'
            }).encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[API] {self.address_string()} - {format % args}")


def run_server(port=3001):
    """启动 API 服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ConfigAPIHandler)

    print(f"=" * 60)
    print(f"配置管理 API 服务器")
    print(f"=" * 60)
    print(f"✓ 服务器启动在: http://localhost:{port}")
    print(f"✓ 配置文件: {CONFIG_FILE}")
    print(f"\nAPI 端点:")
    print(f"  GET  /api/config - 读取配置")
    print(f"  POST /api/config - 保存配置")
    print(f"\n按 Ctrl+C 停止服务器\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ 服务器已停止")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
