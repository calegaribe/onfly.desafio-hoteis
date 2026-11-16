## Defeitos corrigidos 

### 1. NO_Show entrando em totais

- **Caminho:** `src/onfly_report/services/status_policy.py`
- **Antes:** return status != "CANCELLED", Fazia que qualquer valor, exceto CANCELLED entrasse nas conatgens por status, sendo assim qualquer valor entrasse ate mesmo NO_SHOW
- **Depos:**  return status == "CONFIRMED", Agora faz com que apenas o valor CONFIRMED entre nos status.

### 2. Erro de calculo, mais uso desnecessário de float

-**Caminho:** `src/onfly_report/services/currency_converter.py`
- **Antes:** return Decimal(str(float(amount) / float(rate))), Fazia o uso desnecessário de float já que os valores já estão em decimal, e fazia conta de divisão enquanto nas regras exigia multiplicação
- **Depos:** return amount*rate. Agora faz a multiplicação e sem o uso desnecessário de float

### 3. Erro de calculo, ignoravam a datas em troca de mês ou ano

-**Caminho:** `src/onfly_report/services/stay_calculator.py`
- **Antes:** return (checkout.day - checkin.day) * rooms, Quando as reservas fossem feitas em datas que fiquem em troca de mês ou ano o calculo ficava incorreto, pois subtraía apenas os dias do mês
- **Depos:** return (checkout - checkin).days * rooms. Agora faz diferença de datas completas, não so pelo dia 

