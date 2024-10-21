'''
COMMUNITY SOURCES:
- https://pastebin.com/am6zRcMj
'''
import configparser
import requests
import speech_recognition as sr
import re 
import os
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import IPython.display as ipd

os.environ["GIT_CLONE_PROTECTION_ACTIVE"] = "false"
ENDPOINT = "http://127.0.0.1:5001"

config = configparser.ConfigParser()
config.read_file(open(r'config.txt')) 
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

debug = config.get('chatbot_config','debug')
debug_message = "I am testing your capabilities of listening and answering. How are you doing, Spork?"

def split_text(text):
    parts = re.split(r'\n[a-zA-Z]', text)
    return parts

device = "cpu"
repo_id = "parler-tts/parler_tts_mini_v0.1"
model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(repo_id)
description = config.get('chatbot_config', 'description')

username =  config.get('chatbot_config', 'username')
botname = config.get('chatbot_config', 'botname')
instructions = config.get('chatbot_config', 'instructions')

def get_prompt(conversation_history, username, text): # For KoboldAI Generation
    return {
        "prompt": instructions + conversation_history + f"{username}: {text}\n{botname}:",
        "use_story": False,
        "use_memory": True,
        "use_authors_note": False,
        "use_world_info": False,
        "max_context_length": 1024,
        "max_length": 512,
        "rep_pen": 1.0,
        "rep_pen_range": 1024,
        "rep_pen_slope": 0.7,
        "temperature": 0.8,
        "tfs": 0.97,
        "top_a": 0.8,
        "top_k": 0,
        "top_p": 0.5,
        "typical": 0.19,
        "sampler_order": [6, 0, 1, 3, 4, 2, 5],
        "singleline": False, 
        #"sampler_seed": 69420, #set the seed
        #"sampler_full_determinism": False, #set it so the seed determines generation content
        "frmttriminc": False,
        "frmtrmblln": False
    }

global conversation_history
with open(os.path.join(__location__, f'conv_history_{botname}_terminal.txt'), 'a+') as file:
    file.seek(0)
    chathistory = file.read()
    print(chathistory)
conversation_history = f"{chathistory}"

def handle_input():
    if debug == False:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            voice_in = r.listen(source) # Get the user's voice
            try:
                print("Opening microphone.")
                user_message = r.recognize_google(voice_in) # Convert speech to text
                print (f"Google's results:\n{user_message}")
                handle_llm_inference(user_message)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio. Retrying.\n")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}\n".format(e))
    else:
        handle_llm_inference(debug_message)

def handle_llm_inference(user_message):
    global conversation_history
    prompt = get_prompt(conversation_history, username, user_message) # Generate a prompt using the conversation history and user message
    response = requests.post(f"{ENDPOINT}/api/v1/generate", json=prompt) # Send the prompt to KoboldAI and get the response
    if response.status_code == 200:
        results = response.json()['results']
        text = results[0]['text'] # Parse the response and get the generated text
        response_text = split_text(text)[0]
        response_text = response_text.replace("  ", " ")
        conversation_history += f"{username}: {user_message}\n{botname}: {response_text}\n" # Update the conversation history with the user message and bot response
        with open(os.path.join(__location__, f'conv_history_{botname}_terminal.txt'), "a") as f:
            f.write(f"{username}: {user_message}\n{botname}: {response_text}\n") # Append conversation to text file
        response_text = response_text.replace("\n", "")
        print(f"{botname}: {response_text}") # Send the response back to the console
        handle_output(response_text)

def handle_output(response_text):
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(response_text, return_tensors="pt").input_ids.to(device)
    voice_out_generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    voice_out = voice_out_generation.cpu().numpy().squeeze()
    with open(os.path.join(__location__, "parler_tts_out.wav"), "a"):
        sf.write("parler_tts_out.wav", voice_out, model.config.sampling_rate)
    if debug == False:
        ipd.Audio("parler_tts_out.wav")


while True:
    handle_input()
