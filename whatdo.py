import collections

from Config import config

states_list = []
len_max_list = 2
len_all_state = 100
from_define_state = 70 #100フレーム後から判定を始める

history_commands = []

command_list = ["normal", "smile", "surprised", "right", "left"]
add_modes_count = len(mode_list)

def detect_face_state(predict):
    if len(states_list) > len_all_state:
        del(states_list[0:from_define_state])

    states_list.append(predict)

    if len(states_list) == len_all_state:
        count_dict = collections.Counter(states_list[len(states_list) - from_define_state:len(states_list) - 1])
        command_num = count_dict.most_common(1)[0][0]
        command = command_list[command_num]

        what_do = False
        '''
        一度normalに戻る必要がある
        '''
        #
        # if len(history_commands) > 1 and command == history_commands[len(history_commands) - 1]:
        if len(history_commands) > 1:
            if command == "normal" and not history_commands[len(history_commands) - 1] == "normal":
                what_do = history_commands[len(history_commands) - 1]
        #
        history_commands.append(command)
        if len(history_commands) > 3:
            history_commands.pop(0)

        return what_do
