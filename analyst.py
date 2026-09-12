from openai import OpenAI
import json

llm_client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
LLM_MODEL = "llama-3.2-3b-instruct"

def analyze_paper(paper: dict) -> dict:
    prompt = f"""Extract structured info from this paper abstract.

Title: {paper['title']}
Abstract: {paper['summary']}

Respond ONLY as JSON, no markdown fences, no extra text, with these exact keys:
{{"method": "...", "dataset": "...", "reported_result": "...", "relevance_to_gesture_recognition": "one sentence"}}"""

    response = llm_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        extracted = json.loads(raw)
    except json.JSONDecodeError:
        extracted = {"error": "could not parse", "raw": raw}

    return {**paper, **extracted}

if __name__ == "__main__":
    from searcher import search_papers

    papers = search_papers("hand gesture recognition skeletal fusion", max_results=2)
    for paper in papers:
        result = analyze_paper(paper)
        print(json.dumps(result, indent=2))
        print("---")