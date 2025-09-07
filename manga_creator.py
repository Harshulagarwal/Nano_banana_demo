import streamlit as st
import os
from manga_backend import create_script, create_visual_style, generate, create_story, create_folder_name
from PIL import Image

def load_and_display_images(story_idea):
    # Get the story-specific folder name
    story_folder = create_folder_name(story_idea)
    
    # Check if the folder exists
    if not os.path.exists(story_folder):
        return
        
    # Get all image files in the story-specific directory that start with "STORIES_"
    image_files = [f for f in os.listdir(story_folder) if f.startswith('STORIES_') and f.endswith('.png')]
    
    if image_files:
        st.subheader("Generated Manga Scenes")
        # Sort the files to ensure they're displayed in order
        image_files.sort()
        
        # Create columns for displaying images
        cols = st.columns(2)
        for idx, image_file in enumerate(image_files):
            with cols[idx % 2]:
                image = Image.open(os.path.join(story_folder, image_file))
                st.image(image, caption=f"Scene {idx + 1}", width='stretch')
    
def main():
    st.set_page_config(page_title="Manga Creator", layout="wide")
    
    st.title("🎨 AI Manga Creator")
    st.markdown("""
    Create your own manga story with AI-generated scenes and artwork!
    Just provide your story idea, and let the AI do the magic.
    """)
    
    # Story idea input
    st.subheader("📝 Your Story Idea")
    story_idea = st.text_area(
        "Enter your story idea",
        height=100,
        placeholder="Example: A village chief starting his journey to find a legendary sword..."
    )
    
    # Generate button
    if st.button("🚀 Generate Manga"):
        if story_idea:
            with st.spinner("Creating your manga story..."):
                # Create the story
                st.subheader("📜 Generated Story")
                story = create_story(story_idea)
                st.write(story)
                # Create the script
                st.subheader("📜 Generated Script")
                script = create_script(story)
                st.code(script, language='json')
                
                # Create visual style
                st.subheader("🎨 Visual Style Guide")
                visual_style = create_visual_style(script)
                st.markdown(visual_style)
                
                # Generate images
                with st.spinner("Generating manga scenes... This may take a few minutes..."):
                    generate(script, visual_style, story_idea)
                    st.success("✨ Manga scenes generated successfully!")
                
                # Display generated images
                load_and_display_images(story_idea)
        else:
            st.error("Please enter a story idea first!")
    
    # Display existing images if available
    if not st.button and 'story_idea' in locals():
        load_and_display_images(story_idea)
    
    st.markdown("---")
    st.markdown("""
    ### Tips for better results:
    - Be specific about the setting and time period
    - Include details about main characters
    - Mention the overall tone (action, drama, comedy, etc.)
    - Keep the story idea concise but descriptive
    """)

if __name__ == "__main__":
    main()