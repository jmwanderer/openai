curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "quality": "hd",
    "prompt": "Create an image depicting a wild and colorful party of smurfs, gathered together to celebrate the summer solstice! Show the smurfs enjoying drinks, dancing to lively music. Bring the festive atmosphere to life and showcase the joy and excitement of this smurfy celebration!",
    "n": 1,
    "size": "1024x1024"
  }'


#    "prompt": "Imagine a peaceful meadow, with a majestic tree standing tall in the center. The breeze gently rustles its leaves, creating a serene melody. Underneath the shade of the tree, a couple sits on a checkered blanket, surrounded by a spread of delicious picnic treats. As they enjoy their meal, their loyal dog rests peacefully at their feet. The golden sunlight filters through the leaves, casting a warm glow on the scene. Capture this idyllic moment in an image that exudes tranquility and harmony.",

#    "prompt": "Imagine a powerful and timeless image of the female Greek gods gathered in all their glory, their majestic figures towering over the mortal realm. Each deity radiates an aura of divine power as they convene in a grand meeting to determine the fate of the universe. The air crackles as the gods debate passionately, each with their own vision for the future. This classic and awe-inspiring scene captures the drama and magnitude of this pivotal moment in the Greek pantheon.",
