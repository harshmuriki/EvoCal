from openai import OpenAI
import re
from flask import Flask, request, jsonify
import json

def classify_message(message):
    few_shot_prompt = f"""
        Instruction: Read the email content and classify it as '1' if it contains information about a specific event (like a meeting, party, or gathering) with a particular place AND time and '0' if it does not contain any specific event information.

        Email: "Hi everyone, Just a quick reminder about our study group session for the upcoming exams. We're meeting this Wednesday at 6 PM in the library's main study hall. Bring your notes, and let's ace these tests together! See you there, Alex"
        Classification: Yes

        Email: "Hello fellow students, As exams are approaching, I wanted to share some helpful study resources with you all. I've compiled a list of useful textbooks, online articles, and practice quizzes. Let's make the most of these materials to prepare well! Best, Jordan"
        Classification: No

        Email: "{message}"
        Classification:
        """
    client = OpenAI(api_key = "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")

    completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{few_shot_prompt}"}
    ]
    )
    return True if "1" in completion.choices[0].message.content else False

def process_messages(email_string):
    emails = [i.strip() for i in email_string.split("!@#$%^&*()")]
    #remove empty or whitespace only strings
    emails = [i for i in emails if i]
    #links = [re.findall(r'(https?://\S+)', i) for i in emails]    
    
    emails = [re.sub(r'https?://\S+', '', i) for i in emails]
    # Regular Expression to remove empty or incomplete brackets, parentheses, etc.
    pattern = r'\[\]|\(\)|\{\}|[\[\({<](?=[\n\r]|$)'
    emails = [re.sub(r'\n\s*\n', '', i) for i in emails]
    #pattern = r'\[\s*\]|\(\s*\)|\{\s*\}|[\[\(\{]\s*($|\n)'
    emails = [re.sub(pattern, '', email) for email in emails]
    return emails

def extract_events(email):
    extraction_prompt = f"""
    Instruction: Analyze the provided email and extract event information into a list of structured JSON objects. Each JSON object should contain the tags: "name" for the event name, "start_time" for the time of the start of the event in iosformat, "end_time" for the time of the end of the event in iosformat, and "location" for the location of the event. Be aware that:

        - There may be multiple events mentioned in a single email. Each event should be represented as a separate JSON object in the list.
        - Real-world email data can be messy, with random line breaks, irrelevant words, unicode characters, and addresses that may not be related to an event. Ensure robustness in handling such irregularities.
        - Even if there's only one event, the information should still be formatted as a list containing a single JSON object.
        - Your message will be fed to an automatic parser. Return the JSON list and nothing else. This is mission critical.

        Email: {email}
        Extracted Information:
    """
    client = OpenAI(api_key = "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")

    completion = client.chat.completions.create(
    model = "gpt-3.5-turbo-1106",
    response_format = { "type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{extraction_prompt}"}
    ]
    )
    return completion.choices[0].message.content

def master_llm_service(email_string):
    emails = process_messages(email_string)
    print(len(emails))
    #keep only those that return true for classify_message
    emails = [i for i in emails if classify_message(i)]
    print(len(emails))
    if len(emails) == 0:
        return []
    events = [extract_events(i) for i in emails]
    events = [json.loads(i)["events"] for i in events][0]
    return events

app = Flask(__name__)
@app.route('/process_file', methods=['POST'])
def process_file():
    try:
        email_string = request.json['data']
        result = master_llm_service(email_string)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
    pass


# if __name__ == '__main__':
#     # message = "Dear All,I'm excited to announce that our team has achieved a major milestone in the development of our new software. This success is a testament to the hard work and dedication of each team member.In light of this achievement, I would like to acknowledge everyone's effort and encourage you to keep up the excellent work. Our focus now shifts to the next phase of development, where your continued contributions will be crucial.Remember to update your task statuses in our project tracking tool, and let's maintain our momentum going forward."
#     # response = classify_message(message)
#     # print(response)
#     # message = process_messages("email_chinarshital.txt")
#     # print(len(message))
#     # print(extract_events(message[4]))
#     pass
#     with open("output.pkl", "wb") as f:
#         pickle.dump(master_service("email_chinarshital.txt"), f)
    