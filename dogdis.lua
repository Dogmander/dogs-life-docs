local arg = ...
local f = io.open(arg, "rb")
local function tell()
	return f:seek("cur", 0)
end
local function rep(ptr, entry)
	local hex = ""
	for i = 1, #entry do
		if entry:byte(i) == 0 then
			hex = hex .. ".. "
		else
			hex = hex .. string.format("%02x ", entry:byte(i))
		end
	end
	print(string.format("%08x: ", ptr) .. hex)
end
local function readRep(len)
	local ptr = tell()
	local entry = f:read(len)
	rep(ptr, entry)
	return entry
end
local function nl()
	print()
end

-- It begins!

local numTextures, numIdk1, numIdk2 = string.unpack("<III", readRep(0x0C))

nl()

-- Table 1
for i = 1, numIdk2 do
	readRep(0x14)
end

nl()

-- Table 2
local numT2 = string.unpack("<I", readRep(0x04))
for i = 1, numT2 do
	readRep(0x20)
end

nl()

-- oddity hypothesis
readRep(0x04)

-- Table 3
for i = 1, numTextures do
	readRep(0x40)
end

nl()

-- Table 4

print("Table 4")
while true do
	local ptr = tell()
	local entry = f:read(0x14)
	if (entry:byte(13) & 8) ~= 0 then
		entry = entry .. f:read(0x4)
	end
	rep(ptr, entry)
	if entry:sub(5, 8) == "\x00\x00\x00\x00" then
		break
	end
end

nl()

-- Table 5

print("Table 5")
while true do
	local ptr = tell()
	local entry = f:read(0x28)
	if (entry:byte(33) & 0x08) ~= 0 then
		entry = entry .. f:read(0x18)
	end
	rep(ptr, entry)
	if entry:sub(5, 8) == "\x00\x00\x00\x00" then
		--break
	end
end

nl()

-- Table 6

print("Table 6")
local numT5 = string.unpack("<I", readRep(0x4)) -- count (30.ovl @ 3f20)

for i = 1, numT5 do
	readRep(0x08)
end

nl()

-- lookahead

readRep(0x20)

-- It's over

f:close()

