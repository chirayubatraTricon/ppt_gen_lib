from typing import Any, Dict, Optional
import os
import json

import helpers
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLM():
    def _ensure_api_key() -> None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Add GEMINI_API_KEY=<your_key> to a .env file or export it in the environment."
            )


    def generate_text(self, prompt: str, model: Optional[str] = None, max_output_tokens: int = 512) -> str:
        """Generate plain text using Google Gemini.

        Requires the environment variable GEMINI_API_KEY and the `google.generativeai` package.
        Returns the model's text output.
        """
        self._ensure_api_key()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
        mdl = genai.GenerativeModel(model_name=model_name)
        resp = mdl.generate_content(prompt)
        return getattr(resp, "text", str(resp))


    def generate_json(self, prompt: str, model: Optional[str] = None, schema_hint: Optional[str] = None) -> Dict[str, Any]:
        """Generate JSON output using Google Gemini and parse it.

        The LLM is expected to return valid JSON. If parsing fails, a ValueError is raised
        with the raw model output included for debugging.
        """
        text = self.generate_text(prompt, model=model)

        from helpers import extract_json_block

        jblock = extract_json_block(text)
        if jblock:
            try:
                return json.loads(jblock)
            except Exception:
                try:
                    return json.loads(jblock.replace("'", '"'))
                except Exception:
                    raise ValueError(f"Failed to parse extracted JSON. Raw output:\n{text}")

        raise ValueError(f"No JSON block found in model output. Raw output:\n{text}")


    if __name__ == "__main__":
        sample = "Generate 2 slide titles about AI in healthcare. Return JSON with key 'slides'."
        print("----TEXT----")
        print(generate_text(sample))
        print("----JSON----")
        print(json.dumps(generate_json(sample), indent=2))