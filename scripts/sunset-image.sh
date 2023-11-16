# Ask for a sunset based on the ChatGPT description of a sunset.
curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "prompt": "A sunset is a beautiful and mesmerizing sight to behold. As the day comes to a close, the sky is filled with an array of colors that slowly blend together to create a stunning display of natures beauty.  The sun descends towards the horizon, casting its warm golden light across the sky. The sky turns shades of orange, pink, and purple as the sun disappears below the horizon. The clouds in the sky catch the colors of the setting sun, creating a breathtaking spectacle.  As the sky darkens, the colors of the sunset deepen into hues of red and violet. The last rays of sunlight paint the sky with an ethereal glow before finally disappearing, leaving behind a peaceful and calming atmosphere. The silhouette of trees and buildings against the colorful sky creates a magical and serene scene",
    "n": 2,
    "size": "1024x1024"
  }'

