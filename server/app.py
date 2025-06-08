from flask import Flask, request
import json
import logging
from datetime import datetime

app = Flask(__name__)

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

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """全てのパスをキャッチ"""
    return f"Request logged: {request.method} {request.path}", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)