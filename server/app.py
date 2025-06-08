from flask import Flask, request, send_from_directory, Response, send_file
import json
import logging
from datetime import datetime
import os
import mimetypes

app = Flask(__name__, static_folder='static')

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('requests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    """全てのリクエストをログに記録"""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'remote_addr': request.remote_addr,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'form': dict(request.form),
        'json': request.get_json(silent=True),
        'data': request.get_data(as_text=True),
        'cookies': dict(request.cookies),
        'user_agent': request.user_agent.string,
        'referrer': request.referrer,
        'scheme': request.scheme,
        'is_secure': request.is_secure,
        'host': request.host,
        'content_type': request.content_type,
        'content_length': request.content_length
    }
    
    logger.info(f"\n{'='*50}\nREQUEST LOG:\n{json.dumps(log_data, indent=2, ensure_ascii=False)}\n{'='*50}")

@app.route('/static/<path:filename>')
def serve_static(filename):
    """静的ファイルの配信"""
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    file_path = os.path.join(static_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return f"File not found: {filename}", 404

@app.route('/js/<path:filename>')
def serve_js(filename):
    """JavaScriptファイルの動的配信"""
    js_dir = os.path.join(app.root_path, 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
    
    file_path = os.path.join(js_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/javascript')
    else:
        # 動的にJavaScriptを生成して返す
        dynamic_js = f"""
// Dynamically generated JavaScript
console.log('Dynamic JS loaded: {filename}');
console.log('Request from:', document.location.href);
console.log('User Agent:', navigator.userAgent);

// Track all events
document.addEventListener('DOMContentLoaded', function() {{
    console.log('DOM loaded');
    
    // Log all clicks
    document.addEventListener('click', function(e) {{
        console.log('Click:', e.target.tagName, e.clientX, e.clientY);
    }});
    
    // Log form submissions
    document.addEventListener('submit', function(e) {{
        console.log('Form submit:', e.target.action);
    }});
}});

// Custom payload placeholder
{generate_custom_payload(filename)}
"""
        return Response(dynamic_js, mimetype='application/javascript')

def generate_custom_payload(filename):
    """ファイル名に基づいてカスタムペイロードを生成"""
    payloads = {
        'tracker.js': """
// Tracking payload
(function() {
    var data = {
        url: window.location.href,
        referrer: document.referrer,
        cookies: document.cookie,
        localStorage: JSON.stringify(localStorage),
        timestamp: new Date().toISOString()
    };
    console.log('Tracking data:', data);
})();
""",
        'keylogger.js': """
// Keylogger payload (for CTF demonstration)
document.addEventListener('keydown', function(e) {
    console.log('Key pressed:', e.key, e.code);
});
""",
        'xss-test.js': """
// XSS test payload
alert('XSS Test - JavaScript Executed!');
document.body.innerHTML += '<div style="color:red;">XSS Payload Executed</div>';
"""
    }
    
    return payloads.get(filename, "// No custom payload for this file")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """全てのパスをキャッチ"""
    # HTMLレスポンスでJavaScriptを自動的に含める
    html_response = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Request Logger</title>
    <script src="/js/tracker.js"></script>
</head>
<body>
    <h1>Request Logged</h1>
    <p>Method: {request.method}</p>
    <p>Path: {request.path}</p>
    <p>Full URL: {request.url}</p>
    <script src="/js/custom.js"></script>
</body>
</html>
"""
    return html_response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)