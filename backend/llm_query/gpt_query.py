import prompts
import os
import warnings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

_ = load_dotenv(find_dotenv()) # read local .env file
warnings.filterwarnings('ignore')

class LLM_query:
    def __init__(self):
        self.llm_model = "gpt-3.5-turbo"
        self.llm = ChatOpenAI(temperature=0.2, model=self.llm_model)
        self.prompt_dict = {"Terms_Conditions" : prompts.terms_conditions}

    def request(self, db, url, prompt_type="Terms_Conditions"):
        # qeuery mongodb for file_name
        query_result = db.find_one({"url": url})
        file_path = '/data' + query_result["output_file"]
        with open(file_path, 'r') as fh:
            content = "/n".join(fh.readlines())
        
        prompt_template = ChatPromptTemplate.from_template(self.prompt_dict[prompt_type])
        customer_messages = prompt_template.format_messages(
                    policy=content)
        customer_response = self.llm(customer_messages)

        result = db.update_one({"url": url}, {"$set" : {"status":"completed"}})
        return customer_response.content


if __name__ == "__main__":
    k = LLM_query()
    print(k.request(url = '', prompt_type="Terms_Conditions"))
