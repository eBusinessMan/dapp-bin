def fastHashBlock(blockHeaderBinary:str):
    hash1 = sha256(blockHeaderBinary:str)
    hash2 = sha256(hash1)
    res = flip32Bytes(hash2)
    return(res)

# return -1 if there's an error (eg called with incorrect params)
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
