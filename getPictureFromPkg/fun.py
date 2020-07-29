# -*- coding: utf-8 -*-

import os
import shutil
import re

'''
我本来想的是把所有的scene转移过去后再解压，其实没必要，直接在content下运行最好
这样就免去了手动复制过程，只不过需要实现一个命名功能
'''
pictureType = ['jpg', 'jpeg', 'png']
# 当前文件夹路径
basePath = os.path.dirname(__file__)
# 输出文件夹路径
outputFolderPath = os.path.join(basePath, "OutHere")
# 场景源文件夹所在路径
scenesFolderName = "scenes"
sceneFolderPath = os.path.join(basePath, scenesFolderName)
# 把图片放入一个统一的地方 （在输出文件夹文件夹之下）
photoDstFolderPath = os.path.join(outputFolderPath, "photos")

# sceneList实现功能是要在对应文件夹中找到scene
#sceneList = [scene for scene in os.listdir() if "scene" in scene]

# sceneSourceFolderList 是scene所在的文件夹
sceneSourceFolderList = []
# sceneList 是scene应该存储为的名字
sceneList = []

for sceneDir in os.listdir(basePath):
    tempDirPath = os.path.join(basePath, sceneDir)
    if os.path.exists(os.path.join(tempDirPath, "scene.pkg")) and (not os.path.exists(os.path.join(tempDirPath, "shaders"))):
        sceneSourceFolderList.append(sceneDir)

# 把所有的scene都复制到scenes中
if not os.path.exists(sceneFolderPath):
    os.mkdir(sceneFolderPath)

# 新建输出文件夹把output都输出到这里
if not os.path.exists(outputFolderPath):
    os.mkdir(outputFolderPath)
    os.mkdir(photoDstFolderPath)
else:
    if not os.path.exists(photoDstFolderPath):
        os.mkdir(photoDstFolderPath)

# totalScenes: scene的总数，这个值比较重要
totalScenes = len(sceneSourceFolderList)
tempSceneId = 0
for sceneDir in sceneSourceFolderList:
    tempSceneId += 1
    sceneName = "scene" + str(tempSceneId)
    sceneList.append(sceneName)

    tempDirPath = os.path.join(basePath, sceneDir)
    srcPath = os.path.join(tempDirPath, "scene.pkg")
    dstPath = os.path.join(sceneFolderPath, "%s.pkg"%(sceneName))

    # 复制文件
    shutil.copyfile(srcPath, dstPath)

print("Process!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Process !!!
pattern = re.compile("[a-zA-Z0-9]*\.jpg")
pkgProcessPath = os.path.join(basePath, "RePKG", "RePKG.exe")
for scene in sceneList:
    tempOldOutputPath = os.path.join(basePath, "output")
    tempNewOutputPath = os.path.join(basePath, scene)
    # 执行解压程序
    os.system('"%s" extract %s/%s.pkg -o %s'%(pkgProcessPath, sceneFolderPath, scene, tempOldOutputPath))
    
    # output文件夹
    os.rename(tempOldOutputPath, tempNewOutputPath)
    shutil.move(tempNewOutputPath, sceneFolderPath)
    
    # 转移图片
    tempSrcPhotoFolderPath = os.path.join(sceneFolderPath, scene, "materials")
    tempPhotoName = ""
    '''
    正则表达式只能获取jpg，所以不用了，直接获取后三位
    '''
    for filename in os.listdir(tempSrcPhotoFolderPath):
        #if re.match(pattern, filename) is not None:
        if filename.split('.')[-1] in pictureType:
            tempPhotoName = filename
            break
    
    tempSrcPhotoPath = os.path.join(tempSrcPhotoFolderPath, tempPhotoName)
    tempDstPhotoPath = os.path.join(photoDstFolderPath, "%s.jpg"%scene)
    print(tempSrcPhotoPath)
    print(tempDstPhotoPath)
    shutil.copyfile(tempSrcPhotoPath, tempDstPhotoPath)

    #os.system("pause")


'''
  A required value not bound to option name is missing.
  -o, --output         (Default: ./output) Output directory
  -i, --ignoreexts     Don't extract files with specified extensions (delimited by comma ",")
  -e, --onlyexts       Only extract files with specified extensions (delimited by comma ",")
  -t, --tex            Convert all tex files into images from specified directory in input
  -s, --singledir      Should all extracted files be put in one directory instead of their entry path
  -r, --recursive      Recursive search in all subfolders of specified directory
  -c, --copyproject    Copy project.json and preview.jpg from beside PKG into output directory
  -n, --usename        Use name from project.json as project subfolder name instead of id
  --no-tex-convert     Don't convert TEX files into images while extracting PKG
  --overwrite          Overwrite all existing files
  --help               Display this help screen.
  --version            Display version information.
  Input (pos. 0)       Required. Path to file/directory
'''
