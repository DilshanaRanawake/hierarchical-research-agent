import asyncio
import time
import json
from concurrent.futures import ThreadPoolExecutor
from searcher import search_papers
from analyst import analyze_paper


async def run_analysts_parallel(papers):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=5) as pool:
        tasks = [loop.run_in_executor(pool, analyze_paper, p) for p in papers]
        return await asyncio.gather(*tasks)


def run_analysts_sequential(papers):
    return [analyze_paper(p) for p in papers]


if __name__ == "__main__":
    papers = search_papers("hand gesture recognition skeletal fusion", max_results=5)

    # Sequential timing
    start = time.time()
    results_seq = run_analysts_sequential(papers)
    seq_time = time.time() - start
    print(f"Sequential: {len(results_seq)} papers in {seq_time:.1f} seconds")

    # Parallel timing
    start = time.time()
    results_par = asyncio.run(run_analysts_parallel(papers))
    par_time = time.time() - start
    print(f"Parallel:   {len(results_par)} papers in {par_time:.1f} seconds")

    print(f"\nSpeedup: {seq_time / par_time:.2f}x")