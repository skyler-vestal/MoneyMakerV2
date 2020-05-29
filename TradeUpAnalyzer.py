from data_manage.SkinManagerDef import SkinManager


class TUAnalyzer:

    db_path = 'C:\Program Files\MakeMoney\skins.db'
    wear_cutoff = [.07, .15, .38, .45, 1.00]
    conditions = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']

    def __init__(self):
        self.skins = SkinManager(TUAnalyzer.db_path)
        self.tu_lists = []

    def run(self):
        ent_list = []
        for i in range(10):
            ent_list.append(self.skins.collection[0].weapons[2][0].skin_list[3][3])
        profit, outcome_list = self.skins.getOutcomes(ent_list)
        self.tu_lists.append([profit, ent_list, outcome_list])

    def get_print_list(self):
        res_list = []
        for index, tu in enumerate(self.tu_lists):
            tmp_str = "Trade Up #{}:\n".format(index + 1)
            if tu[0] >= 0:
                tmp_str += "\t${:.2f}:\n".format(tu[0])
            else:
                tmp_str += "\t-${:.2f}:\n".format(-tu[0])
            tmp_str += "\t\tCost: ${:.2f}\n".format(TUAnalyzer.__get_price__(tu[1]))
            for ent in tu[1]:
                skin = ent.skin
                condition = TUAnalyzer.__get_word_condition__(ent.sFloat)
                skin_display = str(skin)
                skin_display = skin_display[:skin_display.index('(')]
                tmp_str += "\t\t{} ({}) : ${} ({:.3f})\n".format(
                    skin_display, condition, ent.price, ent.sFloat)
            tmp_str += "\t\t--------OUTCOMES--------\n"
            avg_price = TUAnalyzer.__get_avg_price__(tu[2])
            tmp_str += "\t\tAvg Selling: ${:.2f} (${})\n".format(avg_price, self.skins.getSellerPrice(avg_price))
            prob_list = self.__get_prob_list__(tu[2])
            for skin in prob_list:
                tmp_str += "\t\t{:.2%} | {}\n".format(skin[1], skin[0])
            res_list.append(tmp_str + "\n")
        return "".join(res_list)

    @staticmethod
    def __get_price__(ent_list):
        res = 0
        for ent in ent_list:
            res += ent.price
        return res

    @staticmethod
    def __get_avg_price__(skin_list):
        res = 0
        for skin in skin_list:
            res += skin[2]
        return res / len(skin_list)

    def __get_prob_list__(self, skin_list):
        ret_list = []
        total_skins = len(skin_list)
        for skin in skin_list:
            condition = skin[3]
            if isinstance(skin[3], float):
                condition = TUAnalyzer.__get_word_condition__(condition)
            head_str = "{} - {} ({}): ${} (${})".format(skin[0], 
                    skin[1], condition, skin[2], self.skins.getSellerPrice(skin[2]))
            in_list = False
            for elems in ret_list:
                if head_str == elems[0]:
                    in_list = True
                    elems[1] += 1
                    break
            if not in_list:
                ret_list.append([head_str, 1])
        for ret in ret_list:
            ret[1] /= total_skins
        return sorted(ret_list, key=lambda x:x[1], reverse=True)

    @staticmethod
    def __get_word_condition__(skin_float):
        for i in range(len(TUAnalyzer.wear_cutoff)):
            if skin_float < TUAnalyzer.wear_cutoff[i]:
                return TUAnalyzer.conditions[i]



