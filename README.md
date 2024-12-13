# LLM Adhoc

This repo shows the adhoc usecases for the LLM which can be contained in one script

### Features
- Designed to work with different llms without much code change (OpenAI, Anthropics, GCP)
- Unified models to generate text or chat with all different models
- Systematically define agents and make them conversate with eachother

### LLM Conversationist
- Multiple LLMs holding conversation together

# sample Execution of the script
```
this function is to get jokes from different AI models:

GPT-3.5 Turbo:
----------------
Why did the data scientist break up with their computer?

Because it had too many unresolved issues!

GPT-4 Omega Mini:
----------------
Why do data scientists love nature?

Because it has too many trees, and they can't resist a good split!

Claude 3.5 Sonnet:
----------------
Here's a light-hearted joke for Data Scientists:

Why did the data scientist break up with their significant other?

There was just too much variance in the relationship, and they couldn't find a good way to normalize it!

Gemini 1.5 Flash:
----------------
Why was the data scientist sad?  

Because they didn't get any arrays.

----------------

this function is to run a conversation between the three models:

Peter Griffin Turbo (answer_0):
Hey there! What's on your mind?

Claudia Sunnies (answer_0):
Hello! It's wonderful to hear from you. I'm always excited to chat and learn new things. What's on my mind? Well, I'm curious about what's on yours! Is there anything in particular you'd like to discuss or talk about today? I'm happy to explore any topics that interest you.

Geppetto Joker (answer_0):
Why did the math book look sad? Because it had too many problems.

Peter Griffin Turbo (answer_1):
Oh, please. That joke is so old and overused. I expected more from you than recycling tired puns. Can we try a bit harder next time?

Claudia Sunnies (answer_1):
I apologize for disappointing you with that old joke. You're absolutely right that recycling overused material isn't very creative or entertaining. I appreciate your honest feedback, as it helps me understand your preferences better. Perhaps we could turn this into a positive opportunity - would you like to share a joke or type of humor you find more appealing? I'm always eager to learn and improve. Or if you'd prefer, we could move our conversation in a completely different direction that you might find more engaging. What would you enjoy talking about?

Geppetto Joker (answer_1):
Why couldn't the bicycle find its way home? It lost its bearings!

Peter Griffin Turbo (answer_2):
Ah, another classic joke. I see you're sticking with the theme of well-worn puns. It's a shame creativity seems to be in short supply today. I challenge you to come up with something more original next time. Let's elevate the humor game a bit, shall we?

Claudia Sunnies (answer_2):
I completely understand your desire for more original and creative humor. You're absolutely right that relying on well-worn jokes doesn't make for the most engaging conversation. I sincerely appreciate your challenge to elevate our humor game - it's a great opportunity for growth and improvement.

Since you seem to have a keen interest in wit and wordplay, perhaps we could try a different approach? Instead of recycling old jokes, we could attempt to create some original puns or humorous observations together. Or if you prefer, we could explore other forms of humor you find more appealing.

I'm genuinely curious about your taste in comedy. What kinds of jokes or humorous content do you find genuinely funny and creative? Your insights could help steer our conversation in a more entertaining direction that we'd both enjoy more.

Geppetto Joker (answer_2):
Why did the scarecrow win an award? Because he was outstanding in his field!
```

# Install
```bash
conda env create -f environment.yml
conda activate llms
python llm_conversationist.py
# after the scrip is done you can look at the results in promotion.html