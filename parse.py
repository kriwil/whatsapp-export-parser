# -*- coding: utf-8 -*-

from typing import List, Optional, NamedTuple

import re

__file = "./chat.txt"

"""
conversation start pattern:
- 4/28/17, 4:39:44 PM: ‪+62 856‑4338‑8197‬:
- 4/28/17, 4:49:10 PM: Suamiku:
"""


class Message(NamedTuple):
    timestamp: str
    person: str
    contents: List[str]


def parse() -> List[Message]:
    conversations: List[Message] = []

    with open(__file) as chat_file:

        # clean up
        chats = [line.strip() for line in chat_file.readlines()
                 if len(line.strip()) > 0  # empty lines
                 and not line.strip().endswith("joined using this group's invite link")  # group notification
                 and not line.strip().endswith("<‎image omitted>")  # image?
                 ]

        start_parser = re.compile(
            "^(?P<timestamp>\d+\/\d+\/\d+, \d+:\d+:\d+ [A|P]M): (?P<person>[^:]+): (?P<content>.*)")

        current_contents: List[str] = []
        current_timestamp: Optional[str] = None
        current_person: Optional[str] = None

        for line in chats:
            match = start_parser.match(line)

            # starts of conversation
            if match:

                # store the data to the main storage
                if current_person and current_timestamp:
                    message = Message(current_timestamp, current_person, current_contents)
                    conversations.append(message)

                    current_timestamp = None
                    current_person = None
                    current_contents = []

                groupdict = match.groupdict()
                current_person = groupdict.get("person").lstrip("\u202a").rstrip("\u202c").replace("\xa0", " ")
                current_timestamp = groupdict.get("timestamp")
                current_message = groupdict.get("content")
                current_contents.append(current_message)

            else:  # appends all the content
                current_contents.append(line)

        # the last one
        message = Message(current_timestamp, current_person, current_contents)
        conversations.append(message)

    return conversations


def main():
    conversations = parse()

    with open("./chat.md", "w") as write_file:
        # plain text
        for message in conversations:
            content = "\n".join(message.contents)
            person = message.person
            if person != "Suamiku":
                person = message.person[:-3] + "XXX"

            print(f"{person}: {content}\n")


if __name__ == "__main__":
    main()
