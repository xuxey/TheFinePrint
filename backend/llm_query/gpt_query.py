import warnings
from llm_query.prompts import terms_conditions
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # read local .env file
warnings.filterwarnings('ignore')


class LLM_query:
    def __init__(self):
        self.llm_model = "gpt-3.5-turbo"
        self.llm = ChatOpenAI(temperature=0.2, model=self.llm_model)
        self.prompt_dict = {"Terms_Conditions": terms_conditions}

    def request(self, input_file, output_file, prompt_type="Terms_Conditions"):
        with open(input_file, 'r') as fh:
            content = fh.readlines()

        print("LLM:Read the input file")

        prompt_template = ChatPromptTemplate.from_template(
            self.prompt_dict[prompt_type])
        customer_messages = prompt_template.format_messages(
            policy=content)
        customer_response = self.llm(customer_messages)

        print(customer_response)

        print("LLM:writing to output file")

        with open(output_file, 'w') as fh:
            fh.writelines(customer_response.content)


if __name__ == "__main__":
    k = LLM_query()
    print(k.request(url='', prompt_type="Terms_Conditions"))
