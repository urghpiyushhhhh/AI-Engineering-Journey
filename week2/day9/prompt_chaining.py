import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq
from time import sleep


# --------------------------------
# 1. ENVIRONMENT SETUP
# --------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing!")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"   

jd="""
Full Stack + AI Developer Hiring Drive | Batch 2027
Greetings from the Placement Cell!

We are pleased to inform you that a Full Stack + AI Developer Hiring Drive is being conducted for the 2027 batch. Eligible students interested in pursuing a career in full-stack development and artificial intelligence are invited to register for this opportunity.

1. Hiring Details
Role: Full Stack + AI Developer

Eligible Batch: 2027

Eligible Courses: B.Tech, MCA & M.Tech

Joining Location: Jaipur, Rajasthan

Drive Date: To be announced shortly after completion of registrations.

2. Compensation Structure
Employment Stage	Duration	Compensation
Internship	4 Months	10,000 per month
Trainee	4 Months	18,000 per month
Full-Time Employment	After successful completion	7 LPA
Full-Time CTC Breakup:

Fixed Compensation: 6 LPA

Variable Compensation: 1 LPA

3. Service Agreement
A 24-month service agreement will be applicable.

The agreement period will include both the internship (4 months) and trainee (4 months) phases.

4. Registration Details (All interested students are required to fill out this form first and then apply on Superset.
Registration Form: [FORM LINK)

Last Date to Register: 28 November 2026

Important Instructions
Interested and eligible students are required to complete their registration before the deadline.

Students are advised to review the attached Job Description (JD) carefully before applying.

The recruitment drive schedule and further selection process details will be communicated after the registration process.

Interested students are advised to complete their registration within the stipulated deadline.

5. requied skills: 
JavaScript, Python, React.js, Node.js,
Express.js, MongoDB, MySQL,
HTML, CSS, Tailwind CSS,
REST APIs, Git, GitHub, tensorflow, docker 
"""

resume = """
Name: Piyush Gehlot

Education:
B.Tech in Computer Science & Engineering
JECRC University, Jaipur (2023–2027)

Experience:
Internship experience at Xebia.

Skills:
JavaScript, Python, React.js, Node.js,
Express.js, MongoDB, MySQL,
HTML, CSS, Tailwind CSS,
REST APIs, Git, GitHub

Projects:
Built an AI Resume Analyzer using Python
and LLMs that evaluates resumes against
job descriptions and ranks the top 2 candidates.

Developed full-stack web applications
using the MERN stack.

Built RESTful APIs with Node.js,
Express.js and MongoDB.

"""

def askLLM(system_prompt, user_prompt):
    sys_msg = {
        "role" : "system",
        "content" : system_prompt
    }

    user_msg = {
        "role" : "user",
        "content" : user_prompt
    }

    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)
    ans = response.choices[0].message.content
    return ans



def step1_res_extraction():
    system_prompt = """
        you are a professional HR assistant  extract the skills from the candidate's resume provided.
        only return skill no other information.
        DO NOT invent any skills by yourself 
    """

    user_prompt = f"""
        extract the skills from the resume
        {resume}
    """
    return askLLM(system_prompt, user_prompt)

def step2_jd_extraction():
    system_prompt = """
        you are a professional HR assistant  extract the skills from the Job description provided.
        only return skill no other information.
        DO NOT invent any skills by yourself.

        output format :
        separate the skills using commas.
        just return the comma separated skills do not return any other filler information 
    """

    user_prompt = f"""
        extract the skills from the JD
        {jd}
    """
    return askLLM(system_prompt, user_prompt)

def step3_match(candidate, jd):
    system_prompt = """
        you are a professional HR assistant. compare the skills of candidate and the skills require in the JD.
        and produce a final score between 1 and 100

        also produce a short verdict wheather the candidate is a good fir or not

        output format: 
        1. return all skills that the person should have by looking at the jd 
        2. return resume's skills
        3. return matched skills
        4. return missing skills

        all the skills that you return should be in comma-separated format
    """

    user_prompt = f"""
        compare and match the skills
        JD : {jd}
        Canditate : {candidate}
    """

    return askLLM(system_prompt, user_prompt)

candidate = step1_res_extraction()
sleep(2)
jd = step2_jd_extraction()
sleep(2)
score = step3_match(candidate, jd)
print(score)