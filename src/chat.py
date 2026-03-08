import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from search import search_prompt

load_dotenv()

ENCERRAR_SISTEMA = "2"

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_CHAT_MODEL", "gemini-2.0-flash"))
    return ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"))


def main():
    print("Bem vindo ao Sistema")
    print(f"Digite {ENCERRAR_SISTEMA} para sair\n")

    llm = get_llm()

    while True:
        text = input("Digite a pergunta: ").strip()

        if text == ENCERRAR_SISTEMA:
            print("Encerrando...")
            break

        if not text:
            continue

        prompt = search_prompt(text)

        print("\nRESPOSTA: ", end="", flush=True)
        for chunk in llm.stream(prompt):
            print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()
