# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos 

### 1. NO_SHOW entrando em totais

- **Caminho:** `src/onfly_report/services/status_policy.py`
- **Antes:** return status != "CANCELLED", Fazia que qualquer valor, exceto CANCELLED, passasse como faturável e entrava em noites, valores, por mês e ranking, sendo assim qualquer valor entrasse, até mesmo NO_SHOW
- **Depois:**  return status == "CONFIRMED", Agora faz com que apenas o valor CONFIRMED entre nos status.

### 2. Erro de cálculo, e uso desnecessário de float

- **Caminho:** `src/onfly_report/services/currency_converter.py`
- **Antes:** return Decimal(str(float(amount) / float(rate))), Fazia o uso desnecessário de float já que os valores já estão em decimal, e fazia conta de divisão enquanto nas regras exigia multiplicação
- **Depois:** return amount*rate. Agora faz a multiplicação e sem o uso desnecessário de float

### 3. Erro de cálculo, ignoravam a datas em troca de mês ou ano

- **Caminho:** `src/onfly_report/services/stay_calculator.py`
- **Antes:** return (checkout.day - checkin.day) * rooms, Quando as estadias que atravessam o mês ou o ano fossem reservadas, o cálculo ficava incorreto, pois subtraía apenas os dias do mês
- **Depois:** return (checkout - checkin).days * rooms. Agora faz diferença de datas completas, não só pelo dia 

### 4. Rank dos hotéis em ordem crescente

- **Caminho:** `src/onfly_report/services/report_builder.py`
- **Antes:** key=lambda item: (item[1]["amount"], item[0]), Como os valores não invertiam o sorted listava os hotéis de menor para maior valor
- **Depois:** key=lambda item: (-item[1]["amount"], item[0]), Agora invertendo os valores, Agora o valor é invertido (decrescente) e o desempate por hotel_id continua ascendente, como pede o README.

### 5. Leitura do CSv truncada em 200 linhas

- **Caminho:** `src/onfly_report/repositories/csv_reservation_repository.py`
- **Antes:** o laço for tinha um if len(rows) == 200: break`:
  for values in reader:
      rows.append(RawRow(line_number=reader.line_num, values=values))
      if len(rows) == 200:
          break
  return rows

- **Depois:** o if/break foi removido e o arquivo é lido por inteiro:
  for values in reader:
      rows.append(RawRow(line_number=reader.line_num, values=values))
  return rows
  