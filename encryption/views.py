import random

import zipfile
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os
import sys
import shutil
from django.shortcuts import redirect
from .models import IninitializeUser, UploadFilesForEncrypt
from .models import JsonEncryptionEditor

MAX_FILE_SIZE = 1048576  # 1 Мб

def encryptionRender(request):
    return render(request, 'encryption/encryption.html')

def fileUpload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage(location="upload")
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        returnParams = {'uploadedFileUrl': uploaded_file_url }
        return render(request, 'encryption/encryption.html', returnParams)
    return render(request, 'encryption/encryption.html')

def encryptionImageRender(request):
    return render(request, 'encryption/encryption_image.html')

def finishEncrypt(request):
    returnDict = IninitializeUser.initialize(request.session.get("userId", 0))  # присваиваем словарь с куками
    try:
        if request.method == "POST":
            form = UploadFilesForEncrypt(request.POST, request.FILES)  # модель формы
            # проверка на правильность введённых полей
            if form.is_valid():
                # проверка на максимальный размер файла
                fileSize = form.cleaned_data.get("file").size
                if fileSize > MAX_FILE_SIZE:
                    raise Exception("Выберите файл поменьше!")

                # сохранение файла и изображения на сервер
                filePath = copyToServer("encode", image=request.FILES["image"], file=request.FILES["file"])
                imageDecryptPath = encode(request.FILES["file"].name, request.FILES["image"].name,
                                          os.path.dirname(filePath)+"/", request.session.get("userId", 0))  # шифрование файла
                returnDict["filePath"] = imageDecryptPath
                returnDict["action"] = "encode"
                return render(request, "saveData.html", returnDict)

            raise Exception("Неверные данные формы!")
        redirect("encryption:encryption")  # если зашли по GET запросу
    except Exception as error:
        returnDict["error"] = error
        returnDict["UploadFilesForEncrypt"] = UploadFilesForEncrypt
        return render(request, "encryption/encrypted.html", returnDict)







# копирование файла и изображения на сервер (или то или то, или то и то)
def copyToServer(action, **kwargs):
    path = ""  # путь для сохранения файлов
    fileIn = None  # временнный файл с которого будем считывать
    imageIn = kwargs["image"]  # временное изображение с которого будем считывать
    # определяем действие
    if action == "encode":
        fileIn = kwargs["file"]  # сохраняем ссылку на передаваемый от клиента фйл
        path = "files for encode/"
    elif action == "decode":
        path = "files for decode/"

    # копирование изображения в "files for encode/"
    with open(path + imageIn.name, "wb") as imageOut:
        # ленивое копирование (блочно, т.е. быстрее)
        for chunk in imageIn.chunks():
            imageOut.write(chunk)

        "TODO: освободить память от файлов в kwargs"

        # копирование файла (только при расшифровке) в "files for encode/"
        if action == "encode":
            with open(path + fileIn.name, "wb") as fileOut:
                # ленивое копирование (блочно, т.е. быстрее)
                for chunk in fileIn.chunks():
                    fileOut.write(chunk)
            return path + fileIn.name

        return path + imageIn.name

"TODO: усилить защиту"

# шифрование файла (+44 бита)
def encode(fileName, imageName, pathToFile, userId):
    # определяем кодовые значения
    codeWord = bin(ord("o"))[2:] + bin(ord("k"))[2:]  # кодовое слово, сведения успешно вставлены (14 бит)
    key1 = random.randint(0, 16)  # рандомное число от 0 до 16 (4 бита)
    key2 = random.randint(0, 255)  # рандомное число от 0 до 255 (1 байт)

    # определям id шифрования (18 бит)
    dataBase_Encryption, encryptionsList = JsonEncryptionEditor.decodeJson()
    encryptionId = encryptionsList[len(encryptionsList) - 1]["encryptionId"] + 1
    encryptionIdBits = bin(encryptionId)[2:].zfill(18)

    # архивируем файл
    try:
        zipping(pathToFile + "code{}.zip".format(userId), pathToFile + fileName)
    except Exception as error:
        raise Exception("Ошибка сервера при архивировании!")

    os.chdir(pathToFile)
    fileSize = os.stat("code{}.zip".format(userId)).st_size
    os.chdir("../")

    # шифруем
    with open(pathToFile + "code{}.zip".format(userId), "rb") as file:
        with open(pathToFile + imageName, "rb+") as image:
            if fileSize * 8 + 320 + 32 + 32 + 44 > os.stat(pathToFile + imageName).st_size * 6:
                raise Exception("Файл не вмешается в изображение!")
            fileSizeBinary = bin(fileSize * 8)[2:].zfill(
                8)  # размер файла в битах (для шифровки), берём без обозначения двоичного кода
            fileSizeBinary = fileSizeBinary.zfill(32)  # дополняем размер файла нулями (максимум - 512 Мб)
            image.seek(54)  # пропскаем первые 54 байта изображения
            image.seek(16, 1)  # пропускаем информацию о копирайтинге

            # записываем кодовое слово
            for i in range(0, len(codeWord), 2):
                imageByte = int.from_bytes(image.read(1),
                                           sys.byteorder)  # считываем байт изображения в виде целового числа
                image.seek(-1, 1)  # возвращаемся на шаг назад от текущей позиции(1)
                imageByte &= 0b11111100  # обнуляем последние биты изображения
                imageByte |= int(codeWord[i:i + 2],
                                 base=2)  # устанавливаем последние 2 бита изображения = битам кодового слова
                image.write(int.to_bytes(imageByte, 1, sys.byteorder))
                image.flush()

            # записываем id шифрования
            for i in range(0, len(encryptionIdBits), 2):
                imageByte = int.from_bytes(image.read(1),
                                           sys.byteorder)  # считываем байт изображения в виде целового числа
                image.seek(-1, 1)  # возвращаемся на шаг назад от текущей позиции(1)
                imageByte &= 0b11111100  # обнуляем последние биты изображения
                imageByte |= int(encryptionIdBits[i:i + 2],
                                 base=2)  # устанавливаем последние 2 бита изображения = битам id
                image.write(int.to_bytes(imageByte, 1, sys.byteorder))
                image.flush()

            # шифруем размер файла
            for i in range(0, 32, 8):
                fileSizeByte = int(fileSizeBinary[i:i + 8], base=2)
                # записываем 4 раза по 2 бита одного байта файла
                for j in range(4):
                    imageByte = int.from_bytes(image.read(1),
                                               sys.byteorder)  # считываем байт изображения в виде целового числа
                    image.seek(-1, 1)  # возвращаемся на шаг назад от текущей позиции(1)
                    imageByte = imageMaskEncode(fileSizeByte, imageByte,
                                                2 * j)  # возвращает изменённый байт изображения в виде байта
                    image.write(imageByte)

            # шифруем байты файла
            for i in range(fileSize):
                fileByte = ((int.from_bytes(file.read(1), sys.byteorder) + key1) % 256) ^ key2
                # записываем 4 раза по 2 бита одного байта файла
                for j in range(4):
                    imageByte = int.from_bytes(image.read(1),
                                               sys.byteorder)  # считываем байт изображения в виде целового числа
                    image.seek(-1, 1)  # возвращаемся на шаг назад от текущей позиции(1)
                    imageByte = imageMaskEncode(fileByte, imageByte,
                                                2 * j)  # возвращает изменённый байт изображения в виде байта
                    image.write(imageByte)

                image.flush()

    # перемещаем изображение в др. рабочую директорию и удаляем файл и архив
    try:
        shutil.move(pathToFile + imageName, "encode images/" + imageName)  # перенос изображения
        os.remove(pathToFile + fileName)  # удаление файла
        os.remove(pathToFile + "code{}.zip".format(userId))
    except Exception as error:
        raise Exception("Ошибка сервера при копировании файла!")

    # добавление операции в базу данных
    newEncrypyion = {
        "encryptionId": encryptionId,
        "userId": userId,
        "key1": key1,
        "key2": key2
    }
    encryptionsList.append(newEncrypyion)
    JsonEncryptionEditor.dumpJson(dataBase_Encryption)

    return "encode images/" + imageName  # возвращаем путь до изображения

# замена 2 битов изображения на биты файла
def imageMaskEncode(fileByte, imageByte, bitPos):
    # находим нужные 2 бита файла
    fileByte >>= (6 - bitPos)  # сдвигаем, чтобы все биты, кроме последних двух были нулями
    fileByte &= 0b00000011
    imageByte &= 0b11111100
    imageByte |= fileByte  # устанавливаем последние 2 бита изображения = битам файла
    return int.to_bytes(imageByte, 1, sys.byteorder)

# архивация
def zipping(arhievePath, filePath):
    with zipfile.ZipFile(arhievePath, mode="w", compresslevel=zipfile.ZIP_STORED) as zippingFile:
        currentPath = os.path.abspath(os.curdir)
        os.chdir(os.path.dirname(filePath))  # переходим к каталогу с файлом
        zippingFile.write(os.path.basename(filePath))
        os.chdir(currentPath)
        zippingFile.close()