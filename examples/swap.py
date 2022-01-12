"""Atomic Swap"""

alice = Addr("6ZHGHH5Z5CTPCF5WCESXMGRSVK7QJETR63M3NY5FJCUYDHO57VTCMJOBGY")
bob = Addr("7Z5PWO2C6LFNQFGHWKSK5H47IQP5OJW2M3HA2QPXTY3WTNP5NU2MHBW27M")
secret = Bytes("base32", "2323232323232323")
timeout = 3000
ZERO_ADDR = Global.zero_address()

def teal(
    tmpl_seller=alice,
    tmpl_buyer=bob,
    tmpl_fee=1000,
    tmpl_secret=secret,
    tmpl_hash_fn=Sha256,
    tmpl_timeout=timeout,
):
        
    fee_cond = Txn.fee() < Int(tmpl_fee)
    is_payment = Txn.type_enum() == TxnType.Payment
    no_closeto = Txn.close_remainder_to() == ZERO_ADDR
    no_rekeyto = Txn.rekey_to() == ZERO_ADDR
    no_close_rekey = no_closeto and no_rekeyto
    safety_cond = is_payment and no_close_rekey
      
    recv_cond = (Txn.receiver() == tmpl_seller) and (tmpl_hash_fn(Arg(0)) == tmpl_secret)

    esc_cond = (Txn.receiver() == tmpl_buyer) and (Txn.first_valid() > Int(tmpl_timeout))
    return (fee_cond and safety_cond) and (recv_cond or esc_cond)
