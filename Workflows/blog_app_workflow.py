from llama_index.core.workflow import (Workflow, StartEvent, StopEvent, step, InputRequiredEvent,
                                       HumanResponseEvent, Event)

class BlogWritingEvent(Event):
    def __init__(self, blog_type: str):
        self.blog_type = blog_type

class BlogWriterWorkflow(Workflow):
    @step
    async def information_gathering(self, ev: StartEvent) -> InputRequiredEvent:
        # Emit an InputRequiredEvent to ask the user for input
        return InputRequiredEvent(prefix="Please provide the required property:")

    @step
    async def validate_input(self, ev: HumanResponseEvent) -> InputRequiredEvent | HumanResponseEvent:
        user_input = ev.response
        if self.is_valid_input(user_input):
            return BlogWritingEvent(blog_type=user_input)
        else:
            return InputRequiredEvent(prefix="Invalid input. Please provide the correct property:")

    def is_valid_input(self, user_input: str) -> bool:
        # Example validation logic
        return user_input == "valid"

    def save_property(self, property_value: str):
        # Save the valid property (could be stored in a database or workflow state)
        self.property = property_value

    @step
    async def write_blog(self, ev: BlogWritingEvent) -> InputRequiredEvent:
        # Write the blog using the saved property
        blog_content = f"This blog is about {ev.blog_type}."
        print(blog_content)
        return InputRequiredEvent()

    @step
    async def write_blog_from_feedback(self, ev: HumanResponseEvent) -> StopEvent:
        # Write the blog using the feedback
        blog_content = f"This blog is about {ev.response}."
        print(blog_content)
        return StopEvent()
