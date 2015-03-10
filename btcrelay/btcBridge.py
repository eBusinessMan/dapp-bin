

data owner

extern btc_relay: [verifyTx:iiaai:i]
data btcRelayAddr

extern btc_eth: [processTransfer:s:i]

# records txs that have successfully claimed Ether (thus not allowed to re-claim)
data txClaim[2^256]


def init():
    self.owner = msg.sender

def setBtcRelay(btcRelayAddr):
    if msg.sender == self.owner:
        self.btcRelayAddr = btcRelayAddr
        return(1)
    return(0)

#TODO txHash can eventually be computed (dbl sha256 then flip32Bytes) when
# txStr becomes txBinary
#
# returns the value of processTransfer().  callers should explicitly
# check for a value of 1, since other non-zero values could be error codes
def relayTx(txStr:str, txHash, proofLen, hash:arr, path:arr, txBlockHash, contract):
    if self.txClaim[txHash] == 0 && self.btcRelayAddr.verifyTx(txHash, proofLen, hash, path, txBlockHash) == 1:

        res = contract.processTransfer(txStr)
        self.txClaim[txHash] = res

        return(res)
        # return(call(contract, tx))
    return(0)
