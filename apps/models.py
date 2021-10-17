import os
import json

class JsonEncryptionEditor:
    @staticmethod
    def decodeJson():
        with open(os.path.abspath(os.path.join(__file__, "../../../json files/Encryption.json")), 'r',
                  encoding="utf-8") as jsonFile:
            dataBase_Encryption = json.load(jsonFile)
            encryptionsList = dataBase_Encryption[0]["Encryptions"]
        return dataBase_Encryption, encryptionsList

    @staticmethod
    def dumpJson(dataBase_Encryption):
        with open(os.path.abspath(os.path.join(__file__, "../../../json files/Encryption.json")), 'w',
                  encoding="utf-8") as jsonFile:
            json.dump(dataBase_Encryption, jsonFile, indent=4, ensure_ascii=False)


    """заменить во всех функциях"""
    @staticmethod
    def findEncryptionById(enctyptionId, encryptionsList):
        for encryption in encryptionsList:
            if encryption["encryptionId"] == enctyptionId:
                returnEncryption = {
                    "userId": encryption["userId"],
                    "key1": encryption["key1"],
                    "key2": encryption["key2"],
                }
                return returnEncryption
        return {}
