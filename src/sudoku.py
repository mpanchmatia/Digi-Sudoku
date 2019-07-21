import abc
import itertools

class Sudoku(metaclass=abc.ABCMeta):
    # Static Variables
    size = 1

    @abc.abstractmethod
    def Solve(self):
        pass

    @abc.abstractmethod
    def Load(self, strInput):
        pass

class ClassicSudoku(Sudoku):
    # Static Variables
    size = 9
    sqrt_size = 3
    invert = 1022

    # Static Variables. Response codes
    ZERO_TO_OK = 200
    ZERO_TO_ONE = 1
    ONE_BACKTO_ZERO = 10
    ONE_TO_TWO = 2
    TWO_BACKTO_ZERO = 20
    TWO_TO_THREE = 3
    THREE_BACKTO_ZERO = 30
    THREE_TO_FOUR = 4
    FOUR_BACK_TO_ZERO = 40
    FOUR_TO_ERROR = 500

    char2BitMap = {
        '0': 0,
        '1': 2,
        '2': 4,
        '3': 8,
        '4': 16,
        '5': 32,
        '6': 64,
        '7': 128,
        '8': 256,
        '9': 512
    }
    bitMap2char = {
        2: '1',
        4: '2',
        8: '3',
        16: '4',
        32: '5',
        64: '6',
        128: '7',
        256: '8',
        512: '9'
    }

    # Static Methods
    GetRowIndex = staticmethod(lambda i: i // ClassicSudoku.size)
    GetColIndex = staticmethod(lambda i: i % ClassicSudoku.size)
    GetBlockIndex = staticmethod(lambda x, y : ClassicSudoku.sqrt_size * ( y // ClassicSudoku.sqrt_size )
                                                + ( x // ClassicSudoku.sqrt_size ))

    def __init__(self):
        self.listRow = [i for i in itertools.repeat(0, ClassicSudoku.size)]
        self.listCol = [i for i in itertools.repeat(0, ClassicSudoku.size)]
        self.listBlock = [i for i in itertools.repeat(0, ClassicSudoku.size)]
        self.options = {}
        self.output = {}

    def Load(self, strInput):
        self.strInput = strInput

        for cellIndex in range(0, len(strInput)):
            if strInput[cellIndex] == '0':
                self.options[cellIndex] = 0
            else:
                rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
                colIndex = ClassicSudoku.GetColIndex(cellIndex)
                blockIndex = ClassicSudoku.GetBlockIndex(colIndex, rowIndex)
                bitmap = ClassicSudoku.char2BitMap[strInput[cellIndex]]
                self.listRow[rowIndex] |= bitmap
                self.listCol[colIndex] |= bitmap
                self.listBlock[blockIndex] |= bitmap

        for cellIndex in self.options:
            rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
            colIndex = ClassicSudoku.GetColIndex(cellIndex)
            blockIndex = ClassicSudoku.GetBlockIndex(colIndex, rowIndex)
            temp = self.listRow[rowIndex] | self.listCol[colIndex] | self.listBlock[blockIndex]
            self.options[cellIndex] = ClassicSudoku.invert - temp

        # print("After Intialization")
        # self.PrintOptions()

    def Solve(self):
        """
        This function implements FSM = Finite State Machine
        Parameters:
            None

        Returns:
            None
        """
        status = self.SolveSingleCandidate() # function zero
        while True:
            if status == ClassicSudoku.ZERO_TO_OK:
                return
            if status == ClassicSudoku.FOUR_TO_ERROR:
                return
            if status == ClassicSudoku.ZERO_TO_ONE:
                status = self.SolveExplicitRegion() # function one
            if status == ClassicSudoku.ONE_BACKTO_ZERO:
                status = self.SolveSingleCandidate() # function zero
            if status == ClassicSudoku.ONE_TO_TWO:
                status = self.SolveImplicitRegion() # function two
            if status == ClassicSudoku.TWO_BACKTO_ZERO:
                status = self.SolveSingleCandidate() # function zero
            if status == ClassicSudoku.TWO_TO_THREE:
                status = self.SolveCandidateLineTechnique() # function three
            if status == ClassicSudoku.THREE_BACKTO_ZERO:
                status = self.SolveSingleCandidate() # function zero
            if status == ClassicSudoku.THREE_TO_FOUR:
                status = self.SolveMultipleLinesTechnique() # function four
            if status == ClassicSudoku.FOUR_BACK_TO_ZERO:
                status = self.SolveSingleCandidate() # function zero

    def SolveSingleCandidate(self):
        """
        This function is 'function zero'.
        step 1: check all empty cells.
        step 2: If any empty cell has only one possible value, then set that value.
        Parameters:
            None
        Returns:
            If all empty cells are filled, then returns ZERO_TO_OK
            If further progress is not possible then return ZERO_TO_ONE
        """
        prevSize = 0
        self.strOutput = ''

        while True:

            for cellIndex, bitmap in self.options.copy().items():

                if bin(bitmap).count('1') == 1:
                    # Store final answer in output dictionary
                    self.output[cellIndex] = ClassicSudoku.bitMap2char[bitmap]
                    # Reset the value in options dictionary
                    # update all bitmaps accordingly
                    rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
                    colIndex = ClassicSudoku.GetColIndex(cellIndex)
                    blockIndex = ClassicSudoku.GetBlockIndex(colIndex, rowIndex)
                    self.listRow[rowIndex] |= bitmap
                    self.listCol[colIndex] |= bitmap
                    self.listBlock[blockIndex] |= bitmap

                    for k in self.options:
                        r = ClassicSudoku.GetRowIndex(k)
                        c = ClassicSudoku.GetColIndex(k)
                        b = ClassicSudoku.GetBlockIndex(c, r)
                        if r == rowIndex:
                            self.options[k] = self.options[k] & (ClassicSudoku.invert - bitmap)
                        if c == colIndex:
                            self.options[k] = self.options[k] & (ClassicSudoku.invert - bitmap)
                        if b == blockIndex:
                            self.options[k] = self.options[k] & (ClassicSudoku.invert - bitmap)

                if self.options[cellIndex] == 0:
                    del self.options[cellIndex]

            size = len(self.output)

            # Sudoku puzzle is solved.
            # As the options dictionary is empty.
            # So break the outer Do-while loop
            if len(self.options) == 0:
                break

            # The size of output dictionary is not increasing.
            # This is more complex Sudoku puzzle.
            # So call next function
            if size == prevSize:
                print("ZERO_TO_ONE output size %d"%(size))
                return ClassicSudoku.ZERO_TO_ONE

            # Reset for next iteration within do-while loop
            prevSize = size

        listInput = list(self.strInput)
        for cellIndex, value in enumerate(listInput):
            if value == '0':
                value = self.output[cellIndex]
                listInput[cellIndex] = value

        self.strOutput = ''.join(listInput)

        print("ZERO_TO_OK output size %d" % (size))
        return ClassicSudoku.ZERO_TO_OK

    def ExplicitRegionSolveARegion(self, listCellIndexInRegion):
        """
        This function is a helper function for 'function one'.
        Parameters:
            List of all cellIndex for any given one region = row | column | block
        Returns:
            If possible values at any empty cell is modified, then returns status as 1
            If further progress is not possible then return status as 0
        """

        dictCellIndexInRegion = {cellIndex: self.options[cellIndex] for cellIndex in listCellIndexInRegion}
        listTupleKV = sorted(dictCellIndexInRegion.items(), key=lambda x: bin(x[1]).count('1'), reverse=True)
        listSubSetCellIndex = []
        status = 0

        for i in range(len(listTupleKV)):
            maxValueCount = bin(listTupleKV[i][1]).count('1')
            if maxValueCount == 0:
                break
            maxValueCellIndex = listTupleKV[i][0]
            count = 1
            listSubSetCellIndex.clear()
            listSubSetCellIndex.append(maxValueCellIndex)
            for j in range(i + 1, len(listTupleKV)):
                if listTupleKV[j][1] == 0:
                    break
                if listTupleKV[i][1] == (listTupleKV[i][1] | listTupleKV[j][1]):
                    count = count + 1
                    listSubSetCellIndex.append(listTupleKV[j][0])
            if count == maxValueCount:
                for cellIndex in listCellIndexInRegion:
                    if cellIndex not in listSubSetCellIndex:
                        # Reset bit
                        temp = self.options[cellIndex] & (ClassicSudoku.invert - listTupleKV[i][1])
                        # Check, the candidate list is modified or not.
                        if ( self.options[cellIndex] != temp):
                            status = 1
                            self.options[cellIndex] = temp

        return status

    def SolveExplicitRegion(self):
        """
        This function is 'function one'
        It implements naked pair, naked triple and naked tuple methods
        step 1: check all Regions = all Rows, all Columns and all Blocks
        step 2: If number of empty cell = 1, number of possible values = N
                And
                number of empty cell = N - 1, number of possible values are subset of N
                Then
                those N values should be absent in rest of the cells in given region.
        Parameters:
            None
        Returns:
            If any progress made then ONE_BACKTO_ZERO
            If further progress is not possible then return ONE_TO_TWO
        """
        listCellIndexInRegion = []
        status = 0

        for rowIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                if rowIndex == ClassicSudoku.GetRowIndex(cellIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ExplicitRegionSolveARegion(listCellIndexInRegion)

        for colIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                if colIndex == ClassicSudoku.GetColIndex(cellIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ExplicitRegionSolveARegion(listCellIndexInRegion)

        for blockIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
                colIndex = ClassicSudoku.GetColIndex(cellIndex)
                if blockIndex == ClassicSudoku.GetBlockIndex(colIndex, rowIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ExplicitRegionSolveARegion(listCellIndexInRegion)

        if status == 0:
            print("ONE_TO_TWO output size %d" % (len(self.output)))
            return ClassicSudoku.ONE_TO_TWO
        else:
            print("ONE_BACKTO_ZERO output size %d" % (len(self.output)))
            # self.PrintOptions()
            return ClassicSudoku.ONE_BACKTO_ZERO

    def ImplicitRegionSolveARegion(self, listCellIndexInRegion):
        """
        This function is a helper function for 'function two'.
        Parameters:
            List of all cellIndex for any given one region = row | column | block
        Returns:
            If possible values at any empty cell is modified, then returns status as 1
            If further progress is not possible then return status as 0
        """
        dictCellIndexInRegion = {cellIndex: self.options[cellIndex] for cellIndex in listCellIndexInRegion}
        dicDigit = {digit: [] for digit in range(1, ClassicSudoku.size + 1)}

        for digit in dicDigit:
            for cellIndex, value in dictCellIndexInRegion.items():
                if value == (value | ClassicSudoku.char2BitMap[str(digit)]):
                    dicDigit[digit].append(cellIndex)

        listTupleKV = sorted(dicDigit.items(), key=lambda x: len(x[1]), reverse=True)
        listSubSetDigit = []
        status = 0

        for i in range(ClassicSudoku.size):
            keyCount = len(listTupleKV[i][1])
            if keyCount == 0:
                break
            digitWithmaxNoOfKey = listTupleKV[i][0]
            count = 1
            listSubSetDigit.clear()
            listSubSetDigit.append(digitWithmaxNoOfKey)
            for j in range(i + 1, ClassicSudoku.size):
                if not listTupleKV[j][1]:
                    break
                if all(x in listTupleKV[i][1] for x in listTupleKV[j][1]):
                    count = count + 1
                    listSubSetDigit.append(listTupleKV[j][0])
            if count == keyCount:
                for cellIndex in listCellIndexInRegion:
                    for digit in range(1, ClassicSudoku.size + 1):
                        if (
                                ((cellIndex not in listTupleKV[i][1]) and (digit in listSubSetDigit))
                                or
                                ((cellIndex in listTupleKV[i][1]) and (digit not in listSubSetDigit))
                        ):
                            # Reset bit
                            temp = self.options[cellIndex] & (ClassicSudoku.invert -
                                                              ClassicSudoku.char2BitMap[str(digit)])
                            # Check, the candidate list is modified or not.
                            if (self.options[cellIndex] != temp):
                                status = 1
                                self.options[cellIndex] = temp
        return status

    def SolveImplicitRegion(self):
        """
        This function is 'function two'
        It implements hidden pair, hidden triple and hidden tuple methods
        step 1: check all Regions = all Rows, all Columns and all Blocks
        step 2: Create a reverse map of digit values v/s cellIndex in region.
        step 3: If number of digit value = 1, number of possible cells = N
                And
                number of digit value = N - 1, number of possible cells are subset of N
                Then
                those N digits should be absent in rest of the cells in given region.
        Parameters:
            None
        Returns:
            If any progress made then TWO_BACKTO_ZERO
            If further progress is not possible then return TWO_TO_THREE
        """
        listCellIndexInRegion = []
        status = 0

        for rowIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                if rowIndex == ClassicSudoku.GetRowIndex(cellIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ImplicitRegionSolveARegion(listCellIndexInRegion)

        for colIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                if colIndex == ClassicSudoku.GetColIndex(cellIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ImplicitRegionSolveARegion(listCellIndexInRegion)

        for blockIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
                colIndex = ClassicSudoku.GetColIndex(cellIndex)
                if blockIndex == ClassicSudoku.GetBlockIndex(colIndex, rowIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.ImplicitRegionSolveARegion(listCellIndexInRegion)

        if status == 0:
            print("TWO_TO_THREE output size %d" % (len(self.output)))
            return ClassicSudoku.TWO_TO_THREE
        else:
            print("TWO_BACKTO_ZERO output size %d" % (len(self.output)))
            # self.PrintOptions()
            return ClassicSudoku.TWO_BACKTO_ZERO

    def CandidateLineTechniqueSolveARegion(self, listCellIndexInRegion):
        """
        This function is a helper function for 'function three'.
        Parameters:
            List of all cellIndex for any given one region = row | column | block
        Returns:
            If possible values at any empty cell is modified, then returns status as 1
            If further progress is not possible then return status as 0
        """
        dictCellIndexInRegion = {cellIndex: self.options[cellIndex] for cellIndex in listCellIndexInRegion}
        dicDigit = {digit: [] for digit in range(1, ClassicSudoku.size + 1)}

        for digit in dicDigit:
            for cellIndex, value in dictCellIndexInRegion.items():
                if value == (value | ClassicSudoku.char2BitMap[str(digit)]):
                    dicDigit[digit].append(cellIndex)

        status = 0
        for digit, listCellIndex in dicDigit.items():
            if listCellIndex:

                if all(x % ClassicSudoku.size == listCellIndex[0] % ClassicSudoku.size for x in listCellIndex):
                    colIndex = ClassicSudoku.GetColIndex(listCellIndex[0])
                    for cellIndex in self.options:
                        if cellIndex not in listCellIndex:
                            c = ClassicSudoku.GetColIndex(cellIndex)
                            if c == colIndex:
                                # Reset bit
                                temp = self.options[cellIndex] & (ClassicSudoku.invert -
                                                                  ClassicSudoku.char2BitMap[str(digit)])
                                # Check, the candidate list is modified or not.
                                if (self.options[cellIndex] != temp):
                                    status = 1
                                    self.options[cellIndex] = temp

                if all(x // ClassicSudoku.size == listCellIndex[0] // ClassicSudoku.size for x in listCellIndex):
                    rowIndex = ClassicSudoku.GetRowIndex(listCellIndex[0])
                    for cellIndex in self.options:
                        if cellIndex not in listCellIndex:
                            r = ClassicSudoku.GetRowIndex(cellIndex)
                            if r == rowIndex:
                                # Reset bit
                                temp = self.options[cellIndex] & (ClassicSudoku.invert -
                                                                  ClassicSudoku.char2BitMap[str(digit)])
                                # Check, the candidate list is modified or not.
                                if (self.options[cellIndex] != temp):
                                    status = 1
                                    self.options[cellIndex] = temp

        return status

    def SolveCandidateLineTechnique(self):
        """
        This function is 'function three'
        It implements Single line techniques. Line = Row | Column
        step 1: Iterate through all blocks
        step 2: Create a reverse map of digit values v/s cellIndex in block.
        step 3: Now for each digit if all cellIndex belongs to same one Line,
                (that means, cellIndex does not belong to other two lines within block)
                Then
                remove that digit from other two blocks in that line.
        Parameters:
            None
        Returns:
            If any progress made then THREE_BACKTO_ZERO
            If further progress is not possible then return THREE_TO_ERROR
        """
        listCellIndexInRegion = []
        status = 0

        for blockIndex in range(ClassicSudoku.size):
            listCellIndexInRegion.clear()
            for cellIndex in self.options:
                rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
                colIndex = ClassicSudoku.GetColIndex(cellIndex)
                if blockIndex == ClassicSudoku.GetBlockIndex(colIndex, rowIndex):
                    listCellIndexInRegion.append(cellIndex)
            if listCellIndexInRegion:
                status = status | self.CandidateLineTechniqueSolveARegion(listCellIndexInRegion)

        if status == 0:
            print("THREE_TO_FOUR output size %d" % (len(self.output)))
            return ClassicSudoku.THREE_TO_FOUR
        else:
            print("THREE_BACKTO_ZERO output size %d" % (len(self.output)))
            # self.PrintOptions()
            return ClassicSudoku.THREE_BACKTO_ZERO

    def MultipleLinesTechniqueSolveARegion(self, listCellIndexInRegion1, listCellIndexInRegion2, cr,
                                           listCellIndexInRegion3):
        """
        This function is helper fuctnion for 'function four'.
        Parameters:
            List of all cellIndex for any given block1
            List of all cellIndex for any given block2
            Variable cr indicates weather this operation is on column or on row
            List of all cellIndex for any given block3
        Returns:
            If possible values at any empty cell is modified, then returns status as 1
            If further progress is not possible then return status as 0
        """

        # For Block 1
        dictCellIndexInRegion1 = {cellIndex: self.options[cellIndex] for cellIndex in listCellIndexInRegion1}
        dicDigit1 = {digit: [] for digit in range(1, ClassicSudoku.size + 1)}
        for digit in dicDigit1:
            for cellIndex, value in dictCellIndexInRegion1.items():
                if value == (value | ClassicSudoku.char2BitMap[str(digit)]):
                    dicDigit1[digit].append(cellIndex)
        for digit, listCellIndex in dicDigit1.copy().items():
            if not listCellIndex:
                del digit
        setLineIndex1 = set()

        # For Block 2
        dictCellIndexInRegion2 = {cellIndex: self.options[cellIndex] for cellIndex in listCellIndexInRegion2}
        dicDigit2 = {digit: [] for digit in range(1, ClassicSudoku.size + 1)}
        for digit in dicDigit2:
            for cellIndex, value in dictCellIndexInRegion2.items():
                if value == (value | ClassicSudoku.char2BitMap[str(digit)]):
                    dicDigit2[digit].append(cellIndex)
        for digit, listCellIndex in dicDigit2.copy().items():
            if not listCellIndex:
                del digit
        setLineIndex2 = set()

        status = 0
        for digit, listCellIndex1 in dicDigit1.items():
            if digit in dicDigit2:

                setLineIndex1.clear()
                setLineIndex2.clear()

                for cellIndex in listCellIndex1:
                    if cr == 'c':
                        setLineIndex1.add(ClassicSudoku.GetColIndex(cellIndex))
                    else:
                        setLineIndex1.add(ClassicSudoku.GetRowIndex(cellIndex))

                listCellIndex2 = dicDigit2[digit]
                for cellIndex in listCellIndex2:
                    if cr == 'c':
                        setLineIndex2.add(ClassicSudoku.GetColIndex(cellIndex))
                    else:
                        setLineIndex2.add(ClassicSudoku.GetRowIndex(cellIndex))

                if ((len(setLineIndex1) == (ClassicSudoku.sqrt_size - 1)) \
                        and
                    (setLineIndex1 == setLineIndex2 )):
                    if cr == 'c':
                        for cellIndex in listCellIndexInRegion3:
                            lineIndex = ClassicSudoku.GetColIndex(cellIndex)
                            if lineIndex in setLineIndex1:
                                # Reset bit
                                temp = self.options[cellIndex] & \
                                       (ClassicSudoku.invert - ClassicSudoku.char2BitMap[str(digit)])
                                # Check, the candidate list is modified or not.
                                if (self.options[cellIndex] != temp):
                                    status = 1
                                    self.options[cellIndex] = temp
                    else:
                        for cellIndex in listCellIndexInRegion3:
                            lineIndex = ClassicSudoku.GetRowIndex(cellIndex)
                            if lineIndex in setLineIndex1:
                                # Reset bit
                                temp = self.options[cellIndex] & \
                                       (ClassicSudoku.invert - ClassicSudoku.char2BitMap[str(digit)])
                                # Check, the candidate list is modified or not.
                                if (self.options[cellIndex] != temp):
                                    status = 1
                                    self.options[cellIndex] = temp
        return status

    def SolveMultipleLinesTechnique(self):
        """
        This function is 'function four'
        It implements Multiple lines techniques. Line = Row | Column
        step 1: Create all 9 blocks as dictionay. key = block number, value = list of all member cells
        step 2: Iterate through possible tripplet of blocks sharing common Lines
        step 2: Create two reverse map of digit values v/s cellIndex in for two blocks.
        step 3: Now for each digit if digit presents in exactly two identical lines two blocks
                (that means, digit does not belong to other third line in both blocks)
                Then
                remove that digit from those two lines in third block.
        Parameters:
            None
        Returns:
            If any progress made then FOUR_BACK_TO_ZERO
            If further progress is not possible then return FOUR_TO_ERROR
        """

        dictCellIndexInBlock = {blockIndex: [] for blockIndex in range(ClassicSudoku.size)}
        status = 0

        for cellIndex in self.options:
            rowIndex = ClassicSudoku.GetRowIndex(cellIndex)
            colIndex = ClassicSudoku.GetColIndex(cellIndex)
            blockIndex = ClassicSudoku.GetBlockIndex(colIndex, rowIndex)
            dictCellIndexInBlock[blockIndex].append(cellIndex)

        if all(dictCellIndexInBlock[x] for x in [0, 1, 2]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[0], dictCellIndexInBlock[1], 'r', dictCellIndexInBlock[2])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[1], dictCellIndexInBlock[2], 'r', dictCellIndexInBlock[0])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[2], dictCellIndexInBlock[0], 'r', dictCellIndexInBlock[1])
        if all(dictCellIndexInBlock[x] for x in [3, 4, 5]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[3], dictCellIndexInBlock[4], 'r', dictCellIndexInBlock[5])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[4], dictCellIndexInBlock[5], 'r', dictCellIndexInBlock[3])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[5], dictCellIndexInBlock[3], 'r', dictCellIndexInBlock[4])
        if all(dictCellIndexInBlock[x] for x in [6, 7, 8]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[6], dictCellIndexInBlock[7], 'r', dictCellIndexInBlock[8])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[7], dictCellIndexInBlock[8], 'r', dictCellIndexInBlock[6])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[8], dictCellIndexInBlock[6], 'r', dictCellIndexInBlock[7])
        if all(dictCellIndexInBlock[x] for x in [0, 3, 6]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[0], dictCellIndexInBlock[3], 'c', dictCellIndexInBlock[6])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[3], dictCellIndexInBlock[6], 'c', dictCellIndexInBlock[0])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[6], dictCellIndexInBlock[0], 'c', dictCellIndexInBlock[3])
        if all(dictCellIndexInBlock[x] for x in [1, 4, 7]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[1], dictCellIndexInBlock[4], 'c', dictCellIndexInBlock[7])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[4], dictCellIndexInBlock[7], 'c', dictCellIndexInBlock[1])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[7], dictCellIndexInBlock[1], 'c', dictCellIndexInBlock[4])
        if all(dictCellIndexInBlock[x] for x in [2, 5, 8]):
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[2], dictCellIndexInBlock[5], 'c', dictCellIndexInBlock[8])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[5], dictCellIndexInBlock[8], 'c', dictCellIndexInBlock[2])
            status = status | self.MultipleLinesTechniqueSolveARegion(dictCellIndexInBlock[8], dictCellIndexInBlock[2], 'c', dictCellIndexInBlock[5])

        if status == 0:
            print("FOUR_TO_ERROR output size %d" % (len(self.output)))
            # self.PrintOptions()
            return ClassicSudoku.FOUR_TO_ERROR
        else:
            print("FOUR_BACK_TO_ZERO output size %d" % (len(self.output)))
            # self.PrintOptions()
            return ClassicSudoku.FOUR_BACK_TO_ZERO

    def PrintOptions(self):
        """
        This function is just for debugging. It can invoked after state change to monitor progress.
        Parameters : none
        Returns : none
        """
        for cellIndex, value in self.options.items():
            print("%d : " %(cellIndex), end=" ")
            for digit in range(1, ClassicSudoku.size + 1):
                if value == (value | ClassicSudoku.char2BitMap[str(digit)]):
                    print(digit, end=" ")
            print("\r")
        print("=====================================================")
