#Handles interaction with OpenAI for processing data.
import openai

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

def process_data_with_openai(search_results):
    extracted_info = {}
    for entity, results in search_results.items():
        prompt = f"Extract key information about {entity} from the following:\n{results}"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            extracted_info[entity] = response.choices[0].text.strip()
        except Exception as e:
            extracted_info[entity] = f"Error: {e}"
    return extracted_info
