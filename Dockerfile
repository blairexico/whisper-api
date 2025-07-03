# Dockerfile: Whisper Streaming Transcriber (for RunPod)
FROM ghcr.io/ggerganov/whisper.cpp:cuda


# Copy your app code
WORKDIR /app
COPY . /app

# Install server deps
RUN pip install fastapi uvicorn websockets pydub

# Expose port
EXPOSE 7860

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]

