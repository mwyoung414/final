from BaseModels.RouteBase import *

app = Quart(__name__)

ALLOWED_IP = "192.168.1.100"

@app.route('/admin', methods=['GET'])
async def admin():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

