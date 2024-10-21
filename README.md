# SporkV2
**A Pipeline / local-llm-powered chatbot for VR-Chat.**

Version two of Spork aims to be a simple and easy-to-use AI Chatbot for VR-Chat. It uses koboldcpp for the llm-backend and requires it to be set up and ready for api calls. However, due to it's functionality, it can also be regarded as a pipeline.

## Functionality:
A VR-Chat player's voice is turned into text and thus a prompt. Next, further instructions for the llm to follow are injected into the user's prompt. The modified prompt is then processed by the llm and the result is processed into audio and then played.

I have not yet decided on a tts-backend to use for an optimal quality-to-speed ratio. So expect some future Sporks err I mean forks.

## Installation and usage:
To install SporkV2 you will have to clone the repo to a location of your choice. Next, run the installer.bat.
To run SporkV2, execute the launcher.bat. 

Functionality for VR-Chat have not yet been implemented. This means that SporkV2 can only be used as a console program for now.

## Features to add:
-   virtual microphone and speaker for use with a VR-Chat account and client dedicated to the chatbot
-   llm powered creation of a summarized conversation context
