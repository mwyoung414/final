from quart import Quart, render_template
from quart import request, jsonify
from db.init import init_databases
from dotenv import load_dotenv
from secrets import token_bytes
import hashlib, hmac, base64
import os
import logging
from db.init import *

app = Quart(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
list_of_db_urls = os.getenv("DB_URLS").split(",")

@app.before_serving
async def start_db():
    """Initialize the database before serving requests.

    This function is called before the server starts handling
    requests. It initializes the database connection.

    """
    await init_databases(list_of_db_urls)
    


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

@app.route("/register", methods=['GET'])
async def registration():
    """Render the registration.html template.

    This function handles the GET request to the /registration route
    and renders the registration.html template.

    Returns:
        The rendered HTML template.
    """
    
    states = CommonDataDb.get_all_states()
    
    return await render_template('register.html', states=states)


@app.route("/admin/view_users", methods=['GET'])
async def view_users():
    """Render the view_users.html template.

    This function handles the GET request to the /view_users route
    and renders the view_users.html template.

    Returns:
        The rendered HTML template.
    """
    
    return await render_template('admin_view_users.html', users=[])

@app.route("/admin/add_user", methods=['POST'])
async def add_user():
    """Handle the addition of a new user."""
    data = await request.get_json()  # Get JSON data from the request
    username = data.get("username")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Validate the data (e.g., check if passwords match)
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400


    # Add the user to the database (example logic)
    try:
        new_user = User(username=username, firstname=firstname, lastname=lastname, email=email, role=role, password=password)
        await user_db.addUser(new_user)
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route("/log-js-error", methods=["POST"])
async def log_js_error():
    data = await request.get_json()
    app.logger.error(f"JS Error: {data}")
    return {"status": "ok"}


def hash_password(password: str) -> tuple[str, str]:
    # sourcery skip: avoid-builtin-shadow
    salt = token_bytes(16)
    hash = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100_000)
    return base64.b64encode(salt).decode('utf-8'), base64.b64encode(hash).decode('utf-8')