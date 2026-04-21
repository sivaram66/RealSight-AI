import os
import cv2
import base64
from groq import AsyncGroq

# Initialize the async client so it doesn't block our video stream
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def analyze_behavior(frame):
    try:
        # 1. Compress and encode the OpenCV frame to base64
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        # 2. The specific system prompt for retail security
        prompt = "You are a retail security AI. Look at this CCTV frame. Describe the general behavior of the people in one short, clinical sentence. Be extremely brief."
        
        # 3. Fire to LLaMA 3.2 Vision on Groq
        completion = await client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=50
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "System analyzing behavior..."