from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()
from scrape import get_cur_time 
import os

def process_data(activities):
    '''activties a json conatining gpt3.5 out put '''
    client = OpenAI()
    system_message = {
        "role": "system",
        "content": (
            "You are an AI agent tasked with processing event descriptions happening in NYC. "
            "The user will provide a detailed description of an event. Your job is to extract relevant information "
            "and return a JSON object with the necessary fields for the next step filtering. The JSON should include fields "
            "that people may want to filter on, such as date(Don't need Year), time, location, event type, target audience, cost, and any other relevant details. "
        ),
    }

    results = []
    prompt_token_track = []
    completion_token_track = []
    for activity in activities:
        json_output, prompt_token, completion_token = get_event_json(activity["description"], system_message, client)
        results.append(json_output)
        prompt_token_track.append(prompt_token)
        completion_token_track.append(completion_token)

    filename_timestamp = get_cur_time()
    # Define the directory path and file name
    directory = f'data/processed/{filename_timestamp}'

    # Create the filename
    filename = f"gpt35description.json"
    filepath = os.path.join(directory, filename)

    # Check if the directory exists, and create it if it does not
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the lists to the JSON file
    with open(filepath, "w") as file:
        json.dump(results, file, indent=4)

    print(f"The lists have been saved to {filename}")


    # Create the filename
    filename = f"gpt35token.json"
    filepath = os.path.join(directory, filename)

    data = {
        "prompt_token_track": prompt_token_track,
        "completion_token_track": completion_token_track
    }

    # Save the lists to the JSON file
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    print(f"The lists have been saved to {filename}")



def get_event_json(activity:str, system_message, client):
    '''
    retur json, input token num, output token num
    '''
    user_message = {
        "role": "user",
        "content": f"Here is the description of the event: {activity}"
    }

    messages = [system_message, user_message]

    response = client.chat.completions.create(
        model="gpt-4o-mini",  #"gpt-3.5-turbo""gpt-4o"
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.3,
        # max_tokens=300, # response may end abruptly Hit a lot to 150
        frequency_penalty=0.5,
    )

    return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
