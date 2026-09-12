from openai import OpenAI

llm_client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
LLM_MODEL = "llama-3.2-3b-instruct"

def write_digest(analyzed_papers: list) -> str:
    def format_dataset(d):
        return ", ".join(d) if isinstance(d, list) else str(d)

    papers_text = "\n\n".join(
        f"Title: {p['title']}\n"
        f"Method: {p.get('method')}\n"
        f"Dataset: {format_dataset(p.get('dataset'))}\n"
        f"Result: {p.get('reported_result')}\n"
        f"Relevance: {p.get('relevance_to_gesture_recognition')}\n"
        f"URL: {p['url']}"
        for p in analyzed_papers
    )

    prompt = f"""Write a short weekly research digest (max 400 words) from these papers,
grouped by theme where relevant, in plain readable prose a fellow researcher would
skim in 2 minutes:

{papers_text}"""

    response = llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    import asyncio
    from searcher import search_papers
    from orchestrator import run_analysts_parallel

    papers = search_papers("hand gesture recognition skeletal fusion", max_results=5)
    analyzed = asyncio.run(run_analysts_parallel(papers))
    digest = write_digest(analyzed)

    print("\n=== WEEKLY DIGEST ===\n")
    print(digest)