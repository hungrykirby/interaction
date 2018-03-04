import win32com.client as wincl
import setup
import modify
import whatdo

class SpeakWCommand:
    '''コマンドから生成するよ'''
    speak_line = -1
    scripts = []
    #speak = None
    is_train = False

    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Rate = -3
    speak.Priority = 1
    client = None

    def __init__(self, scripts, is_train, client):
        self.scripts = scripts
        self.is_train = is_train
        self.speak.Speak("Hello Debugging", 3)
        self.client = client

    def speak_w_command(self, add, predict):
        print("")
        command_list = whatdo.detect_face_state(predict)
        print("add:", add, predict, command_list)
        if not command_list is None and not command_list[0] == False and not command_list[0] is None:
            command = command_list[0]
            s = self.speak
            ss = self.scripts
            msg = setup.osc2.osc_message_builder.OscMessageBuilder(address = "/command")
            msg.add_arg(command)
            m = msg.build()
            self.client.send(m)
            if command == "right":
                s.Skip("SENTENCE", 1)
                if self.speak_line < len(ss) - 1:
                    self.speak_line += 1
                    if self.is_train == "t":
                        print(ss[self.speak_line], modify.modify(ss[self.speak_line]))
                    s.Speak(modify.modify(ss[self.speak_line]), 3)
                    #s.Speak("Hello World", 3)
            elif command == "left":
                s.Skip("SENTENCE", 1)
                if self.speak_line > 1:
                    self.speak_line -= 1
                    if self.is_train == "t":
                        print(ss[self.speak_line])
                    s.Speak(modify.modify(ss[self.speak_line]), 3)
            elif command == "surprised":
                s.Skip("SENTENCE", 1)
                if 0 <= self.speak_line and self.speak_line < len(ss) - 1:
                    if self.is_train == "t":
                        print(ss[self.speak_line])
                    s.Speak(modify.modify(ss[self.speak_line]), 3)
        msg2 = setup.osc2.osc_message_builder.OscMessageBuilder(address = "/line")
        msg2.add_arg(self.speak_line)
        m2 = msg2.build()
        self.client.send(m2)
