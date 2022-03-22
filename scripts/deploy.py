from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # Check for Persistent testnet or local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_pair"]

    # Use a Mock Price Feed
    else:
        print(f"Active Network: {network.show_active()}")
        print("Deploying Mock...")
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()][
            "verify"
        ],  # or .get("verify")
    )  # publish_source is to publish source code in etherscan
    print(f"Contract deployed to: {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
