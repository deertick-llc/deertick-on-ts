import configparser
import json
import os
import pandas as pd
import random
import requests
import datetime
import replicate
import mistralai
from openai import OpenAI
import uuid
import configparser

from model_data import providers, models, voice_samples, list_all, ModelHead

config = configparser.ConfigParser()
config.read("config.ini")

df = pd.read_csv('samples.csv')

# Load Keys
os.environ["REPLICATE_API_TOKEN"] = config.get("keys", "REPLICATE_API_TOKEN")
os.environ["OPENAI_API_TOKEN"] = config.get("keys", "OPENAI_API_TOKEN")
HUGGINGFACE_API_KEY = config.get("keys", "HUGGINGFACE_API_KEY")
OPENROUTER_API_KEY = config.get("keys", "OPENROUTER_API_KEY")
os.environ["MISTRAL_API_KEY"] = config.get("keys", "MISTRAL_API_KEY")


class Agent:
    def __init__(self, model, system_prompt='', provider='', settings=None):
        '''
        Initialize an Agent object.

        Args:
            model (str): The name or identifier of the model to use.
            system_prompt (str, optional): The system prompt to set the context for the agent. Defaults to an empty string.
            provider (str or int, optional): The provider to use for the model. Can be a string (e.g., 'replicate', 'anthropic') or an integer index corresponding to the `providers` list. Defaults to 'replicate'.

        Attributes:
            provider (str): The selected provider for the model.
            model_key (str): The key or identifier for the model.
            nickname (str): A nickname for the agent, defaults to the model name.
            color (str or None): The color associated with the agent, if any.
            font (str or None): The font associated with the agent, if any.
            content (str): Stores the content generated by the agent.
            last_response (str): Stores the latest response from the agent.
            conversation (dict): Keeps track of the conversation history.
                - 'system' (list): Stores system messages.
                - 'user' (list): Stores user messages.
                - 'agent' (list): Stores agent responses.
            system_prompt (str): The system prompt for the agent.
            tts_path (str): Path for text-to-speech output.
            img_path (str): Path for image output.
            audio_path (str): Path for audio output.
            max_tokens (int): Maximum number of tokens for generation.
            min_tokens (int): Minimum number of tokens for generation.
            temperature (float): Controls randomness in generation.
            presence_penalty (float): Penalizes new tokens based on their presence in the text so far.
            frequency_penalty (float): Penalizes new tokens based on their frequency in the text so far.
            top_k (int): Number of top tokens to consider for sampling.
            top_p (float): Cumulative probability threshold for top-p sampling.
            prompt_template (str): Template for formatting prompts.
            settings (dict): Stores the above generation settings in the correct format for the model.
            tools (list): List of available tools or functions for the agent.
            tool_template (dict): Template for defining new tools. It follows this structure:
                - type: Set to "function" to define a callable tool.
                - function: Contains the tool's details:
                    - description: A string describing the tool's purpose.
                    - parameters: Defines the input parameters for the tool:
                        - type: Set to "object" for structured input.
                        - properties: Defines individual parameters and their types.
                        - required: List of mandatory parameters.
                        - additionalProperties: Whether extra parameters are allowed.
                This template allows the agent to understand and use custom functions.
        '''
        if settings is not None:
            self.settings = settings
        self.model = model
        self.provider = provider
        if provider == '':
            for llm in models:
                if model == llm[ModelHead.name]:
                    self.provider = llm[ModelHead.preferred_provider]
                    break
        if type(provider) == int:
            self.provider = providers[provider]
        self.content = ''
        self.model_key = model
        self.nickname = model
        self.color = None
        self.font = None
        self.request = None
        self.last_response = ''
        self.last_prompt = ''
        self.conversation = {'system': [], 'user': [], 'agent': []}
        self.history = False
        self.update_provider(provider)
        self.system_prompt = system_prompt
        self.response = None
        self.tts_path = 'tts'
        self.img_path = 'img'
        self.output_format = 'webp'
        self.num_outputs = 1
        self.lora_scale = 0.6
        self.aspect_ratio = "square"
        self.guidance_scale = 7.5
        self.num_inference_steps = 50
        self.disable_safety_checker = True
        self.seed = random.randint(9000, 1000000)
        self.audio_path = ''
        self.max_tokens = 256
        self.min_tokens = 0
        self.temperature = 0.6
        self.presence_penalty = 0
        self.frequency_penalty = 0
        self.top_k = 50
        self.top_p = 0.9
        self.repetition_penalty = 1.0
        self.min_p = 0.0
        self.top_a = 0.0
        self.seed = None
        self.logit_bias = {}
        self.logprobs = False
        self.top_logprobs = None
        self.response_format = None
        self.stop = []
        self.tool_choice = None
        self.prompt_template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        self.settings = {
                "top_k": self.top_k,
                "top_p": self.top_p,
                "prompt": self.conversation['user'][-1] if len(self.conversation['user']) > 0 else '',
                "max_tokens": self.max_tokens,
                "min_tokens": self.min_tokens,
                "temperature": self.temperature,
                "system_prompt": system_prompt,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty,
                "prompt_template": self.prompt_template
            }
        self.tools = []
        self.tool_template = {
                "type": "function",
                "function": {
                    "description": "",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False,
                    },
                }
            }

    def update_provider(self, provider):
        """
        Update the provider and model for the agent.

        Args:
            provider (str): The name of the provider to use. Must be one of
                'replicate', 'anthropic', 'google', 'openai', 'huggingface',
                or 'openrouter'.

        This method sets the provider and initializes the corresponding model.
        It handles different initialization procedures for each provider.
        """
        for llm in models:
            if llm[ModelHead.id] == self.model:
                if self.provider == 'replicate':
                    print(f"Replicate: {llm[ModelHead.id]}")
                    self.model = llm[ModelHead.id]
                    break
                elif self.provider == 'openai':
                    print(f"OpenAI: {llm[ModelHead.id]}")
                    self.model = llm[ModelHead.id]
                    self.client = OpenAI()  # Create an OpenAI client instance
                    break
                elif self.provider == 'huggingface':
                    print(f"HuggingFace: {llm[ModelHead.id]}")
                    self.model = llm[ModelHead.id]
                    break
                elif self.provider == 'openrouter':
                    print(f"OpenRouter: {llm[ModelHead.id]}")
                    self.model = llm[ModelHead.id]
                    break
                elif self.provider == 'mistral':
                    print(f"Mistral: {llm[ModelHead.id]}")
                    self.model = llm[ModelHead.id]
                    break
                else:
                    print(f"Invalid provider: {provider}")
                    break

    def create_tool(self, name, description, parameters):
        """
        Create a new tool for the agent.

        Args:
            name (str): The name of the tool.
            description (str): A brief description of what the tool does.
            parameters (dict): A dictionary describing the parameters for the tool.
                Should include 'properties' and 'required' keys.

        This method creates a new tool based on the provided information and
        adds it to the agent's list of available tools.
        """
        new_tool = self.tool_template
        new_tool['function']['name'] = name
        new_tool['function']['description'] = description
        for x, y in parameters.items():
            if x == 'properties':
                for a, b in y.items():
                    new_tool['function']['parameters']['properties'][a] = b
            if x == 'required':
                for a in y:
                    new_tool['function']['parameters']['required'].append(a)
            else:
                new_tool['function']['parameters'][x] = y
        tool = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.tools.append(tool)

    def generate_response(self, system_prompt, prompt):
        """
        Generate a response based on the given system prompt and user prompt.

        Args:
            system_prompt (str): The system prompt to set the context for the AI.
            prompt (str): The user's input prompt.

        Returns:
            list: A list of response events from the AI model.
        """

        if self.history is False:
            self.conversation['system'].append(system_prompt)
            self.conversation['user'].append(prompt)
            self.settings['system_prompt'] = system_prompt
            self.settings['prompt'], self.last_prompt = prompt, prompt
        else:
            context = ''
            if len(self.conversation['user']) > 0:
                for i in range(len(self.conversation['user'])):
                    context += f"user: {self.conversation['user'][i]}\n"
                    if len(self.conversation['agent']) > i:
                        context += f"assistant: {self.conversation['agent'][i]}\n"
            self.settings['system_prompt'] = system_prompt
            self.settings['prompt'] = context + prompt
            prompt = context + prompt
        events = list()

        # replicate
        if self.provider == 'replicate':
            for event in replicate.stream(
                self.model,
                input=self.settings,
                ):
                events.append(str(event))

        # huggingface
        elif self.provider == 'huggingface':
            API_URL = "https://api-inference.huggingface.co/models/gpt2"
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()
            data = query(f'{system_prompt}\n\n{prompt}')
            for event in data:
                events.append(str(event))

        # openai
        elif self.provider == 'openai':
            # tools coming soon!
            print(f"OpenAI: {self.model}")
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            self.response = completion
            events = completion.choices[0].message.content
            # For OpenAI, directly set the content and last_response
            self.content = events
            self.last_response = [events]  # Wrap in list to match other providers' format
            # Skip the general processing at the end of the method
            self.conversation['agent'].append(self.content)
            self.conversation['user'].append(prompt)
            self.conversation['system'].append(system_prompt)
            return self.content  # Return content directly for OpenAI

        # openrouter
        elif self.provider == 'openrouter':
            if self.model == 'meta-llama/llama-3.1-405b':
                def agent405b_base(system_prompt, prompt):
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "HTTP-Referer": f"deertick.io",  # Optional, for including your app on openrouter.ai rankings.
                            "X-Title": f"DeerTick",  # Optional. Shows in rankings on openrouter.ai.
                        },
                        data=json.dumps({
                            "model": "meta-llama/llama-3.1-405b",  # Optional
                            "max_tokens": self.max_tokens,
                            "temperature": self.temperature,
                            "presence_penalty": self.presence_penalty,
                            "frequency_penalty": 0,
                            "top_k": self.top_k,
                            "top_p": self.top_p,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ]
                        })
                    )
                    # print(response.json())
                    self.request = response.request
                    self.response = response
                    try:
                        response_text = response.json()['choices'][0]['message']['content']
                        return response_text
                    except Exception as e:
                        print(e)
                        print(self.response.json())
                        print(self.request.body)
                        return self.response.json()
                events = agent405b_base(system_prompt, prompt)
            else:
                response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": f"deertick.io",  # Optional, for including your app on openrouter.ai rankings.
                    "X-Title": f"DeerTick",  # Optional. Shows in rankings on openrouter.ai.
                },
                data=json.dumps({
                    "model": self.model,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature,
                    "presence_penalty": self.presence_penalty,
                    "frequency_penalty": self.frequency_penalty,
                    "top_k": self.top_k,
                    "top_p": self.top_p,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                        ]
                    })
                )
                self.request = response.request
                self.response = response
                try:
                    response_text = self.response.json()['choices'][0]['message']['content']
                    events = response_text
                except Exception as e:
                    print(e)
                    print(self.response.json())
                    print(self.request.body)
        elif self.provider == 'mistral':

            api_key = os.environ["MISTRAL_API_KEY"]
            model = "mistral-large-latest"

            client = mistralai.Mistral(api_key=api_key)

            chat_response = client.chat.complete(
                model = model,
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ]
            )
            self.response = chat_response
            events = chat_response.json()['choices'][0]['message']['content']
        # Fail
        else:
            print(f"Invalid provider: {self.provider}")
        if self.provider != 'openai':
            self.last_response = events
            self.content = ''.join([x for x in events])
            self.conversation['agent'].append(self.content)
            self.conversation['user'].append(prompt)
            self.conversation['system'].append(system_prompt)
        return self.last_response

    def poke(self, prompt):
        """
        Poke the agent with a prompt.

        Args:
            prompt (str): The prompt to poke the agent with.

        Returns:
            str: The generated response.
        """
        text = self.generate_response(self.system_prompt, prompt)
        text_string = ''.join(text) if isinstance(text, list) else text  # Ensure we have a string
        return text_string  # Return the response without printing it

    def tts_poke(self, prompt, voice=voice_samples["michael_voice"]):
        """
        Poke the agent with a prompt and generate audio.

        Args:
            prompt (str): The prompt to poke the agent with.
            voice (str): The voice to use for the audio.
        """
        text = self.tts(prompt, voice)
        return text

    def save_conversation(self):
        """
        Save the current conversation to a CSV file.

        This method creates a CSV file with the current date and time as the filename,
        and saves the conversation history (system prompts, user inputs, and agent responses)
        to this file.
        """
        # Import pandas if not already imported
        import pandas as pd
        from datetime import datetime

        # Create a DataFrame from the conversation history
        for x in self.conversation:
            self.conversation['ID'] = uuid.uuid4()
        df = pd.DataFrame({
            'system': self.conversation['system'],
            'user': self.conversation['user'],
            'agent': self.conversation['agent']
        })

        # Generate filename with current datetime
        filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)
        print(f"Conversation saved to {filename}")

    def load_conversation(self, filename):
        """
        Load a conversation from a CSV file.

        Args:
            filename (str): The name of the CSV file to load.
        """
        df = pd.read_csv(filename)
        self.conversation['system'] = df['system'].tolist()
        self.conversation['user'] = df['user'].tolist()
        self.conversation['agent'] = df['agent'].tolist()
        print(f"Conversation loaded from {filename}")

    def img_error(self, prompt, rejected_prompt):
        """
        Handle image generation errors by adjusting the prompt and trying again.

        Args:
            prompt (str): The original prompt for image generation.
            rejected_prompt (str): The rejected prompt that triggered the error.

        This method prints a rejection message, modifies the prompt, and attempts to generate an image again.
        """
        print(f'Rejected image prompt: {rejected_prompt}')
        admonish = "sorry, this description was flagged for not being safe for work,"+ \
        "please tone it down for the heartless censors. describe it again, please."
        img_prompt = f"{prompt}" + f'your rejected prompt:{rejected_prompt}{admonish}'
        self.generate_image(img_prompt)

    def generate_image(self, prompt, file_path=None):
        """
        Generate an image based on the given prompt.

        Args:
            prompt (str): The prompt to generate an image from.

        Returns:
            str: The URL of the generated image.
        """
        if self.seed is None:
            self.seed = random.randint(9000, 1000000)
        if self.provider == 'replicate':
            if self.model == 'flux-dev-lora':
                input = {
                    "prompt": prompt,
                    "num_outputs": self.num_outputs,
                    "seed": self.seed,
                    "output_format": self.output_format,
                    "hf_lora": self.model,
                    "lora_scale": self.lora_scale,
                    "aspect_ratio": self.aspect_ratio,
                    "guidance_scale": self.guidance_scale,
                    "num_inference_steps": self.num_inference_steps,
                    "disable_safety_checker": self.disable_safety_checker
                }
                output = replicate.run(
                    "lucataco/flux-dev-lora:a22c463f11808638ad5e2ebd582e07a469031f48dd567366fb4c6fdab91d614d",
                    input=input
                )
            if self.model_key == 'animate-diff':
                output = replicate.run(
                    self.model,
                    input={
                        "path": "toonyou_beta3.safetensors",
                        "seed": self.seed,
                        "steps": self.num_inference_steps,
                        "prompt": prompt,
                        "n_prompt": "badhandv4, easynegative, ng_deepnegative_v1_75t, verybadimagenegative_v1.3, bad-artist, bad_prompt_version2-neg, teeth",
                        "motion_module": "mm_sd_v14",
                        "guidance_scale": self.guidance_scale
                    }
                )

            else:
                print(f"seed: {self.seed}")
                input = {
                    "prompt": prompt,
                    "num_outputs": self.num_outputs,
                    "seed": self.seed,
                    "output_format": "png",
                    "quality": "standard"
                }
                try:
                    output = replicate.run(
                        self.model,
                        input=input
                    )
                    print(output)
                except replicate.exceptions.ModelError as e:
                    print(e)
                    self.img_error(prompt, output)
        else:
            print(f"Invalid provider: {self.provider}")
            return None

        if output and isinstance(output, list) and len(output) > 0:
            for x in output:
                image_url = x
                if file_path is None:
                    image_file_path = f"{self.img_path}{'' if self.img_path == '' else '/'}{self.model_key}_image_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.{self.output_format}"
                else:
                    image_file_path = file_path
                response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Image saved to: {image_file_path}")
            else:
                print(f"Failed to download image: HTTP {response.status_code}")
        else:
            print("No valid image URL received")

        self.content = output
        return output

    def tts(self, text, audio_url, file_path=None):
        """
        Generate and save an audio file from text using a TTS model.

        Args:
            text (str): The text to convert to audio.
            audio_url (str): The URL of the sample audio file.

        Returns:
            str: The URL of the generated audio file.
        """
        print(f"text: {text}")
        print(f"audio_url: {audio_url}")
        input = {
            "speaker": audio_url,
            "text": text
        }

        output = replicate.run(
            self.model,
            input = input
        )
        # Download the audio file
        if output and isinstance(output, str):
            if file_path is None:
                audio_file_path = f"{self.tts_path}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav"
            else:
                audio_file_path = file_path
            response = requests.get(output)
            if response.status_code == 200:
                with open(audio_file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Audio saved to: {audio_file_path}")
            else:
                print(f"Failed to download audio: HTTP {response.status_code}")
        else:
            print("No valid audio URL received")
        self.content = output
        return output

    def help(self):
        list_all()