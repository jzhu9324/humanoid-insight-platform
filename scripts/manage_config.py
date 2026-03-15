#!/usr/bin/env python3
"""
配置管理工具 - 用于管理 sources.json 配置文件

使用方法:
    python scripts/manage_config.py list                    # 查看当前配置
    python scripts/manage_config.py add-company             # 添加公司（交互式）
    python scripts/manage_config.py add-keyword "embodied AI"  # 添加论文关键词
    python scripts/manage_config.py add-wechat              # 添加微信公众号（交互式）
    python scripts/manage_config.py remove-company "Tesla"  # 删除公司
    python scripts/manage_config.py web                     # 启动网页管理界面
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


CONFIG_FILE = Path(__file__).parent.parent / "config" / "sources.json"


def load_config() -> Dict:
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        return {"companies": [], "paper_keywords": [], "wechat_accounts": []}

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: Dict):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✓ 配置已保存到 {CONFIG_FILE}")


def list_config():
    """显示当前配置"""
    config = load_config()

    print("\n" + "=" * 60)
    print("当前配置")
    print("=" * 60)

    print(f"\n📊 监控公司 ({len(config['companies'])} 家):")
    for i, company in enumerate(config['companies'], 1):
        print(f"  {i}. {company['name']} ({company['name_cn']})")
        print(f"     官网: {company['website']}")
        if company.get('rss_feeds'):
            print(f"     RSS: {', '.join(company['rss_feeds'])}")
        print(f"     关键词: {', '.join(company['keywords'])}")
        print()

    print(f"\n📚 论文关键词 ({len(config['paper_keywords'])} 个):")
    for i, keyword in enumerate(config['paper_keywords'], 1):
        print(f"  {i}. {keyword}")

    print(f"\n📱 微信公众号 ({len(config['wechat_accounts'])} 个):")
    for i, account in enumerate(config['wechat_accounts'], 1):
        print(f"  {i}. {account['name']}")
        print(f"     关键词: {', '.join(account['keywords'])}")

    print("\n" + "=" * 60)


def add_company_interactive():
    """交互式添加公司"""
    config = load_config()

    print("\n添加新公司")
    print("-" * 40)

    name = input("公司名称（英文）: ").strip()
    if not name:
        print("❌ 公司名称不能为空")
        return

    name_cn = input("公司名称（中文）: ").strip()
    website = input("官网地址: ").strip()
    rss_feeds = input("RSS订阅源（多个用逗号分隔，可选）: ").strip()
    keywords = input("关键词（多个用逗号分隔）: ").strip()

    company = {
        "name": name,
        "name_cn": name_cn or name,
        "website": website,
        "rss_feeds": [f.strip() for f in rss_feeds.split(',')] if rss_feeds else [],
        "keywords": [k.strip() for k in keywords.split(',')] if keywords else []
    }

    config['companies'].append(company)
    save_config(config)
    print(f"✓ 已添加公司: {name}")


def add_keyword(keyword: str):
    """添加论文关键词"""
    config = load_config()

    if keyword in config['paper_keywords']:
        print(f"⚠ 关键词已存在: {keyword}")
        return

    config['paper_keywords'].append(keyword)
    save_config(config)
    print(f"✓ 已添加关键词: {keyword}")


def add_wechat_interactive():
    """交互式添加微信公众号"""
    config = load_config()

    print("\n添加微信公众号")
    print("-" * 40)

    name = input("公众号名称: ").strip()
    if not name:
        print("❌ 公众号名称不能为空")
        return

    keywords = input("关键词（多个用逗号分隔）: ").strip()

    account = {
        "name": name,
        "keywords": [k.strip() for k in keywords.split(',')] if keywords else []
    }

    config['wechat_accounts'].append(account)
    save_config(config)
    print(f"✓ 已添加公众号: {name}")


def remove_company(name: str):
    """删除公司"""
    config = load_config()

    original_count = len(config['companies'])
    config['companies'] = [c for c in config['companies'] if c['name'] != name]

    if len(config['companies']) < original_count:
        save_config(config)
        print(f"✓ 已删除公司: {name}")
    else:
        print(f"⚠ 未找到公司: {name}")


def remove_keyword(keyword: str):
    """删除论文关键词"""
    config = load_config()

    if keyword in config['paper_keywords']:
        config['paper_keywords'].remove(keyword)
        save_config(config)
        print(f"✓ 已删除关键词: {keyword}")
    else:
        print(f"⚠ 未找到关键词: {keyword}")


def start_web_interface():
    """启动网页管理界面"""
    print("\n🌐 启动网页管理界面...")
    print("=" * 60)

    try:
        from http.server import HTTPServer, SimpleHTTPRequestHandler
        import webbrowser

        # 创建简单的 HTML 界面
        html_file = Path(__file__).parent.parent / "config_manager.html"

        if not html_file.exists():
            create_web_interface(html_file)

        # 启动服务器
        port = 8888
        print(f"\n✓ 服务器启动在: http://localhost:{port}")
        print(f"✓ 配置文件: {CONFIG_FILE}")
        print("\n按 Ctrl+C 停止服务器\n")

        webbrowser.open(f"http://localhost:{port}/config_manager.html")

        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(CONFIG_FILE.parent.parent), **kwargs)

        httpd = HTTPServer(('localhost', port), Handler)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✓ 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")


def create_web_interface(html_file: Path):
    """创建网页管理界面"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>配置管理 - 人形机器人洞察平台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .section { margin-bottom: 40px; }
        .section h2 { color: #666; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #eee; }
        .item { background: #f9f9f9; padding: 15px; margin-bottom: 10px; border-radius: 4px; }
        .item h3 { color: #333; margin-bottom: 8px; }
        .item p { color: #666; font-size: 14px; margin: 4px 0; }
        .btn { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }
        .btn:hover { background: #45a049; }
        .btn-danger { background: #f44336; }
        .btn-danger:hover { background: #da190b; }
        textarea { width: 100%; min-height: 400px; font-family: monospace; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .notice { background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 配置管理 - 人形机器人洞察平台</h1>

        <div class="notice">
            <strong>📝 使用说明:</strong> 在下方文本框中编辑 JSON 配置，然后点击"保存配置"按钮。保存后需要手动将内容复制到 <code>config/sources.json</code> 文件中。
        </div>

        <div class="section">
            <h2>配置编辑器</h2>
            <textarea id="configEditor"></textarea>
            <br><br>
            <button class="btn" onclick="saveConfig()">💾 下载配置文件</button>
            <button class="btn" onclick="loadConfig()">🔄 重新加载</button>
            <button class="btn" onclick="formatConfig()">✨ 格式化</button>
        </div>
    </div>

    <script>
        async function loadConfig() {
            try {
                const response = await fetch('/config/sources.json');
                const config = await response.json();
                document.getElementById('configEditor').value = JSON.stringify(config, null, 2);
            } catch (error) {
                alert('加载配置失败: ' + error.message);
            }
        }

        function formatConfig() {
            try {
                const config = JSON.parse(document.getElementById('configEditor').value);
                document.getElementById('configEditor').value = JSON.stringify(config, null, 2);
            } catch (error) {
                alert('JSON 格式错误: ' + error.message);
            }
        }

        function saveConfig() {
            try {
                const config = JSON.parse(document.getElementById('configEditor').value);
                const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'sources.json';
                a.click();
                alert('✓ 配置文件已下载！请将其保存到 config/sources.json');
            } catch (error) {
                alert('保存失败: ' + error.message);
            }
        }

        // 页面加载时自动加载配置
        loadConfig();
    </script>
</body>
</html>"""

    html_file.write_text(html_content, encoding='utf-8')
    print(f"✓ 已创建网页界面: {html_file}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "list":
        list_config()

    elif command == "add-company":
        add_company_interactive()

    elif command == "add-keyword":
        if len(sys.argv) < 3:
            print("❌ 请提供关键词")
            return
        add_keyword(sys.argv[2])

    elif command == "add-wechat":
        add_wechat_interactive()

    elif command == "remove-company":
        if len(sys.argv) < 3:
            print("❌ 请提供公司名称")
            return
        remove_company(sys.argv[2])

    elif command == "remove-keyword":
        if len(sys.argv) < 3:
            print("❌ 请提供关键词")
            return
        remove_keyword(sys.argv[2])

    elif command == "web":
        start_web_interface()

    else:
        print(f"❌ 未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
