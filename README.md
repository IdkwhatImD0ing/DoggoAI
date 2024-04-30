# DoggoAI 🐶 🗣️

<div align="center">
  <video src="https://github.com/IdkwhatImD0ing/DoggoAI/assets/100006999/597863ea-e094-4ee1-a9c3-06fe77e619a0" />
</div>

In the US, there are over **5 million** children hospitalized every single year. At the same time, only **1 in 4 of patients have a caretaker**. In the most critical development period in early childhood, this has shown detrimental impacts on a child's mental health and attachment, accelerating future development issues.

So we asked ourself: how can we enable the **creative potential** of our new generations in ways that could **adapt** to the unique accessibility needs of each patient, creating a universally inclusive platform?

We noticed that many of our siblings had stuffed animal companions - further research from renowned psychology researchers shows that **60-70%** of toddlers form a close bond with their stuffed animals that aids in development of healthy attachment and overall well-being. 

## What it does
Doggo AI is a companion to children staying in hospitals for long period of time. Children can interact with Doggo AI naturally through conversation. Doggo AI will tell stories and teach children who feel isolated and give them the attention they need.

There are 3 main functions:
1. Responsive AI - Doggo AI can converse in real time, responding naturally to interruptions, questions, and statements
2. Emotion Detection - Doggo AI can observe emotions and respond accordingly
3. Dashboard - Parents and caretakers can view information, such as a live conversation transcription and the emotions Doggo AI detects in real time.
![core flow](https://cdn.discordapp.com/attachments/1212193794494042202/1234277604631252992/Screenshot_2024-04-28_at_3.56.50_PM.png?ex=66302618&is=662ed498&hm=a452f9ca003a3ccfe3cff5b27c55905b605ab6cb95f820e673076c9d8d8aed54&)

All of this is bundled into a soft, fluffy plush to encourage kids to hug and interact with Doggo AI!

# The Design Process
To bridge the communication between engineering and design, we began with drawing mockups on paper with the entire team. This helped us solidify the high-level concept of what the l**user flow** of the app would look like.
![sketches](https://cdn.discordapp.com/attachments/1212193794494042202/1234251726056329299/Screenshot_2024-04-28_at_2.15.38_PM.png?ex=66300dfe&is=662ebc7e&hm=6460295d97fddb70c3aed893a8b3ea99ac45c7364e2ac8bb2bab89c9ef2fd523&)

We went a comprehensive review of the design process
![designProcess](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/design_process.png?raw=true)

# Research
We conducted **secondary research** on existing options and competitors  and what they had to offer. We noticed that there was no option that offered **fully interactive, responsive, and adaptive companions for children in hospitals**
![market research](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/market_research.png?raw=true)

We collected responses from **4 patients and caretakers** who shared one thing in common: all of them were frustrated by the lack of access to caretakers and a desire for connection 
![summary](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/research_summary.png?raw=true)

With this information, we formulated a comprehensive problem statement that addressed the root of the issue.
![problem](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/problem.png?raw=true)

We developed 2 user personas of the 2 core stakeholders on our platform: long-term patients and caretakers, to **understand** the unique challenges faced by hospital patients and caretakers.
![user personas](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/user_personas.png?raw=true)

# Designing Solutions
We ideated solutions and prioirtized features that would deliver the highest impact is.
![priorities](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/matrix.png?raw=true)

We designed a  user flow of the main use case and game loop of the platform between **the community platform and the live interactive platform** with the teddy bear
![user flow](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/user_flows.png?raw=true)

We designed **low fidelity** wireframes to conceptualize the idea
![lofi](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/lowfi.png?raw=true)

Then we moved to final **high fidelity** prototypes to envision a simple and intuitive interface for all children to access
![hifi](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/highfi.png?raw=true)

# Accessibility and Inclusitivity in Design
1. **WCAG-complient Branding**: Bold and bright colors and large, bubbly buttons makes interaction natural and easy, no matter the level of mobility the child has. We have high contrast ratios and simple, bold font sizes to increase readability on **any screen size**
![brand](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/branding.png?raw=true) 

2. **Consistent Design, aligning with Nielson Principles**: We have a component library where we store our designs for consistency and ensuring that all interactions are aligned
![components](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/component_library.png?raw=true)

3. **Natural voice interaction**: It doesn't matter what your learning style is, we don't make the user learn any complex user interface. Instead, users can conversate with a **cute stuffed animal** that adapts to the user's interactions. 

# How we built it
* Extensive multi-threading, multi-processing, and asyncio code
      * To optimize and create the natural chat-like interruptions, we utilized multi-processing, multi-threading, and asyncio tasks to enable Doggo AI to simultaneously converse, respond, and detect emotions.
      * Here is the system design we underwent:
![threads](https://github.com/IdkwhatImD0ing/DoggoAI/blob/main/devpost/threads.png?raw=true)
* Hume EVI API
      * To detect emotions and talk emotionally, we used the Hume EVI api
* GPT 4
      * Generate the conversation and interactions
* WebSockets
      * Real-time Communication between Plush and Frontend was accomplished through WebSockets and a WebSocket server hosted thorugh FastAPI.
* Next.js, TypeScript, ShadCN, Tailwind, Figma
      * The frontend dashboard, designed by Jasmine using Figma
* Raspberry Pi and Hardware
      * Our hardware includes a webcam, a dedicated microphone, and a small speaker we stuffed into the plush. Also, the plush as a power bank stuffed inside it as well.
      * We originally had a Raspberry Pi, but unfortunately we pushed it too hard and it got way too hot... D:
* Artisan Craftmanship
      * The plush's hat is hand-sewn by hand, utilizing the best merch out there: Hack Davis 2024. Notice the exquisite Hack Davis patch on the plush's head!

## Accomplishments that we're proud of

## What we learned

## What's next for Doggo AI
