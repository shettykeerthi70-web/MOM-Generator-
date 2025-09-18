import google.generativeai as genai
import cv2
import os
from PIL import Image

def extract_text_image(image_path):
    file_bytes = np.asarray(bytearray(image_path.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    #image = cv2.imread('handwritten.jpg')
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  
    image_grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _, image_bw = cv2.threshold(image_grey,150,255,cv2.THRESH_BINARY)

    final_image = Image.fromarray(image_bw)

# configure gen ai model 
    key=os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=key)
    model=genai.GenerativeModel('gemini-2.5-flash-lite')

# lets write prompt for image 
    prompt='''You need to perform OCR on the given image and extract th etext from it. 
              give only the text as output , do not give any other explaination or description.'''

# lets extract and written the text 
    response=model.generate_content([prompt,final_image])
    output_text=response.text
    return(output_text)

import numpy as np