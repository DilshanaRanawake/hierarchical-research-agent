import arxiv

client = arxiv.Client()

def search_papers(query: str, max_results: int = 5):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    results = []
    for paper in client.results(search):
        results.append({
            "title": paper.title,
            "summary": paper.summary,
            "url": paper.entry_id,
            "published": str(paper.published.date()),
        })
    return results

if __name__ == "__main__":
    papers = search_papers("hand gesture recognition skeletal fusion")
    for p in papers:
        print(p["title"], "-", p["published"])