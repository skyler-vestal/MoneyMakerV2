from data_manage.SkinManagerDef import SkinManager

db_path = 'C:\Program Files\MakeMoney\skins.db'

test_file = open("test.info", 'w', encoding='utf-8')

skins = SkinManager(db_path)
ent_list = []
for i in range(10):
    ent_list.append(skins.collection[0].weapons[2][0].skin_list[3][3])
meme1, meme2 = skins.getOutcomes(ent_list)
print(meme1, meme2)
test_file.close()

