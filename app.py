import streamlit as st
from datetime import datetime, timedelta
import random
import string
from twilio.rest import Client

# Twilio Configuration
TWILIO_ACCOUNT_SID = ACf09087dcf27809d5dbf62a90df9c1978  # Replace with your Twilio account SID
TWILIO_AUTH_TOKEN = 30759ef0f8b22335214b41b7ee60b57b  # Replace with your Twilio Auth Token
WHATSAPP_SENDER = "whatsapp:+91 6300138360"  # Twilio's WhatsApp sandbox number

# Function to generate a dummy Google Meet link
def generate_meet_link():
    return f"https://meet.google.com/{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"

# Function to send WhatsApp message using Twilio
def send_whatsapp_message(receiver, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=WHATSAPP_SENDER,
            to=f"whatsapp:{receiver}",
            body=message
        )
        return True
    except Exception as e:
        st.error(f"Failed to send WhatsApp message: {e}")
        return False

# Streamlit App
st.title("Google Meet Scheduler with WhatsApp Integration")

# Input for meeting time
start_time = st.time_input("Select Meeting Start Time")
end_time = st.time_input("Select Meeting End Time")

# Dropdown for selecting WhatsApp group link
whatsapp_groups = {
    "Team A": "+916300138360",
    "Team B": "+918464001960",
    "Team C": "+919121058917"
}
group_name = st.selectbox("Select WhatsApp Group", list(whatsapp_groups.keys()))

# Submit button
if st.button("Submit"):
    try:
        # Parse meeting start and end times
        today = datetime.now().date()
        meeting_start = datetime.combine(today, start_time)
        meeting_end = datetime.combine(today, end_time)

        if meeting_start >= meeting_end:
            st.error("End time must be after start time.")
        else:
            # Generate the Google Meet link
            meet_link = generate_meet_link()

            # Calculate the message send time (15 minutes before the meeting)
            send_time = meeting_start - timedelta(minutes=15)
            now = datetime.now()
            if send_time <= now:
                st.error("The meeting time must be at least 15 minutes from now!")
            else:
                # Send the WhatsApp message
                group_link = whatsapp_groups[group_name]
                message = f"Google Meet link for the meeting: {meet_link}"
                success = send_whatsapp_message(group_link, message)

                if success:
                    st.success(f"Google Meet link sent to {group_name} successfully!")
                    st.write(f"Google Meet Link: {meet_link}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
