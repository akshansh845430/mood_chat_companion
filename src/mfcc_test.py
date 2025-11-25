from features.mfcc_extractor import extract_mfcc

path = "../data/audio_samples/sample_20251124_224355.wav"  # use any .wav you recorded

# D:\mood_chat_companion\data\audio_samples\sample_20251124_224355.wav

mfcc = extract_mfcc(path)

print("MFCC SHAPE =", None if mfcc is None else mfcc.shape)
