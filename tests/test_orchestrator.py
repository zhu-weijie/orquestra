from unittest.mock import MagicMock

from orquestra.core import Orchestrator
from orquestra.models import Agent, Task, Workflow


def test_orchestrator_run_with_mocked_openai(mocker):
    """
    Tests the orchestrator with a mocked OpenAI executor to prevent
    real API calls, using a self-contained workflow.
    """
    # 1. Patch the OpenAI class where it's used
    mock_openai_class = mocker.patch("orquestra.agents.openai.OpenAI")

    # 2. Configure the mock response
    mock_create_method = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Mocked LLM output."
    mock_create_method.return_value = mock_response
    mock_openai_class.return_value.chat.completions.create = mock_create_method

    # 3. Create a simple, self-contained workflow for this test
    test_agent = Agent(name="test_writer", provider="openai", model="gpt-5")
    test_task = Task(
        name="writing_task",
        agent="test_writer",
        instruction="Write something creative.",
    )
    test_workflow = Workflow(
        name="Test OpenAI Workflow",
        agents=[test_agent],
        tasks=[test_task],
    )

    # 4. Instantiate and run the orchestrator
    orchestrator = Orchestrator(test_workflow)
    final_context = orchestrator.run()

    # 5. Assert that our mock method was called correctly
    mock_create_method.assert_called_once_with(
        model="gpt-5",
        messages=[{"role": "user", "content": "Write something creative."}],
    )

    # 6. Assert that the final context contains the mocked output
    expected_output = "Mocked LLM output."
    assert final_context["tasks"]["writing_task"]["output"] == expected_output
