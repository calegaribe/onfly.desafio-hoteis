# Declaração de uso de IA

## Ferramenta e modelo
- **Ferramenta:** Claude (Anthropic), pelo claude.ai, em uma conversa de chat com acesso a ferramentas.
- **Modelo:** Claude Sonnet 5.5.
- **Outras ferramentas de IA:** nenhuma 

## O que a IA fez
- Leu o repositório do desafio e explicou o enunciado e a estrutura do projeto.
- Ajudou a entender as bibliotecas e como usar o PowerShell e o venv.
- Revisou as correções que escrevi e apontou os erros.
- Reproduziu as correções em uma cópia separada do projeto para validar a amostra do README e os totais do arquivo completo.
- Escreveu o modelo do `README-ENTREGA.md` e os 3 testes adicionais, que eu adaptei e executei.

## O que eu fiz
- Criei o repositório, configurei os ambientes e executei todos os comandos.
- Li as falhas do `pytest` e analisei o código de cada módulo.
- Escrevi e testei as correções dos defeitos 1 (status), 2 (câmbio) e 3 (noites); no ranking e na leitura do CSV, e verifiquei que os testes passavam.
- Localizei a leitura truncada ao rodar o CLI no arquivo real e ver `Reservas: 200`.
- Escrevi as causas raiz de cada defeito, revisei e corrigi o texto do `README-ENTREGA.md`, e criei os arquivos de teste.
- Fiz os commits e o push, e conferi o resultado final (`pytest -q`).
- Não alterei os testes fornecidos, os CSVs de `data/` nem o contrato do CLI.

## Observação
Revisei todo o conteúdo gerado pela IA e entendo o motivo de cada correção.
A conversa completa está em `sessao.md`.