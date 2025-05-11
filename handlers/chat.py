"""
    AI chat handler
    "1. Start a new chat" - handler
"""
#!/usr/bin/env python3
import typer
import boto3
import json
import time
import random
from typing import List, Dict
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from botocore.exceptions import ClientError
# ..custom
from util.env_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION
)

app = typer.Typer()
console = Console()

class BedrockChat:
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0", max_retries: int = 5):
        """Initialize Bedrock client with the specified model."""
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=AWS_REGION,
        )
        self.model_id = model_id
        self.messages: List[Dict[str, str]] = []
        self.max_retries = max_retries

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})

    def get_response(self, prompt: str) -> str:
        """Get a response from AWS Bedrock using the conversation history."""
        # Add user message to history
        self.add_message("user", prompt)
        
        try:
            # Prepare the request body based on the model
            if "anthropic" in self.model_id:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": self.messages
                }
            elif "claude" in self.model_id:  # Handle other Claude naming patterns
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": self.messages
                }
            else:
                # Default to a generic format for other models
                body = {
                    "prompt": prompt,
                    "max_tokens": 300,
                    "messages": self.messages
                }

            # Make the request to Bedrock with retry logic
            retry_count = 0
            backoff_time = 1  # Start with 1 second backoff
            
            while retry_count <= self.max_retries:
                try:
                    response = self.bedrock_runtime.invoke_model(
                        modelId=self.model_id,
                        body=json.dumps(body)
                    )
                    break  # Break out of the retry loop on success
                except ClientError as e:
                    error_code = e.response.get("Error", {}).get("Code", "")
                    
                    if error_code == "ThrottlingException" and retry_count < self.max_retries:
                        # Add jitter to the backoff time to prevent all clients retrying at the same time
                        jitter = random.uniform(0, 0.1 * backoff_time)
                        sleep_time = backoff_time + jitter
                        
                        print(f"Rate limited. Retrying in {sleep_time:.2f} seconds (attempt {retry_count+1}/{self.max_retries})")
                        time.sleep(sleep_time)
                        
                        # Exponential backoff
                        backoff_time *= 2
                        retry_count += 1
                    else:
                        # If it's not a throttling exception or we've exhausted retries, re-raise
                        raise
                        
            if retry_count > self.max_retries:
                raise Exception("Max retries exceeded due to rate limiting. Please try again later.")
        
            # Parse the response
            response_body = json.loads(response.get("body").read())
            
            # Extract the response text based on the model
            if "anthropic" in self.model_id or "claude" in self.model_id:
                ai_response = response_body.get("content")[0].get("text")
            elif "llama" in self.model_id.lower():
                ai_response = response_body.get("generation", "")
            else:
                # Default response extraction method
                for key in ["completion", "answer", "generated_text", "response", "output"]:
                    if key in response_body:
                        ai_response = response_body.get(key)
                        break
                else:
                    # If we couldn't find a standard key, return the raw response
                    ai_response = str(response_body)
            
            # Add AI response to history
            self.add_message("assistant", ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = str(e)
            if "AccessDeniedException" in error_msg:
                raise Exception(f"AccessDeniedException: You don't have access to the model {self.model_id}. Please request access in the AWS Bedrock console.")
            elif "ThrottlingException" in error_msg:
                raise Exception(f"ThrottlingException: You've been rate-limited by AWS Bedrock. Please wait a moment before trying again.")
            else:
                raise Exception(f"Error getting response from Bedrock: {error_msg}")

# main function
def init_agent_chat(model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"):
    """Interactive chat with AWS Bedrock AI model."""
    console.print(Panel.fit(
        "🤖 [bold blue]Chat with AWS Bedrock Agent[/bold blue]\n"
        "Type your messages and press Enter. Type 'Thank you' or 'Quit' to exit.",
        title="AWS Bedrock Chat", 
        border_style="blue"
    ))
    
    # Check for AWS credentials
    if not AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        console.print("[bold red]Warning:[/bold red] AWS credentials not found in environment variables.")
        console.print("Make sure you have configured your AWS credentials.")
    
    # Initialize the chat
    bedrock_chat = BedrockChat(model_id=model_id)
    
    console.print(f"[dim]Using model: {model_id}[/dim]\n")
    
    # Initial greeting
    console.print("🤖: Hello! How can I help you today?")
    
    while True:
        # Get user input
        user_input = Prompt.ask("[bold green]You")
        
        # Check for exit commands
        if user_input.lower() in ["thank you", "quit"]:
            console.print("\n🤖: Happy to help! Goodbye!")
            break
        
        # Show "thinking" indication
        with console.status("[dim]🤖...[/dim]", spinner="dots"):
            # Get response from Bedrock
            response = bedrock_chat.get_response(user_input)
        
        # Display the response with Markdown formatting
        console.print("🤖:")
        console.print(Markdown(response))
        console.print()  # Add a blank line for readability
