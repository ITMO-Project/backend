import zipfile

import magic
from django.http import HttpResponse
from django.shortcuts import render
import os
import sys
import shutil
from django.shortcuts import redirect

# Constants
MAX_FILE_SIZE = 1048576  # 1 Мб
PATH_FOR_ENCODE = "files for encode/"
PATH_FOR_DECODE = "files for decode/"
PATH_FOR_UPLOAD = "files for upload/"
PATH_ROOT = os.path.abspath(os.path.dirname(__name__))
PATH_FOR_DEFAULT_IMAGES = PATH_ROOT + "/encryption/static/our_images/"
PATH_FOR_DEFAULT_IMAGES_FRONT = "../../static/our_images/"

# Params
PARAM_UPLOADED_FILE_URL = "filePath"


def encryptionRender(request):
    return render(request, 'encryption/encryption.html')

def encryptionImageRender(request):
    try:
        if request.method == "POST":
            if 'encrypt' in request.POST:
                uploadedFileUrl = copyFileToServer(file=request.FILES["file"], path=PATH_FOR_ENCODE)
                returnParams = {"filePath": uploadedFileUrl}
                return render(request, 'encryption/encryption_images.html', returnParams)

        # если зашли по GET запросу
        return render(request, 'encryption/encryption.html')

    except Exception as error:
        print(error)
        return render(request, "encryption/encryption.html")


def finishEncryptRender(request):
    print(request.POST)
    print(request.FILES)
    try:
        if (request.method == "POST") and ("filePath" in request.POST):
            # form = FileForm(request.POST, request.FILES)  # модель формы
            # # проверка на правильность введённых полей
            # if form.is_valid():
                # проверка на максимальный размер файла
                # fileSize = form.cleaned_data.get("file").size
                # if fileSize > MAX_FILE_SIZE:
                #     raise Exception("Выберите файл поменьше!")

            if "image" in request.FILES:
                image = request.FILES["image"]
                imagePath = copyFileToServer(file=image, path=PATH_FOR_ENCODE)
            elif request.POST["defaultImage"] != "":
                imagePath = copyDefaultImageToServer(
                    defaultPath=PATH_FOR_DEFAULT_IMAGES + request.POST["defaultImage"] + ".bmp",
                    pathForCopy=PATH_FOR_ENCODE + request.POST["defaultImage"] + ".bmp"
                )
            else:
                raise Exception("Incorrect path for image-container")
            filePath = request.POST["filePath"]
            imageDecryptPath = encode(
                filePath=filePath,
                imagePath=imagePath,
                userId=int(request.user.id or 0),
                username=str(request.user.username or "user")
            )
            frontImagePath = PATH_FOR_DEFAULT_IMAGES_FRONT + request.POST["defaultImage"] + ".bmp"
            returnParams = {"filePath": imageDecryptPath, "frontImagePath": frontImagePath}
            return render(request, "encryption/encrypted.html", returnParams)
        else:
            redirect("encryption:encryption")  # если зашли по GET запросу
    except Exception as error:
        print(error)
        return render(request, "encryption/encrypted.html")

def saveToClientRender(request):
    try:
        if request.method == "POST":
            # imagePath = request.POST["filePath"]
            # TODO: заглушка
            imagePath = "files for upload/imageWithFile-" + str(request.user.username or "user") + ".bmp"
            with open(imagePath, "rb") as image:
                dataFile = image.read()  # чтение файла
                mimeType = magic.from_buffer(dataFile, mime=True)  # читаем mime тип файла
                response = HttpResponse(dataFile, content_type=mimeType)  # записываем в response файл и его mime тип
                response["Content-Disposition"] = "attachment; filename = " + os.path.basename(imagePath)  # записываем в response имя файла
            try:
                os.remove(imagePath)
            except Exception as error:
                raise Exception("Ошибка сервера при удалении файла!")
            return response

        if int(request.user.id or 0) > 0:
            return render(request, 'main/index_user.html')
        return render(request, 'main/index.html')
    except Exception as error:
        print(error)
        if int(request.user.id or 0) > 0:
            return render(request, 'main/index_user.html')
        return render(request, 'main/index.html')

def copyFileToServer(file, path):
    try:
        # wb - write binary
        with open(path + file.name, "wb") as fileOut:
            # ленивое копирование (блочно, т.е. быстрее)
            for chunk in file.chunks():
                fileOut.write(chunk)
        return path + file.name
    except Exception as error:
        print(error)
        return ""

def copyDefaultImageToServer(defaultPath, pathForCopy):
    try:
     shutil.copy(defaultPath, pathForCopy)
     return pathForCopy
    except Exception as error:
        print(error)
        return ""

# шифрование файла (+44 бита)
def encode(filePath, imagePath, userId, username):
    # определяем кодовые значения
    codeWord = bin(ord("o"))[2:] + bin(ord("k"))[2:]  # кодовое слово, сведения успешно вставлены (14 бит)
    # TODO: временно
    encryptionId = 0
    encryptionIdBits = bin(encryptionId)[2:].zfill(18)

    # архивируем файл
    try:
        zipping(PATH_FOR_ENCODE + "code{}.zip".format(userId), filePath)
    except Exception as error:
        raise Exception("Ошибка сервера при архивировании!")

    os.chdir(PATH_FOR_ENCODE)
    fileSize = os.stat("code{}.zip".format(userId)).st_size
    os.chdir("../")

    # шифруем
    with open(PATH_FOR_ENCODE + "code{}.zip".format(userId), "rb") as file:
        with open(imagePath, "rb+") as image:
            print("aaaaa fileSize = " + str(fileSize * 8 + 320 + 32 + 32 + 44))
            print("aaaaa imageSize = " + str(os.stat(imagePath).st_size * 6))
            if fileSize * 8 + 320 + 32 + 32 + 44 > os.stat(imagePath).st_size * 6:
                raise Exception("Файл не вмещается в изображение!")
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
                # fileByte = ((int.from_bytes(file.read(1), sys.byteorder) + key1) % 256) ^ key2
                # TODO: Временно
                fileByte = ((int.from_bytes(file.read(1), sys.byteorder)) % 256)
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
        if imagePath.__contains__(PATH_FOR_DEFAULT_IMAGES):
            shutil.copy(imagePath, PATH_FOR_UPLOAD + "imageWithFile-" + username + ".bmp")
        else:
            shutil.move(imagePath, PATH_FOR_UPLOAD + "imageWithFile-" + username + ".bmp")  # перенос изображения
        os.remove(filePath)  # удаление файла
        os.remove(PATH_FOR_ENCODE + "code{}.zip".format(userId))
    except Exception as error:
        print(error)
        raise Exception("Ошибка сервера при копировании файла!")

    return PATH_FOR_UPLOAD + "imageWithFile-" + username + ".bmp"  # возвращаем путь до изображения


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
