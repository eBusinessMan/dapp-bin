window.btcRelayAbi = [{
    "name": "getBlockchainHead()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "getChainScore()",
    "type": "function",
    "inputs": [],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "inMainChain(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "saveAncestors(int256,int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }, { "name": "hashPrevBlock", "type": "int256" }],
    "outputs": []
},
{
    "name": "setRelayUtil(int256)",
    "type": "function",
    "inputs": [{ "name": "relayUtilAddr", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "storeBlockHeader(string)",
    "type": "function",
    "inputs": [{ "name": "blockHeaderBinary", "type": "string" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "testingonlySetGenesis(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "testingonlySetHeaviest(int256)",
    "type": "function",
    "inputs": [{ "name": "blockHash", "type": "int256" }],
    "outputs": []
},
{
    "name": "verifyTx(int256,int256,int256[],int256[],int256)",
    "type": "function",
    "inputs": [{ "name": "tx", "type": "int256" }, { "name": "proofLen", "type": "int256" }, { "name": "hash", "type": "int256[]" }, { "name": "path", "type": "int256[]" }, { "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "within6Confirms(int256)",
    "type": "function",
    "inputs": [{ "name": "txBlockHash", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
}]
