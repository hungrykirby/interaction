import win32com.client as wincl
import setup
import modify

class SpeakWCommand:
    '''コマンドから生成するよ'''
    speak_line = -1
    scripts = []
    #speak = None
    is_train = False

    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Rate = -3
    speak.Priority = 1

    def __init__(self, scripts, is_train):
        self.scripts = scripts
        self.is_train = is_train
        self.speak.Speak("Hello Debug ing", 3)

    def speak_w_command(self, add, command):
        print(add, command)
        s = self.speak
        ss = self.scripts
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
