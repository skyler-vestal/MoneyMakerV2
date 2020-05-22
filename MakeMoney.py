from SkinManagerDef import SkinManager

db_path = 'F:\Dev\py-workspace\SkinDatabase\skins_smol.db'

skins = SkinManager(db_path)
print(skins.collection[0].weapons)

