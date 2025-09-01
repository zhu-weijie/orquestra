# tests/test_models.py
from orquestra.models import Agent, Task, Workflow


def test_workflow_instantiation():
    """
    Tests that a valid Workflow object can be created without errors.
    """
    # 1. Define Agents
    writer_agent = Agent(
        name="writer_agent",
        provider="openai",
        model="gpt-5",
    )
    editor_agent = Agent(
        name="editor_agent",
        provider="anthropic",
        model="claude-opus-4-1-20250805",
    )

    # 2. Define Tasks
    draft_task = Task(
        name="draft_blog_post",
        agent="writer_agent",
        instruction="Write a blog post about the benefits of AI orchestration.",
    )
    edit_task = Task(
        name="edit_blog_post",
        agent="editor_agent",
        instruction="Review the following blog post for grammar and clarity: {{ tasks.draft_blog_post.output }}",
        depends_on=["draft_blog_post"],
    )

    # 3. Define the Workflow
    blog_workflow = Workflow(
        name="Blog Post Creation",
        description="A workflow to draft and edit a blog post.",
        agents=[writer_agent, editor_agent],
        tasks=[draft_task, edit_task],
    )

    # 4. Assertions to ensure data integrity
    assert blog_workflow.name == "Blog Post Creation"
    assert len(blog_workflow.agents) == 2
    assert len(blog_workflow.tasks) == 2
    assert blog_workflow.tasks[1].depends_on == ["draft_blog_post"]
    print("\nWorkflow model instantiated successfully!")
