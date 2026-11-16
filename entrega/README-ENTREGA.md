# Entrega — Consolidador de reservas de hotel

Correção dos defeitos do CLI `onfly_report`, que gerava números errados no relatório JSON consolidado.

## Defeitos corrigidos

### 1. NO_SHOW entrando nos totais
- **Arquivo:** `src/onfly_report/services/status_policy.py`
- **Antes:** `return status != "CANCELLED"`
- **Depois:** `return status == "CONFIRMED"`
- **Causa raiz:** a regra excluía apenas `CANCELLED`, então `NO_SHOW` passava como faturável e entrava em noites, valores, `by_month` e `top_hotels`; só `CONFIRMED` é faturável.
- **Como detectei:** `test_status_rules` esperava `100.00` e recebeu `120.00`; a diferença de 20 era o valor do NO_SHOW.

### 2. Cálculo de câmbio errado e uso de float
- **Arquivo:** `src/onfly_report/services/currency_converter.py`
- **Antes:** `return Decimal(str(float(amount) / float(rate)))`
- **Depois:** `return amount * rate`
- **Causa raiz:** o valor era dividido pela taxa em vez de multiplicado, contrariando `amount * rate_to_brl`, e o cálculo passava por `float`, violando a regra de usar `Decimal` no dinheiro.
- **Como detectei:** `test_currency` esperava `642.00` (100 + 100 × 5,42) e recebeu `118.45` (100 + 100 ÷ 5,42).

### 3. Cálculo de noites ignorava a virada de mês ou ano
- **Arquivo:** `src/onfly_report/services/stay_calculator.py`
- **Antes:** `return (checkout.day - checkin.day) * rooms`
- **Depois:** `return (checkout - checkin).days * rooms`
- **Causa raiz:** o código subtraía apenas o dia do mês (`.day`), então estadias que atravessam o mês ou o ano davam resultado errado ou negativo; funcionava só por coincidência quando as datas estavam no mesmo mês.
- **Como detectei:** `test_nights` esperava 3 noites para 30/01 → 02/02 e recebeu -28 (2 − 30).

### 4. Ranking de hotéis em ordem crescente
- **Arquivo:** `src/onfly_report/services/report_builder.py`
- **Antes:** `key=lambda item: (item[1]["amount"], item[0])`
- **Depois:** `key=lambda item: (-item[1]["amount"], item[0])`
- **Causa raiz:** o valor não era invertido, então o `sorted` listava os hotéis do menor para o maior valor; a regra pede valor decrescente, com desempate por `hotel_id` ascendente.
- **Observação:** não usei `reverse=True`, porque ele inverteria também o desempate por `hotel_id`.
- **Como detectei:** `test_top_hotels` esperava `H01, H02, H03` e recebeu `H04, H03, H02`.

### 5. Leitura do CSV truncada em 200 linhas
- **Arquivo:** `src/onfly_report/repositories/csv_reservation_repository.py`
- **Antes:** o laço `for` tinha um `if len(rows) == 200: break`:
  ```python
  for values in reader:
      rows.append(RawRow(line_number=reader.line_num, values=values))
      if len(rows) == 200:
          break
  return rows
  ```
- **Depois:** o `if`/`break` foi removido e o arquivo é lido por inteiro:
  ```python
  for values in reader:
      rows.append(RawRow(line_number=reader.line_num, values=values))
  return rows
  ```
- **Causa raiz:** um limite fixo de 200 linhas interrompia a leitura, descartando as 100 últimas reservas do arquivo e subestimando todos os totais.
- **Como detectei:** nenhum teste fornecido pega esse defeito (usam menos de 200 linhas). Ao rodar o CLI no arquivo real, o resumo mostrava `Reservas: 200`, mas o CSV tem 300 reservas.

## Como investiguei

1. Li o `README.md` do desafio e as regras de negócio (status, noites, câmbio, exatidão e ordenação).
2. Rodei `pytest -q` e obtive 5 falhas. Li cada mensagem de erro e comparei o valor esperado com o obtido; por exemplo, `118.45` em vez de `642.00` indicava a operação invertida, e `-28` noites indicava o uso de `.day`.
3. Fui do teste ao arquivo responsável, no mapeamento: status → `status_policy.py`, câmbio → `currency_converter.py`, noites → `stay_calculator.py`, ranking → `report_builder.py`. Corrigi um defeito por vez, com um commit para cada.
4. Como os testes usam arquivos pequenos, procurei defeitos que eles não cobrem: rodei o CLI no arquivo completo e comparei `total_reservations` com o número de linhas do CSV, o que revelou o limite de 200.
5. Validei a amostra `data/exemplo-validacao.csv` contra a tabela do README e recalculei os totais do arquivo completo de forma independente, com `Decimal`, para confirmar o resultado.

## Como validar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

Para a amostra de validação do README:

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

Resultado da amostra (confere com o README): 12 reservas, 9 confirmadas, 2 canceladas, 1 no-show, 28 noites, `total_amount_brl` `7566.00`, média `270.21`, e ranking H01, H02, H12, H10, H09.

## Resultado

No arquivo completo (`data/reservas_hoteis.csv`): 300 reservas (235 confirmadas, 31 canceladas, 34 no-show), 1347 noites e `396170.00` BRL.

```
pytest -q
.....
8 passed
```

## Testes adicionados

Os 5 testes fornecidos continuam inalterados. Adicionei 3 testes de regressão, que falham no código original e passam após as correções:

- `tests/test_top_hotels_tiebreak.py`: valida o desempate por `hotel_id` ascendente quando dois hotéis têm o mesmo valor (o teste fornecido não cobre empate).
- `tests/test_large_file.py`: valida que um arquivo com 250 reservas é lido por inteiro; cobre o defeito 5, que nenhum teste fornecido detectava.
- `tests/test_nights_year_boundary.py`: valida o cálculo de noites na virada de ano com mais de um quarto (30/12 → 02/01, 2 quartos = 6 noites de quarto).
Os testes fornecidos não foram alterados.

## Uso de IA

Utilizei IA como apoio. A sessão e a declaração estão em `entrega/uso-de-ia/`.