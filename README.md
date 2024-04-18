# Diário Introdução Alimentar API

Essa API tem como objetivo realizar todas as operações necessárias para a criação de um diário de introdução alimentar

---
## Como executar

### Instalação de dependências

Para o correto funcionamento da API se faz necessária a instalação de todas as dependências listadas no arquivo `requirements.txt`. Os seguintes passos devem ser seguidos:

1. Clonar o repositório
2. Acessar, via terminal, a raiz do diretório
3. Executar o seguinte comando

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências listadas no arquivo `requirements.txt`.

>É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).


### Executando a API

O seguinte comando deve ser executado, via terminal, no diretório raiz

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Acesse [http://localhost:5000/](http://localhost:5000/) para verificar o status da API em execução.


