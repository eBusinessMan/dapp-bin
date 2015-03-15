// TODO bulkStoreHeader first param change to string so that it's
// consistent with relayTx(string...
window.btcBridgeAbi = [{
    "name": "bulkStoreHeader(bytes,int256)",
    "type": "function",
    "inputs": [{ "name": "headersBinary", "type": "bytes" }, { "name": "count", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "relayTx(string,int256,int256,int256[],int256[],int256,int256)",
    "type": "function",
    "inputs": [{ "name": "txStr", "type": "bytes" }, { "name": "txHash", "type": "int256" }, { "name": "proofLen", "type": "int256" }, { "name": "hash", "type": "int256[]" }, { "name": "path", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }, { "name": "contract", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "setBtcRelay(int256)",
    "type": "function",
    "inputs": [{ "name": "btcRelayAddr", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
