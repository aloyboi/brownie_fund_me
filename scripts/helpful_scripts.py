from operator import ge
from brownie import accounts, network, MockV3Aggregator
import os
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or FORKED_LOCAL_ENVIRONMENT
    ):  # if working within brownie
        return accounts[0]

    else:
        return accounts.add(os.getenv("PRIVATE_KEY"))  # if working on testnet


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            18, 20000000000, {"from": get_account()}
        )  # Deploy Fake Aggregator Contract
