# Challenge 4 - Kenzie Buster

Projeto em Django e Django Rest Framework utilizando serializers e relacionamentos 1:N/N:N para montar uma API que gerencia usuários, filmes e compras de filmes, incluindo autenticação e permissões de rotas para diferentes tipos de usuário.
<br><br>

### Rotas users <br>
| Endpoint  | Verbo HTTP | Objetivo  | Permissão |
| --------- | ---------- | --------- | --------- |
| api/users/ | POST | Criar usuários | - |
| api/users/login/ | POST | Autenticar as credenciais de um usuário e retornar um token de acesso JWT | - |
| api/users/user_id/ | GET | Listar usuário | Somente autenticado e dono da conta ou admin
| api/users/user_id/ | PATCH | Atualizar usuário | Somente autenticado e dono da conta ou admin
<br>

### Rotas movies <br>
| Endpoint  | Verbo HTTP | Objetivo  | Permissão |
| --------- | ---------- | --------- | --------- |
| api/movies/| GET | Listar músicas | Livre para acesso |
| api/movies/| POST | Criar músicas | Somente employee |
| api/movies/movie_id/| GET | Listar uma música | Livre para acesso |
| api/movies/movie_id/| DELETE | deletar música | Somente employee |
| api/movies/movie_id/orders/| POST | Comprar música | Somente autenticado |
<br>


