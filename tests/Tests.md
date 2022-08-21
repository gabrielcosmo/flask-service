# TEstes com a API

## Testes em `/user`

### GET

Envie o nome do usuário como parametro de rota.
`print(user_get("marciano@marte.et"))`

### POST

Para cadastrar um novo usuário envie seu nome, email e senha.
```
 body = {
        "name": "Boné",
        "email": "bone@chapelaria.com",
        "password": "virado"
    }
 print(user_post(body))
```

### PUT
    
Para atualizar um registro de usuário envie um novo objeto com atualizações.
 ````
    body = {
        "email": "pet@garrafa.com",
        "emailsec": "petsecurity@garrafa.com",
        "id": 4,
        "name": "Pet",
        "password": "reciclavel"
    }
     print(user_put(body))
````

### DELETE

Para deletar um registro envie email e senha.
````
    body = {
        "email": "Gato",
        "password": "meow!"
    }
     print(user_delete(body))
````
    

## Testes em `/note`

### GET

Envie o nome do usuário como parametro de rota.
`print(user_note(4))`

### POST

Para registrar uma nova nota envie o id do usuário, um título e um texto para ela.
````
       body = {
        "favorite": False,
        "id": 1,
        "tags": '[
          "Feira",
          "mercado"
        ]',
        "text": "Sabado é dia de feira!",
        "title": "Feira"
      }
````

### PUT

Para atualizar um registro de usuário envie um novo objeto com atualizações.
````
 body = {
        "favorite": False,
        "id": 1,
        "tags": '[
          "Feira",
          "Essenciais"
        ]',
        "text": "Sabado é dia de comprar sorvete!",
        "title": "Feira: Essenciais"
      }
````

### DELETE

Para excluir uma nota informe seu id junto ao email e senha do usuário dono.
````
    body = {
        "id" = 4,
        "email": "fulano@detal.com",
        "password": "qualquercoisa123"
    }
````