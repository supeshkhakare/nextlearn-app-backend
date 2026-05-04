import random

GENERIC_TOPIC_BANK = [

    # Basics
    "basic definition",
    "simple concept",
    "fundamental idea",

    # Direct usage
    "what is used for",
    "simple use case",

    # Identification
    "identify the concept",
    "name the data structure",

    # Properties
    "basic property",
    "simple characteristic",

    # Memory triggers
    "full form",
    "abbreviation meaning",

    # Direct facts
    "fact based question",
    "direct concept recall"
]

# 🔁 Track last topic to avoid repetition
_last_topic = None

def get_random_topic(subject_name: str = None):
    """
    Returns a smartly selected topic for a given subject.

    - Avoids repeating the same topic consecutively
    - Uses a generic topic bank (subject-specific can be added later)
    """

    global _last_topic

    topic = random.choice(GENERIC_TOPIC_BANK)

    # 🔥 Avoid same topic repetition
    while topic == _last_topic:
        topic = random.choice(GENERIC_TOPIC_BANK)

    _last_topic = topic
    return topic
