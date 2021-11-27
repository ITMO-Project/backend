from django import forms
from django.db import models
import json
import os


# class JsonEncryptionEditor:
    # @staticmethod
    # def decodeJson():
    #     with open(os.path.abspath(os.path.join(__file__, "../../../json files/Encryption.json")), 'r',
    #               encoding="utf-8") as jsonFile:
    #         dataBase_Encryption = json.load(jsonFile)
    #         encryptionsList = dataBase_Encryption[0]["Encryptions"]
    #     return dataBase_Encryption, encryptionsList
    #
    # @staticmethod
    # def dumpJson(dataBase_Encryption):
    #     with open(os.path.abspath(os.path.join(__file__, "../../../json files/Encryption.json")), 'w',
    #               encoding="utf-8") as jsonFile:
    #         json.dump(dataBase_Encryption, jsonFile, indent=4, ensure_ascii=False)
    #
    #
    # """заменить во всех функциях"""
    # @staticmethod
    # def findEncryptionById(enctyptionId, encryptionsList):
    #     for encryption in encryptionsList:
    #         if encryption["encryptionId"] == enctyptionId:
    #             returnEncryption = {
    #                 "userId": encryption["userId"],
    #                 "key1": encryption["key1"],
    #                 "key2": encryption["key2"],
    #             }
    #             return returnEncryption
    #     return {}


class IninitializeUser:
    @staticmethod
    def initialize(userId):
        # если пользователь авторизован, то находим его логин в базе данных
        if userId != 0:
            # TODO: Заменить на sqlite
            # dataBase_Users, usersList = JsonStudentsEditor.decodeJson()
            # for user in usersList:
            #     if user["userId"] == userId:
            #         userDict = {
            #             "typeAccount": user["typeAccount"],
            #             "userName": user["firstName"]
            #         }
            #         break
            # return userDict
            return {}
        return {}


class FileForm(forms.Form):
    file = forms.FileField(label="Загрузите файл")


class UploadFilesForDecrypt(forms.Form):
    image = forms.ImageField(label="Загрузите изображение")

    def clean(self):
        imageExpansion = os.path.splitext(self.cleaned_data["image"].name)[-1]  # расширение изображения
        if imageExpansion != ".bmp":
            raise Exception("Для изображений доступен только формат .bmp")
        return super().clean()


class FileModel(models.Model):
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.title

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title