import streamlit as st
from datetime import datetime, timedelta
import pywhatkit as kit
import random
import string

# Function to generate a dummy Google Meet link
def generate_meet_link():
    return f"https://meet.google.com/{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"

# Function to schedule the WhatsApp message
def schedule_whatsapp_message(group_link, meeting_link, meeting_time):
    # Calculate the time to send the message (15 minutes before the meeting)
    send_time = meeting_time - timedelta(minutes=15)
    now = datetime.now()
    
    if send_time <= now:
        st.error("The meeting time must be at least 15 minutes from now!")
        return False
    
    hours = send_time.hour
    minutes = send_time.minute
    
    # Schedule the message
    try:
        kit.sendwhatmsg_instantly(
            phone_no=group_link,
            message=f"Google Meet link for the meeting: {meeting_link}",
            wait_time=20,  # Time to wait before sending
            tab_close=True
        )
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


# Streamlit App
st.title("Google Meet Scheduler with WhatsApp Integration")

# Input for meeting time
start_time = st.time_input("Select Meeting Start Time")
end_time = st.time_input("Select Meeting End Time")

# Dropdown for selecting WhatsApp group link
whatsapp_groups = {
    "Team A": "+91 6300138360",
    "Team B": "+91 8464001960",
    "Team C": "+91 9121058917"
}
group_name = st.selectbox("Select WhatsApp Group", list(whatsapp_groups.keys()))

# Submit button
if st.button("Submit"):
    try:
        # Parse the selected start time
        today = datetime.now().date()
        meeting_start = datetime.combine(today, start_time)
        meeting_end = datetime.combine(today, end_time)
        
        if meeting_start >= meeting_end:
            st.error("End time must be after start time.")
        else:
            # Generate the Google Meet link
            meet_link = generate_meet_link()
            
            # Send the WhatsApp message
            group_link = whatsapp_groups[group_name]
            success = schedule_whatsapp_message(group_link, meet_link, meeting_start)
            
            if success:
                st.success(f"Google Meet link sent to {group_name} successfully!")
                st.write(f"Google Meet Link: {meet_link}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
