from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOllama(model="llama3-chatqa")

# Create a simple JSON prompt
prompt = ChatPromptTemplate.from_template(
    "Return information about {topic} in JSON format with keys 'name' and 'uses'."
)

# Format prompt
final_prompt = prompt.format(topic="Python")

# LLM call
response = llm.invoke(final_prompt)

# Parse output into JSON
parser = JsonOutputParser()
parsed = parser.parse(response.content)

print(parsed)
print("Language:", parsed["name"])
print("Uses:", parsed["uses"])
