class Observable:

    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify(self, name, event):
        for listener in self.listeners:
            listener.notify(name, event)

    def track_events(self):
        events = Events()
        self.add_listener(events)
        return events

class Events:

    def __init__(self):
        self.events = []

    def notify(self, name, data):
        self.events.append((name, data))

    def track(self, observable):
        observable.add_listener(self)
        return observable

    def filter(self, filter_name):
        events = Events()
        for name, data in self.events:
            if name == filter_name:
                events.notify(name, data)
        return events

    def __repr__(self):
        def format_event(name, data):
            part = []
            for key, value in data.items():
                if key != "type":
                    part.append(f"\n    {key}: {repr(value)}")
            return f"{name} =>{''.join(part)}"
        return "\n".join(format_event(name, data) for name, data in self.events)