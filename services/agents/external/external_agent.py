from smolagents import LiteLLMModel, CodeAgent
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

print(f"OPENAI_API_KEY: {openai_api_key}")

# Verify the API key is loaded
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

model = LiteLLMModel(
    model_id="openai/gpt-4.1-mini",
    api_key=openai_api_key,
    api_base="https://api.openai.com/v1",
)

agent = CodeAgent(model=model, tools=[])

result = agent.run("What is the capital of France?")  # Fixed: capture the return value
print(result)  # Print the result to see the output
