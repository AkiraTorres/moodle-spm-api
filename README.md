# Pré-processamento de Sequências de Eventos de Aprendizagem para Mineração de Padrões Sequenciais

Este repositório contém o código-fonte desenvolvido para o pré-processamento de sequências de eventos de aprendizagem, visando melhorar a qualidade dos padrões identificados em algoritmos de Mineração de Padrões Sequenciais (SPM), usando especificamente o algoritmo PrefixSpan. Este trabalho foi realizado como parte de um estudo apresentado no Simpósio Brasileiro de Informática na Educação (SBIE 2024) e busca avaliar o impacto de diversas estratégias de pré-processamento em padrões extraídos de logs de interação de alunos em cursos de educação a distância (EaD) oferecidos no Moodle.
Visão Geral

O código simplification.py implementa uma série de funções para manipular dados de logs de eventos em ambientes de aprendizagem, aplicando estratégias de pré-processamento para filtrar e simplificar eventos antes da execução de algoritmos de mineração de padrões. O estudo que acompanha o código analisa como essas estratégias influenciam o desempenho e a qualidade dos padrões detectados pelo algoritmo PrefixSpan.
Estratégias de Pré-processamento Implementadas

Para mais detalhes sobre a metodologia e os resultados da pesquisa, consulte o artigo completo em [Link omitido].

## As principais estratégias de pré-processamento utilizadas são:

    Multilevel Sequential Patterns: Adiciona níveis (ex.: "_START" e "_END") aos eventos, com base na proximidade da data limite da atividade. Essa estratégia permite a diferenciação entre ações realizadas no início ou no fim do período de avaliação.

    Coalescing Repeating Point Events into One: Remove eventos repetitivos consecutivos, mantendo apenas o primeiro evento de uma sequência de ações idênticas. Isso reduz ruídos nos dados e melhora a expressividade dos padrões.

    Converting Hidden Complex Events into One: Agrupa subsequências complexas e previsíveis em eventos únicos, como ações obrigatórias que precedem uma tarefa, reduzindo o volume de dados sem perda de relevância semântica.

    Spell: Agrupa eventos repetidos consecutivamente, indicando a frequência com sufixos como _SOME ou _MANY, para reduzir redundância semântica.

    Temporal Folding: Organiza eventos em sessões baseadas em um intervalo de tempo (session_gap), agrupando eventos próximos para capturar sequências significativas em uma mesma sessão.

## Estrutura do Código

O código consiste nas seguintes funções principais:

    save_to_csv: Salva dataframes de logs em arquivos CSV.
    event_mapping: Mapeia eventos para classes específicas com base em um dicionário de mapeamento.
    temporal_folding: Agrupa eventos em sessões temporais definidas por intervalos de tempo.
    coalescing_hidden e coalescing_repeating: Simplificam as sequências removendo eventos redundantes e agrupando eventos complexos.
    spell: Ajusta eventos repetitivos, atribuindo um sufixo que indica a quantidade de repetições.
    generate_sequence_from_df: Gera uma sequência de eventos para cada aluno a partir do DataFrame de logs.
    prepare_database: Organiza os dados para uso posterior em algoritmos de mineração.
    partitioning e classify_events: Filtram e classificam eventos relevantes para análise.
    read_params: Lê e valida parâmetros de execução passados via linha de comando.
    main: Executa o pré-processamento e armazena as sequências geradas no formato JSON.

## Requisitos

    Python 3.12+
    Pandas para manipulação de dados
    Arquivos CSV de entrada: logs de eventos, mapeamento de eventos, dados de notas e atividades.

## Uso
### Parâmetros de Execução

Para executar o script, forneça os parâmetros necessários:

    --path: Caminho do arquivo de log de eventos.
    --save-path: Caminho para salvar o JSON resultante.
    --grade-path: Caminho do CSV de notas dos alunos.
    --quiz-path: Caminho do CSV de questionários.
    --mapping-path: Caminho do CSV de mapeamento de eventos.

Os parâmetros para seleção das técnicas de pré-processamento são opcionais, necessitando serem fornecidos para as técnicas de pré-processamento serem aplicadas, sendo eles:

    --multilevel
    --coalescing-repeating
    --coalescing-hidden
    --spell
    --temporal-folding

### Exemplo de Execução

```bash
python simplification.py -p <caminho_do_arquivo_de_log> -sp <caminho_para_salvar> -pg <caminho_das_notas> -pq <caminho_do_questionario> -mp <caminho_do_mapeamento>
```

## Resultados e Avaliação

Após o pré-processamento, as sequências resultantes podem ser usadas com algoritmos de mineração de padrões sequenciais. No estudo realizado, o algoritmo PrefixSpan foi utilizado para identificar padrões nos dados processados e avaliar o impacto das estratégias de pré-processamento em termos de qualidade e suporte dos padrões.
Referências

## TODO

- **Implementar novas estratégias de pré-processamento**:
  - [X] **Temporal Folding**: Adicionar suporte para definir uma janela de tempo específica para análise dos eventos.
  - [X] **Spell**: Permitir a exclusão de categorias de eventos que não contribuem para a análise.

- **Melhorar a interface CLI**:
  - [ ] Incluir validação avançada dos arquivos de entrada, com mensagens de erro mais detalhadas.
  - [ ] Adicionar suporte para configurar o `session_gap` na linha de comando.

- **Documentação**:
  - [ ] Expandir a documentação com mais exemplos de uso e descrição das estratégias de pré-processamento.
  - [ ] Incluir um diagrama de fluxo de dados para ilustrar o processo de pré-processamento.
  - [ ] Adicionar link para o artigo quando o mesmo for publicado.
  - [ ] Adicionar imagem ao `README.md` descrevendo os diferentes cenários possíveis.

- **Testes**:
  - [ ] Desenvolver testes unitários para todas as funções de pré-processamento.
  - [ ] Adicionar testes de integração para garantir que a CLI funcione com diferentes combinações de parâmetros.

- **Otimizações de Desempenho**:
  - [ ] Revisar o desempenho da função `temporal_folding` para melhorar a eficiência ao lidar com grandes volumes de dados. 
  - [ ] Separar melhor as funções do script `simplification.py` para melhor organização de código.
  - [ ] Implementar caching para operações de leitura de grandes arquivos CSV, acelerando o processamento.

- **Compatibilidade**:
  - [ ] Adicionar suporte para mais formatos de entrada (ex.: JSON, Parquet).
  - 