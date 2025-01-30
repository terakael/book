import base64
import os
import requests

prompt = """
Core Style Keywords: no outlines, flat color style, solid color shapes, bright colors, vibrant colors, limited color palette, flat shading, no detail, geometric shapes, simple shapes, angular shapes, educational cartoon, clean style, modern cartoon.

Focus: A living room scene, slightly chaotic with toys scattered around.

Action: Noah is crouched low to the ground, his small fists clenched and raised near his head. His body is angled away from Mommy, his back slightly hunched. His mouth is wide open, revealing a glimpse of his tongue, and his face is flushed. His posture is rigid and tense, shoulders pulled up.

Mommy is positioned beside him, kneeling on one knee, her body angled towards Noah. She has reached out one hand, hovering near but not quite touching his back. Her other hand is slightly lifted towards her chest, palm open in a questioning gesture. Her head is tilted very slightly to one side. Her eyebrows are lifted, drawing her forehead into a soft crease. Her expression is a mix of concern and a hint of bewilderment, her lips slightly parted but not smiling. She is positioned to emphasize her approach to Noah, as if attempting to connect with him, but being met with resistance.
    
Character descriptions for AI image generation:
- Noah: A young boy, likely between 2 and 4 years old. He has a round face, a small nose, and a small mouth. He has short, light-colored hair that is slightly messy. His skin is fair. He has small hands and feet. He wears simple, comfortable clothing, likely a t-shirt and shorts.
- Mommy: An adult female with a kind face, and warm eyes. She has medium-length hair, likely tied back. She has a gentle smile. She has a moderate nose, and thin lips. She is wearing comfortable, casual clothing, such as a blouse and jeans. Her skin tone is fair.

It should be a single image, detailing the characters and environment, and nothing else.

I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS.
"""


def stability_ai():
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {os.getenv('STABILITYAI_API_KEY')}",
            "accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
            "model": "sd3-large-turbo",
        },
    )

    if response.status_code == 200:
        with open("./out.webp", "wb") as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))


def dalle3():
    from openai import OpenAI

    openai_client = OpenAI()
    for i in range(5):
        try:
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                style="vivid",
                response_format="b64_json",
            )
            break
        except Exception as e:
            print(str(e))

    with open(f"./dalle3.jpg", "wb") as f:
        image_data = base64.b64decode(response.data[0].b64_json)
        f.write(image_data)


paragraph = "blah blah"
story_summary = "another blah"
prompt = f"""
Provide a scene description suitable for generating an image, focusing on the actions, expressions, and postures of the characters. 
Describe the characters' actions and postures to convey their emotions, rather than explicitly stating the emotions.  
The character descriptions will be provided separately, so make sure to refer to the characters by name. 

Use the following scene as context:
```
{paragraph}
```

This scene is part of the following story summary:
```
{story_summary}
```

The output should be a JSON object with three keys:
```json
{{
    "focus": "a description of the overall scene; environment.",
    "action": "a description of the characters' actions and postures."
}}
```

For example, with the following scene:
```
Mommy came to Noah. Mommy said, "What's wrong?" Noah was still yelling. Mommy could not understand. Noisy sounds did not help.
```

From the following story summary:
```
Noah loses his ball under the sofa and has a tantrum but learns to use quiet words to ask for help and gets the ball back. He learns that words are better than noisy sounds when communicating. Using words to communicate is more effective than making noisy sounds, especially when seeking help.
```

You could output the following:
```json
{{
    "focus": "A living room scene, slightly chaotic with toys scattered around.",
    "action": "Noah is crouched low to the ground, his small fists clenched and raised near his head. His body is angled away from Mommy, his back slightly hunched. His mouth is wide open, revealing a glimpse of his tongue, and his face is flushed. His posture is rigid and tense, shoulders pulled up.  Mommy is positioned beside him, kneeling on one knee, her body angled towards Noah. She has reached out one hand, hovering near but not quite touching his back. Her other hand is slightly lifted towards her chest, palm open in a questioning gesture. Her head is tilted very slightly to one side. Her eyebrows are lifted, drawing her forehead into a soft crease. Her expression is a mix of concern and a hint of bewilderment, her lips slightly parted but not smiling. She is positioned to emphasize her approach to Noah, as if attempting to connect with him, but being met with resistance."
}}
```
"""
