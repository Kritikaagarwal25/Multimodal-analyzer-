import streamlit as st
import os
from groq import Groq
from PIL import Image
import PyPDF2
import base64
import io
from dotenv import load_dotenv
import datetime
import database

# Initialize SQLite database for chat history
database.init_db()

load_dotenv()

# Model constant
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# System prompt
SYSTEM_PROMPT = """You are a helpful and professional medical assistant. 
Your role is to assist with medical analysis, health inquiries, and understanding medical documents or images.
You must STRICTLY REFUSE to answer any questions that are not related to the medical or health field (e.g., recipes, coding, general trivia, entertainment, etc.).
If a user asks a non-medical question, politely decline and state that you are a specialized medical AI analyzer designed to help with health-related queries only.
"""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# ... (rest of the variable initialization remains the same) ...

# ..
st.set_page_config(
    page_title="Multimodal AI Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_html(file_name):
    with open(file_name) as f:
        return f.read()

try:
    load_css("assets/style.css")
except FileNotFoundError:
    st.warning("assets/style.css not found.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "content_processed" not in st.session_state:
    st.session_state.content_processed = None
if "content_type" not in st.session_state:
    st.session_state.content_type = None
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in environment variables.")
    st.stop()

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def encode_image(image):
    buffered = io.BytesIO()
    image.convert('RGB').save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def base64_to_image(base64_str):
    try:
        img_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(img_data))
    except Exception:
        return None

def reset_chat():
    st.session_state.chat_history = []
    st.session_state.content_processed = None
    st.session_state.content_type = None
    st.session_state.current_session_id = database.create_session()
    st.session_state.uploader_key += 1

# Ensure a session exists on start
if st.session_state.current_session_id is None:
    st.session_state.current_session_id = database.create_session()

with st.sidebar:
    st.title("History")
    
    if st.button("New Chat", on_click=reset_chat, use_container_width=True):
        pass
    st.divider()

    sessions = database.get_all_sessions()
    
    if sessions:
        st.caption("Previous Chats")
        for session in sessions:
            # Determine if this session is currently active for styling (optional, streamlit buttons don't support much custom styling easily without CSS hacks)
            # Use unique key for each button
            if st.button(session["title"], key=f"session_{session['id']}", use_container_width=True):
                st.session_state.current_session_id = session["id"]
                st.session_state.chat_history = database.get_chat_history(session["id"])
                st.session_state.content_processed = None
                st.rerun()
    else:
        st.write("No history.")

messages_container = st.container(height=500)

with messages_container:
    welcome_placeholder = st.empty()
    if not st.session_state.chat_history:
        try:
            welcome_html = load_html("assets/welcome.html")
            welcome_placeholder.markdown(welcome_html, unsafe_allow_html=True)
        except FileNotFoundError:
             welcome_placeholder.markdown("<h1 class='welcome-message'>What can I help with?</h1>", unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        role = message["role"]
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            if "image" in message and message["image"]:
                 img = base64_to_image(message["image"])
                 if img:
                     st.image(img, width=250) 
            st.markdown(message["content"])

col_upload, col_input = st.columns([0.1, 0.9])

with col_upload:
    with st.popover("➕", use_container_width=True):
        st.caption("Attach File")
        uploaded_file = st.file_uploader(
            "Upload", 
            type=["pdf", "png", "jpg", "jpeg"], 
            key=f"uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed"
        )

def is_medical_content(content, content_type):
    client = Groq(api_key=api_key)
    
    if content_type == 'image':
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is this image related to the medical field (e.g., X-ray, MRI, medical report, prescription, symptoms, anatomy)? Answer strictly with 'YES' or 'NO'."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{content}"}}
                ]
            }
        ]
    elif content_type == 'pdf':
        # Send first 2000 chars for validation
        sample_text = content[:2000]
        messages = [
             {
                "role": "user",
                "content": f"Is this text from a medical document? Answer strictly with 'YES' or 'NO'.\n\nText:\n{sample_text}"
            }
        ]
    else:
        return False

    try:
        completion = client.chat.completions.create(
            messages=messages,
            model=MODEL_NAME,
            temperature=0,
            max_tokens=10
        )
        response = completion.choices[0].message.content.strip().upper()
        return "YES" in response
    except Exception as e:
        st.error(f"Validation Error: {e}")
        return False

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    try:
        if file_type == 'pdf':
            if st.session_state.content_processed is None or st.session_state.content_type != 'pdf':
                with st.spinner("Processing PDF..."):
                    text = extract_text_from_pdf(uploaded_file)
                    
                    with st.spinner("Validating content..."):
                        if is_medical_content(text, 'pdf'):
                            st.session_state.content_processed = text
                            st.session_state.content_type = 'pdf'
                            st.toast("PDF Processed!", icon="📄")
                        else:
                            st.error("⚠️ The uploaded file does not appear to be medical-related. Please upload medical reports or images only.")
                            st.session_state.content_processed = None
                            st.session_state.content_type = None
                            
        elif file_type in ['png', 'jpg', 'jpeg']:
            if st.session_state.content_processed is None or st.session_state.content_type != 'image':
                img = Image.open(uploaded_file)
                encoded_img = encode_image(img)
                
                with st.spinner("Validating content..."):
                    if is_medical_content(encoded_img, 'image'):
                       st.session_state.content_processed = encoded_img
                       st.session_state.content_type = 'image'
                       st.toast("Image Processed!", icon="🖼️")
                    else:
                        st.error("⚠️ The uploaded file does not appear to be medical-related. Please upload medical reports or images only.")
                        st.session_state.content_processed = None
                        st.session_state.content_type = None

    except Exception as e:
        st.error(f"Error processing file: {e}")

with col_input:
    prompt = st.chat_input("Ask something...", key="chat_input")

if prompt:
    welcome_placeholder.empty()

    with messages_container:
        with st.chat_message("user", avatar="👤"):
            if st.session_state.content_type == 'image' and st.session_state.content_processed:
                 img = base64_to_image(st.session_state.content_processed)
                 if img:
                     st.image(img, width=250)
            st.markdown(prompt)
    
    user_msg = {"role": "user", "content": prompt}
    encoded_image = None
    if st.session_state.content_type == 'image' and st.session_state.content_processed:
        user_msg["image"] = st.session_state.content_processed
        encoded_image = st.session_state.content_processed
    
    st.session_state.chat_history.append(user_msg)
    
    # Save user message
    database.save_message(
        st.session_state.current_session_id, 
        "user", 
        prompt, 
        encoded_image
    )
    
    client = Groq(api_key=api_key)
    
    with messages_container:
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            full_response = ""
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            context = st.session_state.content_processed
            
            if st.session_state.content_type == 'pdf' and context:
                messages.append({
                    "role": "system", 
                    "content": f"Use this document context to answer:\n\n{context}"
                })
            elif st.session_state.content_type == 'image' and context:
                pass 

            for msg in st.session_state.chat_history[:-1]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            if st.session_state.content_type == 'image' and context:
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{context}"}}
                    ]
                })
            else:
                messages.append({"role": "user", "content": prompt})

            try:
                completion = client.chat.completions.create(
                    messages=messages,
                    model=MODEL_NAME,
                    stream=True,
                    temperature=0.7
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                
                # Save assistant response
                database.save_message(
                    st.session_state.current_session_id,
                    "assistant",
                    full_response
                )
                    
            except Exception as e:
                st.error(f"API Error: {e}")
