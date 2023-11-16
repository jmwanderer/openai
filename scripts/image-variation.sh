curl https://api.openai.com/v1/images/variations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@data/pict.png" \
  -F n=2 \
  -F size="1024x1024"

