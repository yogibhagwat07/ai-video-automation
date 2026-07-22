import os
import soundfile as sf
from kokoro import KPipeline

def generate_voiceover():
    script_path = "output/scripts/latest_script.txt"
    audio_output_path = "output/audio/voiceover.wav"
    
    # 1. टेक्स्ट पढ़ना
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            text = f.read()
        print("✅ असली स्क्रिप्ट फाइल मिल गई।")
    else:
        text = "नमस्ते! यह एक टेस्ट ऑडियो है, क्योंकि हमारी असली स्क्रिप्ट कल तैयार होगी।"
        print("⚠️ स्क्रिप्ट नहीं मिली। टेस्टिंग के लिए डमी टेक्स्ट का इस्तेमाल कर रहे हैं।")
    
    # 2. Kokoro AI सेटअप
    print("🎙️ Kokoro-82M मॉडल लोड हो रहा है... (पहली बार में थोड़ा समय लग सकता है)")
    try:
        # 'h' कोड हिंदी (Hindi) के लिए है। 
        # (अगर Kokoro के इस वर्ज़न में 'h' सपोर्ट न करे, तो इसे 'a' (American) करके अंग्रेजी में टेस्ट कर सकते हैं)
        pipeline = KPipeline(lang_code='h') 
        
        print("⏳ आवाज़ जनरेट हो रही है...")
        # आवाज़ (Voice) सेट करना। 
        generator = pipeline(
            text, voice='hi_male', # यहाँ आप Kokoro की उपलब्ध आवाज़ों के अनुसार नाम बदल सकते हैं
            speed=1.0, split_pattern=r'\n+'
        )
        
        # 3. ऑडियो फाइल्स को जोड़ना
        audio_chunks = []
        sample_rate = 24000
        for i, (gs, ps, audio) in enumerate(generator):
            audio_chunks.extend(audio)
            
        # 4. फाइल सेव करना
        os.makedirs("output/audio", exist_ok=True)
        sf.write(audio_output_path, audio_chunks, sample_rate)
        print(f"✅ शानदार! वॉइसओवर तैयार है और '{audio_output_path}' में सेव हो गया है।")
        
    except Exception as e:
        print(f"❌ Kokoro एरर: {e}")
        print("ध्यान दें: अगर यह हिंदी (h) सपोर्ट नहीं कर रहा है, तो हम कल इसे ElevenLabs से रिप्लेस कर देंगे!")

if __name__ == "__main__":
    generate_voiceover()
