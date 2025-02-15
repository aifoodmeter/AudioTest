import streamlit as st
import os
import numpy as np
import tempfile
import time
from datetime import datetime

# Install required packages if they're not already installed
try:
    import streamlit_webrtc
    import av
    import pydub
except ImportError:
    os.system("pip install streamlit-webrtc av pydub")
    import streamlit_webrtc
    import av
    import pydub

st.title("Audio Recorder App")
st.write("Click the 'START' button below to record audio directly in your browser")

# Create a directory to store audio files
TEMP_DIR = tempfile.gettempdir()
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to process audio frames
def process_audio(frame):
    return frame

# Set up the WebRTC component for audio recording
webrtc_ctx = streamlit_webrtc.webrtc_streamer(
    key="audio-recorder",
    mode=streamlit_webrtc.WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"audio": True, "video": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
)

status_indicator = st.empty()
audio_output = st.empty()

if webrtc_ctx.state.playing:
    status_indicator.info("Recording... Click 'STOP' when you're done.")
else:
    status_indicator.info("Click 'START' to begin recording")

if webrtc_ctx.audio_receiver:
    # Get audio frames
    audio_frames = []
    for audio_frame in webrtc_ctx.audio_receiver.get_frames(timeout=1):
        audio_frames.append(audio_frame)
    
    if len(audio_frames) > 0:
        # Process the received audio frames
        status_indicator.success("Audio captured successfully!")
        
        # Convert the audio frames to a WAV file
        sound_chunk = pydub.AudioSegment.empty()
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = f"{TEMP_DIR}/recorded_audio_{timestamp}.wav"
        sound_chunk.export(audio_file, format="wav")
        
        # Display the audio player
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_output.audio(audio_bytes, format="audio/wav")
        
        st.success(f"Audio saved to: {audio_file}")
        st.write(f"Audio duration: {len(sound_chunk)/1000:.2f} seconds")

st.markdown("---")
st.markdown("""
**Notes:**
1. If you don't see the START button, try refreshing the page.
2. For first-time use, you'll need to give your browser permission to access the microphone.
3. The recording will be processed when you click STOP.
""")