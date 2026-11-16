"""Testes adicionais: arquivos com mais de 200 reservas."""

from helpers import run_cli


def test_file_with_more_than_200_rows_is_read_entirely(tmp_path):
    """Nenhuma reserva pode ser descartada por limite de linhas."""
    rows = [{"reservation_id": f"R-{i}", "amount": "10.00"} for i in range(1, 251)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["confirmed_reservations"] == 250
    assert report["summary"]["total_amount_brl"] == "2500.00"