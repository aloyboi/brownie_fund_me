from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_fund_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.checkBalance() == entrance_fee

    tx1 = fund_me.withdraw({"from": account})
    tx1.wait(1)
    assert fund_me.checkBalance() == 0


def test_only_owner_can_withdraw():  # want to restrict testing to local testing only, disable on testnet
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    account = get_account()
    fund_me = deploy_fund_me()
    bad_account = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):  # how to test failure
        fund_me.withdraw({"from": bad_account})
