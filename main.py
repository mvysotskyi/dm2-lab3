"""
FSM of my day.
"""
import random

from enum import Enum
from collections import defaultdict

class FSM:
    """
    FSM of my day.
    """
    class State(Enum):
        """
        States of FSM.
        """
        SLEEP = 0
        EAT = 1
        CODE = 2
        LEARN = 3
        ANGRY = 4

    def __init__(self, state: State = State.SLEEP):
        self.state = state

        self.random_events = {
            "air_alarm": (0.2, "Air Alarm!"),
            "hungry": (0.4, "I'm hungry now!"),
            "tired": (0.5, "I'm so tired!")
        }

        self.transitions = {
            self.State.SLEEP: defaultdict(lambda: self.State.SLEEP, {
                7: self.State.EAT,
                9: self.State.LEARN,
                16: self.State.CODE,
                "air_alarm": self.State.ANGRY,
            }),
            self.State.EAT: defaultdict(lambda: self.State.LEARN, {
                8: self.State.CODE,
                10: self.State.LEARN,
                12: self.State.CODE,
            }),
            self.State.CODE: defaultdict(lambda: self.State.CODE, {
                12: self.State.EAT,
                18: self.State.EAT,
                22: self.State.SLEEP,
                "tired": self.State.SLEEP,
            }),
            self.State.LEARN: defaultdict(lambda: self.State.LEARN, {
                12: self.State.CODE,
                18: self.State.CODE,
                22: self.State.SLEEP,
                "hungry": self.State.EAT,
            }),
            self.State.ANGRY: defaultdict(lambda: self.State.ANGRY, {
                22: self.State.SLEEP,
                5: self.State.SLEEP,
                "tired": self.State.SLEEP,
                "hungry": self.State.EAT,
            }),
        }

        self.states_descriptions = {
            self.State.SLEEP: "I am Sleeping",
            self.State.EAT: "Eating",
            self.State.CODE: "Coding",
            self.State.LEARN: "Learning",
            self.State.ANGRY: "I'm Angry!",
        }

    def next(self, fsm_input: int = 0):
        """
        Next state.
        """
        random_event = random.choice(tuple(self.random_events.keys()) + (None,))
        if random_event and random_event in self.transitions[self.state]:
            if random.random() < self.random_events[random_event][0]:
                self.state = self.transitions[self.state][random_event]
                return self.states_descriptions[self.state], self.random_events[random_event][1]

        self.state = self.transitions[self.state][fsm_input]
        return self.states_descriptions[self.state], None

    def save_fsm(self):
        """
        Save fsm.

        Returns output in format:

        state_before state_after input
        """
        state_names = {"Sleep": self.State.SLEEP, "Eat": self.State.EAT, "Code": self.State.CODE, "Learn": self.State.LEARN, "Angry": self.State.ANGRY}
        state_names = {v: k for k, v in state_names.items()}

        for state, transitions in self.transitions.items():
            for event, next_state in transitions.items():
                if isinstance(event, str):
                    event = str(event) + " " + str(self.random_events[event][0])
                else:
                    event = str(event) + ":00"
                print(f"{state_names[state]} -> {state_names[next_state]} [label=\"{event}\"]")

if __name__ == "__main__":
    fsm = FSM()

    for i in range(24):
        result, random_event = fsm.next(i)
        print(result, random_event if random_event else "")
