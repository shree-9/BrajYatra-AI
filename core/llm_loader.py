import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import MODEL_NAME


class LLM:
    """
    Loads Mistral-7B-Instruct-v0.2 for intent parsing and explanation generation.
    Works on Kaggle T4 GPU (float16) or falls back to CPU (float32, slower).
    """

    _instance = None

    def __new__(cls):
        """Singleton — only one LLM instance across all agents."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        # Skip loading on CPU — Mistral-7B needs ~28GB RAM and takes hours
        if self.device == "cpu":
            print(f"[LLM] Skipping {MODEL_NAME} on CPU (too slow). Using fallback responses.")
            print(f"[LLM] Run on Kaggle with GPU for full LLM support.")
            self.model = None
            self.tokenizer = None
            self._initialized = True
            return

        print(f"[LLM] Loading {MODEL_NAME} on {self.device} ({self.dtype})...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=self.dtype,
                device_map="auto" if self.device == "cuda" else None
            )

            if self.device == "cpu":
                self.model = self.model.to(self.device)

            self.model.eval()
            self._initialized = True
            print(f"[LLM] Model loaded successfully on {self.device}.")

        except Exception as e:
            print(f"[LLM] ERROR loading model: {e}")
            self.model = None
            self.tokenizer = None
            self._initialized = True

    def generate(self, prompt, max_tokens=512):
        """Generate a response from a prompt using the loaded model."""

        if self.model is None:
            return self._fallback_response(prompt)

        try:
            # Try chat template first (Mistral-style)
            try:
                messages = [{"role": "user", "content": prompt}]
                inputs = self.tokenizer.apply_chat_template(
                    messages,
                    return_tensors="pt",
                    add_generation_prompt=True
                )
                if isinstance(inputs, torch.Tensor):
                    input_ids = inputs.to(self.device)
                else:
                    input_ids = inputs["input_ids"].to(self.device)
            except Exception:
                # Fallback: direct tokenization
                encoded = self.tokenizer(prompt, return_tensors="pt")
                input_ids = encoded["input_ids"].to(self.device)

            input_len = input_ids.shape[-1]

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode only the NEW tokens (skip the input prompt tokens)
            new_tokens = outputs[0][input_len:]
            response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

            return response.strip()

        except Exception as e:
            print(f"[LLM] Generation error: {e}")
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt):
        """Fallback when LLM is unavailable — returns a safe default."""
        return (
            "I'm unable to generate a response right now. "
            "Please check that the model is loaded correctly."
        )
