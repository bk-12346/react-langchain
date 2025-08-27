# has all the logic that is going to log all the llm calls

from typing import Any, Dict
from urllib import response
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage, LLMResult

# defined functions taken from callbackhandler langchain documentation
class AgentCallBackHandler(BaseCallbackHandler):
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: list[str],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any,
        ) -> Any:
        """Run when the chat model is started."""
        print(f"***Prompt to llm was:***\n{prompts[0]}")

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
        ) -> Any:
        """Run when the LLM ends running."""
        print(f"***LLM response was:***\n{response.generations[0][0].text}")