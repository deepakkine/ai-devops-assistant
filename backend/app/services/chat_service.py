from pathlib import Path

from app.core.gemini_client import (
    ask_gemini,
    stream_gemini,
)
from app.core.logger import logger
from app.prompts.prompt_builder import PromptBuilder
from app.rag.retriever import Retriever


class ChatService:

    def _build_prompt(
        self,
        repository: str,
        question: str,
        selected_file: str | None = None,
        history=None,
    ):
        if history is None:
            history = []

        retriever = Retriever(repository)

        logger.info("Received question: %s", question)

        results = retriever.retrieve(question)

        relevant_results = [
            item
            for item in results
            if item["distance"] < 1.15
        ]

        relevant_docs = [
            item["content"]
            for item in relevant_results
        ]

        seen = set()
        sources = []

        for item in relevant_results:
            path = item["metadata"]["path"]

            if path not in seen:
                seen.add(path)

                sources.append(
                    {
                        "path": path,
                        "chunk_id": item["metadata"]["chunk_id"],
                    }
                )

        if selected_file:
            file_path = (
                Path("../data")
                / repository
                / selected_file
            )

            if file_path.exists() and file_path.is_file():
                try:
                    file_content = file_path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )

                    relevant_docs.insert(
                        0,
                        f"""
Selected File:
{selected_file}

{file_content}
""",
                    )

                except Exception as e:
                    logger.warning(
                        "Failed to read selected file: %s",
                        e,
                    )

        prompt = PromptBuilder.build(
            question=question,
            documents=relevant_docs,
            history=history,
        )

        return prompt, sources

    def chat(
        self,
        repository: str,
        question: str,
        selected_file: str | None = None,
        history=None,
    ):
        prompt, sources = self._build_prompt(
            repository,
            question,
            selected_file,
            history,
        )

        answer = ask_gemini(prompt)

        return {
            "answer": answer,
            "sources": sources,
        }

    def stream_chat(
        self,
        repository: str,
        question: str,
        selected_file: str | None = None,
        history=None,
    ):
        prompt, _ = self._build_prompt(
            repository,
            question,
            selected_file,
            history,
        )

        return stream_gemini(prompt)

    def project_overview(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context()

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are an expert Software Architect and Senior DevOps Engineer.

Analyze the repository below.

Repository Context
==================

{context}

Generate a professional repository overview.

Include:

# Executive Summary

# Purpose

# Tech Stack

# Folder Structure

# Main Components

# Architecture

# Data Flow

# Security Observations

# DevOps Observations

# Improvements

# Overall Rating (/10)
"""

        return ask_gemini(prompt)

    def generate_architecture(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(
            k=40,
        )

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are a Principal Software Architect.

Analyze the repository using ONLY the context below.

Repository Context
==================

{context}

Generate the following response.

## Architecture

Explain the architecture of the repository.

## Mermaid

Return ONLY ONE Mermaid diagram.

Example Mermaid:

graph TD
User --> Frontend
Frontend --> Backend
Backend --> Database

Rules:

- Do not ask for the repository.
- Do not say repository context is missing.
- Do not invent technologies that are not present.
- Base everything only on the repository context.
"""

        return ask_gemini(prompt)