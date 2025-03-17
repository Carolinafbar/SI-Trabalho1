# SI-Trabalho1
## Descrição do Projeto
Este projeto implementa a resolução do problema 8-Puzzle utilizando dois algoritmos de busca:

- **BFS (Breadth-First Search)**
- **A*** com heurísticas de **Manhattan** e **Hamming**.

O programa recebe um estado inicial e um estado final do tabuleiro e determina o caminho de menor custo para resolver o puzzle, caso uma solução exista.

## Requisitos para Execução

O código foi desenvolvido em **Python 3** e utiliza apenas bibliotecas padrão da linguagem. Certifique-se de ter o Python instalado em seu sistema antes de executar.

## Como Executar o Programa

1. Faça o download do repositório
```git clone https://github.com/Carolinafbar/SI-Trabalho1.git```
2. Navegue até a pasta do projeto
```cd SI-Trabalho1```
3. Execute o programa
   - No VS Code: Abra o arquivo puzzle8.py e clique em Run Python File
     
4. O programa solicitará que você insira o estado inicial do tabuleiro. Digite os números de 0 a 8 separados por espaço, onde 0 representa o espaço vazio.

5. Em seguida, insira o estado final desejado do tabuleiro.

6. O programa verificará se o problema tem solução. Caso tenha, você poderá escolher o algoritmo:
- 1 para BFS
- 2 para A*

7. Se escolher A*, será solicitado que você selecione a heurística:
- 1 para Manhattan
- 2 para Hamming

8. O programa executará o algoritmo e exibirá:
-O número total de movimentos.
-O tempo de execução.
-A memória consumida pelo algoritmo.

## Notas Finais
- O programa verifica se o puzzle é solucionável antes de executar os algoritmos.
- Em casos mais complexos, o tempo e a memória utilizados podem ser significativamente maiores.
- Para mais detalhes sobre a implementação e resultados dos testes, consulte o **Relatório do Trabalho Prático 1.docx**.

 Carolina de Barbosa Fernandees 
 044897@umaia.pt
   
