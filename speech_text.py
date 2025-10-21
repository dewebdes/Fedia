import sounddevice as sd
import queue
import vosk
import json

model_path = r"C:\2025\meet-class\vosk-model-small-fa-0.4\vosk-model-small-fa-0.4"
model = vosk.Model(model_path)

output_file = "transcript.txt"
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

with open(output_file, "a", encoding="utf-8") as f:
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        print("🎧 Listening...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()
                if text:
                    print("📝", text)
                    f.write(text + "\n")
                    f.flush()
            else:
                partial = json.loads(rec.PartialResult())
                partial_text = partial.get("partial", "").strip()
                if partial_text:
                    print("🔄", partial_text)
