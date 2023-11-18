from openai import OpenAI
import re

def send_message(message):
    few_shot_prompt = f"""
        Instruction: Read the email content and classify it as '1' if it contains information about a specific event (like a meeting, party, or gathering) with a particular place AND time and '0' if it does not contain any specific event information.

        Email: "Hi everyone, Just a quick reminder about our study group session for the upcoming exams. We're meeting this Wednesday at 6 PM in the library's main study hall. Bring your notes, and let's ace these tests together! See you there, Alex"
        Classification: Yes

        Email: "Dear Colleagues, Please be reminded of our faculty meeting focused on the new curriculum development. The meeting is scheduled for Friday, 10 AM, in the main conference room (Building A). We'll discuss the proposed changes and gather feedback. Regards, Prof. Elizabeth Johnson"
        Classification: Yes

        Email: "Hello fellow students, As exams are approaching, I wanted to share some helpful study resources with you all. I've compiled a list of useful textbooks, online articles, and practice quizzes. Let's make the most of these materials to prepare well! Best, Jordan"
        Classification: No

        Email: "Team, I've attached the summary of our team's performance for this month. Great work on achieving our targets! Let's keep this momentum going and brainstorm on how we can further improve in the coming month. I look forward to our continued success. Best, Linda"
        Classification: No

        Email: "{message}"
        Classification: [RETURN ONLY THE DIGIT HERE]
        """
    client = OpenAI(api_key = "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")

    completion = client.chat.completions.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{few_shot_prompt}"}
    ]
    )
    return completion

def process_messages(file_name):
    #TODO: method might need to change as we move away from local txt files
    f = open(file_name, 'r').read()
    emails = [i.strip() for i in f.split("!@#$%^&*()")]
    #remove empty or whitespace only strings
    emails = [i for i in emails if i]
    #links = [re.findall(r'(https?://\S+)', i) for i in emails]    
    emails = [re.sub(r'\n\s*\n', '\n', i) for i in emails]
    emails = [re.sub(r'https?://\S+', '', i) for i in emails]
    # Regular Expression to remove empty or incomplete brackets, parentheses, etc.
    pattern = r'\[\s*\]|\(\s*\)|\{\s*\}|[\[\(\{]\s*($|\n)'
    emails = [re.sub(pattern, '', email) for email in emails]
    return emails
    pass
    

if __name__ == '__main__':
    # message = "Dear All,I'm excited to announce that our team has achieved a major milestone in the development of our new software. This success is a testament to the hard work and dedication of each team member.In light of this achievement, I would like to acknowledge everyone's effort and encourage you to keep up the excellent work. Our focus now shifts to the next phase of development, where your continued contributions will be crucial.Remember to update your task statuses in our project tracking tool, and let's maintain our momentum going forward."
    # response = send_message(message)
    # print(response.usage.prompt_tokens)
    # print(response.usage.completion_tokens)
    # print(response.choices[0].message)
    message = process_messages("email_chinarshital.txt")
    print(len(message))
    print(message[3])