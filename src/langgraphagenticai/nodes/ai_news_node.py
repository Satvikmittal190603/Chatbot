from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os

class AINewsNode:
    def __init__(self, llm):
        self.tavily = TavilyClient()
        self.llm = llm

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency

        Args:
            state (dict): the state dictionary containing messages.

        Returns:
            dict: Updated state values.
        """
        frequency = state['messages'][-1].content.lower()

        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'yearly': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 365}

        # Query Tavily News API
        response = self.tavily.search(
            query="Top Artificial intelligence news india and globally",
            topic="news",
            time_range=time_range_map.get(frequency, 'd'),
            include_answer="advanced",
            max_results=20,
            days=days_map.get(frequency, 1)
        )

        # Tavily returns search results under the "results" key (plural)
        news_data = response.get("results", [])
        return {"frequency": frequency, "news_data": news_data}

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM

        Args:
            state (dict): The state dictionary containing "news_data".

        Returns:
            dict: Updated state values containing "summary".
        """
        news_items = state.get('news_data') or []

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize AI news articles into markdown format. for each item include:
            -Date in "YYYY-MM-DD" format in IST timezone
            - Concose sentences summary from latest news
            - Sort news by date wise (latest first)
            -source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        article_str = "\n\n".join([
            f"Content:{item.get('content','')}\nURL:{item.get('url','')}\nDate:{item.get('published_date','')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format_messages(articles=article_str))
        return {"summary": response.content}

    def save_news(self, state: dict) -> dict:
        """
        Save the summarized news to a file

        Args:
            state (dict): The state dictionary containing "frequency" and "summary".

        Returns:
            dict: Updated state values containing "filename".
        """
        frequency = state.get('frequency') or 'daily'
        summary = state.get('summary') or ''
        
        base_filename = f"./AINews/{frequency}_summary"
        extension = ".md"
        
        filename = f"{base_filename}{extension}"
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}{extension}"
            counter += 1
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary \n\n")
            f.write(summary)
            
        return {"filename": filename}
