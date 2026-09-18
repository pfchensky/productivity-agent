from google import genai
import os
from schemas import CHECK_IN_RESPONSE_SCHEMA


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def parse_check_in(check_in_text, task_content):
    prompt = f"""
        Instruction: Extract structured information from this productivity check-in,
        Check_in: {check_in_text},
        Task_context: {task_content}.

        The task context contains existing stored values only
        Do not copy current_progress as the new progress
        Extract progress only when the check-in explicitly provides a new
        completion percentage. Otherwise return null.
        Use the existing task context only to understand the check-in.

        Return only the fields defined by the provided response schema.
        Use null when information is not provided
        Priority Score not calculated here
    """

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents = prompt,
        config = {
            # The config dict structures LLM output to CHECK_IN_RESPONSE_SCHEMA format

            "response_mime_type": "application/json",
            "response_schema": CHECK_IN_RESPONSE_SCHEMA,
        }
    )

    return response.parsed