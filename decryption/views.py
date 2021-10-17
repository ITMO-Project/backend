import os
import zipfile
import sys
from django.shortcuts import render
from .models import JsonEncryptionEditor


def decryptionRender(request):
    return render(request, 'decr`øyption/decryption.html')

def decryptedRender(request):
    return render(request, 'decryption/decrypted.html')





# расшифровка файла
def decode(imageName, userId):
    encryptionId = ""
    codeWordBits = ""
    imagePath = "files for decode/{}".format(imageName)
    with open(imagePath, "rb") as image:
        fileSize = 0  # размер файла
        image.seek(54)  # пропскаем первые 54 байта изображения
        image.seek(16, 1)  # пропускаем информацию о копирайтинге

        # считываем кодовое слово
        for i in range(0, 14, 2):
            imageByte = int.from_bytes(image.read(1),
                                       sys.byteorder)  # считываем байт изображения в виде целового числа
            imageByte &= 0b00000011  # обнуляем последние биты изображения
            codeWordBits += bin(imageByte)[2:].zfill(2)

        # проверка кодового слова
        if "" + chr(int(codeWordBits[0:7], base=2)) + chr(int(codeWordBits[7:14], base=2)) != "ok":
            raise Exception("Данное изображение не содержит зашифрованных данных!")

        # считываем id шифрования
        for i in range(0, 18, 2):
            imageByte = int.from_bytes(image.read(1),
                                       sys.byteorder)  # считываем байт изображения в виде целового числа
            imageByte &= 0b00000011  # обнуляем последние биты изображения
            encryptionId += bin(imageByte)[2:].zfill(2)  # если прочитали 01 или 00 в целом типе нули потеряются

        encryptionId = int(encryptionId, base=2)

        # поиск операции шифрования из БД
        dataBase_Encryption, encryptionsList = JsonEncryptionEditor.decodeJson()
        encryptionDict = JsonEncryptionEditor.findEncryptionById(encryptionId, encryptionsList)

        # проверка на то, что пользователь не может расшифровать файл другого
        if encryptionDict == {}:
            raise Exception("Произошла ошибка в базе данных!")
        elif encryptionDict["userId"] != userId:
            raise Exception("Зашифрованные данные принадлежат не вам!")
        key1 = encryptionDict["key1"]
        key2 = encryptionDict["key2"]

        # расшифровываем размер файла
        for i in range(0, 32, 8):
            # читаем 4*2 = 8 бит размера файла
            for j in range(4):
                imageByte = int.from_bytes(image.read(1), sys.byteorder)
                fileSize |= (imageByte & 0b00000011)  # прибавляем к байту по 2 последних бита изображения
                fileSize <<= 2  # сдвигаем байт на 2 бита

        fileSize >>= 2  # т.к. в цикле сделали лишнее действие << 2 при выходе
        fileSize //= 8  # приводим к байту
        # создание файла и запись битов, прочитанных с изображения
        with open("decode files/code{}.zip".format(userId), "wb") as file:
            for i in range(fileSize):
                fileByteBinary = 0  # отдельный байт файла в двоичном виде
                # читаем 4*2 = 8 бит файла
                for j in range(4):
                    imageByte = int.from_bytes(image.read(1), sys.byteorder)
                    fileByteBinary |= (imageByte & 0b00000011)  # прибавляем к байту по 2 последних бита изображения
                    # чтобы не сдвигать лишний раз при выходе
                    fileByteBinary <<= 2  # сдвигаем байт на 2 бита

                fileByteBinary >>= 2
                # декодируем байт

                fileByteBinary ^= key2
                if fileByteBinary < key1:
                    fileByteBinary = 256 - (key1 - fileByteBinary)
                else:
                    fileByteBinary -= key1
                file.write(int.to_bytes(fileByteBinary, 1, sys.byteorder))  # запись байта в файл
    try:
        os.remove(imagePath)
    except Exception as error:
        raise Exception("Ошибка сервера при удалении изображения!")

# разархивация
def unzipping(arhievePath):
    with zipfile.ZipFile(arhievePath) as unzippingFile:
        fileName = unzippingFile.namelist()[0]  # получаем список заархивированных файлов (пока берём один-первый)
        unzippingFile.extract(member=fileName, path="decode files/")  # разархивация файла
        unzippingFile.close()
        return fileName
