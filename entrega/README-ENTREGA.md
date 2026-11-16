## Defeitos corrigidos 

### 1. NO_Show entrando em totais
- **Caminho:** `src/onfly_report/services/status_policy.py`
- **antes:** return status != "CANCELLED", Fazia que qualquer valor, exceto CANCELLED entrasse nas conatgens por status, sendo assim qualquer valor entrasse ate mesmo NO_SHOW
- **depos:**  return status == "CONFIRMED", Agora faz com que apenas o valor CONFIRMED entre nos status.