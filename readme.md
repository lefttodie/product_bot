# 🛍️ Retail AI Assistant (Agentic System)

##  Overview

This project implements a **Retail AI Assistant** that simulates two real-world business roles:

* **Personal Shopper (Revenue Agent)** → Recommends products based on user preferences
* **Customer Support Assistant (Operations Agent)** → Handles order queries and return decisions

The system is built using an **Agent + Tools architecture**, ensuring:

* No hallucination
* Structured reasoning
* Real-time decision-making using data

---

##  Features

*  Intelligent product recommendations with multi-constraint filtering
*  Order lookup and validation
*  Return eligibility reasoning based on business rules
*  Tool-based agent (no hardcoded responses)
*  Strict out-of-scope rejection
*  Graph-based execution (LangGraph)

---

##  Project Structure

```
project/
│── main.py              # CLI entry point
│── graph.py             # Agent workflow (LangGraph)
│── tools.py             # Tool implementations (business logic)
│── data_loader.py       # Loads datasets
│── products.csv         # Product inventory
│── orders.csv           # Orders data
│── policy.txt           # Return policies
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

---

##  Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd project
```

### 2. Create virtual environment (optional but recommended)

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Setup environment variables (`.env`)

```
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

---

##  Running the Application (CLI)

```
python main.py
```

Example queries:

```
I need a modest evening dress under 300 in size 8 on sale
Can I return order 1043?
Show me fitted dresses under 250
```

---

##  Architecture

###  Agent + Tools Design

The system separates:

* **Reasoning (LLM Agent)**
* **Execution (Tools)**

This ensures:

* Reliability
* No hallucination
* Clear decision-making

---

###  Tools Implemented

| Tool Name         | Description                                       |
| ----------------- | ------------------------------------------------- |
| `search_products` | Filters products based on price, size, tags, sale |
| `get_product`     | Fetch product details                             |
| `get_order`       | Retrieve order details                            |
| `evaluate_return` | Apply return policy rules                         |

---

###  Execution Flow

```
User Input
   ↓
Agent (LLM)
   ↓
Tool Call (if needed)
   ↓
Tool Execution
   ↓
Agent Reasoning
   ↓
Final Response
```

---

##  Hallucination Prevention

The system avoids hallucination using:

*  Mandatory tool usage for data
*  Strict domain restriction (products, orders, returns only)
*  Deterministic backend logic for return decisions
*  Explicit error handling (no fake outputs)

---

##  Example Scenarios

###  Shopping Scenario

**Input:**

```
I need a modest evening dress under 300 in size 8 on sale
```

**Behavior:**

* Filters by price, size, tags, sale
* Checks stock availability
* Sorts by bestseller score
* Returns best matches with reasoning

---

### 📦 Support Scenario

**Input:**

```
Can I return order 1043?
```

**Behavior:**

* Fetches order
* Applies return policy
* Checks time window and clearance rules
* Returns decision with explanation

---

### ⚠️ Edge Case

**Input:**

```
Check order 9999
```

**Output:**

```
Order not found
```

---

## 🎥 Demo Requirements

The project includes a demo video covering:

*  2 Shopping scenarios
*  2 Support scenarios
*  1 Edge case (invalid order)
*  Code walkthrough with explanation

---

##  Docker Deployment (Azure Ready)

### Build & Push Image

```
docker buildx build --platform linux/amd64 --provenance=false -t <acr-name>.azurecr.io/product_bot:v1 --push .
```

### Notes:

* Use `--platform linux/amd64` for Azure compatibility
* Use `--provenance=false` to avoid Azure Container Apps error

---

##  Key Highlights

* 🔹 Agentic AI with tool calling
* 🔹 Real-world retail simulation
* 🔹 Business-rule-based reasoning
* 🔹 Clean modular design
* 🔹 Production-ready structure

---

##  Conclusion

This project demonstrates how to build a **reliable, explainable, and scalable AI assistant** using:

* Tool-based architecture
* Structured reasoning
* Controlled execution flow

It is designed to closely simulate real-world e-commerce AI systems.

---

##  Author

**Aman Singh**
AI/ML Engineer | Agentic AI | RAG Systems | Deep Learning

---
