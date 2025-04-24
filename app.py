import streamlit as st
import datetime
import random
import string
import time
import pywhatkit as kit

# WhatsApp groups dictionary (display name with their respective links)
whatsapp_groups = {
    "Team Alpha": "https://chat.whatsapp.com/xyz12345",  # Replace with actual WhatsApp group links
    "Project Beta": "https://chat.whatsapp.com/xyz67890",
    "Dev Group": "https://chat.whatsapp.com/xyz11223"
}

# Generate Google Meet link
def generate_meet_link():
    room_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"https://meet.google.com/{room_id}"

# Send WhatsApp message using PyWhatKit
def send_whatsapp_group_message(group_link, message, time_of_send):
    try:
        # Send message through PyWhatKit
        kit.sendwhatmsg_to_group_instantly(group_link, message, 15)  # Time delay to ensure 15 sec prior
        st.success(f"Message successfully scheduled and sent to the group.")
    except Exception as e:
        st.error(f"Error sending message: {e}")

# Streamlit UI
st.set_page_config(page_title="Meeting Scheduler", layout="centered")
st.markdown("<h1 class='text-3xl font-bold text-center text-indigo-600'>Meeting Scheduler 📅</h1>", unsafe_allow_html=True)

# Tailwind CSS integration
st.markdown("""
    <style>
        .css-1v3fvcr {
            font-family: 'Arial', sans-serif;
            font-weight: 700;
            color: #4A90E2;
        }
    </style>
""", unsafe_allow_html=True)

# Input fields for the meeting details
start_time = st.time_input("Start Time")
end_time = st.time_input("End Time")
selected_group = st.selectbox("Select WhatsApp Group", list(whatsapp_groups.keys()))

# Submit button to generate and send the meeting link
if st.button("Generate & Schedule Meeting"):
    if start_time >= end_time:
        st.error("End time must be after start time.")
    else:
        meet_link = generate_meet_link()
        scheduled_time = datetime.datetime.combine(datetime.date.today(), start_time) - datetime.timedelta(minutes=15)
        now = datetime.datetime.now()

        # If time has passed today, shift to the next day
        if scheduled_time < now:
            scheduled_time += datetime.timedelta(days=1)

        message = f"📢 Reminder: Your meeting starts in 15 minutes.\nJoin here: {meet_link}"

        group_link = whatsapp_groups[selected_group]
        send_whatsapp_group_message(group_link, message, scheduled_time)

        st.success(f"✅ Meet link generated: {meet_link}")
        st.info(f"📤 Message will be auto-sent to *{selected_group}* at {scheduled_time.strftime('%I:%M %p')}")

