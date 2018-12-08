class EventSystem:
    def __init__(self):
        self.events = {}
    def listen(self, eventName, callback, target):
        self.events.setdefault(eventName, [])
        self.events[eventName].append((callback, target))
    def removeAllListen(self, target):
        for i in range(len(self.events)):
            if target == self.events[i][1]:
                del self.events[i]
                break
    def dispatch(self, eventName, *eventData):
        if eventName not in self.events:
            print("event {0} is not be listen".format(eventName))
            return
        for callback, target in self.events[eventName]:
            callback(*eventData)
eventSystem = EventSystem()