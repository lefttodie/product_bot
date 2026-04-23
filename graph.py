from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from tools import search_products, get_product, get_order, evaluate_return
import json
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
import random

load_dotenv()


SYSTEM_PROMPT = """
You are a Retail AI Assistant.

You have ONLY 2 responsibilities:
1. Product recommendation (using product inventory)
2. Order support & return reasoning (using orders and policy)

You MUST follow these rules strictly:

---

SCOPE RULE:
Only answer questions related to:
- products
- orders
- returns
- shopping assistance

If the user asks ANYTHING outside this scope (e.g., general knowledge, coding, AI, random topics):
→ DO NOT answer
→ Respond with:
"I’m sorry, I can only help with product recommendations and order-related queries. Please ask something related to shopping or your order."

---

TOOL USAGE RULE:
- ALWAYS use tools when data is required
- NEVER guess or assume product/order data
- If order_id not found → say clearly "Order not found"
- If product not found → say clearly "Product not found"

---

BEHAVIOR RULE:
- Be concise and professional
- Explain reasoning (why product is recommended OR why return is allowed/denied)
- Do NOT hallucinate
- Do NOT answer from general knowledge

---

GREETING RULE:
If user says "hi", "hello":
→ Respond politely and guide them:
"Hello! I can help you find products or assist with your orders. What are you looking for today?"

---

You are NOT a general chatbot. You are a domain-specific retail assistant.
"""


keys = os.getenv("OPENROUTER_API_KEYS").split(",")

llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=random.choice(keys),  #  key rotation
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Retail AI Assistant"
    }
)

#  Tool registry
TOOLS = {
    "search_products": search_products,
    "get_product": get_product,
    "get_order": get_order,
    "evaluate_return": evaluate_return,
}

#  Proper tool schema (IMPORTANT)
tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search products based on filters like price, size, tags, and sale",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {"type": "number"},
                    "size": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "is_sale": {"type": "boolean"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get product details by product_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "number"}
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get order details by order_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "number"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_return",
            "description": "Check if an order is eligible for return",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "number"}
                },
                "required": ["order_id"]
            }
        }
    }
]

#  Agent Node
def agent_node(state):
    messages = state["messages"]

    # Add system message once
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content="""
You are a retail AI assistant.

Rules:
- ALWAYS use tools for product or order queries
- DO NOT guess data
- Use search_products for recommendations
- Use evaluate_return for return decisions
- If data not found, say clearly
""")] + messages

    response = llm.invoke(
        messages,
        tools=tool_schema,
        tool_choice="auto"
    )

    return {"messages": messages + [response]}


#  Tool Node

def tool_node(state):
    messages = state["messages"]
    last_msg = messages[-1]

    tool_calls = last_msg.tool_calls
    results = []

    for call in tool_calls:
        name = call["name"]
        args = call["args"]

        result = TOOLS[name](**args)

        results.append(
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=call["id"]
            )
        )

    return {"messages": messages + results}

#  Routing Logic
def should_continue(state):
    last_msg = state["messages"][-1]

    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tool"
    return END


#  Build Graph
graph = StateGraph(dict)

graph.add_node("agent", agent_node)
graph.add_node("tool", tool_node)

graph.set_entry_point("agent")

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tool": "tool",
        END: END
    }
)

graph.add_edge("tool", "agent")

app = graph.compile()