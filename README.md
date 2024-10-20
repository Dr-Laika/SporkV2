# SporkV2
**A Chatbot for VR-Chat powered by a local llm.**

Version two of Spork aims to be a simple and easy-to-use AI Chatbot for VR-Chat. It uses koboldcpp for the llm-backend and requires it to be set up and ready for api calls. However, due to it's functionality, it can also be regarded as a pipeline.

**Functionality:**
A VR-Chat player's voice is turned into text and thus a prompt. Next, further instructions for the llm to follow are injected into the user's prompt. The modified prompt is then processed by the llm and the result is processed into audio and played.

I have not yet decided on a tts-backend to use for the optimal quality-to-speed ratio.

**Features to add:**
-   virtual microphone and speaker for use with a VR-Chat account and client dedicated to the chatbot
-   lm powered creation of a summarized conversation context
