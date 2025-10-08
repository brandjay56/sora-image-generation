# 🎬 Sora Video Generator

A beautiful and intuitive Python application for generating videos using OpenAI's Sora models. Choose between Sora 2 Pro or Sora 2 and watch as AI creates stunning videos from your text descriptions!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🤖 **Multiple Sora Models** - Choose between Sora 2 Pro or Sora 2
- 🖼️ **Image-to-Video & Video-to-Video** - Upload images or videos as input references to guide generation
- 🎨 **Modern and Responsive UI** - Built with Streamlit for a clean interface that works on desktop and mobile
- 🎥 **Multiple Resolutions** - Support for HD and Full HD in both landscape (16:9) and portrait (9:16) formats
- ⏱️ **Flexible Duration** - Generate videos of 4, 8, or 12 seconds
- 📊 **Real-time Progress Tracking** - Monitor your video generation status with live API status updates
- 💾 **Session Video History** - View and download all videos generated in your current session
- 📹 **Manual Video Recovery** - Add videos to history by ID to recover previously generated videos
- 💰 **Cost Estimation** - See estimated costs before generating videos
- 💡 **Example Prompts** - Get inspired with pre-written prompt examples
- 🔒 **Secure API Key Management** - Session-based key storage (not persisted to disk)
- ⚠️ **Smart Error Handling** - Detects content violations and generation failures automatically
- 📐 **Automatic Image Resizing** - Images are automatically resized to match your selected resolution

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key with access to Sora models
- Internet connection

## 🚀 Installation

1. **Clone or download this repository:**

```bash
git clone <repository-url>
cd sora2protest
```

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Get your OpenAI API key:**

- Sign up or log in to [OpenAI Platform](https://platform.openai.com/)
- Navigate to API Keys section
- Create a new API key with access to Sora models
- Copy the key (you'll enter it in the app sidebar)

## 🎮 Usage

1. **Start the application:**

```bash
streamlit run app.py
```

2. **Open your browser:**

The app will automatically open in your default browser at `http://localhost:8501`

3. **Configure settings:**

- Open the sidebar (click the arrow in the top-left if not visible)
- Enter your OpenAI API key in the sidebar
- Select your preferred Sora model (sora-2-pro or sora-2)
- Choose your desired video resolution (options vary by model)
- Select the video duration (4, 8, or 12 seconds)

4. **Generate a video:**

- Enter a descriptive prompt in the text area
- (Optional) Upload an image or video as input reference
  - Images will be automatically resized to match your selected resolution
- Review the estimated cost
- Click the "🎬 Generate Video" button
- Monitor the real-time progress (typically 45-120 seconds depending on model)
- Watch and download your generated video!

5. **Manage your videos:**

- View all generated videos in the Video History section
- Download any video using the download button
- Recover previous videos by entering the video ID in "Add Video by ID"

## 🖼️ Image-to-Video Generation

Sora can now animate or transform your images and videos! This powerful feature allows you to:

### Text-to-Video (Default)
Generate videos purely from text descriptions - no input needed. Perfect for creating scenes from scratch.

### Image-to-Video
1. **Upload an image** (PNG, JPG, JPEG, WEBP)
2. **Write a prompt** describing how you want it animated
3. Examples:
   - "The person smiles and waves at the camera"
   - "Camera slowly zooms in, clouds moving across the sky"
   - "Waves crash against the shore at sunset"

### Video-to-Video
1. **Upload a video** (MP4, MOV, AVI)
2. **Write a prompt** describing how you want it transformed
3. Sora will modify and enhance your video based on the prompt

### Important Notes:
- ⚠️ **Real People**: Uploading images of real people is restricted. Only use images with explicit permission.
- 🎯 **Best Results**: Be specific in your prompt about the motion/transformation you want
- 📐 **Resolution**: Input should ideally match your desired output resolution

## 🤖 Available Models

Choose the right model for your needs:

### Sora 2 Pro
- **Quality**: Highest quality and most realistic
- **Resolutions**: 720p HD and 1080p Full HD (both 16:9 and 9:16)
- **Available Resolutions**: 1280×720, 720×1280, 1792×1024, 1024×1792
- **Best for**: Professional content, final productions, highest quality output
- **Generation Time**: ~60-120 seconds
- **Cost**: Higher pricing for premium quality

### Sora 2 (Standard)
- **Quality**: Great balance of quality and speed
- **Resolutions**: 720p HD (both 16:9 and 9:16)
- **Available Resolutions**: 1280×720, 720×1280
- **Best for**: Most use cases, general content creation, cost-effective
- **Generation Time**: ~45-90 seconds
- **Cost**: Lower pricing for standard quality

## 💡 Tips for Best Results

- **Be specific and descriptive** - The more detail you provide, the better the results
- **Mention camera movements** - Include details like "camera pans left to right" or "slow zoom in"
- **Describe lighting and mood** - Specify "golden hour lighting" or "dramatic shadows"
- **Include subject details** - Describe what's in the scene thoroughly
- **Specify time of day** - "at sunset", "early morning fog", etc.

## 📝 Example Prompts

**Nature Scene:**
```
A serene sunrise over a misty mountain lake, with a lone canoe gliding across the water. The camera slowly pans from left to right, capturing the golden light reflecting off the gentle ripples.
```

**Urban Scene:**
```
A bustling Tokyo street at night, neon signs reflecting on wet pavement after rain, people with umbrellas walking past glowing storefronts, camera tracking shot.
```

**Abstract:**
```
Colorful ink drops dispersing in crystal clear water, shot in slow motion against a white background, vibrant purples and blues mixing together.
```

**Cinematic:**
```
An astronaut floating in space, Earth visible in the background, dramatic lighting from the sun, slow rotation revealing details of the spacesuit, wide cinematic shot.
```

## 🎨 Video Settings

### Available Resolutions:

**Sora 2 Pro supports all resolutions:**
- **1792×1024** - Full HD (16:9) - Highest quality landscape, great for YouTube, presentations
- **1280×720** - HD (16:9) - High-quality landscape, balanced performance
- **1024×1792** - Full HD (9:16) - Highest quality portrait for TikTok, Instagram Reels
- **720×1280** - HD (9:16) - High-quality portrait, mobile-optimized

**Sora 2 supports HD resolutions only:**
- **1280×720** - HD (16:9) - Landscape format
- **720×1280** - HD (9:16) - Portrait format

### Duration Options:
- **4 seconds** - Quick clips, fast generation
- **8 seconds** - Standard length, balanced content
- **12 seconds** - Longer sequences, more complex scenes

## 🔧 Troubleshooting

**"Please enter your OpenAI API key"**
- Make sure you've entered a valid API key in the sidebar
- Ensure your API key is active and has access to the Sora models
- API keys can be obtained from [OpenAI Platform](https://platform.openai.com/)

**"Error creating video" or "API Error"**
- Check that your API key has access to Sora models
- Verify your OpenAI account has sufficient credits
- Ensure your prompt doesn't violate OpenAI's usage policies
- If uploading an image of a person, ensure you have explicit permission

**"Video generation likely failed" or status check errors**
- This often indicates a content policy violation
- The video may have contained prohibited content (e.g., real people without permission)
- Try a different prompt or image
- Some prompts may be flagged by OpenAI's safety systems

**"Video generation is taking longer than expected"**
- Sora 2 Pro typically takes 60-120 seconds
- Sora 2 typically takes 45-90 seconds
- Complex prompts or high resolutions may take longer
- Check the video history section and use the "Refresh Status" button

**App won't start**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.8 or higher: `python --version`
- Verify Streamlit is installed: `streamlit --version`

**Cannot recover a previous video**
- Use the "Add Video by ID" feature in the Video History section
- Note: Videos may expire or be removed after a certain period
- Content policy violations will result in videos being removed from the API

## 📚 API Documentation

This app uses the OpenAI Videos API. For more information:
- [Video Creation API](https://platform.openai.com/docs/api-reference/videos/create)
- [Video Retrieval API](https://platform.openai.com/docs/api-reference/videos/retrieve)
- [Sora Models Documentation](https://platform.openai.com/docs/models)
- [OpenAI Usage Policies](https://openai.com/policies/usage-policies)

## 🛡️ Security Notes

- **Never share your API key publicly or commit it to version control**
- Keep your API key secure and rotate it if exposed
- API keys entered in the app are only stored in session state (not persisted to disk)
- You'll need to re-enter your API key each time you restart the app
- Generated videos are stored temporarily and should be moved to a secure location if needed

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI's Sora Models](https://openai.com/)
- Uses [Pillow (PIL)](https://pillow.readthedocs.io/) for image processing

## 📞 Support

If you encounter any issues or have questions:
1. Check the [OpenAI API Documentation](https://platform.openai.com/docs)
2. Review the troubleshooting section above
3. Open an issue on the repository

---

**Made with ❤️ for creators and AI enthusiasts**

