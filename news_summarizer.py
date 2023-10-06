import os
import openai
from metaphor_python import Metaphor

openai.api_key = os.getenv("OPENAI_API_KEY")
metaphor = Metaphor(os.getenv("METAPHOR_API_KEY"))

def get_search_query(user_question):
    SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_question},
        ],
    )
    return completion.choices[0].message.content

def get_summary(extracted_content):
    SYSTEM_MESSAGE = "You are a helpful assistant that summarizes the content of a webpage. Summarize the users input."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": extracted_content},
        ],
    )
    return completion.choices[0].message.content

def get_recent_news_summary(user_question):
    # Get the search query
    query = get_search_query(user_question)

    # Get recent articles related to the query
    search_response = metaphor.search(query, use_autoprompt=True, start_published_date="2023-06-01")
    
    # Display article titles to the user and let them select
    print("\nSelect the articles you want summarized:")
    for idx, result in enumerate(search_response.results, start=1):
        print(f"{idx}. {result.title}")

    selected_indices = input("\nEnter article numbers separated by commas (e.g., '1,2,3'): ")
    selected_indices = [int(idx.strip()) for idx in selected_indices.split(",")]

    summaries = []
    for idx in selected_indices:
        # Summarize the selected articles
        selected_result = search_response.results[idx-1]
        summary = get_summary(selected_result.extract)
        summaries.append(f"\nSummary for {selected_result.title}: {summary}")

    return "\n".join(summaries)

if __name__ == "__main__":
    user_query = input("What recent news topic would you like to know about? ")
    print(get_recent_news_summary(user_query))
