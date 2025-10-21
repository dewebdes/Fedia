import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import torch
import soundfile as sf
import os
import numpy as np

# --------- تنظیمات ----------
language = "en"
speaker = "lj_v2"
device = torch.device("cpu")
TARGET_SR = 16000  # نرخ نهایی ذخیره‌سازی
input_file = "en.txt"
output_folder = "narration_output"
os.makedirs(output_folder, exist_ok=True)
# ----------------------------

print("🔄 در حال بارگذاری مدل Silero TTS...")
model, _ = torch.hub.load(
    repo_or_dir="snakers4/silero-models",
    model="silero_tts",
    language=language,
    speaker=speaker,
)
model.to(device)
print("✅ مدل با موفقیت بارگذاری شد.")

# خواندن متن‌ها
with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]
if not lines:
    print("⚠️ فایل en.txt خالی است.")
    exit()

# حلقه نریشن
for i, line in enumerate(lines, start=1):
    print(f"\n🎙️ خط {i}: {line}")
    try:
        audio = model.apply_tts(texts=[line])
        audio_np = audio[0].cpu().numpy()

        # نرمال‌سازی ساده
        audio_np = audio_np.astype(np.float32)
        if audio_np.size and np.abs(audio_np).max() > 1.0:
            audio_np = audio_np / np.abs(audio_np).max()

        # ذخیره با نرخ صحیح
        output_path = os.path.join(output_folder, f"line_{i}.wav")
        sf.write(output_path, audio_np, TARGET_SR, subtype="PCM_16")
        print(f"💾 ذخیره شد: {output_path}")
        os.system(f'start "" "{output_path}"')

    except Exception as e:
        print(f"❌ خطا در خط {i}:", e)
