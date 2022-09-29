# SICXE Assembler
# Mahmoud Saeed Osman  18102867
# Walid Kamal Eldin    18100647

import os

Instruction_Table = {

    'FIX': [1, 0xC4, 0], 'FLOAT': [1, 0xC0, 0], 'HIO': [1, 0xF4, 0], 'NORM': [1, 0xC8, 0], 'SIO': [1, 0xF0, 0], 'TIO': [1, 0xF8, 0],
    'ADDR': [2, 0x90, 2], 'CLEAR': [2, 0xB4, 1], 'COMPR': [2, 0xA0, 2], 'DIVR': [2, 0x9C, 2], 'MULR': [2, 0x98, 2], 'RMO': [2, 0xAC, 2],
    'SHIFTL': [2, 0xA4, 2], 'SHIFTR': [2, 0xA8, 2], 'SUBR': [2, 0x94, 2], 'SVC': [2, 0xB0, 1], 'TIXR': [2, 0xB8, 1], 'ADD': [3, 0x18, 1],
    'ADDF': [3, 0x58, 1], 'AND': [3, 0x40, 1], 'COMP': [3, 0x28, 1], 'COMPF': [3, 0x88, 1], 'DIV': [3, 0x24, 1], 'DIVF': [3, 0x64, 1],
    'J': [3, 0x3C, 1], 'JEQ': [3, 0x30, 1], 'JGT': [3, 0x34, 1], 'JLT': [3, 0x38, 1], 'JSUB': [3, 0x48, 1], 'LDA': [3, 0x00, 1],
    'LDB': [3, 0x68, 1], 'LDCH': [3, 0x50, 1], 'LDF': [3, 0x70, 1], 'LDL': [3, 0x08, 1], 'LDS': [3, 0x6C, 1], 'LDT': [3, 0x74, 1],
    'LDX': [3, 0x04, 1], 'LPS': [3, 0xD0, 1], 'MUL': [3, 0x20, 1], 'MULF': [3, 0x60, 1], 'OR': [3, 0x44, 1], 'RD': [3, 0xD8, 1],
    'RSUB': [3, 0x4C, 0], 'SSK': [3, 0xEC, 1], 'STA': [3, 0x0C, 1], 'STB': [3, 0x78, 1], 'STCH': [3, 0x54, 1], 'STF': [3, 0x80, 1],
    'STI': [3, 0xD4, 1], 'STL': [3, 0x14, 1], 'STS': [3, 0x7C, 1], 'STSW': [3, 0xE8, 1], 'STT': [3, 0x84, 1], 'STX': [3, 0x10, 1],
    'SUB': [3, 0x1C, 1], 'SUBF': [3, 0x5C, 1], 'TD': [3, 0xE0, 1], 'TIX': [3, 0x2C, 1], 'WD': [3, 0xDC, 1]
}

Resgisters = {
    'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6, 'PC': 8, 'SW': 9
}
Loc = 0
StarteAddr=0

def Get_OP(Instruction):    #Returns OP Code of Instrunction
    if any((Instruction in Instruction) for Instruction in Instruction_Table):
        try:
            OP = Instruction_Table[Instruction][1]
            return OP
        except KeyError:
            pass

def Get_Format(Instruction):    #Returns Formats of Instruction
    if any((Instruction in Instruction) for Instruction in Instruction_Table):
        try:
            Format = Instruction_Table[Instruction][0]
            return Format
        except KeyError:
            pass

def PASS_1():   #Executes Pass 1 to get LOC , stores it in Support Files/Program.txt 
    global Loc
    global StartAddr
    Byte_Counter = 0
    LiteralFlag = 0
    starCounter = 0
    
    FileName = input('Enter Test File Name: ')+ '.txt'
    Fname=Insert_Literals(FileName)

    open('Support Files/Program.txt', 'w').close()
    open('Support Files/temp.txt', 'w').close()
    open('Support Files/tempL.txt', 'w').close()

    Name = open(Fname, 'r')  
    First_line = Name.readline().split()
    Loc = int(str(First_line[-1]), 16)          # Gets Start Address for Relocation
    StartAddr=int(str(First_line[-1]), 16)   
    Name.close()

    with open(Fname, 'r') as file:
        Out = open('Support Files/Program.txt', 'a')
        Out.write('Loc       Source Statement               OBJECT CODE\n')

        for line in file:
            
            Out = open('Support Files/Program.txt', 'a')
            temp = open('Support Files/temp.txt', 'a')
            tempL = open('Support Files/tempL.txt', 'a')
            if('LTORG' in line):
                Out.write(''+line)

            elif('.' in line):
                Out.write('\n'+line+'\n')
                continue

            elif(line.split()):
                Out.write("{:<12}{:<6}".format('0x'+hex(Loc)[2:].zfill(4), line))
                Out.close()

            if (line[0] != ' ') and (line[0] != '\t') and (line[0] != '*'):
                temp.write(hex(Loc)+'     '+line)
                temp.close()

            if (line[0] == '*'):
                tempL.write(hex(Loc)+'     '+line)
                tempL.close()

            for word in line.split():
                if ('+' in word):
                    Loc += 4

                elif ('&' in word):
                    Loc += 3

                elif ('$' in word):
                    Loc += 4

                elif (word == 'WORD'):
                    Loc += 3

                elif (word == 'BYTE'):
                    Byte_Counter = 1
                    continue

                elif(word == 'RESB'):
                    Byte_Counter = 2
                    continue

                elif(word == 'RESW'):
                    Byte_Counter = 3
                    continue
                
                elif (word == 'LTORG' or word=='END' ):    
                    LiteralFlag = 1
                    continue

                elif (word == '*'):
                    starCounter = 1

                elif (Byte_Counter == 1):                                  
                    Byte_Counter = 0
                    WordsB = word.split(',')  
                    for i in range (len(WordsB)):
                        if(WordsB[i][0] == 'C'):                            
                            Loc += len(WordsB[i][2:-1])

                        elif(WordsB[i][0] == 'X'):
                            Loc += 1
                        else:
                            Loc+=3

                elif (Byte_Counter == 2):
                    Loc = Loc+int(word)
                    Byte_Counter = 0

                elif (Byte_Counter == 3):
                    Loc = Loc+int(word)*3
                    Byte_Counter = 0

                elif (LiteralFlag == 1 and word[0] == '=' and starCounter == 1):
                    if(word[1] == 'C'):
                        Loc += len(word[3:-1])
                    if(word[1] == 'X'):
                        Loc += 1
                    elif(word[1].isdigit()):
                        print(word)
                        Loc+=3

                    starCounter=0

                elif any((word in word) for word in Instruction_Table):
                    try:
                        Format = int(Instruction_Table[word][0])
                        Loc = Loc+Format
                    except KeyError:
                        continue
    
    file.close()
    Out.close()
    temp.close()
    tempL.close()
    Symbol_Table()
    Literal_Table()
    os.remove(Fname)
    print('\nPass 1 Successful\n')


def Insert_Literals(File):  #Support function to handle Literals
    Lit1=[]
    Lit2=[]
    Fname='Temp '+File
    open(Fname, 'w').close()

    with open('Test Programs/'+File, 'r') as file:
        Out=open(Fname,'a')

        for line in file:
            if (line.split()[len(line.split())-1][0]=='='):
                skip=0
                for i in range (len (Lit2)):
                    if(Lit2[i]==line.split()[len(line.split())-1]):
                        skip=1
                if(skip==0):
                    Lit1.append(line.split()[len(line.split())-1])
                    Lit2.append(line.split()[len(line.split())-1])
            
            if (line.split()[0]=='LTORG') or (line.split()[0]=='END'):
                Out.write(line)
                for i in range (len(Lit1)):
                        if(line.split()[0]=='END'):
                            Out.write('\n'+'*'+'         '+Lit1[i])
                        else:
                            Out.write('*'+'         '+Lit1[i]+'\n')
                Lit1.clear()
            else:
                Out.write(line)
    
    Out.close()
    return(Fname)

def Symbol_Table(): #Gets Symbol Table, stores it in Support Files/Symbol Table.txt
    open('Support Files/Symbol Table.txt', 'w').close()

    Out = open('Support Files/Symbol Table.txt', 'a')
    Out.write('Symbol      Location')

    with open('Support Files/temp.txt', 'r') as tmpfile:
        for line in tmpfile:
            word = line.split()
            if('.' in line or 'COPY' in line):
                continue
            Out.write("{:<8}{:<4}".format('\n'+word[1], '     '+word[0]))

    os.remove('Support Files/temp.txt')

def Literal_Table():    #Gets Literal Table, stores it in Support Files/Literal Table.txt
    open('Support Files/Literal Table.txt', 'w').close()

    Out = open('Support Files/Literal Table.txt', 'a')
    Out.write('Literal     Location     Value')

    with open('Support Files/tempL.txt', 'r') as tmpfile:
        value=''
        for line in tmpfile:
            word = line.split()

            if(word[2][1]=='X'):
                value=word[2][3:-1]
            elif(word[2][1] == 'C'):
                chars = word[2][3:-1]
                for d in range(len(chars)):
                    value+= hex(ord(chars[d]))[2:]
            else:
                value= hex(int(word[2]))[2:]

            Out.write("{:<8}{:<9}{:<9}".format('\n'+word[2], '     '+word[0], '         '+value))

    os.remove('Support Files/tempL.txt')


def Format_1(Instruction):  #Returns OBJECT CODE of Format 1 Instructions
    OP = Get_OP(Instruction)
    return hex(OP)[2:]


def Format_2(Instruction, Operand): #Returns OBJECT CODE of Format 2 Instructions
    OP = Get_OP(Instruction)
    operands = Operand.split(',')
    if (Instruction == 'SHIFTL') or (Instruction == 'SHIFTR'):
        op1 = Resgisters[operands[0]]
        op2 = operands[1]
        return hex(OP)[2:] + str(op1)+hex(int(op2, 10))[2:]

    elif(Instruction == 'SVC'):
        op1 = int(operands[0], 16)
        return hex(OP)[2:]+str(op1)+'0'

    elif(len(operands) == 2):
        op1 = Resgisters[operands[0]]
        op2 = Resgisters[operands[1]]
        return hex(OP)[2:] + str(op1)+str(op2)

    else:
        op1 = Resgisters[operands[0]]
        return hex(OP)[2:]+str(op1)+'0'

def Format_3(Instruction, Operand, Base, PC):   #Returns OBJECT CODE of Format 3 Instructions
    OP = Get_OP(Instruction)
    address = ' '
    disp = 0
    xflag = 0
    bpflag = 0

    Operands = Operand.split(',')
    if (len(Operands) == 2) and (Operands[1] == 'X'):
        xflag = 8
        Operand = Operand[:-2]

    if(Operand[0] == '#'):
        OP += 1
        CODE = hex(OP)[2:]

        if(Operand[1:].isdigit()):
            if(xflag == 8):
                return CODE.zfill(2)+'8'+hex(int(Operand[1:])).zfill(3)
            return CODE.zfill(2)+'0'+hex(int(Operand[1:]))[2:].zfill(3)

        else:
            address = int((str(symboladdress(Operand[1:]))), 16)
            disp, bpflag = getDisp(address, PC, Base)

    elif(Operand[0] == '@'):
        OP += 2
        CODE = hex(OP)[2:]
        address = int((str(symboladdress(Operand[1:]))), 16)
        disp, bpflag = getDisp(address, PC, Base)

    elif(Operand[0] == '='):
        OP += 3
        CODE = hex(OP)[2:]
        address = int((str(literaladdress(Operand))), 16)
        disp, bpflag = getDisp(address, PC, Base)

    else:
        OP += 3
        CODE = hex(OP)[2:]
        address = int((str(symboladdress(Operand))), 16)
        disp, bpflag = getDisp(address, PC, Base)
    
    if(bpflag==10):
        return ('Address Unreacahble')

    if(disp >= 0):
        return CODE.zfill(2) + hex(xflag+bpflag)[2:] + hex(disp)[2:].zfill(3)
    else:
        return CODE.zfill(2) + hex(xflag+bpflag)[2:] + hex((disp) & (2**32-1))[7:].zfill(3)

def Format_4(Instruction, Operand): #Returns OBJECT CODE of Format 4 Instructions
    OP = Get_OP(Instruction)
    address = ''

    Operands = Operand.split(',')

    if(len(Operands) == 1):
        exflag = 1
    elif (len(Operands) == 2) and (Operands[1] == 'X'):
        exflag = 9
        Operand = Operand[:-2]

    if(Operand[0] == '#'):
        OP += 1
        CODE = hex(OP)[2:]

        if(Operand[1:].isdigit()):
            address = hex(int(Operand[1:]))[2:]
        else:
            address = int((str(symboladdress(Operand[1:]))), 16)

    elif(Operand[0] == '@'):
        OP += 2
        CODE = hex(OP)[2:]
        address = symboladdress(Operand[1:])[2:]
        print(address)

    else:
        OP += 3
        CODE = hex(OP)[2:]
        address = symboladdress(Operand)[2:]

    return CODE.zfill(2)+str(exflag)+address.zfill(5)

def MFormat_5(Instruction, Operand, Base, PC):  #Returns OBJECT CODE of Mystery Format 5 Instructions
    OP = Get_OP(Instruction)
    xflag = 0
    F1 = F2 = F3 = 0
    address = int((str(symboladdress(Operand))), 16)

    Operands = Operand.split(',')
    if (len(Operands) == 2) and (Operands[1] == 'X'):
        xflag = 8
        Operand = Operand[:-2]

    disp, bpflag = getDisp(address, PC, Base)
    if(disp % 2 == 0):
        F1 = 2
        OP += F1
    if(disp < 0):
        F2 = 1
        OP += F2
    if(disp == 0):
        F3 = 1

    xbp = xflag+bpflag+F3
    CODE = hex(OP)[2:]

    if(bpflag==10):
        return ('Address Unreacahble')


    if(disp >= 0):
        return CODE.zfill(2)+str(xbp)+hex(disp)[2:].zfill(3)
    else:
        return CODE.zfill(2)+str(xbp)+hex((disp) & (2**32-1))[7:].zfill(3)

def MFormat_6(Instruction, Operand):    #Returns OBJECT CODE of Mystery Format 6 Instructions
    OP = Get_OP(Instruction)
    address = ''
    xflag = 0
    F4 = F5 = F6 = 0

    Operands = Operand.split(',')
    if(len(Operands) == 1):
        xflag = 0
    elif (len(Operands) == 2) and (Operands[1] == 'X'):
        xflag = 8
        Operand = Operand[:-2]

    if(Operand[0] == '#'):
        OP += 1
        CODE = hex(OP)[2:]

        if(Operand[1:].isdigit()):
            address = hex(int(Operand[1:]))[2:]
        else:
            address = (symboladdress(Operand[1:]))[2:]

    elif(Operand[0] == '@'):
        OP += 2
        CODE = hex(OP)[2:]
        address = symboladdress(Operand[1:])[2:]
        print(address)

    else:
        OP += 3
        CODE = hex(OP)[2:]
        address = symboladdress(Operand)[2:]

    if(int((address), 16) % 2 != 0):
        F4 = 4
    if(int((address), 16) != 0):
        F5 = 2
    if(int((address), 16) != int((str(getBase())), 16)):
        F6 = 1

    return CODE.zfill(2)+str(xflag+F4+F5+F6)+address.zfill(5)

def getBase():  #Returns Base of Program
    #address = hex(StartAddr)
    address='0x00'
    with open('Support Files/Program.txt', 'r') as file:
        for line in file:
            words = line.split()
            if not words:
                continue
            if(words != 'LTORG') and (line[0] != '.') and (line[0] != ' ') and (line[0] != '\t'):
                idx = 1
                if len(words) == 4:
                    idx = 2
                if(words[idx] == 'BASE'):
                    if(words[idx+1] == '*'):
                        address = words[0]
                    else:
                        address = symboladdress(words[idx+1])
    return address

def getDisp(address, PC, Base): #Returns Displacement for Format 3 and 5 Instructions
    x = address-PC
    if(x <= 2047) and (x >= -2048):
        disp = address-PC
        bpflag = 2
    else:
        disp = address-int((str(Base)), 16)
        if(disp>=0) and (disp<=4095):
            bpflag = 4
        else:
            bpflag=10

    return disp, bpflag


def symboladdress(text):    #Returns Address of Symbol
    location_symb = ''
    symb = open('Support Files/Symbol Table.txt')
    for line in symb:
        words = line.split()
        if(text == words[0]):
            location_symb = words[1]
            return location_symb

def literaladdress(text):   #Returns Address of Literal
    location_lit = ''
    literal = open('Support Files/Literal Table.txt')
    for line in literal:
        words = line.split()
        if(text == words[0]):
            location_lit = words[1]
            return location_lit

def Pass_2():   #Exectues Pass 2, stores it in Output/out.txt
    err=0
    open('Output/out.txt', 'w').close()
    with open('Support Files/Program.txt', 'r') as file:
        Out = open('Output/out.txt', 'a')
        Out.write('Loc         Source Statement            OBJECT CODE\n\n')

        for line in file:
            OBJECT_CODE = ''
            #  Check for keywords
            words = line.split()

            if ('LTORG'in line):
                 Out=open('Output/out.txt','a')
                 Out.write(line)
            if not words:
                continue
            if(words[0] != 'LTORG') and (line[0] != '.') and (line[0] != ' ') and (line[0] != '\t'):
                idx = 1
                if len(words) == 4:
                    idx = 2

                Instruction = words[idx]
                Format = Get_Format(Instruction)

                if (Format == 1):
                    OBJECT_CODE = Format_1(Instruction)
                   
                if (Format == 2):
                    OBJECT_CODE = Format_2(Instruction, words[idx+1])
                   
                if(Format == 3):
                    if(words[idx] == 'RSUB'):
                        OBJECT_CODE = hex(
                            Get_OP(words[idx])+3)[2:]+'0000'
                    else:
                        PC = int((str(words[0])), 16)+3
                        OBJECT_CODE = Format_3(Instruction, words[idx+1], getBase(), PC)
                   
                if('+' in words[idx]):
                    OBJECT_CODE = Format_4(Instruction[1:], words[idx+1])
                   
                if('&' in words[idx]):
                    PC = int((str(words[0])), 16)+3
                    OBJECT_CODE = MFormat_5(Instruction[1:], words[idx+1], getBase(), PC)
                   
                if('$' in words[idx]):
                    OBJECT_CODE = MFormat_6(Instruction[1:], words[idx+1])
                   
                if(words[idx] == 'BYTE'):
                    BYTES = words[idx+1].split(',')
                    for i in range(len(BYTES)):
                        if(BYTES[i][0] == 'X'):
                            OBJECT_CODE += BYTES[i][2:-1]
                        elif(BYTES[i][0] == 'C'):
                            chars = BYTES[i][2:-1]
                            for d in range(len(chars)):
                                OBJECT_CODE += hex(ord(chars[d]))[2:]
                        else:
                            OBJECT_CODE += hex(int(BYTES[i]))[2:]
                   
                if(words[idx] == 'WORD'):
                    WORDS = words[idx+1]
                    if(WORDS[0] == 'X'):
                        OBJECT_CODE += WORDS[2:-1]
                    elif(WORDS[0] == 'C'):
                        chars = BYTES[i][2:-1]
                        for d in range(len(chars)):
                            OBJECT_CODE += hex(ord(chars[d]))[2:]
                    else:
                        OBJECT_CODE += hex(int(WORDS[i]))[2:].zfill(6)
                   
                if(words[idx] == '*'):
                    literals = words[idx+1]
                    if(literals[1] == 'X'):
                        OBJECT_CODE = literals[3:-1]

                    elif(literals[1] == 'C'):
                        chars = literals[3:-1]
                        for d in range(len(chars)):
                            OBJECT_CODE += hex(ord(chars[d]))[2:]
                    else:
                        OBJECT_CODE = hex(int(literals[1:]))[2:]
                   
                if(words[idx] == 'BASE') or (words[idx] == 'RESW') or (words[idx] == 'RESB') or (words[idx] == 'EQU') or (words[idx] == 'END') or (words[idx]=='START'):
                    OBJECT_CODE='NO OBJECT CODE'
                
                
                if(line[0]=='0'):
                    Out=open('Output/out.txt','a')
                    Out.write("{:<40}{:<}".format(line[2:].rstrip('\n').upper(),OBJECT_CODE.upper()+'\n'))
                
                if(OBJECT_CODE=='Address Unreacahble'):
                    err=1
                    print('\nError in Program\n')
                    break
    Out.close()
    if(err==1):
        open('Output/HTE.txt', 'w').close()
        Out=open('Output/HTE.txt','a')
        Out.write('ERROR OCCURED IN PROGRAM\n UNREACHABLE ADDRESS')
        Out.close()
    else:
        print('\nPass 2 Successful\n')
        HTME_Records()

def HTME_Records(): #Gets HTME Records, stores it in 'Output/HTE.txt'
    Size=0
    SizeT=0
    ProgName=''
    StartAddress=''
    TStartAddress=''
    EStartAddress=''
    T_Rec=''
    M_Record=[]
    T_Record=[]

    open('Output/HTE.txt', 'w').close()

    with open('Output/out.txt', 'r') as file:
        for last_line in file:  
            pass   

    with open('Output/out.txt', 'r') as file:
        for line in file:
            words = line.split()

            if not words:
                continue
            if(words[0] != 'LTORG') and (line[0] != '.') and (line[0] != ' ') and (line[0] != '\t'):
                idx = 1
                if len(words) == 5 or len(words) == 7:
                    idx = 2
            
            if(words[0] == 'LTORG'):
                continue
            if(words[idx]=='START'):
                 ProgName=words[idx-1]
                 StartAddress=int(('0x'+words[idx+1]),16)
                 continue

            if(words[1]=='FIRST'):
                EStartAddress=int(('0x'+words[0]),16)
            
            if(words[idx][0]=='+') or (words[idx][0]=='$') :
                if(not(words[len(words)-2][1:].isdigit())):
                    M_Record.append('M'+'.'+hex(int(('0x'+words[0]),16)+1)[2:].upper().zfill(6)+'.05')

            if(words[len(words)-1]=='CODE') and (words[idx]!='RESW') and(words[idx]!='RESB'):
                continue
            
            if(SizeT==0):
                TStartAddress=int(('0x'+words[0]),16)

            if(words[len(words)-1]!='CODE'):
                SizeT+=len(words[len(words)-1])/2

            if(words[idx]=='RESW') or (words[idx]=='RESB'):
                if(SizeT==0)and(T_Rec==''):
                    continue
                T_Record.append('T'+'.'+hex(TStartAddress)[2:].upper().zfill(6)+'.'+hex(int(SizeT))[2:].upper().zfill(2)+T_Rec)
                SizeT=0
                T_Rec=''
                continue

            if(SizeT>30):
                SizeT=SizeT-len(words[len(words)-1])/2
                T_Record.append('T'+'.'+hex(TStartAddress)[2:].upper().zfill(6)+'.'+hex(int(SizeT))[2:].upper().zfill(2)+T_Rec)
                SizeT=len(words[len(words)-1])/2
                TStartAddress=int(('0x'+words[0]),16)
                T_Rec=''

            T_Rec+='.'+words[len(words)-1]

            if(SizeT==30):
                T_Record.append('T'+'.'+hex(TStartAddress)[2:].upper().zfill(6)+'.'+hex(int(SizeT))[2:].upper().zfill(2)+T_Rec)
                SizeT=0
                T_Rec=''

        if(SizeT!=30):
            T_Record.append('T'+'.'+hex(TStartAddress)[2:].upper().zfill(6)+'.'+hex(int(SizeT))[2:].upper().zfill(2)+T_Rec)

    Size= Loc-StartAddress
    H_Record= 'H'+'.'+ProgName.ljust(6,'_')+'.'+hex(StartAddress)[2:].zfill(6)+'.'+hex(Size)[2:].zfill(6)
    E_Record= 'E'+'.'+hex(EStartAddress)[2:].zfill(6)

    Out=open('Output/HTE.txt','a')
    Out.write(H_Record+'\n')
    for i in range (len(T_Record)):
        Out.write(T_Record[i]+'\n')
    for i in range (len(M_Record)):
        Out.write(M_Record[i]+'\n')
    Out.write(E_Record+'\n')

PASS_1()
Pass_2()