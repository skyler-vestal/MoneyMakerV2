import random
from TradeUpAnalyzer import TUAnalyzer


def main():
    test_file = open("test.info", 'w', encoding='utf-8')
    tu = TUAnalyzer()
    #tu.run()
    tmp_list = tu.get_all_best()
    #print_list = tu.get_print_list()
    #test_file.write(print_list)
    for index, elem in enumerate(tmp_list):
        stat_str = "Stat-Trak" if elem[3] else ""
        sign = "+" if elem[7] > 0 else "-"
        test_file.write(f"{index}: {elem[1]} - {elem[2]} {stat_str} ({elem[4]})"
                + f" (float: {elem[5]:.4f}) (${elem[6]}) ->" 
                + f" ${elem[7]/10:.2f} | {sign}${abs(elem[8])/10:.2f} ({elem[9]/10:.2f}x)\n")
    test_file.close()


main()