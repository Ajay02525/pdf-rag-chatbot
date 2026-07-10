from collections import defaultdict


class ChatMemory:
    conversations = defaultdict(list)

    @classmethod
    def add_message(cls, session_id, role, content):

        if session_id not in cls.conversations:
            cls.conversations[session_id] = []

        cls.conversations[session_id].append({"role": role, "content": content})

    @classmethod
    def get_history(cls, session_id):

        return cls.conversations.get(session_id, [])

    @classmethod
    def format_history(cls, session_id):

        history = cls.get_history(session_id)

        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
