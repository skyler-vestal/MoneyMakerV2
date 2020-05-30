from TradeUpAnalyzer import TUAnalyzer

test_file = open("test.info", 'w', encoding='utf-8')

tu = TUAnalyzer()
#tu.run()
ent_list = []
tmp_list = tu.get_all_best()
for i in range(6, 16):
    ent_list.append(tmp_list[i][0])
tu.trade_up(ent_list)
test_file.write(tu.get_print_list())
for elem in tmp_list:
    stat_str = "Stat-Trak" if elem[3] else ""
    sign = "+" if elem[6] > 0 else "-"
    test_file.write(f"{elem[1]} - {elem[2]} {stat_str} ({elem[4]})"
            + f" (${elem[6]}) (float: {elem[5]:.4f}) |" 
            + f" {sign}${abs(elem[7]):.2f} / {elem[8]:.1f}x\n")
test_file.close()