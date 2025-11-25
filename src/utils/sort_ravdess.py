import os
import shutil

# -------------------------------------------------------
# AUTO-DETECT PROJECT ROOT NO MATTER WHERE SCRIPT IS RUN
# -------------------------------------------------------
THIS_FILE = os.path.abspath(__file__)
UTILS_DIR = os.path.dirname(THIS_FILE)
SRC_DIR = os.path.dirname(UTILS_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)

RAW_FOLDER = os.path.join(PROJECT_ROOT, "data", "ravdess_raw")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "data", "processed")

emotion_map = {
    "01": "neutral",
    "02": "neutral",
    "03": "happy",
    "04": "sad",
    "05": "angry",
}


def sort_ravdess():
    print("🔍 Looking for RAVDESS at:", RAW_FOLDER)

    if not os.path.exists(RAW_FOLDER):
        print("❌ RAVDESS raw folder not found!")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Create emotion dirs
    for emotion in set(emotion_map.values()):
        os.makedirs(os.path.join(OUTPUT_FOLDER, emotion), exist_ok=True)

    print("📁 Sorting RAVDESS files...\n")

    for root, dirs, files in os.walk(RAW_FOLDER):
        for file in files:
            if not file.endswith(".wav"):
                continue

            file_path = os.path.join(root, file)
            parts = file.split("-")
            emotion_code = parts[2]

            if emotion_code not in emotion_map:
                continue

            emotion = emotion_map[emotion_code]
            dest_dir = os.path.join(OUTPUT_FOLDER, emotion)

            shutil.copy(file_path, dest_dir)
            print(f"✔ {file} → {emotion}")

    print("\n🎉 Sorting complete!")
    print("➡ Processed folder:", OUTPUT_FOLDER)


if __name__ == "__main__":
    sort_ravdess()
