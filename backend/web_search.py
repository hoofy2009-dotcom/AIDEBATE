import asyncio
from ddgs import DDGS
from typing import List, Dict

class WebSearcher:
    """联网搜索工具"""
    
    def __init__(self):
        pass
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        搜索互联网信息
        
        Args:
            query: 搜索关键词
            max_results: 最多返回结果数
            
        Returns:
            搜索结果列表，每个结果包含 title, body, href
        """
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        'title': r.get('title', ''),
                        'snippet': r.get('body', ''),
                        'url': r.get('href', '')
                    })
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def format_search_results(self, results: List[Dict]) -> str:
        """格式化搜索结果为文本"""
        if not results:
            return "未找到相关信息。"
        
        formatted = "【互联网搜索结果】\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n"
            formatted += f"   来源: {result['url']}\n\n"
        
        return formatted

# 测试代码
if __name__ == "__main__":
    searcher = WebSearcher()
    
    # 测试搜索
    print("测试搜索功能...\n")
    query = "人工智能最新发展 2026"
    results = searcher.search(query, max_results=3)
    
    print(f"搜索关键词: {query}")
    print("=" * 60)
    print(searcher.format_search_results(results))
