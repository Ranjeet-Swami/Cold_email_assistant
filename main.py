import streamlit as st
import requests
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import os

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.nstayhomes.com/carrers")
    submit_button = st.button("Submit")

    if submit_button:
        if url_input:
            try:
                st.write(f"Fetching data from: {url_input}")

                # Get User-Agent from environment variable or default
                user_agent = os.getenv('USER_AGENT', 'default-user-agent')
                headers = {'User-Agent': user_agent}
                
                # Fetch content using requests with custom User-Agent
                response = requests.get(url_input, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes
                data = clean_text(response.text)
                
                
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                for job in jobs:
                    skills = job.get('skills', [])
                    print(skills)
                    links = portfolio.query_links(skills)
                    print("4")
                    email = llm.write_mail(job, links)
                    print("5")
                    st.code(email, language='markdown')
            except requests.RequestException as e:
                st.error(f"An Error Occurred while fetching the URL: {e}")
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.error("Please enter a valid URL.")

if __name__ == "__main__":
    # Make a request to get the User-Agent string
    #response = requests.get('https://www.google.com')
    #user_agent_string = response.request.headers['User-Agent']
    
    # Set the USER_AGENT environment variable
    #os.environ['USER_AGENT'] = user_agent_string

    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
