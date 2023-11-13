import os
import openai
from azure.identity import AzureCliCredential

# if "openai.azure.com" not in os.environ["no_proxy"]:
#     os.environ["no_proxy"]=os.environ["no_proxy"]+",openai.azure.com"

# os.environ["http_proxy"]="proxy.jpmchase.net:10443"
# os.environ["https_proxy"]="proxy.jpmchase.net:10443"

# venv_name = "openai"  # change as needed
# os.environ["PATH"] = os.environ["PATH"] + f":/opt/omniai/work/instance1/jupyter/venvs/{venv_name}/bin"

from transformers import GPT2Tokenizer
import tiktoken

# Load the GPT-3.5 tokenizer
# Initialize the tiktoken tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
gpt_version = "gpt-4-0613"
tokenizer = tiktoken.encoding_for_model("cl100k_base")


def truncate_prompt(input_prompt, max_tokens=4000):
    # Tokenize the input prompt using GPT-2 tokenizer
    input_prompt_tokens = tokenizer.encode(
        input_prompt, 
        # add_special_tokens=False, 
        # return_tensors="pt"
    )

    # Calculate the number of tokens in the input prompt
    num_tokens = len(
        input_prompt_tokens
        # input_prompt_tokens[0]
    )

    # Check if the input prompt exceeds the maximum token limit
    if num_tokens > max_tokens:
        # If it exceeds, you need to truncate it
        # Calculate how many tokens to keep from the beginning
        num_tokens_to_keep = max_tokens - 500  # Reserve 50 token for the model's response
        truncated_input_tokens = (
            input_prompt_tokens[:num_tokens_to_keep]
            # input_prompt_tokens[:, :num_tokens_to_keep]
        )

        # Decode the truncated input
        truncated_input_text = tokenizer.decode(
            truncated_input_tokens
            # truncated_input_tokens[0], 
            # skip_special_tokens=True
        )

        return truncated_input_text
    else:
        # If it doesn't exceed the limit, you can use the original input prompt as-is
        return input_prompt


def get_completion(doc, question):
    prompt = f"""
        Based on the given Document, {question} Please only provide the exact answer string (no paraphrasing).

        Use the following format:
        Answer:<answer string>

        Document:
        ```{doc}```
    """
    # print(prompt)

    messages = [{"role": "user", "content":truncate_prompt(prompt)}]

    retry = True
    while retry:
        try:
            response = openai.ChatCompletion.create(
                # engine = "gpt-3.5-turbo",
                engine = gpt_version,   # global param
                messages = messages,
                temperature = 0,
                # max_tokens = 50
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            error_message = str(e).lower()
            if 'rate limit' in error_message and 'second' in error_message:
                print(' sleep and retry')
                retry = True
                time.sleep(10)
            elif "maximum context length" in error_message:
                return 
            else:
                raise(e)


