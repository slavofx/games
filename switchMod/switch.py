# -*- coding: utf-8 -*-

import os
import re

# 读取文件所在路径
# py 文件是os.path.dirname(__file__)
# exe 文件是os.getcwd()
currentPath = os.path.dirname(__file__)
#currentPath = os.getcwd() 
# 文件夹数据文件路径
foldersDataPath = os.path.join(currentPath, "switch.dat")
# 默认的文件名
defaultFolder = ['NativeGK', 'NativeLeague', 'NativeStream']
usingFolder = []
# 已改名的指针以及指针的表达式
pattern = re.compile("[a-zA-Z0-9]*\*")
nativePtr = ""

'''
指针的用法:
    在程序运行中，指针指向的文件名有助于显示信息
    在磁盘存储时，要在相应的文件名后写*，而在程序运行中则不必考虑文件名
        读出时先利用正则表达式判断，然后写入
        写入时先将相应位置写成带*的形式，然后再写入
'''

# =======用户交互界面=========
# 菜单
def menu():
    print("======请选择需要使用的Mod======")
    i = 0
    displayAdded()
    print("=============================")
    print("a: 添加文件夹")
    print("d: 删除文件夹")
    print("h: 帮助")
    print("q: 退出\n")

# 用户输入处理
def getUserInput():
    '''
        返回值为3: 成功修改文件夹名
        返回值为2: 进行删除或添加
        返回值为1: 进入帮助界面或者
        返回值为0: 退出 
        返回值为-1: 输入失败 
    '''
    modChoose = input()
    # 退出
    if modChoose == 'q':
        return 0
    # 帮助界面
    elif modChoose == 'h':
        displayHelp()
        return 1
    elif modChoose == 'a':
        appendFoldesrData()
        return 2
    elif modChoose == 'd':
        deleteFoldersData()
        return 2
    #elif modChoose == 'i':
    #    initialFoldersData()
    #    return 2
    # 判断输入是否为正确的数字
    modChoose = eval(modChoose)
    if modChoose > len(usingFolder) and modChoose < 0 and type(modChoose) == int:
        print("请输入正确的数字!")
        return -1
    # 转换文件夹名为Native
    else:
        global nativePtr
        '''
        这里会产生这样几种情况（瞎分的，懒得想了）：
        1. 啥都没动，结果数据文件被删了
            这样其实最好，也不需要考虑恢复数据
        2. 已经改了，数据文件被删了
            那就没办法了...
        3. 已添加的文件夹名字被改了，这个被改的不是Native 
            那进行相应操作的时候就会出现错误，自动将其删除即可
        4. 已添加的文件夹名字被改了，这个被改的是Native
            这怎么可能呢
        
        其实就第三种情况需要考虑
            此时数据文件里面的名称与外部文件夹名称不对应，当转到这个
        文件夹时，会自动报错，此时就要删除了
        '''
        # 不仅要改名，还要修改指针。如果之前指针指向一个名字，就应该先改回来
        if nativePtr != "":
            folderReset()
        # 下面就是重点了，要先判断，再改
        try:
            nativePtr = usingFolder[modChoose-1]
            folderRename()
            setFolderData(usingFolder)
        except FileNotFoundError:
            # 清除即可
            print("未找到文件夹: " + nativePtr)
            print("已自动在菜单中清除文件夹名，请重新添加！")
            usingFolder.remove(nativePtr)
            setFolderData(usingFolder)
            nativePtr = ""
        return 3

# =========帮助界面与展示数据==========
def displayHelp():
    os.system('cls')
    print("如果当前路径下没有switch.dat数据文件，就会自动地进行初始化操作，选择想要添加的数据即可")
    print("=====已经转换为Native的文件已经用*标识出来=====")
    print("直接输入文件名序号就可以将相应的文件夹转换为Native")
    print("如果要将需要快速转换的文件夹添加到菜单，输入a即可")
    print("如果要将不需要转换的文件夹从菜单中删除，输出d即可")
    os.system("pause")

def displayAdded():
    tempFolderId = 0
    for tempFolderName in usingFolder:
        tempFolderId += 1
        print("\t" + str(tempFolderId) + ": " + tempFolderName, end="")
        if nativePtr == tempFolderName:
            print('\t*', end="")
        print("")

def displayAllUnadded():
    tempFolderId = 0
    tempFolders = []
    for folderName in os.listdir(currentPath):
        if (folderName in usingFolder) or not os.path.isdir(os.path.join(currentPath, folderName)):
            continue
        tempFolderId += 1
        # 输出未添加文件夹
        print(str(tempFolderId) + ": " + folderName)
        tempFolders.append(folderName)
    return tempFolders

# ==========写入数据与删除数据==========    

# 在已有文件菜单后添加
def appendFoldesrData():
    os.system('cls')
    # 读入用户输入
    while (True):
        # 从当前路径中查询所有文件夹
        tempFolders = displayAllUnadded()
        # 读取用户输入
        tempFolderChoose = input("请输入需要添加的文件夹的序号（输入q退出）: ")
        if tempFolderChoose == 'q':
            break
        usingFolder.append(tempFolders[eval(tempFolderChoose)-1])

    # 将需要的文件夹全部写入磁盘
    setFolderData(usingFolder)

# 从已有文件菜单中删除
def deleteFoldersData():
    os.system('cls')
    while(True) :
        # 展示所有已添加文件夹
        displayAdded()
        # 读取用户输入
        deleteId = input("\n请输入要清除的文件名序号（输入q退出）: ")
        if deleteId == 'q':
            break
        else:
            # 清除指针
            if usingFolder[eval(deleteId)-1] == nativePtr:
                updatePtr()
            del(usingFolder[eval(deleteId)-1])
    
    # 从数据文件中删除文件夹名称，其实就是重新设置数据文件
    setFolderData(usingFolder)

# 初始化文件夹数据
def initialFoldersData():
    global usingFolder
    usingFolder = []
    appendFoldesrData()
    
# 读取文件夹名数据
def getFolderData():
    # 如果有数据文件，就读取；不然就返回默认的
    folders = ""
    if os.path.exists(foldersDataPath):
        with open(foldersDataPath, 'r') as f:
            folders = f.read().strip()
        print(folders)
        if folders == "":
            return []
        return decodeList(folders.split(" "))
    else:
        return []

# 写入文件夹名数据
def setFolderData(foldersData):
    global nativePtr
    with open(foldersDataPath, 'w') as f:
        for tempFolderName in foldersData:
            if tempFolderName == nativePtr:
                tempFolderName = tempFolderName + "*"
            f.write(tempFolderName+" ")

# 对指针进行相应的处理
def decodeList(foldersNameList):
    tempFolderId = 0
    global nativePtr
    for tempFolderName in foldersNameList:
        if re.match(pattern, tempFolderName) == None:
            tempFolderId += 1
            continue
        else:
            tempFolderName = tempFolderName.strip("*")
            foldersNameList[tempFolderId] = tempFolderName
            nativePtr = tempFolderName
            break
    return foldersNameList

# 如果菜单中已被选中的文件被清除了，就重置nativePtr
def updatePtr():
    # 先把名改回来，然后清除指针
    global nativePtr
    folderReset()
    if nativePtr not in usingFolder:
        nativePtr = ""

# 利用指针，将指向的文件夹设置为Native
def folderRename():
    srcFolder = os.path.join(currentPath, nativePtr)
    dstFolder = os.path.join(currentPath, "Native")
    os.rename(srcFolder, dstFolder)

# 利用指针，将指向的Native文件夹恢复为原来的文件名
def folderReset():
    srcFolder = os.path.join(currentPath, "Native")
    dstFolder = os.path.join(currentPath, nativePtr)
    os.rename(srcFolder, dstFolder)
# ===========主程序============ 
if __name__ == "__main__":
    if os.path.exists(foldersDataPath):
        usingFolder = getFolderData()
    else:
        initialFoldersData()
    while(True) :
        menu()
        result = getUserInput()
        # 退出界面
        if result == 0:
            break
    os.system("cls")

