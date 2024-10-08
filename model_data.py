from enum import Enum
import pandas as pd



class ModelHead(Enum):
    name = 0
    id = 1
    type = 2
    preferred_provider = 3
    providers = 4

#more options can be found online, this is just a sample of what's available
models = [
["I-8b", "meta/meta-llama-3-8b-instruct", "llm", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["I-70b", "meta/meta-llama-3-70b-instruct", "llm", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["405b-base", "meta-llama/llama-3.1-405b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["I-405b", "meta/meta-llama-3.1-405b-instruct", "llm", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["flux-schnell", "black-forest-labs/flux-schnell", "image", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["xtts-v2", "lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e", "tts", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["gpt-4o-or", "openai/gpt-4o", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4o-mini-or", "openai/gpt-4o-mini", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4-turbo-or", "openai/gpt-4-turbo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4-or", "openai/gpt-4", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-3.5-turbo-or", "openai/gpt-3.5-turbo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["llava-13b", "yorickvp/llava-13b", "image", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["flux-dev-lora", "lucataco/flux-dev-lora", "image", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["gemini-pro-exp", "google/gemini-pro-1.5-exp", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gemini-flash-exp", "google/gemini-flash-8b-1.5-exp", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gemini-pro", "google/gemini-pro-1.5", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gemini-flash", "google/gemini-flash-8b-1.5", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["gpt-4o-mini", "gpt-4o-mini", "llm", "openai", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4o", "gpt-4o", "llm", "openai", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4-turbo", "gpt-4-turbo", "llm", "openai", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-4", "gpt-4", "llm", "openai", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["gpt-3.5-turbo", "gpt-3.5-turbo", "llm", "openai", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["animate-diff", "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f", "video", "replicate", ['replicate', 'mistral', 'huggingface', 'openai']],
["dolphin", "cognitivecomputations/dolphin-llama-3-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["codestral", "codestral-latest", "llm", "mistral", ['replicate', 'mistral', 'huggingface', 'openai']],
["Qwen2-VL 72B Instruct", "qwen/qwen-2-vl-72b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Lumimaid v0.2 8B", "neversleep/llama-3.1-lumimaid-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: o1-mini (2024-09-12)", "openai/o1-mini-2024-09-12", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["OpenAI: o1-mini", "openai/o1-mini", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["OpenAI: o1-preview (2024-09-12)", "openai/o1-preview-2024-09-12", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["OpenAI: o1-preview", "openai/o1-preview", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai']],
["Mistral: Pixtral 12B (free)", "mistralai/pixtral-12b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Pixtral 12B", "mistralai/pixtral-12b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Reflection 70B (free)", "mattshumer/reflection-70b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Reflection 70B", "mattshumer/reflection-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R (03-2024)", "cohere/command-r-03-2024", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R+ (04-2024)", "cohere/command-r-plus-04-2024", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R+ (08-2024)", "cohere/command-r-plus-08-2024", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R (08-2024)", "cohere/command-r-08-2024", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen2-VL 7B Instruct (free)", "qwen/qwen-2-vl-7b-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen2-VL 7B Instruct", "qwen/qwen-2-vl-7b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Flash 8B 1.5 Experimental", "google/gemini-flash-8b-1.5-exp", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Flash 1.5 Experimental", "google/gemini-flash-1.5-exp", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3.1 Euryale 70B v2.2", "sao10k/l3.1-euryale-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["AI21: Jamba 1.5 Large", "ai21/jamba-1-5-large", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["AI21: Jamba 1.5 Mini", "ai21/jamba-1-5-mini", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3.5 Mini 128K Instruct", "microsoft/phi-3.5-mini-128k-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 3 70B Instruct", "nousresearch/hermes-3-llama-3.1-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 3 405B Instruct", "nousresearch/hermes-3-llama-3.1-405b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 3 405B Instruct (free)", "nousresearch/hermes-3-llama-3.1-405b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 3 405B Instruct (extended)", "nousresearch/hermes-3-llama-3.1-405b:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama 3.1 Sonar 405B Online", "perplexity/llama-3.1-sonar-huge-128k-online", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: ChatGPT-4o", "openai/chatgpt-4o-latest", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3 8B Lunaris", "sao10k/l3-lunaris-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Nemo 12B Starcannon", "aetherwiing/mn-starcannon-12b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o (2024-08-06)", "openai/gpt-4o-2024-08-06", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3.1 405B (base)", "meta-llama/llama-3.1-405b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Nemo 12B Celeste", "nothingiisreal/mn-celeste-12b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Pro 1.5 Experimental", "google/gemini-pro-1.5-exp", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama 3.1 Sonar 70B Online", "perplexity/llama-3.1-sonar-large-128k-online", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama 3.1 Sonar 70B", "perplexity/llama-3.1-sonar-large-128k-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama 3.1 Sonar 8B Online", "perplexity/llama-3.1-sonar-small-128k-online", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama 3.1 Sonar 8B", "perplexity/llama-3.1-sonar-small-128k-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3.1 70B Instruct", "meta-llama/llama-3.1-70b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3.1 8B Instruct (free)", "meta-llama/llama-3.1-8b-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3.1 8B Instruct", "meta-llama/llama-3.1-8b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3.1 405B Instruct", "meta-llama/llama-3.1-405b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Codestral Mamba", "mistralai/codestral-mamba", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral Nemo", "mistralai/mistral-nemo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o-mini (2024-07-18)", "openai/gpt-4o-mini-2024-07-18", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o-mini", "openai/gpt-4o-mini", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen 2 7B Instruct (free)", "qwen/qwen-2-7b-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen 2 7B Instruct", "qwen/qwen-2-7b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemma 2 27B", "google/gemma-2-27b-it", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Magnum 72B", "alpindale/magnum-72b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 2 Theta 8B", "nousresearch/hermes-2-theta-llama-3-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemma 2 9B (free)", "google/gemma-2-9b-it:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemma 2 9B", "google/gemma-2-9b-it", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["AI21: Jamba Instruct", "ai21/jamba-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3.5 Sonnet", "anthropic/claude-3.5-sonnet", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3.5 Sonnet (self-moderated)", "anthropic/claude-3.5-sonnet:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3 Euryale 70B v2.1", "sao10k/l3-euryale-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3 Medium 4K Instruct", "microsoft/phi-3-medium-4k-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Dolphin 2.9.2 Mixtral 8x22B", "cognitivecomputations/dolphin-mixtral-8x22b", "llm", "nan", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen 2 72B Instruct", "qwen/qwen-2-72b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["NousResearch: Hermes 2 Pro - Llama-3 8B", "nousresearch/hermes-2-pro-llama-3-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct v0.3", "mistralai/mistral-7b-instruct-v0.3", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct (free)", "mistralai/mistral-7b-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct", "mistralai/mistral-7b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct (nitro)", "mistralai/mistral-7b-instruct:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3 Mini 128K Instruct (free)", "microsoft/phi-3-mini-128k-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3 Mini 128K Instruct", "microsoft/phi-3-mini-128k-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3 Medium 128K Instruct (free)", "microsoft/phi-3-medium-128k-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Phi-3 Medium 128K Instruct", "microsoft/phi-3-medium-128k-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3 Lumimaid 70B", "neversleep/llama-3-lumimaid-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Flash 1.5", "google/gemini-flash-1.5", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["DeepSeek V2.5", "deepseek/deepseek-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama3 Sonar 70B Online", "perplexity/llama-3-sonar-large-32k-online", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama3 Sonar 70B", "perplexity/llama-3-sonar-large-32k-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama3 Sonar 8B Online", "perplexity/llama-3-sonar-small-32k-online", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Perplexity: Llama3 Sonar 8B", "perplexity/llama-3-sonar-small-32k-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: LlamaGuard 2 8B", "meta-llama/llama-guard-2-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o (2024-05-13)", "openai/gpt-4o-2024-05-13", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o", "openai/gpt-4o", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4o (extended)", "openai/gpt-4o:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen 1.5 72B Chat", "qwen/qwen-72b-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Qwen 1.5 110B Chat", "qwen/qwen-110b-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3 Lumimaid 8B", "neversleep/llama-3-lumimaid-8b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Llama 3 Lumimaid 8B (extended)", "neversleep/llama-3-lumimaid-8b:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Fimbulvetr 11B v2", "sao10k/fimbulvetr-11b-v2", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 70B Instruct", "meta-llama/llama-3-70b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 70B Instruct (nitro)", "meta-llama/llama-3-70b-instruct:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 8B Instruct (free)", "meta-llama/llama-3-8b-instruct:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 8B Instruct", "meta-llama/llama-3-8b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 8B Instruct (nitro)", "meta-llama/llama-3-8b-instruct:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama 3 8B Instruct (extended)", "meta-llama/llama-3-8b-instruct:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mixtral 8x22B Instruct", "mistralai/mixtral-8x22b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["WizardLM-2 7B", "microsoft/wizardlm-2-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["WizardLM-2 8x22B", "microsoft/wizardlm-2-8x22b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Pro 1.5", "google/gemini-pro-1.5", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 Turbo", "openai/gpt-4-turbo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R+", "cohere/command-r-plus", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Databricks: DBRX 132B Instruct", "databricks/dbrx-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Midnight Rose 70B", "sophosympatheia/midnight-rose-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command R", "cohere/command-r", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Cohere: Command", "cohere/command", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Haiku", "anthropic/claude-3-haiku", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Haiku (self-moderated)", "anthropic/claude-3-haiku:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Sonnet", "anthropic/claude-3-sonnet", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Sonnet (self-moderated)", "anthropic/claude-3-sonnet:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Opus", "anthropic/claude-3-opus", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude 3 Opus (self-moderated)", "anthropic/claude-3-opus:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Large", "mistralai/mistral-large", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 Turbo Preview", "openai/gpt-4-turbo-preview", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo (older v0613)", "openai/gpt-3.5-turbo-0613", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 2 Mixtral 8x7B DPO", "nousresearch/nous-hermes-2-mixtral-8x7b-dpo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Medium", "mistralai/mistral-medium", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Small", "mistralai/mistral-small", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral Tiny", "mistralai/mistral-tiny", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Chronos Hermes 13B v2", "austism/chronos-hermes-13b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 2 Yi 34B", "nousresearch/nous-hermes-yi-34b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct v0.2", "mistralai/mistral-7b-instruct-v0.2", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Dolphin 2.6 Mixtral 8x7B", "cognitivecomputations/dolphin-mixtral-8x7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Pro Vision 1.0", "google/gemini-pro-vision", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: Gemini Pro 1.0", "google/gemini-pro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mixtral 8x7B Instruct", "mistralai/mixtral-8x7b-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mixtral 8x7B Instruct (nitro)", "mistralai/mixtral-8x7b-instruct:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mixtral 8x7B (base)", "mistralai/mixtral-8x7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["StripedHyena Nous 7B", "togethercomputer/stripedhyena-nous-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["MythoMist 7B (free)", "gryphe/mythomist-7b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["MythoMist 7B", "gryphe/mythomist-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenChat 3.5 7B (free)", "openchat/openchat-7b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenChat 3.5 7B", "openchat/openchat-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Noromaid 20B", "neversleep/noromaid-20b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude Instant v1.1", "anthropic/claude-instant-1.1", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2.1", "anthropic/claude-2.1", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2.1 (self-moderated)", "anthropic/claude-2.1:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2", "anthropic/claude-2", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2 (self-moderated)", "anthropic/claude-2:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenHermes 2.5 Mistral 7B", "teknium/openhermes-2.5-mistral-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 Vision", "openai/gpt-4-vision-preview", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["lzlv 70B", "lizpreciatior/lzlv-70b-fp16-hf", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Goliath 120B", "alpindale/goliath-120b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Toppy M 7B (free)", "undi95/toppy-m-7b:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Toppy M 7B", "undi95/toppy-m-7b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Toppy M 7B (nitro)", "undi95/toppy-m-7b:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Auto (best for prompt)", "openrouter/auto", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 Turbo (older v1106)", "openai/gpt-4-1106-preview", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo 16k (older v1106)", "openai/gpt-3.5-turbo-1106", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: PaLM 2 Code Chat 32k", "google/palm-2-codechat-bison-32k", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: PaLM 2 Chat 32k", "google/palm-2-chat-bison-32k", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Airoboros 70B", "jondurbin/airoboros-l2-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Xwin 70B", "xwin-lm/xwin-lm-70b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mistral: Mistral 7B Instruct v0.1", "mistralai/mistral-7b-instruct-v0.1", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo Instruct", "openai/gpt-3.5-turbo-instruct", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Pygmalion: Mythalion 13B", "pygmalionai/mythalion-13b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 32k (older v0314)", "openai/gpt-4-32k-0314", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 32k", "openai/gpt-4-32k", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo 16k", "openai/gpt-3.5-turbo-0125", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Nous: Hermes 13B", "nousresearch/nous-hermes-llama2-13b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Hugging Face: Zephyr 7B (free)", "huggingfaceh4/zephyr-7b-beta:free", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Mancer: Weaver (alpha)", "mancer/weaver", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude Instant v1.0", "anthropic/claude-instant-1.0", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v1.2", "anthropic/claude-1.2", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v1", "anthropic/claude-1", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude Instant v1", "anthropic/claude-instant-1", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude Instant v1 (self-moderated)", "anthropic/claude-instant-1:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2.0", "anthropic/claude-2.0", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Anthropic: Claude v2.0 (self-moderated)", "anthropic/claude-2.0:beta", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["ReMM SLERP 13B", "undi95/remm-slerp-l2-13b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["ReMM SLERP 13B (extended)", "undi95/remm-slerp-l2-13b:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: PaLM 2 Code Chat", "google/palm-2-codechat-bison", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Google: PaLM 2 Chat", "google/palm-2-chat-bison", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["MythoMax 13B", "gryphe/mythomax-l2-13b", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["MythoMax 13B (nitro)", "gryphe/mythomax-l2-13b:nitro", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["MythoMax 13B (extended)", "gryphe/mythomax-l2-13b:extended", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["Meta: Llama v2 13B Chat", "meta-llama/llama-2-13b-chat", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4 (older v0314)", "openai/gpt-4-0314", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-4", "openai/gpt-4", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo (older v0301)", "openai/gpt-3.5-turbo-0301", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
["OpenAI: GPT-3.5 Turbo", "openai/gpt-3.5-turbo", "llm", "openrouter", ['replicate', 'mistral', 'huggingface', 'openai', 'openrouter']],
]
providers = [
    'replicate',
    'mistral',
    'huggingface',
    'openai',
    'openrouter',
]

def list_all():
    """
    Display available models and providers.

    This function prints the available models and providers to the console.
    It helps users understand the options for model and provider selection.
    """
    print("\nmodels:\n")
    for model in models:
        print(f'"{model[0]}": "{model[1]}",')
    print("\nproviders:\n")
    index = 0
    for x in providers:
        print(f'{index}. {x}')
        index += 1



df = pd.read_csv('samples.csv')

voice_samples = {}

# Populate the voice_samples dictionary
for _, row in df.iterrows():
    voice_name = row['voice_name']
    voice_samples[voice_name] = row['url']

# Print some information to verify the data loading
print(f"Loaded data for {len(models)} models")
print(f"Loaded {len(voice_samples)} voice samples")

# Example of how to access the data (WIP):
# print(model_data['Meta: Llama 3.2 3B Instruct']['id'])
# print(model_data['Meta: Llama 3.2 3B Instruct']['context_length'])
# print(model_index['Meta: Llama 3.2 3B Instruct'])  # Get index of a model
# print(index_to_model[0])  # Get model name for index 0
