# setBtcRelay() should be called immediately after creating this contract


data owner

# TODO remove unused and testingonly externs (check that tests files that include btcBridge still pass when this extern is updated)
extern btc_relay: [getBlockchainHead:_:i, getChainScore:_:i, inMainChain:i:i, saveAncestors:ii:_, setRelayUtil:i:i, storeBlockHeader:s:i, testingonlySetGenesis:i:_, testingonlySetHeaviest:i:_, verifyTx:iiaai:i, within6Confirms:i:i]
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
