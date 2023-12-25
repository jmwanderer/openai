import requests
import sys
import os

#
# Exercise the calls for the REST API
# - creates a new document
#

URL_PRE = "http://localhost:5000/"
URL_PRE_PROD = "https://www.nov95.net/docserve/"
AUTH_KEY=os.getenv('AUTH_KEY', '')
GPT_USER="Openai-Ephemeral-User-Id"
GPT_CONVO="Openai-Conversation-Id"


def url(doc_id=None, element_type=None, index=None):
  url = URL_PRE + "docs"
  if doc_id is not None:
    url += f"/{doc_id}"
  if element_type is not None:
    url += f"/elements/{element_type}"
  if index is not None:
    url += f"/{index}"
  print(f"url: {url}")
  return url

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def run_pop():
  response = requests.post(url(), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user1", GPT_CONVO: "c1"},
                           json={ "title" : "A user1 document",
                                  "doc_id" : os.urandom(2).hex()                                  
                                 })
  print(str(response.json()))

  response = requests.post(url(), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user2", GPT_CONVO: "c2"},
                           json={ "title" : "first doc title",
                                  "doc_id" : "Another doc id"
                                 })
  print(str(response.json()))
  doc_id = response.json()['doc_id']
  user_id = response.json()['user_id']  

  data = { "value": "This is the document title" }
  response = requests.post(url(doc_id, 'title'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user2", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))

  data = { "value": "Abstract for the document" }
  response = requests.post(url(doc_id, 'abstract'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user2", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))

  data = { "value": """
Introduction: Setting the Tone for Motivation
The Power of Positive Thinking
a. Understanding Positive Thinking
b. Real-life Examples of Positive Mindsets
Persistence in the Face of Challenges
a. Stories of Resilience
b. Strategies for Maintaining Persistence
Setting and Pursuing Meaningful Goals
a. Importance of Goal Setting
b. Steps to Identify and Achieve Goals
Harnessing Inner Strength
a. Identifying Personal Strengths
b. Techniques to Cultivate Inner Strength
Conclusion: Embracing the Journey Towards Excellence
  """}
  response = requests.post(url(doc_id, 'outline'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))

  data = { "value": "Introduction" }
  response = requests.post(url(doc_id, 'heading'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))


  data = { "value": """
The introduction for "The Best Document" has been written. It sets a motivational tone, emphasizing that the document is more than just words—it's a transformative journey. It highlights the importance of motivation in personal and professional success and promises to delve into the practical applications of positive thinking, resilience, goal-setting, and harnessing inner strength. The introduction aims to inspire readers to take the first step towards their aspirations and to persevere through challenges, welcoming them to a journey of transformation and empowerment.
  """}
  response = requests.post(url(doc_id, 'text'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))

  # Image
  data = { "value": "image.png" }
  response = requests.post(url(doc_id, 'image'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                           json=data)
  image_index = response.json()['index']
  print(str(response.json()))

  # Upload an image
  filename = 'water.png'
  filepath = f'test/{filename}'
  f = open(filepath, 'rb')
  data = { 'file': (filename, f),
           'Content-Type': 'image/png',
           #'Content-Length': l            
          }
  
  image_url = URL_PRE + f"images/{doc_id}/{image_index}?q={user_id}"
  print(f"post image with {image_url}")
  response = requests.post(image_url, files=data)
  f.close()
  print(str(response))

  data = { "value": """
  another paragraph
  """}
  response = requests.post(url(doc_id, 'text'), auth=BearerAuth(AUTH_KEY),
                           headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                           json=data)
  print(str(response.json()))
  element_index = response.json()['index']

  

  # Overwrite text
  data = { "value": """
  Here we have more information that is replacing the previous short paragraph
  """}
  response = requests.put(url(doc_id, 'text', element_index),
                          headers={ GPT_USER: "user3", GPT_CONVO: "c1"},
                          auth=BearerAuth(AUTH_KEY),
                           json=data)
  print(str(response.json()))

  # Read doc element
  response = requests.get(url(doc_id, 'text', element_index),
                          headers={ GPT_USER: "user3", GPT_CONVO: "c1"},
                          auth=BearerAuth(AUTH_KEY))
  print(str(response.json()))

  # Read the document
  response = requests.get(url(doc_id),
                          headers={ GPT_USER: "user3", GPT_CONVO: "c2"},
                          auth=BearerAuth(AUTH_KEY))
  data = response.json()
  print(str(data))
  doc_view_url = data['doc_view_url']
  doc_id = data['doc_id']
  user_id = data['user_id']

  print(f"doc view url: {doc_view_url}?doc_id={doc_id}&q={user_id}")

  # List docs
  response = requests.get(url(), auth=BearerAuth(AUTH_KEY),
                          headers={ GPT_USER: "user3", GPT_CONVO: "c1"},)
  print(str(response.json()))
  

if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == 'prod':
    URL_PRE = URL_PRE_PROD
  print("Running against %s" % URL_PRE)
  run_pop()

  
    
  

