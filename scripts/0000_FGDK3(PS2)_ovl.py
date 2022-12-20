#  FGDK3 (PS2) ovl bone importer by Bigchillghost
from inc_noesis import *
import copy

def registerNoesisTypes():
	handle = noesis.register("FGDK3 (PS2)", ".ovl")
	noesis.setHandlerTypeCheck(handle, noepyCheckType)
	noesis.setHandlerLoadModel(handle, noepyLoadModel)
	#noesis.logPopup()
	return 1

#check if it's this type based on the data
def noepyCheckType(data):
	if len(data) < 0x80:
		return 0
	return 1

#load the model
def noepyLoadModel(data, mdlList):
	#noesis.logPopup()
	bs = NoeBitStream(data)
	boneCount = 0x36
	bs.seek(0x3C106, NOESEEK_ABS)
	parentIdMap = {}
	matrixMap = {}
	for i in range(0, boneCount):
		boneIndex = bs.readInt()
		parentIndex = bs.readInt()
		Mat43 = NoeMat43.fromBytes( bs.readBytes(0x30) )
		parentIdMap[boneIndex] = parentIndex
		matrixMap[boneIndex] = Mat43.transpose()
		bs.seek(4, NOESEEK_REL)
	strCount = 0x38
	bs.seek(0x3CEDA, NOESEEK_ABS)
	nmapData = bs.readBytes(strCount*8)
	bs.seek(0x3D3D6, NOESEEK_ABS)
	strData = bs.readBytes(0x2E8)
	ms = NoeBitStream(nmapData)
	ss = NoeBitStream(strData)
	nameMap = {}
	for i in range(0, strCount):
		strAddress = ms.readInt()
		boneIndex = ms.readInt()
		ss.seek(strAddress, NOESEEK_ABS)
		boneName = ss.readString()
		nameMap[boneIndex] = boneName
	
	bones = []
	boneIndexMap = {}
	idx = 0
	for boneIndex in parentIdMap:
		boneIndexMap[boneIndex] = idx
		idx += 1
	
	for boneIndex in parentIdMap:
		idx = boneIndexMap[boneIndex]
		parentIndex = parentIdMap[boneIndex]
		boneName = nameMap[boneIndex]
		boneMat = matrixMap[boneIndex]
		if parentIndex in boneIndexMap:
			parentIndex = boneIndexMap[parentIndex]
		else:
			parentIndex = -1
		bones.append( NoeBone(idx, boneName, boneMat, None, parentIndex) )
	
	# Converting local matrix to world space
	newBones = rapi.multiplyBones(bones)
	mdl = NoeModel()
	mdl.setBones(newBones)
	mdlList.append(mdl)
	
	return 1
