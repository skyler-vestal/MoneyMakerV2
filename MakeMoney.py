from TradeUpAnalyzer import TUAnalyzer

test_file = open("test.info", 'w', encoding='utf-8')

tu = TUAnalyzer()
tu.run()
test_file.write(tu.get_print_list())
test_file.close()