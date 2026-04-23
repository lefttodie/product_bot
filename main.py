from graph import app
from langchain_core.messages import HumanMessage
from langchain_core.messages import HumanMessage, AIMessage

def run():
    print("Retail AI Assistant (LangGraph)")

    while True:
        user_input = input("\nUser: ")

        # state = {
        #     "messages": [HumanMessage(content=user_input)]
        # }
        history = []
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                history.append(HumanMessage(content=msg["content"]))
            else:
                history.append(AIMessage(content=msg["content"]))

        state = {"messages": history}

        result = app.invoke(state)

        final_msg = result["messages"][-1].content
        print("Agent:", final_msg)


if __name__ == "__main__":
    run()