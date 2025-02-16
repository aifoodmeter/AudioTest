import streamlit as st
from st_audiorec import st_audiorec
import tempfile
import os
from openai import OpenAI

# Set your OpenAI API key
api_key = st.secrets["api_key"]  # Store in Streamlit secrets
# Alternatively: api_key = os.environ.get("OPENAI_API_KEY")

st.title("Audio Recorder with Transcription")

# Record audio
wav_audio_data = st_audiorec()


if wav_audio_data is not None:
    # Display the recorded audio
    st.audio(wav_audio_data, format='audio/wav')
    
    # Create a temporary file to store the audio data
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        tmp_file.write(wav_audio_data)
        tmp_file_path = tmp_file.name
    
    # Transcribe with OpenAI
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            try:
                # Initialize OpenAI client
                client = OpenAI(api_key=api_key)
                
                # Open the temporary file and send to OpenAI
                with open(tmp_file_path, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en",
                        prompt="Please transcribe this audio in English only."
                    )
                
                # Display the transcript
                st.subheader("Transcript")
                st.write(transcript.text)
                
            except Exception as e:
                st.error(f"Error during transcription: {str(e)}")
            finally:
                # Clean up the temporary file
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)