from quart import Quart, render_template
from quart import request, jsonify
from db.init import init_databases
from dotenv import load_dotenv
import os
import logging

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
user_db_url = os.getenv("USER_DB_URL")

@app.before_serving
async def start_db():
    """Initialize the database before serving requests.

    This function is called before the server starts handling
    requests. It initializes the database connection.

    """
    await init_databases(user_db_url)
    


@app.after_request
def add_headers(response):
    """Modify response headers to enable CORS.

    This function adds headers to the HTTP response to allow
    Cross-Origin Resource Sharing (CORS) from any origin.

    Args:
        response: The Flask response object.

    Returns:
        The modified Flask response object.
    """
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE OPTIONS"
    return response

@app.route("/", methods=['GET'])
async def index():
    return await render_template('index.html')

@app.route("/admin", methods=['GET'])
async def admin():
    return await render_template('base_admin.html')

@app.route("/admin/view_users", methods=['GET'])
async def view_users():
    """Render the view_users.html template.

    This function handles the GET request to the /view_users route
    and renders the view_users.html template.

    Returns:
        The rendered HTML template.
    """
    
    return await render_template('admin_view_users.html', users=[])

@app.route("/log-js-error", methods=["POST"])
async def log_js_error():
    data = await request.get_json()
    app.logger.error(f"JS Error: {data}")
    return {"status": "ok"}