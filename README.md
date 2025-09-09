Workmate.ai

Workmate.ai is an AI-powered assistant designed to help new joiners, employees, and teams interact seamlessly with company resources.
It integrates RAG (Retrieval-Augmented Generation), LangGraph workflows, and a custom frontend for a complete end-to-end solution.

📂 Project Structure

architecture.py
Contains the LangGraph architecture that powers the AI agent's reasoning and workflow.

prompts.py
Centralized storage of prompts used by the architecture for generating responses.

front_end.py
The user-facing frontend code for interacting with Workmate.ai.

rag_tool_test.ipynb
Jupyter Notebook for building and experimenting with vector stores for RAG integration.

server.py
Backend server setup that handles API requests and routes between the frontend and AI core.

server_utilities.py
Utility functions to support server operations and manage communication with the AI system.

test.py
Testing file currently implementing chat deletion functionality. More features will be added here progressively.

🚀 Features

LangGraph-based AI architecture for agentic reasoning

Retrieval-Augmented Generation (RAG) for context-aware answers

Frontend interface for seamless user interaction

Server & utilities for smooth backend communication

Extendable test framework for new features (starting with chat deletion)
