# Stored variables:
#
# Last known block
# 10: version
# 11: hashPrevBlock
# 12: hashMerkleRoot
# 13: time
# 14: bits
# 15: nonce
# 16: blockHash / heaviestBlock
# 17: score
#

inset('btcChain.py')

# block with the highest score (the end of the blockchain)
data heaviestBlock

# highest score among all blocks (so far)
data highScore

# note: _ancestor[9]
data block[2^256](_height, _score, _ancestor[9], _blockHeader[])

# records txs that have successfully claimed Ether (thus not allowed to re-claim)
data txClaim[2^256]

extern relay_util: [computeMerkle:iiaa:i, fastHashBlock:s:i]
data btcrelayUtil


extern btc_eth: [processTransfer:s:i]


#self.block.blockHeader[]

def shared():
    DIFFICULTY_1 = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
    TWO_POW_24 = 2 ^ 24
    ZEROS = 0x0000000000000000000000000000000000000000000000000000000000000000
    LEFT_HASH = 1
    RIGHT_HASH = 2

def init():
    # TODO what to init
    self.init333k()


def init333k():
    self.heaviestBlock = 0x000000000000000008360c20a2ceff91cc8c4f357932377f48659b37bb86c759
    trustedBlock = self.heaviestBlock
    self.block[trustedBlock]._height = 333000
    self.block[trustedBlock]._score = 1
    ancLen = self.numAncestorDepths
    i = 0
    while i < ancLen:
        self.block[trustedBlock]._ancestor[i] = trustedBlock
        i += 1


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


def storeBlockHeader(blockHeaderBinary:str):
    hashPrevBlock = getBytesLE(blockHeaderBinary, 32, 4)

    if self.block[hashPrevBlock]._score == 0:  # score0 means block does NOT exist; genesis has score of 1
        return(0)

    blockHash = self.btcrelayUtil.fastHashBlock(blockHeaderBinary)

    # log(333)
    # log(blockHash)

    # bits = getBytesLE(blockHeaderBinary, 4, 72)
    # target = targetFromBits(bits)

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
    $exp = div($bits, TWO_POW_24)
    $mant = $bits & 0xffffff
    $target = $mant * shiftLeftBytes(1, ($exp - 3))
    $target


macro getPrevBlock($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    getBytesLE($tmpStr, 32, 4)


macro getMerkleRoot($blockHash):
    $tmpStr = load(self.block[$blockHash]._blockHeader[0], chars=80)
    getBytesLE($tmpStr, 32, 36)


def verifyTx(tx, proofLen, hash:arr, path:arr, txBlockHash):
    if !self.inMainChain(txBlockHash):
    # if self.within6Confirms(txBlockHash) || !self.inMainChain(txBlockHash):
        return(0)

    merkle = self.btcrelayUtil.computeMerkle(tx, proofLen, hash, path)
    # realMerkleRoot = getMerkleRoot(txBlockHash)

    if merkle == realMerkleRoot:
        return(1)
    else:
        return(0)


#TODO txHash can eventually be computed (dbl sha256 then flip32Bytes) when
# txStr becomes txBinary
#
# returns the value of processTransfer().  callers should explicitly
# check for a value of 1, since other non-zero values could be error codes
def relayTx(txStr:str, txHash, proofLen, hash:arr, path:arr, txBlockHash, contract):
    if self.txClaim[txHash] == 0 && self.verifyTx(txHash, proofLen, hash, path, txBlockHash) == 1:

        res = contract.processTransfer(txStr)
        self.txClaim[txHash] = res

        return(res)
        # return(call(contract, tx))
    return(0)





# def within6Confirms(txBlockHash):
#     blockHash = self.heaviestBlock
#
#     i = 0
#     while i < 6:
#         if txBlockHash == blockHash:
#             return(1)
#
#         # blockHash = self.block[blockHash]._prevBlock
#         blockHash = getPrevBlock(blockHash)
#         i += 1
#
#     return(0)


# little endian get $size bytes from $inStr with $offset
macro getBytesLE($inStr, $size, $offset):
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


macro concatHash($tx1, $tx2):
    $left = flip32Bytes($tx1)
    $right = flip32Bytes($tx2)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256([$hash1], items=1)

    flip32Bytes($hash2)
