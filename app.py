import streamlit as st
import datetime
import pywhatkit
import random
import string
import time
import threading

# Define your WhatsApp groups here
whatsapp_groups = {
    "Team Alpha": "+919876543210",
    "Project Beta": "+918765432109",
    "Dev Group": "+911234567890"
}

def generate_meet_link():
    room_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"https://meet.google.com/{room_id}"

def schedule_whatsapp_message(phone_no, message, scheduled_time):
    def send():
        time_diff = (scheduled_time - datetime.datetime.now()).total_seconds()
        if time_diff > 0:
            time.sleep(time_diff)
        pywhatkit.sendwhatmsg_instantly(phone_no, message, wait_time=10, tab_close=True)

    threading.Thread(target=send).start()

# UI
st.set_page_config(page_title="Meeting Scheduler", layout="centered")

st.markdown("<h1 class='text-3xl font-bold text-center text-indigo-600'>Meeting Scheduler 📅</h1>", unsafe_allow_html=True)

start_time = st.time_input("Start Time")
end_time = st.time_input("End Time")
selected_group = st.selectbox("Select WhatsApp Group", list(whatsapp_groups.keys()))

if st.button("Generate & Schedule"):
    if start_time >= end_time:
        st.error("End time must be after start time.")
    else:
        meet_link = generate_meet_link()
        scheduled_time = (datetime.datetime.combine(datetime.date.today(), start_time) - datetime.timedelta(minutes=15))
        now = datetime.datetime.now()

        # Adjust if the meeting is set for tomorrow
        if scheduled_time < now:
            scheduled_time += datetime.timedelta(days=1)

        phone_number = whatsapp_groups[selected_group]
        message = f"📢 Reminder: Your meeting starts in 15 minutes.\nJoin here: {meet_link}"

        schedule_whatsapp_message(phone_number, message, scheduled_time)
        st.success(f"Google Meet link generated and scheduled: {meet_link}")
        st.info(f"Message will be sent to *{selected_group}* at {scheduled_time.strftime('%H:%M')}")

