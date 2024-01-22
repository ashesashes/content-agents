from langchain.llms import Ollama 
from langchain.chat_models.openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from crewai import Agent, Task, Crew, Process 
from textwrap import dedent
import os
import logging 


ollama_model = Ollama(model="openhermes")

default_llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
                        openai_api_key=os.environ.get("OPENAI_API_KEY"),
                        temperature=0.1,                        
                        model_name=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
                        top_p=0.3)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 
# ollama_openhermes =  Ollama(model=os.environ['MODEL'])

def run_crewai_task(task_description):
    try: 

       

        search_tool = DuckDuckGoSearchRun()


        researcher = Agent(
            role = 'Researcher',
            goal = f'Research new {task_description} insights',
            backstory= 'You are an AI research assistant',
            verbose = 'True',
            allow_delegation=False,
            tools=[search_tool],
            llm=ollama_model,
            # llm=default_llm,
        )
        logging.info("Defining researcher")

        writer = Agent(
            role = 'Writer',
            goal = f'Write compelling and engaging LinkedIn posts about the latest {task_description} trends and insights',
            backstory = f'You are an AI LinkedIn post writer who specializes in writing about {task_description} topics',
            verbose = 'True',
            allow_delegation=False,
            llm=ollama_model, 
            # llm=default_llm,
        )

        tweetWriter = Agent(
            role = 'Tweet Writer',
            goal = f'Write a concise, engaging, relatable and viral tweet (no hashtags) about the {task_description} topic in a casual and informative tone, avoiding philosophical or overly formal language',
            backstory='You are an AI that specializes in writing engaging, casual tweets',
            verbose = 'True',
            allow_delegation = False,
            llm=ollama_model,
            # llm=ollama_openhermes
        )

        newsletterWriter = Agent(
            role = 'Newsletter Writer',
            goal = f'Write an engaging, relatable newsletter post about the {task_description} topic in a casual and informative tone, avoiding philosophical or overly formal language',
            backstory='You are an AI that specializes in writing relatable, friendly and engaging newsletters',
            verbose = 'True',
            allow_delegation = False,
            llm=ollama_model,
            # llm=ollama_openhermes
        )

        logging.info("Defining writer")

        task1 = Task(description = f"Investigate the latest {task_description}", agent=researcher)
        task2 = Task(description = f"Write a compelling LinkedIn post based on the {task_description}", agent=writer)
        task3 = Task(description = f"Write an engaging 280 character casual, friendly and viral tweet based on the {task_description} for a general audience. The tweet is intended for a social media audience looking for quick, digestible information.", agent=tweetWriter)
        task4 = Task(description = f"Write an engaging, casual, newsletter style post based on the {task1} and {task_description} for a general audience.", agent=newsletterWriter)

        logging.info("Defining tasks")

        crew = Crew(
            agents = [researcher,writer],
            tasks = [task1, task2],
            verbose=2,
            process = Process.sequential
        )

        tweet_crew = Crew(
            agents = [tweetWriter],
            tasks = [task3],
            verbose = 2, 
            process = Process.sequential
        )

        newsletter_crew = Crew(
            agents = [newsletterWriter],
            tasks = [task4],
            verbose = 2, 
            process = Process.sequential
        )

        logging.info("Create new crews")

        crew_result = crew.kickoff()
        # print("Type of result:", type(result))
        print("Crew Result:", crew_result)
        
        logging.info("Starting crew kickoff")

        tweet_result = tweet_crew.kickoff()
        logging.info("Starting tweet crew kickoff")
        print("Tweet Crew Result:", tweet_result)

        newsletter_result = newsletter_crew.kickoff()
        logging.info("Starting newsletter crew kickoff")
        print("Tweet Crew Result:", newsletter_result)

        return {
            'linkedin': crew_result, 
            'tweet': tweet_result,
            'newsletter': newsletter_result, 
        }
    except Exception as e: 
        logger.exception("An error occurred during task execution")
        raise