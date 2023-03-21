import json
'''
管理设置
'''
class SettingManager: 
    settings = {}
    @staticmethod
    def getSettings(kind:str):
        if not SettingManager.settings:
            with open("./settings.json", mode="r", encoding="utf-8") as f:
                SettingManager.settings = json.loads(f.read())
        return SettingManager.settings[kind]
                