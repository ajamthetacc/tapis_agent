import asyncio
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from opentelemetry import trace # For manual span creation
from phoenix_setup import init_tracer

# 1. Setup Environment and Tracing
load_dotenv()
init_tracer()
tracer = trace.get_tracer(__name__)
client = OpenAI() # Automatically uses OPENAI_API_KEY from .env

# 2. Define the local MCP server process
server_params = StdioServerParameters(
    command="python",
    args=["tapis_mcp_server.py"]
)

async def run_agent(user_prompt: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Discover tools from local Tapis MCP
            mcp_tools = await session.list_tools()
            
            # Map MCP tools to OpenAI format
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in mcp_tools.tools
            ]

            # 2. The System Prompt defines the routing behavior
            messages = [
                {
                    "role": "system", 
                    "content": (
                        "You are a Tapis Assistant. "
                        "If the user asks a conceptual or 'how-to' question, use the 'search_docs' tool. "
                        "If the user asks about live systems, status use the Tapis system tools."
                    )
                },
                {"role": "user", "content": user_prompt}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls

            if tool_calls:
                for tool_call in tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    # Tracing the specific tool chosen (RAG vs Systems)
                    with tracer.start_as_current_span(f"execute_{name}") as span:
                        span.set_attribute("routing_category", "conceptual" if name == "search_docs" else "systems")
                        
                        result = await session.call_tool(name, arguments=args)
                        
                        # 4. Final Answer Generation
                        final_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages + [
                                response.choices[0].message,
                                {"role": "tool", "tool_call_id": tool_call.id, "content": str(result.content)}
                            ]
                        )
                        answer = final_response.choices[0].message.content
                        print(f"\nFinal Answer: {answer}")
                        return answer
            else:
                    answer = assistant_message.content
                    return answer

if __name__ == "__main__":
    # Test 1: Routing to RAG
     asyncio.run(run_agent("How does Tapis handle security?"))
    
    # Test 2: Routing to Tapis Systems
    #asyncio.run(run_agent("What systems are online right now?"))

