# Wedge - Minimal, Local-first Coding Agent

## Disclaimer
This is a personal project. I can not make any guarantees of safety, fitness for purpose, stability, or support.

## How to use
Configure llama-swap on your server.
Adjust settings.json to your match your setup and needs. Then, launch it, optionally with your desired model ID:

```python main.py gpt-oss:20b```

## Dependencies
- Requests
- Colorama

## Commands
- ```/exit``` or ```/quit```: Close Wedge
- ```/danger {0,1,2}``` or ```/safety {0,1,2}```: Change the danger level (see below)
- ```/compact```: Compact the current context window
- ```/clear```: Clear the context window
- ```/model {model-id}```: Change models without clearing context.

## Safety
Wedge has three "danger levels:" 0, 1, and 2. The lower the number, the safer the harness.
- 0: All destructive operations require approval. This is the default.
- 1: The model can freely edit any files in the working directory. All other file edits are auto-denied. Shell commands still require approval. Use this mode to let the model freely work on a repo where you can revert the changes if something goes wrong.
- 2: Everything is auto-approved. Basically "YOLO" mode. Use this in a sandbox/container.

---

## Q&A

### Will there be an installer / standalone build / etc?
I'm honestly not sure yet. On the off chance that other people like this tool and want that, maybe I'll set something up like that. I might even try to get it on PyPi. For now, that's just a lot of extra work for not much reward, and I have other projects I want to get to.

### Why use Wedge?
Most coding agent harnesses *can* be used with self-hosted models, but are really intended to be used with a specific company's cloud models. This creates two very annoying discrepencies:
- The system prompts are huge and quickly fill up small context windows.
- The user has to manually configure all of their models on the client side, even though the server side already provides all the necessary information. Testing and changing models becomes very slow as a result.

Also, most harnesses are just plain overkill for my workflow. I don't have autonomous agents managing production repos 24/7. I just spin up some small models on my gaming PC and use them supervised to help with whatever task I'm working on at the time. That means I don't need planning tools, one-shot support, etc.

### Why not use Pi?
Pi is fantastic. Honestly, most people should probably use Pi instead of this just from a design perspective, let alone the fact that Wedge is a personal project while Pi has real developer support and a community.

There's just a few ways that Pi doesn't fit nicely into my workflow, but Wedge does.

- Most critically, Pi has no safety model built in. Using external plugins or tools to make it safe adds complexity, which is what I'm trying to avoid. A containerized approach makes a ton of sense if you're going all-in on agentic development, but it's kind of ridiculous if all you're trying to do is fire up the harness and say something like "evaluate this function for potential runtime errors."
- I switch between models and configurations fairly often, and Pi (just like every other harness) wants me to configure models on the client side. *Every time* I want to try a new model, change my context window size, etc. I have to also go in and update my harness config. I use llama.cpp proxied through llama-swap, which means that the harness *should* be able to get all this information from the server as long as I provide the model id, but it's not plug-and-play. You can *sort of* get Pi to work this way, but it always feels like a hacky workaround. In contrast, Wedge expects zero local config regarding your models except for the id of your preferred default model.

### Wouldn't it have been easier to make a Pi plugin?
Maybe. Any plugin I could make wouldn't quite be what I want though, since Pi is just fundamentally designed to work differently than how I want it to.

### Then, wouldn't a fork of Pi have been easier?
Probably, yes!

Honestly, if I were *just* worried about making the best possible tool for myself, that's what I would have done. Frankly, I *wanted* to make this. It gave me a chance to make something I can be proud of and that I'll actually use. It also gave me a chance to get very familiar with AI APIs.

### This is awful.
That's not a question, but thank you for noticing.
