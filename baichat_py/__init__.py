__version__ = "0.3.0"
__version_tuple__ = tuple(map(int, __version__.split(".")))

from http import client
from json import dumps, loads
from queue import Empty, Queue
from random import choice
from re import findall
from string import ascii_letters
from threading import Thread
from typing import Generator, Optional

from curl_cffi import requests
from fake_useragent import UserAgent

class CompletionError(Exception):
    pass

class Completion:
    part1 = '{"role":"assistant","id":"chatcmpl'
    part2 = '"},"index":0,"finish_reason":null}]}}'
    regex = rf"{part1}(.*){part2}"

    timer = None
    message_queue = Queue()
    stream_completed = False
    last_msg_id = None

    @staticmethod
    def get_random_string(length: Optional[int] = 15) -> str:
        """Internal method for generating a random string for the first message id"""
        return "".join(choice(ascii_letters) for i in range(length))

    @staticmethod
    def request(
        prompt: str, proxies: Optional[dict[str, str]] = None,
    ):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Host": "chatbot.theb.ai",
            "Origin": "https://chatbot.theb.ai",
            "Referer": "https://chatbot.theb.ai",
            "User-Agent": UserAgent().random,
            "Content-Type": "application/json",
        }

        if not Completion.last_msg_id:
            Completion.last_msg_id = f"chatcmpl-{Completion.get_random_string()}"

        payload = dumps(
            {"prompt": prompt, "options": {"parentMessageId": Completion.last_msg_id}}
        )

        response = requests.post("https://chatbot.theb.ai/api/chat-process", headers=headers, data=payload, impersonate="chrome101", content_callback=Completion.handle_stream_response, proxies=proxies)

        if response.status_code != 200:
            raise CompletionError()
        Completion.stream_completed = True

    @staticmethod
    def create(prompt: str, proxy: Optional[str] = None) -> Generator[str, None, None]:
        Completion.stream_completed = False

        Thread(target=Completion.request, args=[prompt, proxy]).start()

        while not Completion.stream_completed or not Completion.message_queue.empty():
            try:
                message = Completion.message_queue.get(timeout=0.01)
                for message in findall(Completion.regex, message):
                    message_json = loads(Completion.part1 + message + Completion.part2)
                    Completion.last_msg_id = message_json["id"]
                    yield message_json["delta"]

            except Empty:
                pass

    @staticmethod
    def handle_stream_response(response):
        Completion.message_queue.put(response.decode("utf-8"))

    @staticmethod
    def get_response(prompt: str, proxy: Optional[str] = None) -> str:
        response_list = []
        for message in Completion.create(prompt, proxy):
            response_list.append(message)
        return "".join(response_list)

        Completion.message_queue.put(response.decode(errors="replace"))


if __name__ == "__main__":
    while True:
        x = input("> ")
        for token in Completion.create(x):
            print(token, end="", flush=True)
        print("")
