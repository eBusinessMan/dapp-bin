# setRelayUtil() should be called immediately after creating this contract


inset('btcChain.py')

# block with the highest score (the end of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# note: _ancestor[9]
data block[2^256](_height, _score, _ancestor[9], _blockHeader[])

data owner

extern relay_util: [computeMerkle:iiaa:i, fastHashBlock:s:i, getBytesLE:sii:i]
data btcrelayUtil


def shared():
    DIFFICULTY_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000


def init():
    self.owner = msg.sender

    # TODO what to init
    # self.init333k()


# def init333k():
#     self.heaviestBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
#     trustedBlock = self.heaviestBlock
#     self.block[trustedBlock]._height = 333000
#     self.block[trustedBlock]._score = 1
#     ancLen = self.numAncestorDepths
#     i = 0
#     while i < ancLen:
#         self.block[trustedBlock]._ancestor[i] = trustedBlock
#         i += 1


#TODO for testing only
def testingonlySetHeaviest(blockHash):
    self.heaviestBlock = blockHash

#TODO for testing only
def testingonlySetGenesis(blockHash):
    self.heaviestBlock = blockHash
    self.block[blockHash]._height = 1
    self.block[blockHash]._score = 1  # genesis has score of 1, since score0 means block does NOT exist. see check in storeBlockHeader()
    ancLen = self.numAncestorDepths
    i = 0
    while i < ancLen:
        self.block[blockHash]._ancestor[i] = blockHash
        i += 1

def setRelayUtil(relayUtilAddr):
    if msg.sender == self.owner:
        self.btcrelayUtil = relayUtilAddr
        return(1)
    return(0)

# note: needs DIFFICULTY_1 constant
def storeBlockHeader(blockHeaderBinary:str):
    hashPrevBlock = self.btcrelayUtil.getBytesLE(blockHeaderBinary, 32, 4)

    if self.block[hashPrevBlock]._score == 0:  # score0 means block does NOT exist; genesis has score of 1
        return(0)

    blockHash = self.btcrelayUtil.fastHashBlock(blockHeaderBinary)

    # log(333)
    # log(blockHash)

    bits = self.btcrelayUtil.getBytesLE(blockHeaderBinary, 4, 72)
    target = targetFromBits(bits)

    difficulty = DIFFICULTY_1 / target # https://en.bitcoin.it/wiki/Difficulty

    # TODO other validation of block?  eg timestamp

    if gt(blockHash, 0) && lt(blockHash, target):  #TODO should sgt and slt be used?
        self.saveAncestors(blockHash, hashPrevBlock)

        save(self.block[blockHash]._blockHeader[0], blockHeaderBinary, chars=80) # or 160?

        self.block[blockHash]._score = self.block[hashPrevBlock]._score + difficulty

        if gt(self.block[blockHash]._score, self.highScore):  #TODO use sgt?
            self.heaviestBlock = blockHash
            self.highScore = self.block[blockHash]._score

        return(self.block[blockHash]._height)

    return(0)


# eg 0x6162 will be 0x6261
macro flipBytes($n, $numByte):
    $b = byte(31, $n)

    $i = 30
    $j = 1
    while $j < $numByte:
        $b = ($b * 256) | byte($i, $n)
        $i -= 1
        $j += 1

    $b


# fast string flip bytes
# macro vflip($x, $L):
#     with $o = alloc($L + 32):
#         with $lim = $o + 2:
#             $o += $L
#             with $y = $x - 31:
#                 while $o > $lim:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                 if $o > $lim - 2:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#                 if $o > $lim - 2:
#                     mstore($o, mload($y))
#                     $o -= 1
#                     $y += 1
#         mstore($o, $L)
#         $o + 32



# shift left bytes
macro shiftLeftBytes($n, $x):
    $n * 256^$x  # set the base to 2 (instead of 256) if we want a macro to shift only bits

# shift right
macro shiftRightBytes($n, $x):
    div($n, 256^$x)


# http://www.righto.com/2014/02/bitcoin-mining-hard-way-algorithms.html#ref3
macro targetFromBits($bits):
    $exp = div($bits, 0x1000000)  # 2^24
    $mant = $bits & 0xffffff
    $target = $mant * shiftLeftBytes(1, ($exp - 3))
    $target


macro getPrevBlock($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    m_getBytesLE($tmpStr, 32, 4)


macro getMerkleRoot($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    m_getBytesLE($tmpStr, 32, 36)


def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.btcrelayUtil.computeMerkle(tx, proofLen, hash, path)
    realMerkleRoot = getMerkleRoot(txBlockHash)

    if merkle == realMerkleRoot:
        return(1)
    else:
        return(0)



def within6Confirms(txBlockHash):
    blockHash = self.heaviestBlock

    i = 0
    while i < 6:
        if txBlockHash == blockHash:
            return(1)

        # blockHash = self.block[blockHash]._prevBlock
        blockHash = getPrevBlock(blockHash)
        i += 1

    return(0)



# little endian get $size bytes from $inStr with $offset
macro m_getBytesLE($inStr, $size, $offset):
    $endIndex = $offset + $size

    $result = 0
    $exponent = 0
    $j = $offset
    while $j < $endIndex:
        $char = getch($inStr, $j)
        # log($char)
        $result += $char * 256^$exponent
        # log(result)

        $j += 1
        $exponent += 1

    $result
