import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io
import openai
from tempfile import NamedTemporaryFile

def record_audio(duration=5, sample_rate=44100):
    """Record audio from microphone"""
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1,
                      dtype=np.int16)
    st.info("Recording...")
    sd.wait()
    st.success("Recording complete!")
    return recording, sample_rate

def save_audio(recording, sample_rate):
    """Save the recording to a temporary WAV file"""
    with NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        wav.write(temp_audio.name, sample_rate, recording)
        return temp_audio.name

def transcribe_audio(audio_file_path, api_key):
    """Transcribe audio using OpenAI's API"""
    client = openai.OpenAI(api_key=api_key)
    
    with open(audio_file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def main():
    st.title("Voice Input Demo")
    
    # Create a text input field
    text_input = st.text_input("Enter text or use voice input:", key="text_input")
    
    # Add OpenAI API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    
    # Add a button to trigger voice recording
    if st.button("🎤 Record Voice"):
        if not api_key:
            st.error("Please enter your OpenAI API key first.")
            return
        
        try:
            # Record audio
            recording, sample_rate = record_audio()
            
            # Save audio to temporary file
            audio_file_path = save_audio(recording, sample_rate)
            
            # Transcribe audio
            transcribed_text = transcribe_audio(audio_file_path, api_key)
            
            # Update text input with transcribed text
            st.session_state.text_input = transcribed_text
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
