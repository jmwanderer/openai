curl https://api.openai.com/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
     "model": "gpt-3.5-turbo-instruct",
     "prompt": "Write a prompt for image creation that describes a fun party of smurfs, celebrating the soltice. There are drinks and music and dancing with some bad behavior.",
     "max_tokens": 1000,
     "temperature": 0.7
   }'

