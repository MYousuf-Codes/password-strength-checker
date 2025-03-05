import streamlit as st
import re
import random
import string

# Common weak passwords list
COMMON_PASSWORDS = {"123456", "password", "123456789", "qwerty", "abc123", "password1", "letmein", "12345"}

# Function to analyze password
def analyze_password(password):
    contains_upper = bool(re.search(r"[A-Z]", password))
    contains_lower = bool(re.search(r"[a-z]", password))
    contains_digit = bool(re.search(r"\d", password))
    contains_special = bool(re.search(r"[!@#$%^&*]", password))
    return contains_upper, contains_lower, contains_digit, contains_special

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []
    
    if password.lower() in COMMON_PASSWORDS:
        return "⚠️ Extremely Weak: Common password detected. Choose something unique.", 0, "gray", "❌ Avoid common passwords!"
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Make your password at least 8 characters long.")
        
    # Character Type Checks
    contains_upper, contains_lower, contains_digit, contains_special = analyze_password(password)
    
    if contains_upper and contains_lower:
        score += 1
    else:
        feedback.append("❌ Mix uppercase and lowercase letters.")
    
    if contains_digit:
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    if contains_special:
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Ratings
    if score == 4:
        return "✅ Strong Password! 🚀", 100, "#2E8B57", "🌟 Fantastic! This password makes you as secure as Fort Knox."
    elif score == 3:
        return "⚠️ Moderate Password - Almost there!", 70, "#FFD700", "🟡 Good job, but consider adding more complexity."
    else:
        return "❌ Weak Password - Needs improvement.", 30, "#FFA500", "🟠 Too simple! Follow the suggestions to strengthen it."

# Function to generate a strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

# Styling
st.markdown("""
    <style>
        body { background-color: #f7f7f7; }
        .reportview-container { background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333366; text-align: center; }
        .password-feedback { font-size: 16px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🔐 Password Strength Meter")

# User Input
password = st.text_input("Enter your password:", type="password")

# Button to trigger the password check
if st.button("Check Password"):
    if not password:
        st.warning("Please enter a password!")
    else:
        strength_message, strength_score, strength_color, strength_review = check_password_strength(password)
        
        # Strength Message
        st.markdown(f"<p style='color:{strength_color}; font-size:18px;'>{strength_message}</p>", unsafe_allow_html=True)
        
        # Progress Bar
        st.progress(strength_score / 100)
        
        # Review Message
        st.markdown(f"<p class='password-feedback' style='color: {strength_color};'>{strength_review}</p>", unsafe_allow_html=True)
        
        # Password Analysis
        contains_upper, contains_lower, contains_digit, contains_special = analyze_password(password)
        st.write("🔍 **Password Contains:**")
        st.write("✅ Uppercase Letters" if contains_upper else "❌ No Uppercase Letters")
        st.write("✅ Lowercase Letters" if contains_lower else "❌ No Lowercase Letters")
        st.write("✅ Numbers" if contains_digit else "❌ No Numbers")
        st.write("✅ Special Characters (!@#$%^&*)" if contains_special else "❌ No Special Characters")
        
        # Suggest a strong password only if the password is weak or moderate
        if strength_score < 100:
            strong_password = generate_strong_password()
            st.write("💡 **Suggested Strong Password:**")
            st.code(strong_password, language="")
            
            # Copy Button (simulated copy action)
            if st.button("Copy Suggested Password"):
                st.session_state["password_copy"] = strong_password
                st.write("✅ Password copied! (Simulated)")

# Security Tagline
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🔒 Your passwords are never stored. Even if they were, we have no idea who you are! 🔒</p>", unsafe_allow_html=True)
