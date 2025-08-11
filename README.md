# Image Conveter

Conversor de imagem para WEBP usado pelo WhatsApp.

## Texto para lembrar quando fizer manutenção

### Subindo em homolog

Quando você der ``sam build; sam deploy``, vai buildar uma nova versão e o **alias 'dev' vai apontar para a nova versão sempre**.
O alias 'dev' é usado na API Gateway de homolog, na branch 'homolog' do projeto *best-stickerapp-api*.

### Subindo em prod

A API Gateway de prod aponta para o alias 'prod' deste projeto, então você precisa mudar a versão que o alias prod aponta.

``aws lambda update-alias \
--function-name StickerImageConverter \
--name prod \
--function-version <NUMERO_VERSAO>``

Para saber qual versão foi subida em homolog ou para mostrar todos os alias, o comando é:
`` aws lambda list-aliases --function-name StickerImageConverter``


