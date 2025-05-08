from quart import Quart, render_template, make_response, redirect, url_for
from quart import request, jsonify
from db.init import init_databases
from sqlalchemy.future import select
from dotenv import load_dotenv
from secrets import token_bytes
import hashlib, hmac, base64, secrets
import os
import logging
from db.init import *
from models.models import User
from db.HotelsDbContext import HotelsDb
from db.RoomDbContext import RoomDb
from Services import LoggingService, AuthService, JWTService
from AuthDecorater import token_required

app = Quart(__name__)

logging.basicConfig(level=logging.INFO)

load_dotenv()
db_urls = os.getenv("DB_URLS", "").split(",")

list_of_db_urls = [url.strip() for url in db_urls if url.strip()]

Logger = LoggingService.Log()

Auth = AuthService.Authentication()

SECRET_KEY = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
JWT = JWTService.JWTService(SECRET_KEY)

app.JWT = JWT

if not list_of_db_urls:
    raise ValueError("No database URLs provided in the environment variable DB_URLS.")

user_db = UserDb(os.getenv("USERS_DB_URL"))
common_db = CommonDataDb(os.getenv("STATES_DB_URL"))
hotels_db = HotelsDb(os.getenv("HOTELS_DB_URL"), os.getenv("HOTELS_SYNC_DB_URL"))
rooms_db = RoomDb(os.getenv("ROOMS_DB_URL"))

@app.before_serving
async def start_db():
    """Initialize the database before serving requests.

    This function is called before the server starts handling
    requests. It initializes the database connection.

    """
    await hotels_db.init_db()
    await user_db.init_db()
    await common_db.init_db()
    await rooms_db.init_db()
    logging.info("Database initialized successfully.")
    


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
    logged_in_user = None
    
    paged_hotels = await hotels_db.getPagedHotels(1, 9)
    
    return await render_template('index.html', users=logged_in_user, hotels=paged_hotels["hotels"])

@app.route("/admin", methods=['GET', 'POST'])
@token_required
async def admin():
    username = request.username
    role = request.role
    
    return await render_template('base_admin.html', username=username, role=role)
    
@app.route("/admin/login", methods=['POST'])
async def admin_login():
    """Handle admin authentication and token generation"""
    data = await request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
    
    async with user_db.session() as session:
        result = await session.execute(select(User).where((User.USERNAME == username) & (User.ROLE == "ADMIN")))
        user = result.scalars().first()
        
    print(user)
    print(Auth.verify_password(password, user.SALT, user.HASH))
    if user and Auth.verify_password(password, user.SALT, user.HASH):
        # Create JWT token
        token_data = JWT.create_token(user.ID, user.USERNAME, user.ROLE)
        
        # Create response with redirect to admin dashboard
        response = await make_response(redirect(url_for('admin')))
        
        # Set token in cookie
        response.set_cookie(
            'access_token', 
            token_data['access_token'],
            httponly=True,
            secure=False,  # Set to True in production
            max_age=JWT.token_expire_time
        )
        
        return response
    else:
        # Redirect back to home with error
        return redirect(url_for('index', error="Invalid admin credentials"))

@app.route("/register", methods=['GET', 'POST'])
async def registration():
    if request.method == 'POST':
        # Get form data
        form_data = await request.form
        username = form_data.get('username')
        firstname = form_data.get('firstname')
        lastname = form_data.get('lastname')
        address = form_data.get('address')
        city = form_data.get('city')
        state = form_data.get('state')  # Will contain the selected state_code
        zipcode = form_data.get('zip')
        email = form_data.get('email')
        password = form_data.get('password')
        confirm_password = form_data.get('confirm_password')
        
        if password != confirm_password:
            return await render_template('register.html', error="Passwords do not match", states=await common_db.get_all_states())
        
        salt, hash = Auth.hash_password(password)
        
        user = User(
            USERNAME=username,
            FIRSTNAME=firstname,
            LASTNAME=lastname,
            ADDRESS=address,
            CITY=city,
            STATE=state,
            ZIPCODE=zipcode,
            EMAIL=email,
            ROLE="USER",
            HASH=hash,
            SALT=salt
        )
        
        res, status_code = await user_db.addUser(user)
        if status_code != 200:
            return await render_template('register.html', error=res.json.get("message"), states=await common_db.get_all_states())
        
        logging.info(res)
        
        
    states = await common_db.get_all_states()
    
    return await render_template('register.html', states=states)


@app.route("/admin/view_users", methods=['GET'])
async def view_users():
    """Render the view_users.html template.

    This function handles the GET request to the /view_users route
    and renders the view_users.html template.

    Returns:
        The rendered HTML template.
    """
    
    users = await user_db.getAllUsers()
    return await render_template('admin_view_users.html', users=users)

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

@app.route("/hotel_detail/<int:hotel_id>", methods=['GET'])
async def hotel_details(hotel_id):
    """Render the hotel details page."""
    hotel = await hotels_db.getHotelById(hotel_id)
    if not hotel:
        return jsonify({"message": "Hotel not found"}), 404
    return await render_template('hotel_details.html', hotel=hotel)

@app.route("/hotel/book/<int:hotel_id>", methods=['GET'])
async def book_hotel(hotel_id):
    selected_hotel = await hotels_db.getHotelById(hotel_id)
    rooms = await rooms_db.GetAllRooms()
    if not selected_hotel:
        return jsonify({"message": "Hotel not found"}), 404
    return await render_template('book_hotel.html', hotel=selected_hotel, rooms=rooms)

@app.route("/checkout", methods=['GET'])
async def checkout():
    hotel_name = request.args.get('hotel_name')
    num_of_rooms = int(request.args.get('num_of_rooms'))
    room_type = request.args.get('room_type')
    price_per_night = int(request.args.get('price_per_night'))
    total_nights = int(request.args.get('total_nights'))
    total_price = int(request.args.get('total_price'))
    checkin_date = request.args.get('checkin_date')
    checkout_date = request.args.get('checkout_date')
    
    return await render_template('checkout.html', hotel_name=hotel_name, num_of_rooms=num_of_rooms, room_type=room_type, price_per_night=price_per_night, total_nights=total_nights, total_price=total_price, checkin_date=checkin_date, checkout_date=checkout_date)

@app.route("/confirmation", methods=['GET'])
async def confirmation():
    booking_id = request.args.get("booking_id")
    if not booking_id:
        return jsonify({"message": "Booking ID is required"}), 400
    
    return await render_template('confirmation.html', booking_id=booking_id)