'''
Krysten Tachiyama
Week 2 homework: Apply a given animation onto a given
                 character and save the file
'''

import maya.cmds
import os

# creates a namespace from a given file


def createFileNamespace(filePath):

    if not os.path.exists(filePath):
        maya.cmds.error('File does not exist: {0}'.format(filePath))
        return

    filePathDir, filePathName = os.path.split(filePath)
    fileNamespace, filePathExt = os.path.splitext(filePathName)

    return fileNamespace

# creates a reference from a file path and namespace


def createReference(filePath, ns):

    if not os.path.exists(filePath):
        maya.cmds.error('File does not exist: {0}'.format(filePath))
        return

    maya.cmds.file(filePath, r=True, ns=ns)


def connectAttributes(src, dst, attr):

    srcString = '{0}.{1}'.format(src, attr)
    dstString = '{0}.{1}'.format(dst, attr)

    maya.cmds.connectAttr(srcString, dstString, f=True)


def connectAttributesInList(src, dst, attrList):
    for arrt in attrList:
        connectAttributes(src, dst, attr)


def getJointsFromNamespace(ns):
    return maya.cmds.ls('{0}:*'.format(ns), type='joint')


def connectJoints(srcJointsList, dstJointsList, dstNS):
    for s in srcJointsList:
        srcJoint = s.split(':')[1]
        dstJoint = '{}:{}'.format(dstNS, srcJoint)

        if dstJoint in dstJointsList:
            maya.cmds.parentConstraint(s, dstJoint, mo=True)


def saveFile(filePath):
    maya.cmds.file(rename=filePath)
    maya.cmds.file(save=True, f=True)


def batchAnimations(charPath, animPath, saveDir):
    charPath.replace("\\", "/")
    animPath.replace("\\", "/")
    saveDir.replace("\\", "/")

    # create new scene
    maya.cmds.file(new=True, force=True)

    # create char and anim namespace
    charNS = createFileNamespace(charPath)
    animNS = createFileNamespace(animPath)

    # bring in character
    createReference(charPath, charNS)

    # bring in animation
    createReference(animPath, animNS)

    # Get a list of joints of both the anim and char
    maya.cmds.select(cl=True)
    charJoints = getJointsFromNamespace(charNS)
    animJoints = getJointsFromNamespace(animNS)

    # We want the current framerate and the referenced
    # animation framerates to match
    firstKeyframe = maya.cmds.findKeyframe(animJoints[0], which="first")
    maya.cmds.playbackOptions(
        animationStartTime=firstKeyframe, minTime=firstKeyframe)
    maya.cmds.currentTime(firstKeyframe)

    # Connect the joints of the animation onto the character
    connectJoints(animJoints, charJoints, charNS)

    # Shake 'n Bake animation bones to character bones
    startTime = maya.cmds.playbackOptions(q=True, min=True)
    endTime = maya.cmds.playbackOptions(q=True, max=True)

    maya.cmds.select(cl=True)
    maya.cmds.select(charJoints)
    maya.cmds.bakeResults(simulation=True,
                          time=(startTime, endTime),
                          sampleBy=1,
                          oversamplingRate=1,
                          disableImplicitControl=True,
                          preserveOutsideKeys=True,
                          sparseAnimCurveBake=False,
                          removeBakedAnimFromLayer=False,
                          bakeOnOverrideLayer=False,
                          minimizeRotation=True,
                          controlPoints=False,
                          shape=True)

    # Remove animation reference
    maya.cmds.file(animPath, rr=True)

    # Save file
    # saveFile(newFilePath)


if __name__ == '__main__':

    # create char and anim namespace
    charPath = r'C:\Users\k_tac\OneDrive\Documents\LMU\Intro to Tech Art\Week 2\homework\character.mb'.replace(
        "\\", "/")
    animPath = r'C:\Users\k_tac\OneDrive\Documents\LMU\Intro to Tech Art\Week 2\homework\animations_maya\char01_07.ma'.replace(
        "\\", "/")
    saveDir = r'C:\Users\k_tac\OneDrive\Documents\LMU\Intro to Tech Art\Week 2\homework\wk02_homework.mb'.replace(
        "\\", "/")

    batchAnimations(charPath, animPath, saveDir)
