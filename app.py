# # Apply monkey patching first
# import eventlet
# eventlet.monkey_patch()

# # Imported Libraries
# from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from werkzeug.security import check_password_hash, generate_password_hash
# import openai 
# import whisper
# import os
# import uuid
# from pytube import YouTube
# import tempfile
# from flask_cors import CORS
# from openai import OpenAI
# from itsdangerous import URLSafeTimedSerializer
# from flask_mail import Mail, Message
# from flask_socketio import SocketIO, emit
# # import threading




# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)
# bcrypt = Bcrypt(app)
# socketio = SocketIO(app, async_mode='eventlet')

# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Cp%40746437@localhost:6400/Luna_Database" # %40 is @ in URL Encoding
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
# db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = "Chotu_is_Great_and_number_1."

# # API Keys
# os.environ["OPENAI_API_KEY"] = "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"

# # Initialize Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # google STMP server
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'cprakash.work@gmail.com'
# app.config['MAIL_PASSWORD'] = 'mcwt dchg gezs ewzd'

# mail = Mail(app)

# # Serializer for generating a safe token
# s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# # Database Models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.String(101), nullable=False, unique=True)
#     email = db.Column(db.String(1001), nullable=False, unique=True)
#     password = db.Column(db.String(501), nullable=False)
    
#     def __repr__(self):
#         return f"User('{self.id}' ,'{self.fullname}', '{self.email}', '{self.password}')"
    
# class Video(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     video_name = db.Column(db.String(21), nullable=False)
#     video_url = db.Column(db.String(1001))
#     transcription = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f"Video('{self.id}' ,'{self.video_name}', '{self.video_url}', '{self.transcription}')"
    
# # Committing to the database
# with app.app_context():
#     db.create_all()

# # Get Logged in User
# def get_logged_in_user():
#     user_id = session.get("user_id")
#     print(f"User ID from session: {user_id}")
#     if user_id:
#         return User.query.get(user_id)
#     return None

# # Routes
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         fullname = request.form['fullname']
#         email = request.form['email']
#         password = request.form['password']

#         existing_user = User.query.filter_by(email=email).first()

#         if existing_user:
#             flash("Email Already Exists, Please Login!", 'error')
#             return render_template('signup.html')

#         hashed_password = generate_password_hash(password)

#         user = User(fullname=fullname, email=email, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()

#         session['user_id'] = user.id
#         flash("Account created Successfully!", 'success')
#         return redirect(url_for('video_input'))

#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first()

#         if user:
#             if check_password_hash(user.password, password):
#                 session['user_id'] = user.id
#                 flash(f"Welcome back, {user.fullname}!", 'success')
#                 return redirect(url_for('video_input'))
#             else:
#                 flash("Incorrect Password", 'error')
#         else:
#             flash("User not found. Please sign up.", 'error')

#     return render_template('login.html')

# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']
#         user = User.query.filter_by(email=email).first()

#         if user:
#             token = s.dumps(email, salt='reset-password-salt')
#             reset_url = url_for('reset_password_token', token=token, _external=True)
#             msg = Message('Reset Your Password', sender='cprakash.work@gmail.com', recipients=[email])
#             msg.body = f'Click the link to reset your password: {reset_url}'
#             mail.send(msg)
#             flash('Please check your email for a password reset link.', 'info')
#         else:
#             flash('No account with that email exists.', 'warning')

#         return redirect(url_for('forgot_password'))
    
#     return render_template('forgot_password.html')

# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password_token(token):
#     try:
#         email = s.loads(token, salt='reset-password-salt', max_age=3600)
#     except:
#         flash('The reset link is invalid or has expired.', 'error')
#         return redirect(url_for('forgot_password'))

#     if request.method == 'POST':
#         new_password = request.form['new_password']
#         confirm_password = request.form['confirm_password']

#         if new_password != confirm_password:
#             flash('Passwords do not match. Please try again.', 'error')
#             return redirect(url_for('reset_password_token', token=token))

#         user = User.query.filter_by(email=email).first()

#         if user:
#             hashed_password = generate_password_hash(new_password)
#             user.password = hashed_password
#             db.session.commit()
#             flash('Your password has been reset successfully!', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('User not found.', 'error')
#             return redirect(url_for('forgot_password'))

#     return render_template('reset_password.html', token=token)

# @app.route('/')
# def video_input():
#    user = get_logged_in_user()

#    if not user:
#        return redirect(url_for('login'))
   
#    return render_template('video_input.html', user = user)

# def transcribe_audio(audio_file):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file)
#     return result["text"]

# def save_transcription(transcription):
#     filename = f"transcriptions/{uuid.uuid4()}.txt"
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#     with open(filename, "w") as file:
#         file.write(transcription)
#     return filename

# @app.route('/upload-video', methods=['POST'])
# def upload_video():
#     if 'videoFile' in request.files:
#         video_file = request.files['videoFile']
#         temp_path = os.path.join(tempfile.gettempdir(), video_file.filename)
#         video_file.save(temp_path)
#         transcription = transcribe_audio(temp_path)
#         os.remove(temp_path)
#         transcription_filename = save_transcription(transcription)
#         session['transcription_filename'] = transcription_filename
#         return redirect(url_for('ask_ai'))

#     return "No video file provided", 400

# @app.route('/process-url', methods=['GET'])
# def process_url():
#     youtube_url = request.args.get('youtubeUrl')
#     if youtube_url:
#         yt = YouTube(youtube_url)
#         video_stream = yt.streams.filter(only_audio=True).first()
#         temp_path = video_stream.download(output_path=tempfile.gettempdir())
#         transcription = transcribe_audio(temp_path)
#         os.remove(temp_path)
#         transcription_filename = save_transcription(transcription)
#         session['transcription_filename'] = transcription_filename
#         return redirect(url_for('ask_ai'))

#     return "Invalid or no YouTube URL provided", 400

# @app.route('/get-transcription', methods=['GET'])
# def get_transcription():
#     filename = session.get('transcription_filename')
#     if filename and os.path.exists(filename):
#         with open(filename, "r") as file:
#             transcription = file.read()
#         return {'transcription': transcription}
#     return {'transcription': ''}

# @app.route('/ask_ai', methods=['GET', 'POST'])
# def ask_ai():
#     user = get_logged_in_user()
#     if not user:
#         return redirect(url_for('login'))
#     return render_template('ask_ai.html', user=user)

# @socketio.on('ask_ai')
# def handle_ask_ai(data):
#     user_question = data.get('question')
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     client = OpenAI()

#     transcription_filename = session.get('transcription_filename')
#     transcription = ""
#     if transcription_filename and os.path.exists(transcription_filename):
#         with open(transcription_filename, "r") as file:
#             transcription = file.read()

#     try:
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "assistant", "content": transcription}
#         ]

#         if transcription:
#             messages.append({"role": "user", "content": user_question})
#         else:
#             messages = [{"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content": user_question}]

#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )
#         answer = response.choices[0].message.content.strip() if response.choices else "No response"

#         emit('ai_response', {'answer': answer})
#     except Exception as e:
#         emit('ai_response', {'answer': f"An error occurred: {str(e)}"})

# # Run the program
# if __name__ == '__main__':
#     socketio.run(app, debug=True, host="0.0.0.0", port=8080)



import eventlet
eventlet.monkey_patch()

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from flask_caching import Cache
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect
import openai
import whisper
import os
import uuid
import cv2
import re
import json
from pytube import YouTube
import tempfile
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
import yt_dlp as youtube_dl  # Ensure this is updated
from object_detection import ObjectDetector  # Import the ObjectDetector class
import pytesseract  # Import pytesseract for OCR
from flask_migrate import Migrate  # Import Flask-Migrate

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CORS(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
socketio = SocketIO(app, async_mode='eventlet')
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
mail = Mail(app)
cache = Cache(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask-Session
app.config['SESSION_SQLALCHEMY'] = db  # Use the existing SQLAlchemy instance
Session(app)

# Serializer for generating a safe token
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Enforce HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize ObjectDetector
object_detector = ObjectDetector()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(101), nullable=False, unique=False)
    email = db.Column(db.String(1001), nullable=False, unique=True, index=True)
    password = db.Column(db.String(501), nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}' ,'{self.fullname}', '{self.email}', '{self.password}')"

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(255), nullable=False)  # Increased length to 255
    video_url = db.Column(db.String(1001))
    transcription = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Video('{self.id}' ,'{self.video_name}', '{self.video_url}', '{self.transcription}')"

class Frame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    frame_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Frame('{self.id}', '{self.video_id}', '{self.frame_path}', '{self.timestamp}')"

# Committing to the database
with app.app_context():
    db.create_all()

# Get Logged in User
def get_logged_in_user():
    user_id = session.get("user_id")
    print(f"User ID from session: {user_id}")
    if user_id:
        return User.query.get(user_id)
    return None

# Function to extract and save frames from video with timestamps
def extract_and_save_frames(video_path, output_dir, frame_interval=1, video_id=None):
    """
    Extracts and saves frames from a video at specified intervals and reads text using OCR.

    Parameters:
    - video_path: str, path to the input video file
    - output_dir: str, directory to save the extracted frames
    - frame_interval: int, interval in seconds to extract frames
    - video_id: int, ID of the video in the database
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # Get video frame rate
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    success, frame = cap.read()
    count = 0

    while success:
        if count % (frame_rate * frame_interval) == 0:
            timestamp = count / frame_rate
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            frame_filename = os.path.join(output_dir, f"frame_{minutes}m_{seconds}s.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved frame at {minutes} minutes and {seconds} seconds as {frame_filename}")

            # Save frame information to the database
            if video_id:
                new_frame = Frame(video_id=video_id, frame_path=frame_filename, timestamp=timestamp)
                db.session.add(new_frame)
                db.session.commit()

            # Perform OCR on the saved frame
            ocr_text = pytesseract.image_to_string(frame)
            print(f"OCR text at {minutes} minutes and {seconds} seconds: {ocr_text}")

        success, frame = cap.read()
        count += 1

    cap.release()
    print("Frame extraction completed.")

# Routes
@app.route('/signup', methods=['GET', 'POST'])
@csrf.exempt
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email Already Exists, Please Login!", 'error')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)

        user = User(fullname=fullname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash("Account created Successfully!", 'success')
        return redirect(url_for('video_input'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash(f"Welcome back, {user.fullname}!", 'success')
                return redirect(url_for('video_input'))
            else:
                flash("Incorrect Password", 'error')
        else:
            flash("User not found. Please sign up.", 'error')

    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
@csrf.exempt
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = s.dumps(email, salt='reset-password-salt')
            reset_url = url_for('reset_password_token', token=token, _external=True)
            msg = Message('Reset Your Password', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            mail.send(msg)
            flash('Please check your email for a password reset link.', 'info')
        else:
            flash('No account with that email exists.', 'warning')

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
@csrf.exempt
def reset_password_token(token):
    try:
        email = s.loads(token, salt='reset-password-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('reset_password_token', token=token))

        user = User.query.filter_by(email=email).first()

        if user:
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been reset successfully!', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'error')
            return redirect(url_for('forgot_password'))

    return render_template('reset_password.html', token=token)

@app.route('/')
def video_input():
    user = get_logged_in_user()

    if not user:
        return redirect(url_for('login'))

    return render_template('video_input.html', user=user)

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result

def save_transcription(transcription):
    filename = f"transcriptions/{uuid.uuid4()}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        json.dump(transcription, file)
    return filename

def extract_frames(video_path, timestamps):
    frames = {}
    cap = cv2.VideoCapture(video_path)
    for segment in timestamps:
        timestamp = segment['start']
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        success, image = cap.read()
        if success:
            frame_path = f"frames/{uuid.uuid4()}.jpg"
            cv2.imwrite(frame_path, image)
            frames[timestamp] = frame_path
    cap.release()
    return frames

@app.route('/upload-video', methods=['POST'])
@csrf.exempt
def upload_video():
    if 'videoFile' in request.files:
        video_file = request.files['videoFile']
        temp_path = os.path.join(tempfile.gettempdir(), video_file.filename)
        video_file.save(temp_path)

        # Save video information to the database
        new_video = Video(video_name=video_file.filename[:255], transcription="")
        db.session.add(new_video)
        db.session.commit()

        # Extract frames and perform OCR
        output_dir = os.path.join("extracted_frames", os.path.splitext(video_file.filename)[0])
        extract_and_save_frames(temp_path, output_dir, frame_interval=1, video_id=new_video.id)

        transcription = transcribe_audio(temp_path)
        new_video.transcription = transcription.get('text', '')
        db.session.commit()
        transcription_filename = save_transcription(transcription)
        session['transcription_filename'] = transcription_filename

        # Extract frames for the transcription timestamps
        frames = extract_frames(temp_path, transcription['segments'])
        session['frames'] = frames
        os.remove(temp_path)

        return redirect(url_for('ask_ai'))

    return "No video file provided", 400

@app.route('/process-url', methods=['GET'])
@csrf.exempt
def process_url():
    youtube_url = request.args.get('youtubeUrl')
    if youtube_url:
        try:
            yt = YouTube(youtube_url)
            video_stream = yt.streams.filter(only_audio=False).first()
            if video_stream is None:
                available_streams = yt.streams.all()
                logger.info("Available streams: %s", available_streams)
                raise ValueError("No valid video streams found for the provided URL.")
            temp_path = video_stream.download(output_path=tempfile.gettempdir())

            # Save video information to the database
            new_video = Video(video_name=yt.title[:255], transcription="")
            db.session.add(new_video)
            db.session.commit()

            # Extract frames and perform OCR
            output_dir = os.path.join("extracted_frames", yt.title)
            extract_and_save_frames(temp_path, output_dir, frame_interval=1, video_id=new_video.id)

            transcription = transcribe_audio(temp_path)
            new_video.transcription = transcription.get('text', '')
            db.session.commit()
            transcription_filename = save_transcription(transcription)
            session['transcription_filename'] = transcription_filename

            # Extract frames for the transcription timestamps
            frames = extract_frames(temp_path, transcription['segments'])
            session['frames'] = frames
            os.remove(temp_path)

            return redirect(url_for('ask_ai'))
        except Exception as e:
            logger.error("Error processing YouTube URL with pytube: %s", str(e))
            try:
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(tempfile.gettempdir(), '%(id)s.%(ext)s'),
                    'quiet': True,
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(youtube_url, download=True)
                    video_path = ydl.prepare_filename(info_dict)

                    # Save video information to the database
                    new_video = Video(video_name=info_dict['title'][:255], transcription="")
                    db.session.add(new_video)
                    db.session.commit()

                    # Extract frames and perform OCR
                    output_dir = os.path.join("extracted_frames", info_dict['title'])
                    extract_and_save_frames(video_path, output_dir, frame_interval=1, video_id=new_video.id)

                    transcription = transcribe_audio(video_path)
                    new_video.transcription = transcription.get('text', '')
                    db.session.commit()
                    transcription_filename = save_transcription(transcription)
                    session['transcription_filename'] = transcription_filename

                    # Extract frames for the transcription timestamps
                    frames = extract_frames(video_path, transcription['segments'])
                    session['frames'] = frames
                    os.remove(video_path)

                    return redirect(url_for('ask_ai'))
            except Exception as fallback_e:
                logger.error("Error processing YouTube URL with yt-dlp: %s", str(fallback_e))
                return jsonify({"error": f"Failed to process YouTube URL: {str(fallback_e)}"}), 400

    return jsonify({"error": "Invalid or no YouTube URL provided"}), 400

@app.route('/detect-object', methods=['POST'])
@csrf.exempt
def detect_object():
    video_url = request.form.get('video_url')
    target_object = request.form.get('target_object')
    if not video_url or not target_object:
        return jsonify({"error": "Missing video URL or target object"}), 400

    yt = YouTube(video_url)
    video_stream = yt.streams.filter(only_audio=False).first()
    temp_path = video_stream.download(output_path=tempfile.gettempdir())

    results = object_detector.find_object_in_video(temp_path, [target_object])
    os.remove(temp_path)

    if results:
        response = [{"timestamp": timestamp, "label": label} for timestamp, label, frame in results]
        return jsonify(response)
    else:
        return jsonify({"message": "Object not found"}), 404

@app.route('/get-transcription', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_transcription():
    filename = session.get('transcription_filename')
    if filename and os.path.exists(filename):
        with open(filename, "r") as file:
            transcription_data = json.load(file)
            transcription = transcription_data.get("text", "")  # Extract only the plain text
        return {'transcription': transcription}
    return {'transcription': ''}

@app.route('/ask_ai', methods=['GET', 'POST'])
def ask_ai():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('login'))
    return render_template('ask_ai.html', user=user)

@socketio.on('ask_ai')
@csrf.exempt
def handle_ask_ai(data):
    user_question = data.get('question')
    transcription_filename = session.get('transcription_filename')
    transcription = ""
    if transcription_filename and os.path.exists(transcription_filename):
        with open(transcription_filename, "r") as file:
            transcription = json.load(file)

    frames = session.get('frames', {})

    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistant", "content": transcription.get('text', '')}
        ]
        messages.append({"role": "user", "content": user_question})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use GPT-4 for better performance
            messages=messages
        )
        answer = response.choices[0].message.content.strip() if response.choices else "No response"

        # Prepare the response data
        response_data = {'answer': answer}

        # Extract timestamp from user question
        timestamp_match = re.search(r'timestamp\s*(\d+\.?\d*)', user_question.lower())
        if timestamp_match:
            timestamp = float(timestamp_match.group(1))
            frame_path = frames.get(timestamp, None)
            if frame_path:
                response_data['frame_path'] = frame_path
                response_data['timestamp'] = timestamp
        else:
            # Search the transcription segments for the relevant timestamp
            relevant_timestamps = [seg['start'] for seg in transcription['segments'] if user_question.lower() in seg['text'].lower()]
            if relevant_timestamps:
                frame_path = frames.get(relevant_timestamps[0], None)
                if frame_path:
                    response_data['frame_path'] = frame_path
                    response_data['timestamp'] = relevant_timestamps[0]

        emit('ai_response', response_data)

    except Exception as e:
        emit('ai_response', {'answer': f"An error occurred: {str(e)}"})

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# Run the program
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8080)





