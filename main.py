import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import base64
from io import BytesIO
from PIL import Image

def generate_image_from_prompt(prompt):
    # Initialize
    openai = OpenAI()
    MODEL = 'gpt-4o-mini'
    
    # Call OpenAI API to generate an image based on the user's prompt
    image_response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1,
        response_format="b64_json",
    )
    
    # Extract the base64 encoded image
    image_base64 = image_response.data[0].b64_json
    
    # Decode the image data
    image_data = base64.b64decode(image_base64)
    
    #Example using the function:
    #image = generate_image_from_prompt("An image representing a vacation in Paris, showing tourist spots and everything unique about Paris, in a vibrant pop-art style")
    #image.show()

    # Return the image as a PIL object
    return Image.open(BytesIO(image_data))



def main():
    print("Hello from image-generator!")


    load_dotenv(override=True)
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
    else:
        print("OpenAI API Key not set")

    # Define the Gradio interface
    demo = gr.Interface(
        fn=generate_image_from_prompt,
        inputs=gr.Textbox(
            label="Enter your prompt",
            placeholder="Describe the image you want (e.g., A futuristic city skyline at sunset)...",
            lines=2
        ),
        outputs=gr.Image(type="pil", label="Generated Image"),
        title="🎨 AI Image Generator",
        description="Enter a creative prompt and generate an image using DALL·E 3."
    )

    # Launch the interface
    demo.launch()


if __name__ == "__main__":
    main()
