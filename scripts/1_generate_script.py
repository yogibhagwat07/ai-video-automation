import google.generativeai as genai
import os
import time

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_video_script(topic, retries=3):
    # Using the confirmed model identifier from your diagnostic list
    model_name = "models/gemini-2.0-flash"
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    मुझे YouTube Shorts के लिए एक वायरल AI वीडियो स्क्रिप्ट चाहिए।
    Topic: {topic}
    """

    for i in range(retries):
        try:
            print(f"प्रयास {i+1}: {model_name} के साथ स्क्रिप्ट बन रही है...")
            response = model.generate_content(prompt)
            os.makedirs("output/scripts", exist_ok=True)
            output_path = "output/scripts/latest_script.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"✅ स्क्रिप्ट तैयार!")
            return
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Quota full! 30 सेकंड इंतज़ार...")
                time.sleep(30)
            else:
                print(f"❌ Error: {e}")
                break

if __name__ == "__main__":
    generate_video_script("अंतरिक्ष के 3 डरावने रहस्य")
