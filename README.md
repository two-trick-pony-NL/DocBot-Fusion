# Document Search Proof of Concept

Simple script to use ChatGPT with the knowledge of your own files your own files. Inspired by this [Video](https://youtu.be/9AXP7tCI9PI).

Take a testdrive on https://petervandoorn.streamlit.app

## Installation

- Clone the repo to your own github
- Get a OpenAI API key 
- Add the API key to your `secrets.toml` file in `.streamlit`
- Create a streamlit account and link the repository. 
- Go to the URL from streamlit to play round

## File support usage
Add data to the `data` folder. Currently we only support .txt and .pdf files. 
Restarting the server will add the new files into the model. 

