# Events based off https://www.youtube.com/watch?v=oNalXg67XEE&feature=youtu.be & https://www.reddit.com/r/Python/comments/lngfnw/i_never_knew_events_were_this_powerful_a_pythonfrom collections import defaultdict
from collections import defaultdict

subscribers = defaultdict(list)

def subscribe(event_type: str, fn):
    subscribers[event_type].append(fn)

def post_event(event_type: str, data):
    for fn in subscribers[event_type]:
        fn(data)
