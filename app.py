import streamlit as st
import datetime
import random
import string
import time

# WhatsApp groups dictionary (display name only)
whatsapp_groups = {
    "Team Alpha": "Team Alpha",
    "Project Beta": "Project Beta",
    "Dev Group": "Dev Group"
}

def generate_meet_link():
    room_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"https://meet.google.com/{room_id}"

# App UI
st.set_page_config(page_title="Meeting Scheduler", layout="centered")
st.markdown("<h1 class='text-3xl font-bold text-center text-indigo-600'>Meeting Scheduler 📅</h1>", unsafe_allow_html=True)

start_time = st.time_input("Start Time")
end_time = st.time_input("End Time")
selected_group = st.selectbox("Select WhatsApp Group", list(whatsapp_groups.keys()))

if st.button("Generate Meeting Link"):
    if start_time >= end_time:
        st.error("End time must be after start time.")
    else:
        meet_link = generate_meet_link()
        scheduled_time = datetime.datetime.combine(datetime.date.today(), start_time) - datetime.timedelta(minutes=15)
        now = datetime.datetime.now()

        # If time has passed today, shift to next day
        if scheduled_time < now:
            scheduled_time += datetime.timedelta(days=1)

        message = f"📢 Reminder: Your meeting starts in 15 minutes.\nJoin here: {meet_link}"

        st.success(f"Meet link generated: {meet_link}")
        st.markdown(f"**Copy-paste this message to WhatsApp group:**\n\n```\n{message}\n```")
        st.info(f"⏰ Please send the message to *{selected_group}* at {scheduled_time.strftime('%I:%M %p')} manually.")
