from data_manage.SkinManagerDef import SkinManager

db_path = 'C:\Program Files\MakeMoney\skins.db'

test_file = open("test.info", 'w', encoding='utf-8')

skins = SkinManager(db_path)
for coll in skins.collection:
    test_file.write(str(coll) + " " + str(coll.weapons) + "\n")
    for weps in coll.weapons:
        for skin in weps:
            price_list = []
            for ent in skin.skin_list:
                price_list.append("[" + str(ent.price) + " | " + str(ent.real_info) + "]")
            test_file.write("[{} | {}] | {} - {} | {}\n".format(skin.weapon, skin.skin_name, str(skin.real_info), str(skin.getLowestPrice()), str(price_list)))
    test_file.write("\n\n\n")
test_file.close()

