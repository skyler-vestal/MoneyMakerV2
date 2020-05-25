from SkinManagerDef import SkinManager

db_path = 'C:\Program Files\MakeMoney\skins.db'

test_file = open("test.info", 'w', encoding='utf-8')

skins = SkinManager(db_path)
for coll in skins.collection:
    test_file.write(str(coll) + " " + str(coll.weapons))
test_file.close()

