"""Testes adicionais: noites na virada de ano e com vários quartos."""

from helpers import run_cli


def test_nights_across_year_boundary_with_multiple_rooms(tmp_path):
    """30/12 -> 02/01 são 3 noites; com 2 quartos, 6 noites de quarto."""
    report = run_cli(
        tmp_path,
        [{"checkin_date": "2024-12-30", "checkout_date": "2025-01-02", "rooms": "2"}],
    )
    assert report["summary"]["total_room_nights"] == 6