



def shared():
    LEFT_HASH = 1
    RIGHT_HASH = 2


def fastHashBlock(blockHeaderBinary:str):
    hash1 = sha256(blockHeaderBinary:str)
    hash2 = sha256(hash1)
    res = flip32Bytes(hash2)
    return(res)

# return -1 if there's an error (eg called with incorrect params)
# note: needs LEFT_HASH and RIGHT_HASH constants
def computeMerkle(tx, proofLen, hash:arr, path:arr):
    resultHash = tx
    i = 0
    while i < proofLen:
        proofHex = hash[i]
        if path[i] == LEFT_HASH:
            left = proofHex
            right = resultHash
        elif path[i] == RIGHT_HASH:
            left = resultHash
            right = proofHex

        resultHash = concatHash(left, right)

        i += 1

    if !resultHash:
        return(-1)

    return(resultHash)


def getBytesLE(inStr:str, size, offset):
    return(m_getBytesLE(inStr, size, offset))

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

macro flip32Bytes($a):
    $o = 0
    with $i = 0:
        while $i < 32:
            mstore8(ref($o) + $i, byte(31 - $i, $a))
            $i += 1
    $o

macro concatHash($tx1, $tx2):
    $left = flip32Bytes($tx1)
    $right = flip32Bytes($tx2)

    $hash1 = sha256([$left, $right], chars=64)
    $hash2 = sha256([$hash1], items=1)

    flip32Bytes($hash2)



# unused for now
# eg 0x6162 will be 0x6261
# macro flipBytes($n, $numByte):
#     $b = byte(31, $n)
#
#     $i = 30
#     $j = 1
#     while $j < $numByte:
#         $b = ($b * 256) | byte($i, $n)
#         $i -= 1
#         $j += 1
#
#     $b
