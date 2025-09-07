import base64
import mimetypes
import os
from google import genai
from google.genai import types
from ratelimit import limits
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_client():
    """
    Initialize and return a Google Generative AI client using API key from environment variables.
    
    Returns:
        genai.Client: Configured Google Generative AI client
    """
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    client = genai.Client(api_key=api_key)
    return client

def create_folder_name(story_idea: str) -> str:
    """
    Create a standardized folder name from a story idea.
    
    Args:
        story_idea (str): The original story idea text
        
    Returns:
        str: A cleaned folder name using first 10 alphanumeric characters
    """
    folder_name = ''.join(e for e in story_idea[:10] if e.isalnum()).lower()
    return folder_name

def save_binary_file(file_name: str, data: bytes, story_folder: str) -> None:
    """
    Save binary data to a file in a specific story folder.
    
    Args:
        file_name (str): Name of the file to create
        data (bytes): Binary data to save
        story_folder (str): Name of the folder to save the file in
        
    Returns:
        None
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(story_folder):
        os.makedirs(story_folder)
    
    # Save file in the story folder
    file_path = os.path.join(story_folder, file_name)
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_path}")
    except IOError as e:
        print(f"Error saving file: {e}")

def create_story(story_idea: str) -> str:
    """
    Generate a detailed story outline from a basic story idea.
    
    Args:
        story_idea (str): The initial story concept
        
    Returns:
        str: Generated story outline
        
    Note:
        The story will be structured for manga format with:
        - Multiple chapters
        - At least 4 scenes
        - Character arcs and plot points
        - Limited to 1000 words
    """
    client = get_client()

    full_prompt = (
        f"Create a detailed story based on the following idea: {story_idea}. "
        f"The outline should include key plot points, character arcs, and major themes. Be creative and add more characters and dialogues"
        f"Make it suitable for a manga format with clear scene descriptions. Add at least 4 scenes."
        f"Add multiple chapters with different scenes."
        f"story should not be more than 1000 words."
    )

    generate_content_config = types.GenerateContentConfig(temperature=1)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[full_prompt],
            config=generate_content_config
        )
        return response.text
    except Exception as e:
        print(f"Error generating story: {e}")
        return ""

def create_script(story):
    client = get_client()
#     example = """{
#   "chapter": 1,
#   "title": "Blood Moon Awakening",
#   "scenes": [
#     {
#       "scene_id": 1,
#       "setting": "Snowy mountain village, late evening",
#       "narration": [
#         "The mountain village lived in quiet isolation, wrapped in snow and silence.",
#         "Yet whispers spread of creatures that stalked under the red moon."
#       ],
#       "characters": ["Kaito (protagonist)", "Mother", "Younger Sister Hana"],
#       "dialogue": [
#         { "character": "Mother", "line": "Kaito, don’t stay too long in the forest. The snow grows heavier tonight." },
#         { "character": "Kaito", "line": "I’ll return before moonrise. I promised Hana I’d bring her firewood." },
#         { "character": "Hana", "line": "Big brother, be careful… the villagers whisper of shadows in the woods." }
#       ]
#     },
#     {
#       "scene_id": 2,
#       "setting": "Forest path, under a blood-red moon",
#       "narration": [
#         "The forest was still. Too still.",
#         "Every branch creaked like bone, and the snow carried the scent of iron."
#       ],
#       "characters": ["Kaito", "Unknown Demon"],
#       "dialogue": [
#         { "character": "Kaito", "line": "Strange… the woods are too silent tonight." },
#         { "character": "Unknown Demon", "line": "Heh… your scent is strong, boy. Fresh blood under the red moon." },
#         { "character": "Kaito", "line": "Who’s there?! Show yourself!" }
#       ]
#     }
#   ] 
# }
# """

    full_prompt = (
        f"Create a detailed manga script based on the following story: {story}. "
        f"The script should include character names, settings, dialogues, and narration. Be creative and add dialogues."
        f"Make it suitable for a manga format with clear scene descriptions. Create at least 4 scenes and maximum upto 8 scenes."
        f"Create maximum of 3 chapters."
        f"Write a json format script with dialogue of all the characters"
    )

    generate_content_config = types.GenerateContentConfig( temperature=1)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[full_prompt],
        config=generate_content_config,

    )
    #script
    return response.text

def create_visual_style(script: str) -> str:
    """
    Generate a detailed visual style guide based on the manga script.
    
    Args:
        script (str): The complete manga script in JSON format
        
    Returns:
        str: Visual style guide including color schemes, designs, and compositions
        
    Note:
        Style guide includes:
        - Color schemes
        - Character designs
        - Panel compositions
        - Text styling
        Each section is limited to 200 words for clarity
    """
    client = get_client()

    full_prompt = (
        f"Given the script for a manga, create a detailed visual style guide for the manga artist to follow. Limit to 200 words for each section."
        f"Include specifics only on color schemes, character designs, panel compositions, and text styling. The manga script is as follows: {script}"
        f"""Example: 
            Use vibrant colors with dramatic contrasts
            - Incorporate dynamic lighting effects, especially for the blood moon scenes
            - Add atmospheric effects like snow particles and mist
            - Use dramatic shadows and highlights to enhance mood
            - Include detailed backgrounds that match the setting"""
    )

    generate_content_config = types.GenerateContentConfig(temperature=1)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[full_prompt],
            config=generate_content_config
        )
        return response.text
    except Exception as e:
        print(f"Error generating visual style: {e}")
        return ""

def create_characterd_design(script):
    client = get_client()
    example = """
    - Kaito: A determined teenage protagonist with traditional Japanese clothing
   - Mother: A gentle but strong-looking woman in winter attire
   - Hana: A young girl with innocent features
   - Demon: Dark, imposing figure with glowing red eyes
   - Demon Slayer: Battle-hardened warrior with distinctive armor"""
    
    full_prompt = (
        f"Given the script for a manga, create detailed character designs for each character. "
        f"Include physical descriptions, clothing styles, and any unique features that will help the artist visualize them. The manga script is as follows: {script}"
        f"Example: {example}"
        """Output format should be like according to the script: """
    )
    
    generate_content_config = types.GenerateContentConfig( temperature=1)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[full_prompt],
        config=generate_content_config,

    )
    #character design
    return response.text

def generate(script: str, visual_style: str, story_idea: str) -> None:
    """
    Generate manga-style images based on the script and visual style guide.
    
    Args:
        script (str): The complete manga script in JSON format
        visual_style (str): The visual style guide
        story_idea (str): The original story idea for folder naming
        
    Returns:
        None
        
    Note:
        - Creates 4 images per chapter
        - Images are saved in a story-specific folder
        - Each image represents a distinct scene
        - Includes English dialogue integration
    """
    client = get_client()
    story_folder = create_folder_name(story_idea)
    
    model = "gemini-2.5-flash-image-preview"
    contents = [
        types.Content(
            role = "model",
            parts=[
                types.Part.from_text(text=""" You are a manga creator AI. Create 4 manga-style images for each chapter based on the user's script and visual style guide. Dialogues should strictly be in Enlish and clearly reasdable. """)]
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f""" 
Create manga-style images based on the following for each chapter and scene in the manga script. Each image should represent a distinct scene from the manga script.
Ensure the images capture the mood, setting, and character emotions as described in the script Please follow these specific style guidelines:

Visual Style and Character Design: {visual_style}

                                     
The manga script is as follows: 
      {script}   

Create multiple images for every chapter.

 """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
        ],
                temperature=1,
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"STORIES_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer, story_folder)
        else:
            print(chunk.text)

if __name__ == "__main__":
    story_idea = "A village chief starting his journey to find a legendary sword to protect his people from an impending invasion, facing numerous trials and forging unexpected alliances along the way."
    story = create_story(story_idea)
    script = create_script(story)
    visual_style = create_visual_style(script)
    # character_design = create_characterd_design(script)
    print(script)
    print(visual_style)
    # print(character_design)
    generate(script, visual_style, story_idea)
