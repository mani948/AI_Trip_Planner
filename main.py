
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from starlette.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
async def home():
    return {"message": "AI Trip Planner backend is running"}


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(f"Received question: {query.question}")

        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()

        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved in {os.getcwd()}")

        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            response_messages = output["messages"]

            if response_messages:
                last_message = response_messages[-1]
                final_output = getattr(
                    last_message, "content", str(last_message)
                )
            else:
                final_output = "The agent returned no messages."
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        print("Error while processing the travel query:")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
