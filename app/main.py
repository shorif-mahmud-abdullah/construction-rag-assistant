from app.llm.client import LLMClient

llm = LLMClient()

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Say hello in one sentence and greeting me as SHorif Mahmud Abdullah."
    }
]

print(llm.chat(messages))