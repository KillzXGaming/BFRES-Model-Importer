import sys
import struct
import array
import binascii
import argparse

class poly(object):
        def __init__(self):
                self.name = ""
                self.verts = []
                self.normals = []
                self.tangents = []
                self.colors =[]
                self.uv0 = []
                self.uv1 = []
                self.uv2 = []
                self.uv3 = []
                self.faces = []
                self.boneName = []
                self.boneI = []
                self.boneW = []

polys = []

curPoly = 0

numUVs = 0

def compress(float32):
    F16_EXPONENT_BITS = 0x1F
    F16_EXPONENT_SHIFT = 10
    F16_EXPONENT_BIAS = 15
    F16_MANTISSA_BITS = 0x3ff
    F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
    F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

    a = struct.pack('>f',float32)
    b = binascii.hexlify(a)

    f32 = int(b,16)
    f16 = 0
    sign = (f32 >> 16) & 0x8000
    exponent = ((f32 >> 23) & 0xff) - 127
    mantissa = f32 & 0x007fffff

    if exponent == 128:
        f16 = sign | F16_MAX_EXPONENT
        if mantissa:
            f16 |= (mantissa & F16_MANTISSA_BITS)
    elif exponent > 15:
        f16 = sign | F16_MAX_EXPONENT
    elif exponent > -15:
        exponent += F16_EXPONENT_BIAS
        mantissa >>= F16_MANTISSA_SHIFT
        f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
    else:
        f16 = sign
    return f16


def decompress(h):
    s = int((h >> 15) & 0x00000001)    # sign
    e = int((h >> 10) & 0x0000001f)    # exponent
    f = int(h & 0x000003ff)            # fraction

    if e == 0:
       if f == 0:
          return int(s << 31)
       else:
          while not (f & 0x00000400):
             f <<= 1
             e -= 1
          e += 1
          f &= ~0x00000400
    elif e == 31:
       if f == 0:
          return int((s << 31) | 0x7f800000)
       else:
          return int((s << 31) | 0x7f800000 | (f << 13))

    e = e + (127 -15)
    f = f << 13

    return int((s << 31) | (e << 23) | f)

def readByte(file):
    return struct.unpack("B", file.read(1))[0]
 
def readu16be(file):
    return struct.unpack(">H", file.read(2))[0]
 
def readu16le(file):
    return struct.unpack("<H", file.read(2))[0]

def readu32be(file):
    return struct.unpack(">I", file.read(4))[0]
 
def readu32le(file):
    return struct.unpack("<I", file.read(4))[0]
 
def readfloatbe(file):
    return struct.unpack(">f", file.read(4))[0]
 
def readfloatle(file):
    return struct.unpack("<f", file.read(4))[0]

def readhalffloatbe(file):
    v = readu16be(file)
    x = decompress(v)
    str = struct.pack('I',x)
    f = struct.unpack('f',str)[0]
    return float(f)

def updateDamit(file):
    file.seek(0,1)

def writefloatbe(file,val):
    file.write(struct.pack(">f", val))
    updateDamit(file)
def writehalffloatbe(file,val):
    half = compress(val)
    file.write(struct.pack(">H", half))
    updateDamit(file)

def ReadOffset(file):
    offset = file.tell()
    return (offset + readu32be(file))

def getString(file):
    result = ""
    tmpChar = file.read(1)
    while ord(tmpChar) != 0:
        result += tmpChar.decode('utf-8')
        tmpChar =file.read(1)
    return result

#New Defs
def readSignedByte(file):
    return struct.unpack("b", file.read(1))[0]

def readlongle(file):
    return struct.unpack("<l", file.read(4))[0]
	
def readu64(file):
    return struct.unpack("<Q", file.read(8))[0]
	
def readshortle(file):
    return struct.unpack("<h", file.read(2))[0]

def readunshortle(file):
    return struct.unpack("<H", file.read(2))[0]
	
def writelongle(file,val):
    file.write(struct.pack("<l", val))
    updateDamit(file)

def writefloatle(file,val):
    file.write(struct.pack("<f", val))
    updateDamit(file)
def writehalffloatle(file,val):
    half = compress(val)
    file.write(struct.pack("<H", half))
    updateDamit(file)	
	
def writeUShortle(file,val):
    file.write(struct.pack("<H", val))
    updateDamit(file)

def writeByte(file,val):
    file.write(struct.pack("B", int(val)))
    updateDamit(file)
def writeSByte(file,val):
    file.write(struct.pack("b", val))
    updateDamit(file)
def write16be(file,val):
    file.write(struct.pack(">H", val))
    updateDamit(file)
def write16le(file,val):
    file.write(struct.pack("<H", val))
    updateDamit(file)	
def writes16be(file,val):
    file.write(struct.pack(">h", val))
    updateDamit(file)
def writes16le(file,val):
    file.write(struct.pack("<h", val))
    updateDamit(file)
def write32be(file,val):
    file.write(struct.pack(">I", val))
    updateDamit(file)
def write32le(file,val):
    file.write(struct.pack("<I", val))
    updateDamit(file)	
def write10be(file,x,y,z):
        x *= -1
        y *= -1
        z *= -1
        x -= 1
        y -= 1
        z -= 1
        x = ~x
        y = ~y
        z = ~z
        x = 0x3ff & x
        y = 0x3ff & y
        z = 0x3ff & z
        x = x<<0
        y = y<<10
        z = z<<20
        base = x + y + z
        write32be(file,base)
		
def write10le(file,x,y,z):
        x *= -1
        y *= -1
        z *= -1
        x -= 1
        y -= 1
        z -= 1
        x = ~x
        y = ~y
        z = ~z
        x = 0x3ff & x
        y = 0x3ff & y
        z = 0x3ff & z
        x = x<<0
        y = y<<10
        z = z<<20
        base = x + y + z
        write32le(file,base)
		
class fmdlh:
    def __init__(self,file):
        self.fmdl = file.read(4)
        self.headerLength1 = readlongle(file)
        self.headerLength2 = readu64(file)
        self.fnameOff = readu64(file)
        self.eofString = readu64(file)
        self.fsklOff = readu64(file)
        self.fvtxArrOff = readu64(file)
        self.fshpIndx = readu64(file)
        self.fshpSubIndx = readu64(file)
        self.fmatOff = readu64(file)
        self.fmatIndx = readu64(file)
        self.paramOff = readu64(file)
        self.padding = readu64(file)
        self.padding = readu64(file)
        self.fvtxCount = readshortle(file)
        self.fshpCount = readshortle(file)
        self.fmatCount = readshortle(file)
        self.paramCount = readshortle(file)
        self.fmdlUnk3 = readlongle(file)
        self.padding = readlongle(file)
class fvtxh:
    def __init__(self,file):
        self.fvtx = file.read(4)
        self.padding = readu64(file)
        self.padding = readlongle(file)
        self.attArrOff = readu64(file)
        self.attIndxOff = readu64(file)
        self.UnkOffset1 = readu64(file)
        self.UnkOffset3 = readu64(file)
        self.UnkOffset4 = readu64(file)
        self.vtxBuffSizeOff = readu64(file)
        self.vtxStrideSizeOff = readu64(file)
        self.buffArrOff = readu64(file)
        self.buffOff = readlongle(file)
        self.attCount = readByte(file)
        self.buffCount = readByte(file)
        self.sectIndx = readshortle(file)
        self.vertCount = readlongle(file)
        self.UnkCount3 = readlongle(file)
class fmath:
    def __init__(self,file):
        self.fmat = file.read(4)
        self.UnkOffset1A = readu64(file)
        self.padding = readlongle(file)
        self.matOff = readu64(file)
        self.shadParamIndxOff = readu64(file)
        self.rendParamIndx = readu64(file)
        self.shadeOff = readu64(file)
        self.Unk1Off = readu64(file)
        self.texSelOff = readu64(file)
        self.Unk2Off = readu64(file)
        self.texAttSelOff = readu64(file)
        self.texAttIndxOff = readu64(file)
        self.matParamArrOff = readu64(file)
        self.matParamIndxOff = readu64(file)
        self.matParamOff = readu64(file)
        self.Unk3Off = readu64(file)
        self.Unk4Off = readu64(file)
        self.Unk5Off = readu64(file)
        self.Unk6Off = readu64(file)
        self.Unk7Off = readu64(file)
        self.Unk8Off = readu64(file)
        self.u1 = readlongle(file)
        self.sectIndx = readshortle(file)
        self.rendParamCount = readshortle(file)
        self.texSelCount = readByte(file)
        self.texAttSelCount = readByte(file)
        self.matParamCount = readshortle(file)
        self.u2 = readshortle(file)
        self.matParamSize = readshortle(file)
        self.padding = readlongle(file)
        self.padding = readlongle(file)

class fsklh:
    def __init__(self,file,verNumB):
        self.fskl = file.read(4)
        self.UnkOffset1A = readu64(file)
        self.padding = readlongle(file)
        self.boneIndxOff = readu64(file)
        self.boneArrOff = readu64(file)
        self.invIndxArrOff = readu64(file)
        self.invMatrArrOff = readu64(file)
        if verNumB == 8:
            self.padding = readu64(file)
            self.padding = readu64(file)
            self.padding = readu64(file)
        else:
            self.padding = readu64(file)
        self.UnkOffset5 = readlongle(file)
        self.boneArrCount = readshortle(file)
        self.invIndxArrCount = readshortle(file)
        self.exIndxCount = readshortle(file)
        self.UnkCount2 = readshortle(file)
        self.padding = readlongle(file)

class bonedatah:
    def __init__(self,file,verNumB):
        self.bNameOff = readlongle(file)
        if verNumB == 8:
            self.padding = readu64(file)
            self.padding = readu64(file)
            self.padding = readu64(file)
            self.padding = readu64(file)		
            self.padding = readu32be(file)		
        else:
            self.padding = readu64(file)
            self.padding = readu64(file)
            self.padding = readu32be(file)
        self.bIndx = readshortle(file)
        self.parIndx1 = readshortle(file)
        self.parIndx2 = readshortle(file)
        self.parIndx3 = readshortle(file)
        self.parIndx4 = readshortle(file)
        self.u1 = readshortle(file)
        self.bFlags = readshortle(file)
        self.u2 = readshortle(file)
        self.scaleX = readfloatle(file)
        self.scaleY = readfloatle(file)
        self.scaleZ = readfloatle(file)
        self.rotX = readfloatle(file)
        self.rotY = readfloatle(file)
        self.rotZ = readfloatle(file)
        self.rotW = readfloatle(file)
        self.posX = readfloatle(file)
        self.posY = readfloatle(file)
        self.posZ = readfloatle(file)

class fshph:
    def __init__(self,file):
        self.fshp = file.read(4)
        self.padding = readu64(file)
        self.padding = readlongle(file)
        self.polyNameOff = readu64(file)
        self.fvtxOff = readu64(file)
        self.lodMdlOff = readu64(file)
        self.ofsSkinBoneIndexList = readu64(file)
        self.padding = readu64(file)
        self.padding = readu64(file)
        self.BoundingBoxOffset = readu64(file)
        self.RadiusOffset = readu64(file)
        self.padding = readu64(file)
        self.Flags = readlongle(file)
        self.Index = readshortle(file)
        self.fmatIndx = readshortle(file)
        self.fsklIndx = readshortle(file)
        self.fvtxIndx = readshortle(file)
        self.fsklIndxArrCount = readshortle(file)
        self.VertexSkinCount = readByte(file)
        self.lodMdlCount = readByte(file)
        self.visGrpCount = readlongle(file)
        self.visGrpIndex = readshortle(file)
        self.fsklIndxArrOff = readshortle(file)

class shaderparam:
    def __init__(self,file):
        self.padding = readu64(file) 
        self.ShaderParamNameOffset = readu64(file) 
        self.Type = readByte(file)
        self.Size = readByte(file)
        self.Offset = readu16le(file)
        self.Uniform_variable_offset = readlongle(file) 
        self.IndexThingy = readlongle(file)
        self.padding = readlongle(file)
		
class attdata:
    def __init__(self,attName,buffIndx,buffOff,vertType):
        self.attName = attName
        self.buffIndx = buffIndx
        self.buffOff = buffOff
        self.vertType = vertType
class buffData:
    def __init__(self,buffSize,strideSize,dataOffset):
        self.buffSize = buffSize
        self.strideSize = strideSize
        self.dataOffset = dataOffset

#Now parse Wii U
class WiiUfmdlh:
    def __init__(self,file):
        self.fmdl = file.read(4)
        self.fnameOff = ReadOffset(file)
        self.eofString = ReadOffset(file)
        self.fsklOff = ReadOffset(file)
        self.fvtxArrOff = ReadOffset(file)
        self.fshpIndx = ReadOffset(file)
        self.fmatIndx = ReadOffset(file)
        self.paramOff = ReadOffset(file)
        self.fvtxCount = readu16be(file)
        self.fshpCount = readu16be(file)
        self.fmatCount = readu16be(file)
        self.paramCount = readu16be(file)
class WiiUfvtxh:
    def __init__(self,file):
        self.fmdl = file.read(4)
        self.attCount = readByte(file)
        self.buffCount = readByte(file)
        self.sectIndx = readu16be(file)
        self.vertCount = readu32be(file)
        self.u1 = readu16be(file)
        self.u2 = readu16be(file)
        self.attArrOff = ReadOffset(file)
        self.attIndxOff = ReadOffset(file)
        self.buffArrOff = ReadOffset(file)
        self.padding = readu32be(file)
class WiiUfmath:
    def __init__(self,file):
        self.fmat = file.read(4)
        self.matOff = ReadOffset(file)
        self.u1 = readu32be(file)
        self.sectIndx = readu16be(file)
        self.rendParamCount = readu16be(file)
        self.texSelCount = readByte(file)
        self.texAttSelCount = readByte(file)
        self.matParamCount = readu16be(file)
        self.matParamSize = readu32be(file)
        self.u2 = readu32be(file)
        self.rendParamIndx = ReadOffset(file)
        self.unkMatOff = ReadOffset(file)
        self.shadeOff = ReadOffset(file)
        self.texSelOff = ReadOffset(file)
        self.texAttSelOff = ReadOffset(file)
        self.texAttIndxOff = ReadOffset(file)
        self.matParamArrOff = ReadOffset(file)
        self.matParamIndxOff = ReadOffset(file)
        self.matParamOff = ReadOffset(file)
        self.shadParamIndxOff = ReadOffset(file)

class WiiUfsklh:
    def __init__(self,file):
        self.fskl = file.read(4)
        self.u1 = readu16be(file)
        self.fsklType = readu16be(file)
        self.boneArrCount = readu16be(file)
        self.invIndxArrCount = readu16be(file)
        self.exIndxCount = readu16be(file)
        self.u3 = readu16be(file)
        self.boneIndxOff = ReadOffset(file)
        self.boneArrOff = ReadOffset(file)
        self.invIndxArrOff = ReadOffset(file)
        self.invMatrArrOff = ReadOffset(file)
        self.padding = readu32be(file)

class WiiUfshph:
    def __init__(self,file):
        self.fshp = file.read(4)
        self.polyNameOff = ReadOffset(file)
        self.u1 = readu32be(file)
        self.fvtxIndx = readu16be(file)
        self.fmatIndx = readu16be(file)
        self.fsklIndx = readu16be(file)
        self.sectIndx = readu16be(file)
        self.fsklIndxArrCount = readu16be(file)
        self.matrFlag = readByte(file)
        self.lodMdlCount = readByte(file)
        self.visGrpCount = readu32be(file)
        self.u3 = readfloatbe(file)
        self.fvtxOff = ReadOffset(file)
        self.lodMdlOff = ReadOffset(file)
        self.fsklIndxArrOff = ReadOffset(file)
        self.u4 = readu32be(file)
        self.visGrpNodeOff = ReadOffset(file)
        self.visGrpRangeOff = ReadOffset(file)
        self.visGrpIndxOff = ReadOffset(file)
        self.u5 = readu32be(file)

class WiiUattdata:
    def __init__(self,attName,buffIndx,buffOff,vertType):
        self.attName = attName
        self.buffIndx = buffIndx
        self.buffOff = buffOff
        self.vertType = vertType
class WiiUbuffData:
    def __init__(self,buffSize,strideSize,dataOffset):
        self.buffSize = buffSize
        self.strideSize = strideSize
        self.dataOffset = dataOffset

def readCSV(cvsIn):

    ii = 0
    for line in cvsIn:
        if line.startswith("Obj Name"):
                if(ii > 0):
                    polys.append(data)
                data = poly()
                data.name = line.split(":")[1].replace("\n", "")
                ii += 1
                SubType = 0
        elif line.startswith("tex_Array:"):
            pass
        elif line.startswith("Bone_Suport"):
            pass
        elif line.startswith("Color_Suport"):
            colorEnable = True
        elif line.startswith("UV_Num:"):
            numUVs = int(line.split(":")[1].replace("\n", ""))
        elif line.startswith("vert_Array"):
            Type = 1
        elif line.startswith("face_Array"):
            Type = 2
        elif line.startswith("bone_Array"):
            Type = 3
        else:
            line = line.replace("\n", "").replace("\r", "").split(",")
            if(Type == 1):
                if(SubType == 0):
                    data.verts.append(line)
                    SubType += 1
                elif(SubType == 1):
                    data.normals.append(line)
                    SubType += 1
                elif(SubType == 2):
                    data.colors.append(line)
                    SubType += 1
                elif(SubType == 3):
                    data.uv0.append(line)
                    if(numUVs == 1):SubType = 0
                    else:SubType += 1
                elif(SubType == 4):
                    data.uv1.append(line)
                    if(numUVs == 2):SubType = 0
                    else:SubType += 1
                elif(SubType == 5):
                    data.uv2.append(line)
                    if(numUVs == 3):SubType = 0
                    else:SubType += 1
                elif(SubType == 6):
                    data.uv3.append(line)
                    SubType = 0
            elif(Type == 2):
                data.faces.append(line)
            elif(Type == 3):
                line.pop()
                bbs = 0
                StrNames = []
                BonArry = []
                for obj in line:
                        
                        if(bbs == 0):
                                StrNames.append(obj)
                                bbs += 1
                        else:
                                BonArry.append(float(obj))
                                bbs = 0
                data.boneName.append(StrNames)
                data.boneW.append(BonArry)
              
    try:
        if(numUVs == 1):print("\nNo second UV map found in CSV. \nScript will automatically assign the first one if exists! \n");
    except:
        print("Error! CSV is either blank or invalid!")	
    polys.append(data)


#lets start binomial and tangent calculation. These are done off of UV maps (BOTW possibly by UV layer 2 which has the normal map on(

def cross(u, v):
        return [u[1]*v[2] - u[2]*v[1],
                u[2]*v[0] - u[0]*v[2],
                u[0]*v[1] - u[1]*v[0]]


def mag(u):
        return (u[0]**2 + u[1]**2 + u[2]**2)**(1/2)


def scale(u, c):
        return [c*u[0], c*u[1], c*u[2]]


def unit(u):
        return scale(u, 1/mag(u))


	


		

		

def readBFRES(f, Index): #This index variable is for the FMDL choosen.

    endianness = "<"


    AllVerts = []

    f.seek(4) #Magic
    SwitchCheck = readlongle(f)

	#First it checks if it's a Switch BFRES, if not then assume it's a Wii U BFRES
	
    if (SwitchCheck == 0x20202020): #Check magic padding from fres....
        print("Found Switch BFRES! \n")

        f.seek(0x08)
        verNumD = readByte(f)
        verNumC = readByte(f)
        verNumB = readByte(f)
        verNumA = readByte(f)


        print ("BFRES Version: " + str(verNumD) + "." + str(verNumB) + "." + str(verNumC) + "." + str(verNumA))



                
        f.seek(0x28)
        FMDLOffset = readlongle(f)

        f.seek(0xBC)
        FMDLTotal = readunshortle(f)

        if Index != None:
            if Index > FMDLTotal:
                print('Error. Model index you typed in is too high than model count (' + str(FMDLTotal) + ')')

                
        f.seek(FMDLOffset,0)
        for mdl in range(1, FMDLTotal + 1):
            FMDLOffset = f.tell()
            f.seek(FMDLOffset)

            GroupArray = []
            FMDLArr = []
            FVTXArr = []
            FSKLArr = []
            FMATArr = []
            FMATNameArr = []
            FSHPArr = []
            VTXAttr = []
            MatParamArr = []
            MatParamNameArr = []
            MatParamDataArr = []
            BoneArray =  []
            BoneDataArr = []
            BoneFixArray = []
            invIndxArr = []
            invMatrArr = []
            Node_Array = []

            #F_Model Header
            fmdl_info = fmdlh(f)
            FMDLArr.append(fmdl_info)
            NextFMDL = f.tell()

            if Index != None:
                if Index:
                    if mdl != Index:
                       continue
                        
                   
            f.seek(fmdl_info.fnameOff)
            f.seek(0x02,1)
            FMDLName = getString(f)
            print("-------------------")
            print("FMDL = " + FMDLName)
            print("-------------------")
            #F_Vertex Header
            f.seek(fmdl_info.fvtxArrOff)
            for vtx in range(fmdl_info.fvtxCount):FVTXArr.append(fvtxh(f))	
            f.seek(fmdl_info.fmatOff)
            #F_Material Header
            for mat in range(fmdl_info.fmatCount):
                fmat_info = fmath(f)
                FMATArr.append(fmat_info)
                        
                pos = f.tell()
                        
                f.seek(fmat_info.matOff)
                f.seek(0x02,1)
                MatParamName = getString(f)

                #Shader Param
                f.seek(fmat_info.matParamArrOff) 
                for matparam in range(fmat_info.matParamCount):
                

                    Rtn = f.tell()
                        
                    matparam_info = shaderparam(f)
                    MatParamArr.append(matparam_info)
                        

                    if matparam_info.Type == 0:
                        f.seek(fmat_info.matParamOff + matparam_info.Offset)
                        Value = readByte(f)
                        f.seek(matparam_info.ShaderParamNameOffset)
                        f.seek(0x02,1)
                        MatParamName1 = getString(f)
                        
                    if matparam_info.Type == 12:
                        f.seek(fmat_info.matParamOff + matparam_info.Offset)
                        Value = readfloatle(f)
                        f.seek(matparam_info.ShaderParamNameOffset)
                        f.seek(0x02,1)
                        MatParamName1 = getString(f)

                    if matparam_info.Type == 15:
                        f.seek(matparam_info.ShaderParamNameOffset + 2)
                        MatParamName1 = getString(f)
                                                                
                                        #Here this will reset bake map coordinates so the bake map can be edited. 
                        if MatParamName1 == "gsys_bake_st1":
                            f.seek(fmat_info.matParamOff + matparam_info.Offset)
                            writefloatle(f,1)
                            writefloatle(f,1)
                            writefloatle(f,0)
                            writefloatle(f,0)
                        if MatParamName1 == "gsys_bake_st0":
                            f.seek(fmat_info.matParamOff + matparam_info.Offset)
                            writefloatle(f,1)
                            writefloatle(f,1)
                            writefloatle(f,0)
                            writefloatle(f,0)




                    if matparam_info.Type == 14:
                        f.seek(fmat_info.matParamOff + matparam_info.Offset)
                        test = "vector3f"
                        ValueX = readfloatle(f)
                        ValueY = readfloatle(f)
                        ValueZ = readfloatle(f)

                    if matparam_info.Type == 13:
                        f.seek(fmat_info.matParamOff + matparam_info.Offset)
                        test = "vector2f"
                        ValueX = readfloatle(f)
                        ValueY = readfloatle(f)
                                
                    if matparam_info.Type == 30:
                        f.seek(fmat_info.matParamOff + matparam_info.Offset)


                                
                    f.seek(matparam_info.ShaderParamNameOffset)
                    f.seek(0x02,1)
                    MatParamName = getString(f)
                                
                                
                    f.seek(Rtn)
                    f.seek(32,1) #32 is length of a single shader param in array.
                                
                f.seek(pos)	
            #F_Skeleton Header
            f.seek(fmdl_info.fsklOff)
            fskl_info = fsklh(f, verNumB)
            FSKLArr.append(fskl_info)

            #Get Bone names
            BoneNameArray = []
            f.seek(fskl_info.boneArrOff)
            for bonz in range(fskl_info.boneArrCount):
                    bonedata_info = bonedatah(f, verNumB)
                    BoneDataArr.append(bonedata_info)
            
                                    
                    rtn = f.tell()
                    f.seek(bonedata_info.bNameOff)
                    f.seek(0x02,1)
                    BoneNameArray.append(getString(f))

                                
                    f.seek(rtn)

           
                                
                                
            OptimizedBoneInd = []
            #Node Setup
            f.seek(fskl_info.invIndxArrOff)
            for nodes in range(fskl_info.invIndxArrCount + fskl_info.exIndxCount):Node_Array.append(readshortle(f))
            for thing in Node_Array:
                    OptimizedBoneInd.append(BoneNameArray[thing])
            #print(BoneNameArray)
            #print(OptimizedBoneInd)
            for pol in polys:
                    pol.boneI = []
                    
                    for nams in pol.boneName:
                            boneInx = []
                            for nnn in nams:
                                    for b,boneName in enumerate(OptimizedBoneInd):
                                            if nnn == boneName:
                                                    boneInx.append(b)
                            pol.boneI.append(boneInx)
                  #  print(pol.boneI)
            #print(polys[0].boneName)
                                            

            #F_Shape Header
            f.seek(fmdl_info.fshpIndx)
            for shp in range(fmdl_info.fshpCount):
                #print(hex(f.tell()))
                
                FSHPArr.append(fshph(f))
                Rtn = f.tell()
                f.seek(Rtn)

            #Mesh Building

            for m in range(len(FSHPArr)):
                    

                f.seek(FSHPArr[m].polyNameOff)
                f.seek(0x02,1)
                        
                MeshName = getString(f)
                print(MeshName)
                
                #Hacky RLT Reading from RTB
                f.seek(0x18)
                RLTOff = readlongle(f)
                f.seek(RLTOff)

                f.seek(0x30,1)
                Datastart = readlongle(f)
                                
                
                AttrArr = []

                f.seek(FVTXArr[FSHPArr[m].fvtxIndx].attArrOff)
                for att in range(FVTXArr[FSHPArr[m].fvtxIndx].attCount):
                    AttTypeOff = readlongle(f)
                    padding = readlongle(f)
                    Rtn1 = f.tell()
                    f.seek(AttTypeOff)
                    AttTypeLength = readshortle(f)
                    AttType = getString(f)
                  #  print(AttType)

                    f.seek(Rtn1)
                    vertType = readu16be(f)
                  #  print(str(AttType) + " " + str(vertType))

                    padding = readshortle(f)
                    buffOff = readshortle(f)
                    buffIndx = readshortle(f)
                    AttrArr.append(attdata(AttType,buffIndx,buffOff,vertType))
              #  print("Buff Count = " + str((FVTXArr[FSHPArr[m].fvtxIndx].buffCount)))
                        
                        
                BuffArr = []
                for buf in range(0, FVTXArr[FSHPArr[m].fvtxIndx].buffCount):
                    f.seek(FVTXArr[FSHPArr[m].fvtxIndx].vtxBuffSizeOff + ((buf) * 0x10))
                    BufferSize = readlongle(f)
                    f.seek(FVTXArr[FSHPArr[m].fvtxIndx].vtxStrideSizeOff + ((buf) * 0x10))
                    StrideSize = readlongle(f)
                    if buf == 0:
                        DataOffset = Datastart + FVTXArr[FSHPArr[m].fvtxIndx].buffOff
                    if buf > 0:
                        DataOffset = BuffArr[buf - 1].dataOffset + (BuffArr[buf - 1].buffSize)
                    if DataOffset % 8 != 0:
                        DataOffset = DataOffset + ((8 - DataOffset) % 8)


                   # print(DataOffset)
                  #  print(StrideSize)
                  #  print(BufferSize)

               #     if mod (DataOffset)  != 0:
               #         DataOffset = (DataOffset + (8 - (mod (DataOffset)  )))

                    BuffArr.append(buffData(BufferSize,StrideSize,DataOffset))
                                
              #  for item in BuffArr:
                         #  print("Buffer Size = " + str(item.buffSize))
                          # print("StrideSize Size = " + str(item.strideSize))
                         #  print("DataOffset Size = " + str(item.dataOffset))

                                
                        
                f.seek(FSHPArr[m].lodMdlOff)
                        
                FaceArray = []

                SubMeshOff = readlongle(f)
                padding = readlongle(f)
                unk1 = readlongle(f)
                padding = readlongle(f)
                unk2 = readlongle(f)
                padding = readlongle(f)
                IndexBufferSizeOff = readlongle(f)
                padding = readlongle(f)
                FaceBuffer = readlongle(f)
                PrimativefaceType = readlongle(f)
                faceType = readlongle(f)
                FaceCount = readlongle(f)
                PolyStart = readlongle(f)
                SubmeshCount = readlongle(f)
               # print("Face Type = " + str(faceType))
               # print("PrimativefaceType = " + str(PrimativefaceType))
               # print("FaceBuffer = " + str(FaceBuffer + Datastart))
               # print("Datastart = " + str(Datastart))

                LODRet = f.tell()

                        #This will redirect the LOD data to the first one. 
                        #Todo. Auto optmize face data or accept LOD models
                for something in range(FSHPArr[m].lodMdlCount):
                       write32le(f,SubMeshOff)
                       f.seek(0x4,1)
                       write32le(f,unk1)
                       f.seek(0x4,1)
                       write32le(f,unk2)
                       f.seek(0x4,1)
                       write32le(f,IndexBufferSizeOff)
                       f.seek(0x4,1)
                       write32le(f,FaceBuffer)
                       write32le(f,PrimativefaceType)
                       write32le(f,faceType)
                       write32le(f,FaceCount)
                       write32le(f,PolyStart)
                       write32le(f,SubmeshCount)
                        
                f.seek(FaceBuffer + Datastart)
                        
                enablePop = True
                pp = poly()
                p = 0
                if(len(polys)>0):
                        while(enablePop):
                                if(MeshName == polys[p].name):
                                       print("A Match! %s" % polys[p].name)
                                       pp = polys.pop(p)
                                       enablePop = False
                                p += 1
                                if(len(polys)<=p):
                                      enablePop = False
                if(len(pp.verts) > 1):
                        print("CSV Vertex Count:%i" % len(pp.verts))
                print("\tBFRES Max VertCount:%i" % FVTXArr[FSHPArr[m].fvtxIndx].vertCount)
                if FVTXArr[FSHPArr[m].fvtxIndx].vertCount < len(pp.verts):
                        print("\n Error! This model has too many vertices! \n")
                        break
                #FVTXArr[FSHPArr[m].fvtxIndx].vertCount
                        
                for v in range(FVTXArr[FSHPArr[m].fvtxIndx].vertCount):
                        for attr in range(len(AttrArr)):
                                f.seek(((BuffArr[AttrArr[attr].buffIndx].dataOffset) + (AttrArr[attr].buffOff) + (BuffArr[AttrArr[attr].buffIndx].strideSize * v)))
                                if(len(pp.verts) > v):
                                        #print(pp.verts[v])
                                        vert = pp.verts[v]
                                        uv0 = pp.uv0[v]
                                        if(len(pp.uv1)>v):
                                                uv1 = pp.uv1[v]
                                        else:
                                                uv1 = [0,0]
                                        if(len(pp.uv2)>v):
                                                uv2 = pp.uv2[v]
                                        else:
                                                uv2 = [0,0]
                                        norm = pp.normals[v]
                                        color0 = pp.colors[v]
                                      #  tan = pp.tangents[v]
                                        if(len(pp.boneI)>v):
                                                binx = pp.boneI[v]
                                                bwgt = pp.boneW[v]
                                        else:
                                                binx = [0]
                                                bwgt = [1.0]
                                        tan = [0,0,0,0]
                                        bit = [0,0,0,0]
                                else:
                                        vert = [0,0,0]
                                        uv0 = [0,0]
                                        uv1 = [0,0]
                                        uv2 = [0,0]
                                        norm = [1,1,1]
                                        # test code, super hacky, probably wrong
                                        tan = cross([0, 1, 0], norm)
                                        if mag(tan) < 0.00001:
                                            tan = cross([0, 0, -1], norm)
                                        tan = unit(tan)
                                        bit = cross(norm, tan)
                                        tan.append(0)
                                        bit.append(0)
                                        # tan = [0,0,0,0]
                                        # bit = [0,0,0,0]]
                                        binx = [0]
                                        bwgt = [1.0]
                                        color0 = [127,127,127,127]
                                if(AttrArr[attr].attName == "_p0"):
                                        #print(hex(f.tell()))
                                        if(AttrArr[attr].vertType == 1301):
                                            #print(hex(f.tell()))
                                            for vt in vert:writehalffloatle(f,float(vt)) 
                                        elif(AttrArr[attr].vertType == 1304):
                                           # print(hex(f.tell()))
                                            for vt in vert:writefloatle(f,float(vt))
                                        else:print("Unk Vertex attr:%s" % hex(AttrArr[attr].vertType))
                                if(AttrArr[attr].attName == "_n0"):
                                        if(AttrArr[attr].vertType == 526):
                                                write10le(f,int(float(norm[0])*511),int(float(norm[1])*511),int(float(norm[2])*511))
                                if(AttrArr[attr].attName == "_t0"): #Todo tangent calulation from uv maps!
                                        if(AttrArr[attr].vertType == 523):
                                                for t in tan:
                                                        writeSByte(f,int(float(t)*127))
                                if(AttrArr[attr].attName == "_b0"):
                                        if(AttrArr[attr].vertType == 523):
                                                for b in bit:
                                                        writeSByte(f,int(float(b)*127))
                                if(AttrArr[attr].attName == "_c0"):
                                        if(AttrArr[attr].vertType == 267):
                                                for clr in color0:
                                                       writeByte(f,int(float(clr)))
                                        if(AttrArr[attr].vertType == 523):
                                                for clr in color0:
                                                       writeSByte(f,int(float(clr)/127))
                                        if(AttrArr[attr].vertType == 1301):
                                                for clr in color0:
                                                       writeByte(f,float(clr)/255)
                                if(AttrArr[attr].attName == "_u0"):
                                        if(AttrArr[attr].vertType == 1303):
                                                writefloatle(f,float(uv0[0]))
                                                writefloatle(f,float(uv0[1])*-1)
                                        elif(AttrArr[attr].vertType == 1298):
                                                writehalffloatle(f,float(uv0[0]))
                                                writehalffloatle(f,(float(uv0[1])*-1))
                                        elif(AttrArr[attr].vertType == 530):
                                                writelongle(f,float(uv0[0]))
                                                writelongle(f,(float(uv0[1])*-1))
                                        elif(AttrArr[attr].vertType == 519):
                                                writes16le(f,int(float(uv0[0])*32767))
                                                vvv = (float(uv0[1])*-1)+1
                                                writes16le(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 274):
                                                write16le(f,int(float(uv0[0])*65535))
                                                vvv = (float(uv0[1])*-1)+1
                                                write16le(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 265 or AttrArr[attr].vertType == 521):
                                                writeByte(f,int(float(uv0[0])*255))
                                                vvv = (float(uv0[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u1" % AttrArr[attr].vertType)
                                if(AttrArr[attr].attName == "_u1"):
                                        if(AttrArr[attr].vertType == 1303):
                                                writefloatle(f,float(uv1[0]))
                                                writefloatle(f,float(uv1[1])*-1)
                                        elif(AttrArr[attr].vertType == 1298):
                                                writehalffloatle(f,float(uv1[0]))
                                                writehalffloatle(f,(float(uv1[1])*-1))
                                        elif(AttrArr[attr].vertType == 530):
                                                writes16le(f,int(float(uv1[0])*32767))
                                                vvv = (float(uv1[1])*-1)+1
                                                writes16le(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 274):
                                                write16le(f,int(float(uv1[0])*65535))
                                                vvv = (float(uv1[1])*-1)+1
                                                write16le(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 265 or AttrArr[attr].vertType == 521):
                                                writeByte(f,int(float(uv1[0])*255))
                                                vvv = (float(uv1[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u1" % AttrArr[attr].vertType)

                                if(AttrArr[attr].attName == "_u2"):
                                        if(AttrArr[attr].vertType == 1303):
                                                writefloatle(f,float(uv2[0]))
                                                writefloatle(f,float(uv2[1])*-1)
                                        elif(AttrArr[attr].vertType == 1298):
                                                writehalffloatle(f,float(uv2[0]))
                                                writehalffloatle(f,(float(uv2[1])*-1))
                                        elif(AttrArr[attr].vertType == 530):
                                                writelongle(f,float(uv1[0]))
                                                writelongle(f,(float(uv1[1])*-1))
                                        elif(AttrArr[attr].vertType == 519):
                                                writes16be(f,int(float(uv2[0])*32767))
                                                vvv = (float(uv2[1])*-1)+1
                                                writes16be(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 274):
                                                write16be(f,int(float(uv2[0])*65535))
                                                vvv = (float(uv2[1])*-1)+1
                                                write16be(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 265 or AttrArr[attr].vertType == 521):
                                                writeByte(f,int(float(uv2[0])*255))
                                                vvv = (float(uv2[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u2" % AttrArr[attr].vertType)

                                if(AttrArr[attr].attName == "_i0"):
                                        if(AttrArr[attr].vertType == 779):
                                                for iii in range(4):
                                                        if(len(binx)<(iii+1)):
                                                                writeByte(f,0)
                                                        else:
                                                                writeByte(f,binx[iii])
                                        elif(AttrArr[attr].vertType == 777):
                                                for iii in range(2):
                                                        if(len(binx)<(iii+1)):
                                                                writeByte(f,0)
                                                        else:
                                                                writeByte(f,binx[iii])
                                        elif(AttrArr[attr].vertType == 770):
                                                writeByte(f,binx[0])
                                        else:print("Unk %i for _i0" % AttrArr[attr].vertType)
                                                
                                if(AttrArr[attr].attName == "_w0"):
                                        if(AttrArr[attr].vertType == 267):
                                                maxWeght = 255
                                                for iii in range(4):
                                                        #print("WGT%i\nRemaining Weight:%i" % (iii,maxWeght))
                                                        if(len(bwgt)<(iii+1)):
                                                                writeByte(f,0)
                                                                maxWeght = 0
                                                        else:
                                                                valWeght = int(bwgt[iii]*255)
                                                                if(len(bwgt) == iii+1):
                                                                        valWeght = maxWeght
                                                                if(valWeght>=maxWeght):
                                                                        #print("haythere")
                                                                        valWeght = maxWeght
                                                                        maxWeght = 0
                                                                else:
                                                                        maxWeght -= valWeght
                                                                writeByte(f,valWeght)
                                        if(AttrArr[attr].vertType == 265):
                                                maxWeght = 255
                                                for iii in range(2):
                                                        if(len(bwgt)<(iii+1)):
                                                                writeByte(f,maxWeght)
                                                                maxWeght = 0
                                                        else:
                                                                valWeght = (bwgt[iii]*255)
                                                                if(valWeght>maxWeght):
                                                                        valWeght = maxWeght
                                                                        maxWeght = 0
                                                                else:
                                                                        maxWeght -= valWeght
                                                                writeByte(f,valWeght)
                                                        
                                        #print("UV Type:%d" % AttrArr[attr].vertType)

                
                DataS = FaceBuffer + Datastart
                f.seek(FaceBuffer + Datastart)

                if(len(pp.verts) > 0):
                        print("CSV Face Count is %i" % len(pp.faces))
                        if faceType == 1:
                                for ff in range(FaceCount // 3):
                                        if(len(pp.faces) > ff):
                                                #print(pp.faces[ff])
                                                face = pp.faces[ff]    
                                        else:
                                                face = [1,2,3]
                                        for point in face:
                                                writeUShortle(f,int(float(point))-1)
                        if faceType == 9:
                                for ff in range(FaceCount // 12):
                                        if(len(pp.faces) > ff):face = pp.faces[ff]    
                                        else:face = [1,2,3]
                                        for point in face:
                                                write32be(f,int(float(point))-1)
                if faceType == 1:
                        print("\tBFRES Max Face Count:%i" % (FaceCount // 3))
                        if FaceCount // 3 < len(pp.faces):
                                print("Error! Too many faces!")
                                break
                if faceType == 9:
                        print("\tBFRES Max Face Count:%i" % (FaceCount // 12))
                        if int(FaceCount // 12) < len(pp.faces):
                                print("Error! Too many faces!")
                                break
                print("")

            f.seek(NextFMDL)
    else:
        print("Found Wii U BFRES! \n")

        f.seek(4)
        verNumD = readByte(f)
        verNumC = readByte(f)
        verNumB = readByte(f)
        verNumA = readByte(f)

        print ("BFRES Version: " + str(verNumD) + "." + str(verNumB) + "." + str(verNumC) + "." + str(verNumA))

        f.seek(5)
        verNum = readByte(f)
        f.seek(26,1)
        FileOffset = ReadOffset(f)
        f.seek(FileOffset)
        BlockSize = readu32be(f)
        FMDLTotal = readu32be(f)
        f.seek(0x10,1)

        if Index != None:
            if Index > FMDLTotal:
                print('Error. Model index you typed in is too high than model count (' + str(FMDLTotal) + ')')
            
        for mdl in range(1, FMDLTotal + 1):
            f.seek(12,1)
            FMDLOffset = ReadOffset(f)
            NextFMDL = f.tell()
            f.seek(FMDLOffset)

            GroupArray = []
            FMDLArr = []
            FVTXArr = []
            FSKLArr = []
            FMATArr = []
            FMATNameArr = []
            FSHPArr = []
            VTXAttr = []
                
            BoneArray = []
            BoneFixArray = []
            invIndxArr = []
            Node_Array = []
            invMatrArr = []

            #F_Model Header
            fmdl_info = WiiUfmdlh(f)
            FMDLArr.append(fmdl_info)
			
            f.seek(NextFMDL)
            if Index != None:
                if mdl != Index:
                    continue
                    
            f.seek(fmdl_info.fnameOff)
            FMDLName = getString(f)
            print("-------------------")
            print("FMDL = " + FMDLName)
            print("-------------------")
                    
            #F_Vertex Header
            f.seek(fmdl_info.fvtxArrOff)
            for vtx in range(fmdl_info.fvtxCount):FVTXArr.append(WiiUfvtxh(f))
            f.seek(fmdl_info.fmatIndx)
            f.seek(24,1)
            #F_Material Header
            for mat in range(fmdl_info.fmatCount):
                f.seek(8,1)
                FMATNameOffset = ReadOffset(f)
                Rtn = f.tell()
                f.seek(FMATNameOffset)

                FMATNameArr.append(getString(f))
                f.seek(Rtn)

                FMATOffset = ReadOffset(f)
                Rtn = f.tell()

                f.seek(FMATOffset)
                FMATArr.append(WiiUfmath(f))
                f.seek(Rtn)
            #F_Skeleton Header
            f.seek(fmdl_info.fsklOff)
            fskl_info = WiiUfsklh(f)
            FSKLArr.append(fskl_info)

            #Get Bone names
            BoneNameArray = []
            f.seek(fskl_info.boneArrOff)
            for bonz in range(fskl_info.boneArrCount):
                    #print(hex(f.tell()))
                    boneOffset = ReadOffset(f)
                                    
                    rtn = f.tell() + 0x3c
 
                                    
                    f.seek(boneOffset)
                    BoneNameArray.append(getString(f))
                    if(verNum <= 2):rtn += 48
                    f.seek(rtn)

            OptimizedBoneInd = []
            #Node Setup
            f.seek(fskl_info.invIndxArrOff)
            for nodes in range(fskl_info.invIndxArrCount + fskl_info.exIndxCount):Node_Array.append(readu16be(f))
            for thing in Node_Array:
                    OptimizedBoneInd.append(BoneNameArray[thing])
            #print(BoneNameArray)
            #print(OptimizedBoneInd)
            for pol in polys:
                    pol.boneI = []
                    
                    for nams in pol.boneName:
                            boneInx = []
                            for nnn in nams:
                                    for b,boneName in enumerate(OptimizedBoneInd):
                                            if nnn == boneName:
                                                    boneInx.append(b)
                            pol.boneI.append(boneInx)
                    #print(pol.boneI)
            #print(polys[0].boneName)
     
            #F_Shape Header
            f.seek(fmdl_info.fshpIndx + 24)
            for shp in range(fmdl_info.fshpCount):
                f.seek(12,1)
                #print(hex(f.tell()))
                FSHPOffset = ReadOffset(f)
                Rtn = f.tell()

                f.seek(FSHPOffset)
                
                FSHPArr.append(WiiUfshph(f))
                f.seek(Rtn)

            #Mesh Building

            for m in range(len(FSHPArr)):
                    

                f.seek(FSHPArr[m].polyNameOff)
                #print(FSHPArr[m].polyNameOff)
                MeshName = getString(f)
                print(MeshName)

                f.seek(FVTXArr[FSHPArr[m].fvtxIndx].attArrOff)
                AttrArr = []
                for att in range(FVTXArr[FSHPArr[m].fvtxIndx].attCount):
                    AttTypeOff = ReadOffset(f)
                    Rtn1 = f.tell()
                    f.seek(AttTypeOff)
                    AttType = getString(f)
                    f.seek(Rtn1)
                    buffIndx = readByte(f)
                    skip = readByte(f)
                    buffOff = readu16be(f)
                    vertType = readu32be(f)
                    AttrArr.append(attdata(AttType,buffIndx,buffOff,vertType))
                BuffArr = []
                f.seek(FVTXArr[FSHPArr[m].fvtxIndx].buffArrOff)
                for buf in range(FVTXArr[FSHPArr[m].fvtxIndx].buffCount):
                    f.seek(4,1)
                    BufferSize = readu32be(f)
                    f.seek(4,1)
                    StrideSize = readu16be(f)
                    f.seek(6,1)
                    DataOffset = ReadOffset(f)
                    BuffArr.append(buffData(BufferSize,StrideSize,DataOffset))

                f.seek(FSHPArr[m].lodMdlOff + 4)
                
                faceType = readu32be(f)
                f.seek(0xC,1)
                indxBuffOff = ReadOffset(f)
                f.seek(0x4,1)
                f.seek(indxBuffOff + 4)
                FaceCount = readu32be(f)
                f.seek(12,1)
                FaceBuffer = ReadOffset(f)
                enablePop = True
                pp = poly()
                p = 0
                if(len(polys)>0):
                        while(enablePop):
                                if(MeshName == polys[p].name):
                                       print("A Match! %s" % polys[p].name)
                                       pp = polys.pop(p)
                                       enablePop = False
                                p += 1
                                if(len(polys)<=p):
                                      enablePop = False
                if(len(pp.verts) > 1):
                        print("CSV Vertex Count:%i" % len(pp.verts))
                                        
                        print("\tMax VertCount:%i" % FVTXArr[FSHPArr[m].fvtxIndx].vertCount)
                                        
                        if FVTXArr[FSHPArr[m].fvtxIndx].vertCount < len(pp.verts):
                                            print("\n Error! This model has too many vertices! \n")
                                            break
                else:
                        print("\tBFRES Max VertCount:%i" % FVTXArr[FSHPArr[m].fvtxIndx].vertCount)

                                        
                for v in range(FVTXArr[FSHPArr[m].fvtxIndx].vertCount):
                        for attr in range(len(AttrArr)):
                                f.seek(((BuffArr[AttrArr[attr].buffIndx].dataOffset) + (AttrArr[attr].buffOff) + (BuffArr[AttrArr[attr].buffIndx].strideSize * v)))
                                if(len(pp.verts) > v):
                                        #print(pp.verts[v])
                                        vert = pp.verts[v]
                                        uv0 = pp.uv0[v]
                                        if numUVs == 1:
                                                if(AttrArr[attr].attName == "_u1"):
                                                        if(AttrArr[attr].vertType != 7):
                                                                uv1 = pp.uv0[v]
                                                        else:
                                                                if(len(pp.uv1)>v):
                                                                        uv1 = pp.uv1[v]
                                                                else:
                                                                        uv1 = [0,0]
                                        else:
                                                if(len(pp.uv1)>v):
                                                        uv1 = pp.uv1[v]
                                                else:
                                                        uv1 = [0,0]
                                        norm = pp.normals[v]
                                        color0 = pp.colors[v]
                                        if(len(pp.boneI)>v):
                                                binx = pp.boneI[v]
                                                bwgt = pp.boneW[v]
                                        else:
                                                binx = [0]
                                                bwgt = [1.0]
                                        tan = [0,0,0,0]
                                        bit = [0,0,0,0]
                                        uv2 = [0,0]
                                else:
                                        vert = [0,0,0]
                                        uv0 = [0,0]
                                        uv1 = [0,0]
                                        uv2 = [0,0]
                                        norm = [1,1,1]
                                        tan = [0,0,0,0]
                                        bit = [0,0,0,0]
                                        binx = [0]
                                        bwgt = [1.0]
                                        color0 = [127,127,127,127]
                                if(AttrArr[attr].attName == "_p0"):
                                        #print(hex(f.tell()))
                                        if(AttrArr[attr].vertType == 2063):
                                            #print(hex(f.tell()))
                                            for vt in vert:writehalffloatbe(f,float(vt)) 
                                        elif(AttrArr[attr].vertType == 2065):
                                            #print(hex(f.tell()))
                                            for vt in vert:writefloatbe(f,float(vt))
                                        else:print("Unk Vertex attr:%s" % hex(AttrArr[attr].vertType))
                                if(AttrArr[attr].attName == "_n0"):
                                        if(AttrArr[attr].vertType == 523):
                                                write10be(f,int(float(norm[0])*511),int(float(norm[1])*511),int(float(norm[2])*511))
                                if(AttrArr[attr].attName == "_t0"):
                                        if(AttrArr[attr].vertType == 522):
                                                for t in tan:
                                                        writeSByte(f,int(float(t)*127))
                                if(AttrArr[attr].attName == "_t0"):
                                        if(AttrArr[attr].vertType == 522):
                                                for b in bit:
                                                        writeSByte(f,int(float(b)*127))
                                if(AttrArr[attr].attName == "_c0"):
                                        if(AttrArr[attr].vertType == 10):
                                                for clr in color0:
                                                       writeByte(f,int(float(clr)))
                                        if(AttrArr[attr].vertType == 522):
                                                for clr in color0:
                                                       writeSByte(f,int(float(clr)/127))
                                        if(AttrArr[attr].vertType == 2063):
                                                for clr in color0:
                                                       writeByte(f,float(clr)/255)
                                if(AttrArr[attr].attName == "_u0"):
                                        if(AttrArr[attr].vertType == 2061):
                                                writefloatbe(f,float(uv0[0]))
                                                writefloatbe(f,float(uv0[1])*-1)
                                        elif(AttrArr[attr].vertType == 2056):
                                                writehalffloatbe(f,float(uv0[0]))
                                                writehalffloatbe(f,(float(uv0[1])*-1))
                                        elif(AttrArr[attr].vertType == 519):
                                                writes16be(f,int(float(uv0[0])*32767))
                                                vvv = (float(uv0[1])*-1)+1
                                                writes16be(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 7):
                                                write16be(f,int(float(uv0[0])*65535))
                                                vvv = (float(uv0[1])*-1)+1
                                                write16be(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 4 or AttrArr[attr].vertType == 516):
                                                writeByte(f,int(float(uv0[0])*255))
                                                vvv = (float(uv0[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u0" % AttrArr[attr].vertType)
                                if(AttrArr[attr].attName == "_u1"):
                                        if(AttrArr[attr].vertType == 2061):
                                                writefloatbe(f,float(uv1[0]))
                                                writefloatbe(f,float(uv1[1])*-1)
                                        elif(AttrArr[attr].vertType == 2056):
                                                writehalffloatbe(f,float(uv1[0]))
                                                writehalffloatbe(f,(float(uv1[1])*-1))
                                        elif(AttrArr[attr].vertType == 519):
                                                writes16be(f,int(float(uv1[0])*32767))
                                                vvv = (float(uv1[1])*-1)+1
                                                writes16be(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 7):
                                                write16be(f,int(float(uv1[0])*65535))
                                                vvv = (float(uv1[1])*-1)+1
                                                write16be(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 4 or AttrArr[attr].vertType == 516):
                                                writeByte(f,int(float(uv1[0])*255))
                                                vvv = (float(uv1[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u1" % AttrArr[attr].vertType)
                                if(AttrArr[attr].attName == "_u2"):
                                        if(AttrArr[attr].vertType == 2061):
                                                writefloatbe(f,float(uv2[0]))
                                                writefloatbe(f,float(uv2[1])*-1)
                                        elif(AttrArr[attr].vertType == 2056):
                                                writehalffloatbe(f,float(uv2[0]))
                                                writehalffloatbe(f,(float(uv2[1])*-1))
                                        elif(AttrArr[attr].vertType == 519):
                                                writes16be(f,int(float(uv2[0])*32767))
                                                vvv = (float(uv2[1])*-1)+1
                                                writes16be(f,int(vvv*32767))
                                        elif(AttrArr[attr].vertType == 7):
                                                write16be(f,int(float(uv2[0])*65535))
                                                vvv = (float(uv2[1])*-1)+1
                                                write16be(f,int(vvv*65535))
                                        elif(AttrArr[attr].vertType == 4 or AttrArr[attr].vertType == 516):
                                                writeByte(f,int(float(uv2[0])*255))
                                                vvv = (float(uv2[1])*-1)+1
                                                writeByte(f,int(vvv*255))
                                        else:
                                                print("Unk %i for _u2" % AttrArr[attr].vertType)
                                if(AttrArr[attr].attName == "_i0"):
                                        if(AttrArr[attr].vertType == 266):
                                                for iii in range(4):
                                                        if(len(binx)<(iii+1)):
                                                                writeByte(f,0)
                                                        else:
                                                                writeByte(f,binx[iii])
                                        elif(AttrArr[attr].vertType == 260):
                                                for iii in range(2):
                                                        if(len(binx)<(iii+1)):
                                                                writeByte(f,0)
                                                        else:
                                                                writeByte(f,binx[iii])
                                        elif(AttrArr[attr].vertType == 256):
                                                writeByte(f,binx[0])
                                        else:print("Unk %i for _i0" % AttrArr[attr].vertType)
                                                
                                if(AttrArr[attr].attName == "_w0"):
                                        if(AttrArr[attr].vertType == 10):
                                                maxWeght = 255
                                                for iii in range(4):
                                                        #print("WGT%i\nRemaining Weight:%i" % (iii,maxWeght))
                                                        if(len(bwgt)<(iii+1)):
                                                                writeByte(f,0)
                                                                maxWeght = 0
                                                        else:
                                                                valWeght = int(bwgt[iii]*255)
                                                                if(len(bwgt) == iii+1):
                                                                        valWeght = maxWeght
                                                                if(valWeght>=maxWeght):
                                                                        #print("haythere")
                                                                        valWeght = maxWeght
                                                                        maxWeght = 0
                                                                else:
                                                                        maxWeght -= valWeght
                                                                writeByte(f,valWeght)
                                        if(AttrArr[attr].vertType == 4):
                                                maxWeght = 255
                                                for iii in range(2):
                                                        if(len(bwgt)<(iii+1)):
                                                                writeByte(f,maxWeght)
                                                                maxWeght = 0
                                                        else:
                                                                valWeght = (bwgt[iii]*255)
                                                                if(valWeght>maxWeght):
                                                                        valWeght = maxWeght
                                                                        maxWeght = 0
                                                                else:
                                                                        maxWeght -= valWeght
                                                                writeByte(f,valWeght)
                                                        
                                        #print("UV Type:%d" % AttrArr[attr].vertType)

                

                f.seek(FaceBuffer)

                
                        
              
                if(len(pp.verts) > 0):
                        print("CSV Face Count is %i" % len(pp.faces))
                        if faceType == 4:
                                for ff in range(FaceCount // 6):
                                        if(len(pp.faces) > ff):
                                                #print(pp.faces[ff])
                                                face = pp.faces[ff]    
                                        else:
                                                face = [1,2,3]
                                        for point in face:
                                                write16be(f,int(float(point))-1)
                        if faceType == 9:
                                for ff in range(FaceCount // 12):
                                        if(len(pp.faces) > ff):face = pp.faces[ff]    
                                        else:face = [1,2,3]
                                        for point in face:
                                                write32be(f,int(float(point))-1)
     
                if faceType == 4:
                        print("\tBFRES Max Face Count:%i" % (FaceCount // 6))
                        if (FaceCount // 6) < len(pp.faces):
                                print("Error! Too many faces!")
                                break
                if faceType == 9:
                        print("\tBFRES Max Face Count:%i" % (FaceCount // 12))
                        if (FaceCount // 12) < len(pp.faces):
                                print("Error! Too many faces!")
                                break


                                                                                            
            f.seek(NextFMDL)
            
    f.close()
