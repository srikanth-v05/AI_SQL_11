from langchain_core.prompts.prompt import PromptTemplate
from savedex import final_output





_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE = """{final_output}"""

Prompt_template=_DEFAULT_ENTITY_MEMORY_CONVERSATION_TEMPLATE.format(final_output=final_output)

ENTITY_MEMORY_CONVERSATION_TEMPLATE1 = PromptTemplate(
    input_variables=["entities","history","input"],
    template=Prompt_template,
)
