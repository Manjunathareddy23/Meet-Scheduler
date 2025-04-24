import streamlit as st
import datetime
import random
import string
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
import os

# Define your WhatsApp groups here (by name!)
whatsapp_groups = {
    "Team Alpha": "Team Alpha",
    "Project Beta": "Project Beta",
    "Dev Group": "Dev Group"
}

def generate_meet_link():
    room_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"https://meet.google.com/{room_id}"

def send_whatsapp_group_message(group_name, message):
    # Setup Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=chrome-data")  # Persistent session
    driver = webdriver.Chrome(options=options)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    st.info("Scan the QR code on first run. Waiting 15 seconds...")
    time.sleep(15)  # Give time to scan QR

    try:
        # Search group
        search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        search_box.click()
        search_box.send_keys(group_name)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

        # Type and send message
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        message_box.click()
        message_box.send_keys(message)
        pyautogui.press("enter")

        time.sleep(3)
        driver.quit()
    except Exception as e:
        st.error(f"Error sending message: {e}")
        driver.quit()

def schedule_group_message(group_name, message, scheduled_time):
    def send():
        time_diff = (scheduled_time - datetime.datetime.now()).total_seconds()
        if time_diff > 0:
            time.sleep(time_diff)
        send_whatsapp_group_message(group_name, message)

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

        # Adjust for tomorrow
        if scheduled_time < now:
            scheduled_time += datetime.timedelta(days=1)

        group_name = whatsapp_groups[selected_group]
        message = f"📢 Reminder: Your meeting starts in 15 minutes.\nJoin here: {meet_link}"

        schedule_group_message(group_name, message, scheduled_time)
        st.success(f"Meet link generated and scheduled: {meet_link}")
        st.info(f"Message will be sent to *{group_name}* at {scheduled_time.strftime('%H:%M')}")
