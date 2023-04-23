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

    def filter(self, *filter_names, **fields):
        """
        >>> events = Events()
        >>> events.notify("FOO", {"a": 1})
        >>> events.notify("FOO", {"a": 2})
        >>> events
        FOO =>
            a: 1
        FOO =>
            a: 2

        I can filter on event names:

        >>> events.filter("FOO")
        FOO =>
            a: 1
        FOO =>
            a: 2

        I can filter on data fields:

        >>> events.filter("FOO", a=1)
        FOO =>
            a: 1
        """
        events = Events()
        for name, data in self.events:
            if name in filter_names:
                for field_name, field_value in fields.items():
                    if data.get(field_name) != field_value:
                        break
                else:
                    events.notify(name, data)
        return events

    def collect(self, *fields):
        """
        >>> events = Events()
        >>> events.notify("FOO", {"a": 1})
        >>> events.notify("FOO", {"a": 2})
        >>> events.collect("a")
        [(1,), (2,)]
        """
        items = []
        for name, data in self.events:
            item = []
            for name in fields:
                item.append(data.get(name))
            items.append(tuple(item))
        return items

    def __repr__(self):
        def format_event(name, data):
            part = []
            for key, value in data.items():
                if key != "type":
                    part.append(f"\n    {key}: {repr(value)}")
            return f"{name} =>{''.join(part)}"
        return "\n".join(format_event(name, data) for name, data in self.events)
