from pyethereum import tester

from utilRelay import makeMerkleProof

import pytest
slow = pytest.mark.slow



class TestBtcBridge(object):

    CONTRACT = 'btcBridge.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed



    # tx[1] of block 100K sends enough BTC, so ether should be transferred
    def testRelayTx(self):
        BTC_RELAY = self.s.abi_contract('btcrelay.py', endowment=2000*self.ETHER)
        self.c.setBtcRelay(BTC_RELAY.address)

        BTC_ETH = self.s.abi_contract('btc-eth.py', endowment=2000*self.ETHER)
        BTC_ETH.setTrustedBtcRelay(self.c.address)

        #
        # store block headers
        #
        block100kPrev = 0x000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250
        self.c.testingonlySetGenesis(block100kPrev)

        headers = [
            "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710",
            "0100000006e533fd1ada86391f3f6c343204b0d278d4aaec1c0b20aa27ba0300000000006abbb3eb3d733a9fe18967fd7d4c117e4ccbbac5bec4d910d900b3ae0793e77f54241b4d4c86041b4089cc9b",
            "0100000090f0a9f110702f808219ebea1173056042a714bad51b916cb6800000000000005275289558f51c9966699404ae2294730c3c9f9bda53523ce50e9b95e558da2fdb261b4d4c86041b1ab1bf93",
            "01000000aff7e0c7dc29d227480c2aa79521419640a161023b51cdb28a3b0100000000003779fc09d638c4c6da0840c41fa625a90b72b125015fd0273f706d61f3be175faa271b4d4c86041b142dca82",
            "01000000e1c5ba3a6817d53738409f5e7229ffd098d481147b002941a7a002000000000077ed2af87aa4f9f450f8dbd15284720c3fd96f565a13c9de42a3c1440b7fc6a50e281b4d4c86041b08aecda2",
            "0100000079cda856b143d9db2c1caff01d1aecc8630d30625d10e8b4b8b0000000000000b50cc069d6a3e33e3ff84a5c41d9d3febe7c770fdcc96b2c3ff60abe184f196367291b4d4c86041b8fa45d63",
            "0100000045dc58743362fe8d8898a7506faa816baed7d391c9bc0b13b0da00000000000021728a2f4f975cc801cb3c672747f1ead8a946b2702b7bd52f7b86dd1aa0c975c02a1b4d4c86041b7b47546d"
        ]
        blockHeaderBinary = map(lambda x: x.decode('hex'), headers)
        for i in range(7):
            res = self.c.storeBlockHeader(blockHeaderBinary[i])
            assert res == i+2

        # tx[1] fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        txStr = '0100000001032e38e9c0a84c6046d687d10556dcacc41d275ec55fc00779ac88fdf357a187000000008c493046022100c352d3dd993a981beba4a63ad15c209275ca9470abfcd57da93b58e4eb5dce82022100840792bc1f456062819f15d33ee7055cf7b5ee1af1ebcc6028d9cdb1c3af7748014104f46db5e9d61a9dc27b8d64ad23e7383a4e6ca164593c2527c038c0857eb67ee8e825dca65046b82c9331586c82e0fd1f633f25f87c161bc6f8a630121df2b3d3ffffffff0200e32321000000001976a914c398efa9c392ba6013c5e04ee729755ef7f58b3288ac000fe208010000001976a914948c765a6914d43f2a7ac177da2c2f6b52de3d7c88ac00000000'

        # block 100000
        header = {'nonce': 274148111, 'hash': u'000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506', 'timestamp': 1293623863, 'merkle_root': u'f3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766', 'version': 1, 'prevhash': u'000000000002d01c1fccc21636b607dfd930d31d01c3a62104612a1719011250', 'bits': 453281356}
        hashes = [u'8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87', u'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4', u'6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4', u'e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d']
        [txHash, siblings, path, txBlockHash] = makeMerkleProof(header, hashes, 1)

        # verify the proof and then hand the proof to the btc-eth contract, which will check
        # the tx outputs and send ether as appropriate
        res = self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address, profiling=True)
        print('GAS: '+str(res['gas']))

        ethAddrBin = txStr[-52:-12].decode('hex')
        userEthBalance = self.s.block.get_balance(ethAddrBin)
        print('USER ETH BALANCE: '+str(userEthBalance))
        expEtherBalance = 13
        assert userEthBalance == expEtherBalance
        assert res['output'] == 1  # ether was transferred

        assert 0 == self.c.relayTx(txStr, txHash, len(siblings), siblings, path, txBlockHash, BTC_ETH.address)  # re-claim disallowed
