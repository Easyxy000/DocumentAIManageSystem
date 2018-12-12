class EventSystem:
    def __init__(self):
        self.events = {}
    def listen(self, eventName, callback, target):
        self.events.setdefault(eventName, [])
        self.events[eventName].append((callback, target))
    def removeAllListen(self, target):
        for event in self.events.values():
            removeItem = None
            for item in event:
                if item[1] == target:
                    removeItem = item
                    break
            if removeItem is not None:
                event.remove(removeItem)
    def dispatch(self, eventName, *eventData):
        if eventName not in self.events:
            print("event {0} is not be listen".format(eventName))
            return
        for callback, target in self.events[eventName]:
            callback(*eventData)
eventSystem = EventSystem()