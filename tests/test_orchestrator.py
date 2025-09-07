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


def test_orchestrator_run_with_mocked_anthropic(mocker):
    """
    Tests the orchestrator with a mocked Anthropic executor.
    """
    # 1. Patch the Anthropic class where it's used
    mock_anthropic_class = mocker.patch("orquestra.agents.anthropic.Anthropic")

    # 2. Configure the mock response
    mock_create_method = MagicMock()
    mock_response = MagicMock()
    # The response structure is message.content[0].text
    mock_response.content[0].text = "Mocked Claude output."
    mock_create_method.return_value = mock_response

    # 3. Attach the configured create method to the mock instance's path
    mock_anthropic_class.return_value.messages.create = mock_create_method

    # 4. Create a self-contained workflow for this test
    test_agent = Agent(
        name="test_editor",
        provider="anthropic",
        model="claude-3-opus-20240229",
    )
    test_task = Task(
        name="editing_task",
        agent="test_editor",
        instruction="Review for clarity.",
    )
    test_workflow = Workflow(
        name="Test Anthropic Workflow",
        agents=[test_agent],
        tasks=[test_task],
    )

    # 5. Instantiate and run the orchestrator
    orchestrator = Orchestrator(test_workflow)
    final_context = orchestrator.run()

    # 6. Assert that our mock method was called correctly
    mock_create_method.assert_called_once_with(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Review for clarity."}],
    )

    # 7. Assert that the final context contains the mocked output
    expected_output = "Mocked Claude output."
    assert final_context["tasks"]["editing_task"]["output"] == expected_output
