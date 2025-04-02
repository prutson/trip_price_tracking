# Trip Price Tracking

API em Python para busca de preços de passagens de ônibus

## 🚀 Como executar

1. Crie um arquivo .env contendo seu token
```bash
API_TOKEN=<SEU_TOKEN>
```
2. Crie a imagem do docker e execute
```bash
docker-compose build && docker-compose up -d
```

ou se for no Windows
```bash
docker-compose build ; docker-compose up -d
```

## 🤖 Exemplo de requisição

1. Coloque no body as informações de origem, destino, data e quantidade de passageiros
```bash
{    
    "origem": "petrolina-pe",
    "destino": "salvador-ba",
    "data": "11-5-2025",
    "passageiros": 4
}
```

2. Não esqueça de colcoar seu Bearer Token
3. A resposta será algo como
```bash
{
    "result": [
        {
            "CATEGORIA": "SEMI LEITO",
            "CHEGADA": "22:00",
            "DATA": "11-5-2025",
            "DESTINO": "SALVADOR-BA",
            "ORIGEM": "PETROLINA-PE",
            "PASSAGEIROS": 4,
            "PRECO": "R$ 259,99",
            "SAIDA": "05:50"
        },
        {
            "CATEGORIA": "LEITO",
            "CHEGADA": "22:00",
            "DATA": "11-5-2025",
            "DESTINO": "SALVADOR-BA",
            "ORIGEM": "PETROLINA-PE",
            "PASSAGEIROS": 4,
            "PRECO": "R$ 279,99",
            "SAIDA": "05:50"
        },
        {
            "CATEGORIA": "LEITO INDIVIDUAL",
            "CHEGADA": "22:00",
            "DATA": "11-5-2025",
            "DESTINO": "SALVADOR-BA",
            "ORIGEM": "PETROLINA-PE",
            "PASSAGEIROS": 4,
            "PRECO": "R$ 339,99",
            "SAIDA": "05:50"
        }
    ]
}
```

## 💜 Apoie este projeto

Se meu código te ajudou ou você quer incentivar meu trabalho, pode me pagar um café via PIX!  

**Chave PIX:**  
`b3ebc88c-6b71-4134-aeb9-6fdb6cc0e6a0`
