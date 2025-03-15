import os
import sys
import datetime
import openai


# Different prompts for each day of the week.
prompts = [
  'Today is Monday. Mondays can be tough. Give an inspirational thought.',
  'Today is Tuesday. The week is early. Give a discouraging thought.',
  'Today is Wednesday. Middle of the work week. Give an inspirational thought.',
  'Today is Thursday. The weekend is almost here. Give a funny thought.',
  'Today is Friday. Fun plans tomorrow. Give a sarcastic thought.',
  'Today is Saturday. Relaxing and fun day. Give advice for relaxing.',
  'Today is Sunday. Get ready for the week ahead. Give an insightful thought.',
]

# HTML file static contents.


html = """
<!DOCTYPE html>
<html lang="en" style="box-sizing: border-box; border: 0 solid #e5e7 eb;">
  <head style="box-sizing: border-box; border: 0 solid #e5e7eb;"><meta charset="utf-8"><title>Thought of the day.</title></head>
  <body>
    <main>
      <div style="background:lightblue; padding: 20px 20px;">
	<h1>
          <span style="color:black;">Thought Of the Day - ChatGPT</span>
	</h1>
	<h2>
          <span style="color:darkgrey;">
            {weekday} {month} {day}
	  </span>
	</h2>
	<div style="background:pink; padding: 20px 30px;">
          {text}
	</div>
	<div style="padding: 20px 20px;"></div>
	<div style="color:darkgrey; padding: 20px 30px;">
	  <p>Prompt: {prompt}
	</div>
      </div>
    </main>
  </body>
</html>
"""


def WriteThought(target_dir):
  today  = datetime.datetime.today()
  # Select a prompt based on the day of the week, Monday == 0.
  prompt = prompts[today.weekday()]

  # Generate the message with a chat completion.
  client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  response = client.responses.create(model="gpt-4o",
                                     instructions="You are a clever and funny poet.",
                                     input=prompt)

  text = response.output_text

  # Write info to the log
  fp = open('thought.log.txt', 'a')
  fp.write(today.strftime("%Y %B %d"))
  fp.write(" ")
  fp.write(text)
  fp.write('\n')
  fp.close()         

  # Generate HTML file
  fp = open(target_dir + '/thought.new.html', "w")
  fp.write(html.format(weekday = today.strftime("%A"),
                       month = today.strftime('%B'),
                       day = str(today.day),
                       text = text,
                       prompt = prompt))
  fp.close()

  # If we got this far, remove the old file and move the new one into place.
  if os.path.isfile(target_dir + '/thought.html'):
    os.remove(target_dir + '/thought.html')
  os.rename(target_dir + '/thought.new.html',
            target_dir + '/thought.html')


if __name__ == "__main__":
  # Optional argument is directory for file generation.
  if len(sys.argv) < 2:
    target_dir = '.'
  else:
    target_dir = sys.argv[1]
  WriteThought(target_dir)
