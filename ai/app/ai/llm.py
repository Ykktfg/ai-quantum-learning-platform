from google import genai

from .config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini and return a clean response.

    Handles quota and API errors gracefully so the
    AI API does not crash with a traceback.
    """

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            store=False
        )

        return interaction.output_text

    except Exception as error:
        error_message = str(error)

        if "quota" in error_message.lower() or "429" in error_message:
            return (
                "The AI tutor is temporarily unavailable because "
                "the Gemini API quota has been exceeded. "
                "Please try again after the quota resets."
            )

        return (
            "The AI tutor could not process the request right now. "
            "Please try again shortly."
        )
