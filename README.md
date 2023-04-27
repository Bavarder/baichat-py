# BAIChat API Python

## Installation

You can install it from PyPi

``` shell
pip install baichat-py
```

## Usage

### Async

``` python
import asyncio

loop = asyncio.get_event_loop() 
hello = loop.run_until_complete(chat.async_ask("Hi"))

print(hello.text)

# => Hello! How can I assist you today?
```

### Context manager

``` python
with BAIChat() as (loop, chat):
    hello = chat.ask("Hi")

    print(hello.text)

# => Hello! How can I assist you today?
```

### Delta

``` python
with BAIChat() as (loop, chat):
    hello = chat.ask("Hi")

    for delta in hello:
        print(delta.text)
    
# => Hello
# => Hello!
# => Hello! How
# => Hello! How may
# => Hello! How may I
# => Hello! How may I assist
# => Hello! How may I assist you
# => Hello! How may I assist you today
# => Hello! How may I assist you today?
```

### Sync

``` python
chat = BAIChat()
print(chat.sync_ask("Hello, how are you?").text)

# => Hello! As an AI language model, I don't have feelings, but I'm functioning properly and ready to assist you. How may I help you today?
```