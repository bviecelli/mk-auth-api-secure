# mk-auth-api-secure
Camada de segurança para utilização da API do sistema de gerência de provedores MK-AUTH.
Saiba mais sobre o MK-AUTH em [mk-auth.com.br](http://www.mkauth.com.br).

## Conceitos
A motivação para escrever esta API foi a necessidade de criar uma interface com os dados dos clientes do provedor segura
, moderna e totalmente compatível com dispositivos móveis.

A linguagem escolhida foi [Python](http://python.org) em sua versão 3.

Também foi escolhido utilizar [JWT](http://jwt.io) para criptografar os dados ponto a ponto.

O acesso aos dados do MK-AUTH é feito através de uma conexão direta com o banco de dados do software. Você tem a 
liberdade de escolher se roda este software juntamente com a VM do MK-AUTH ou também pode rodar em outro servidor, desde
que o acesso externo ao banco de dados esteja liberado.

## Como usar
Instale os pacotes de requisitos com
```
pip install -r requirements.txt
```

E rode o código
```
python app.py
```

O serviço vai rodar por padrão localmente na porta 5000.

## Futuro
O ambiente ideal para que este software rode é com SSL ativo, então daria para tirar o JWT da jogada e o nível de
segurança já estaria garantido.

Também ainda há muito o que fazer, então otimizar os dados que trafegam seria o próximo passo. Ainda tenho a ideia de
implantar um sistema de autenticação mais moderno, como o [OAuth2](https://oauth.net/2/) que é bastante utilizado em
sistemas para celulares, porém o fluxo deve ser bem pensado para que os usuários da API não tenham mais malefícios do
que benefícios.
 
## Contribuições
Fiquem à vontade para submeterem pull-requests e/ou abrir issues. Assim que possível estarei verificando.

Qualquer coisa enviem e-mail para bviecelli@gmail.com 