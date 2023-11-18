from openai import OpenAI

def send_message(message):
    few_shot_prompt = """
        Instruction: Read the email content and classify it as 'Yes' if it contains information about a specific event (like a meeting, party, or gathering) with a particular place AND time and 'No' if it does not contain any specific event information.

        Email: "Hi everyone, Just a quick reminder about our study group session for the upcoming exams. We're meeting this Wednesday at 6 PM in the library's main study hall. Bring your notes, and let's ace these tests together! See you there, Alex"
        Classification: Yes

        Email: "Dear Colleagues, Please be reminded of our faculty meeting focused on the new curriculum development. The meeting is scheduled for Friday, 10 AM, in the main conference room (Building A). We'll discuss the proposed changes and gather feedback. Regards, Prof. Elizabeth Johnson"
        Classification: Yes

        Email: "Hello fellow students, As exams are approaching, I wanted to share some helpful study resources with you all. I've compiled a list of useful textbooks, online articles, and practice quizzes. Let's make the most of these materials to prepare well! Best, Jordan"
        Classification: No

        Email: "Team, I've attached the summary of our team's performance for this month. Great work on achieving our targets! Let's keep this momentum going and brainstorm on how we can further improve in the coming month. I look forward to our continued success. Best, Linda"
        Classification: No

        Email: "Hi Team, Just a heads-up that the new version of our design software is now available. It includes several new features and bug fixes. Please ensure you update your software by the end of this week. Let's make the most of these new tools to enhance our creativity! Cheers, Tom"
        Classification: No

        Email: "Hey friends, We're throwing a BBQ party this Saturday at our place and you're all invited! Expect good food, music, and lots of fun. When: Saturday, 5 PM onwards Where: 123 Sunshine Street Feel free to bring your favorite dish or drink. Let's make this a day to remember! Can't wait to see you all, Sarah and Dave"
        Classification: Yes

        Email: "Hello team,I wanted to share with you the latest updates to our project management guidelines. These changes are aimed at improving workflow efficiency and communication within the team.You can find the updated guidelines attached to this email. Please review them by the end of this week and implement the new procedures in your ongoing projects.If you have any questions or need clarification on the new guidelines, feel free to reach out to me."
        Classification: No

        Email: f"{message}"
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
    return (completion.choices[0].message)

if __name__ == '__main__':
    send_message()

