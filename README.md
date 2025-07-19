# Script KAutoHunt
## Descrição
---
Este script utiliza modelos treinados pelo Teachable Machine para realizar reconhecimento de imagens em tempo real no jogo, automatizando ações com base nos objetos detectados.
Funcionamento

    O modelo treinado (.h5) é utilizado para reconhecimento de imagens capturadas da tela.

    Um arquivo .txt gerado junto com o modelo contém as categorias dos objetos (nomes dos monstros) reconhecíveis.

    O script faz ajustes e pré-processamento das imagens para melhorar a detecção.
---
## Automação
---
Com base no resultado da detecção:

    Move o mouse até a posição do objeto reconhecido.

    Usa a habilidade configurada no F2 para atacar o alvo.

    Caso não encontre um objeto viável (por falha de detecção ou o objeto não ser alvejável, por exemplo, se houver uma parede na frente), utiliza F3 para teletransporte, buscando um novo local e repetindo o processo.
---
## Requisitos
---
    Modelo treinado (.h5) pelo Teachable Machine seguindo o padrão do projeto.

    Arquivo .txt contendo as categorias dos monstros detectáveis, gerado junto ao modelo.

    Python 3.10 ou superior.

    Bibliotecas listadas em requirements.txt.
---
## Observações
---
    Os modelos devem ser criados por mapa, evitando misturar monstros de mapas diferentes em um único modelo.

    O script foi desenvolvido para uso integrado à interface KAutoHunt, porém pode ser adaptado para execução independente.
---
## Status

Em desenvolvimento, com melhorias contínuas em performance de detecção, organização do código e implementação de novas funcionalidades.
