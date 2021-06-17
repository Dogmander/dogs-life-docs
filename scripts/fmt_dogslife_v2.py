# Dog's Life (PS2)
# Noesis script by Dave, 2021

from inc_noesis import *

def registerNoesisTypes():
	handle = noesis.register("Dog's Life (PS2)",".ovl")
	noesis.setHandlerTypeCheck(handle, bcCheckType)
	noesis.setHandlerLoadModel(handle, bcLoadModel)
	return 1

# Check file type

def bcCheckType(data):
	return 1


# Read the model data

def bcLoadModel(data, mdlList):
	bs = NoeBitStream(data)
	ctx = rapi.rpgCreateContext()

	curr_folder = rapi.getDirForFilePath(rapi.getInputName()).lower()
	curr_file = rapi.getLocalFileName(rapi.getInputName()).lower()

# Some hard coded values for various meshes

	if curr_file == "29.ovl":
		DrawMesh(bs, 0x326e3c, 0)
		DrawMesh(bs, 0x3358e4, 2)

	if curr_file == "5.ovl":
		DrawMesh(bs, 0x3d752, 0)					# jake
		DrawMesh(bs, 0x3e1ba, 0)
		DrawMesh(bs, 0x42332, 2)
		DrawMesh(bs, 0x43596, 0)
		DrawMesh(bs, 0x6659e, 2)

	if curr_file == "7.ovl":
		DrawMesh(bs, 0x4e913, 2)

	if curr_file == "30.ovl":
		DrawMesh(bs, 0x3a253a, 2)					# dog 1 eyes
		DrawMesh(bs, 0x3a4572, 2)					# dog 1 collar
		DrawMesh(bs, 0x3c99a2, 0)					# dog 1 nose and teeth
		DrawMesh(bs, 0x3a7012, 0)					# dog 1 body
		DrawMesh(bs, 0x3c99a2, 0)					# dog 1 nose and teeth


	mdl = rapi.rpgConstructModel()
	mdlList.append(mdl)

	return 1


# Process the mesh data
# "adjust" value is temporary until it can be properly calculated

def DrawMesh(bs, offset, adjust):
	bs.seek(offset)

	bs.readUShort()						# Always 0xFFFF ?
	face_parts = bs.readUShort()
	face_count = bs.readUShort()
	vert_count = bs.readUShort()
	bs.readUInt()						# Always 0x0000411C ?
	face_start = offset + (face_parts * 2) + 12
	vert_start = face_start + (face_count * 2) + adjust			# sometimes + 2 to get the right offset (not sure why yet - doesn't seem to be for 4-byte alignment)

	face_info = []

	for a in range(face_parts):
		face_info.append(bs.readUShort())

	vertices = bytearray(vert_count * 12)
	normals = bytearray(vert_count * 12)
	uvs = bytearray(vert_count * 8)

	print(hex(vert_start))
	bs.seek(vert_start)

	for v in range(vert_count):
		vx = bs.readFloat()
		vy = bs.readFloat()
		vz = bs.readFloat()
		bs.readBytes(20)
		nx = bs.readFloat()
		ny = bs.readFloat()
		nz = bs.readFloat()
		uvx = bs.readFloat()
		uvy = bs.readFloat()
		struct.pack_into("<fff", vertices, v * 12, vx, vy, vz)
		struct.pack_into("<fff", normals, v * 12, nx, ny, nz)
		struct.pack_into("<ff", uvs, v * 8, uvx, uvy)

	rapi.rpgBindPositionBuffer(vertices, noesis.RPGEODATA_FLOAT, 12)
	rapi.rpgBindUV1Buffer(uvs, noesis.RPGEODATA_FLOAT, 8)
	rapi.rpgBindNormalBuffer(normals, noesis.RPGEODATA_FLOAT, 12)

	bs.seek(face_start)

	for f in range(face_parts):
		fcount = face_info[f]
		faces = bs.readBytes(fcount * 2)
		rapi.rpgSetName("Mesh_" + str(offset))
		rapi.rpgCommitTriangles(faces, noesis.RPGEODATA_USHORT, fcount, noesis.RPGEO_TRIANGLE_STRIP)

	return 1

