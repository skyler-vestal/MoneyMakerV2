import time

class SkinPulse:
    freq_list = [1000, 700, 320, 50]
    req_list = [100, 75, 60, 50]
    update_list = [10, 40, 60, 80]

    def __init__(self, *args):
        self.currTick = args[0] if len(args) > 0 else 1
        print("Starting Tick: {}".format(self.currTick))
        self.__initData__()
        self.timeCheck = time.time()

    def pulse(self):
        if self.__check_time__():
            retList = []
            for index in range(len(SkinPulse.update_list)):
                if self.currTick % SkinPulse.update_list[index] == 0:
                    print("Index Statuses: {}/{}".format(self.current_index, [len(x) for x in self.skin_groups]))
                    skinNum = self.current_index[index]
                    tmpList = self.skin_groups[index][skinNum][:3]
                    tmpList.append(SkinPulse.req_list[index])
                    retList.append(tmpList)
                    self.current_index[index] = (skinNum + 1) % len(self.skin_groups[index])
            self.currTick += 1
            return retList

    def __check_time__(self):
        if time.time() - self.timeCheck > 1:
            self.timeCheck = time.time()
            return True
        return False

    def __initData__(self):
        skin_file = open("requested_data/skinList.info", "r", encoding='utf-8')
        self.skin_list = [x.strip().split(",") for x in skin_file.readlines()]
        skin_file.close()
        self.skin_groups = ([],[],[],[])
        for skin in self.skin_list:
            index = SkinPulse.__skin_group__(int(skin[3]))
            if index != -1:
                self.skin_groups[index].append(skin)
        self.current_index = []
        for index in range(len(SkinPulse.update_list)):
            newIndex = (self.currTick // SkinPulse.update_list[index]) % len(self.skin_groups[index])
            self.current_index.append(newIndex)

    @staticmethod
    def __skin_group__(freq):
        for index in range(len(SkinPulse.freq_list)):
            if freq >= SkinPulse.freq_list[index]:
                return index
        return -1

