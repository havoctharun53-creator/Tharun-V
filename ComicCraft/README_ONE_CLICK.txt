COMICCRAFT - ONE CLICK WINDOWS SETUP

1. Make sure Python 3.11+ is installed.
2. Open this folder in VS Code.
3. Open .env and replace:
   GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
   with your real Gemini API key.
4. Double-click START_COMICCRAFT.bat.
5. Wait for installation to finish.
6. Open http://127.0.0.1:8000

For the first test, IMAGE_PROVIDER=demo is enabled. This avoids needing a Hugging Face key and confirms the Gemini/backend/PDF pipeline works.
To use real AI artwork later, change IMAGE_PROVIDER=huggingface and add HF_API_KEY.

If pip cannot download packages, the computer's internet/DNS connection to PyPI must be fixed; no ZIP can include the entire Python ecosystem reliably.
