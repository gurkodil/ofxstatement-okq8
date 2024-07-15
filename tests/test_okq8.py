import os

from ofxstatement.ui import UI
from datetime import datetime

from ofxstatement_okq8.plugin import OKQ8Plugin


def test_okq8() -> None:
    plugin = OKQ8Plugin(UI(), {})
    here = os.path.dirname(__file__)
    sample_filename = os.path.join(here, "transaktioner.xlsx")

    parser = plugin.get_parser(sample_filename)
    statement = parser.parse()

    assert statement is not None
    assert statement.account_id == "OKQ8"
    assert statement.currency == "SEK"
    assert statement.bank_id == "OKQ8"

    assert len(statement.lines) == 3

    expected = [
        {
            "memo": "Finska pinnar",
            "amount": -12,
            "date": datetime(2024, 7, 4, 0, 0),
            "trntype": "DEBIT",
        },
        {
            "memo": "Bg Inbetalning",
            "amount": 5579.64,
            "date": datetime(2024, 6, 28, 0, 0),
            "trntype": "CREDIT",
        },
        {
            "memo": "OKQ8, Dubbelt Upp!",
            "amount": 120,
            "date": datetime(2024, 6, 27, 0, 0),
            "trntype": "CREDIT",
        },
    ]

    for expected, stmt_line in zip(expected, statement.lines):
        assert expected["memo"] == stmt_line.memo
        assert expected["amount"] == stmt_line.amount
        assert expected["date"] == stmt_line.date
        assert expected["trntype"] == stmt_line.trntype
