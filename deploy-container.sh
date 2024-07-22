APP_NAME="ticketif-api"
# O volume é onde ficará o banco de dados
VOLUME_MAPPING=ticketif-data:/sqlite_db

VERSAO_ANTERIOR=$(docker image ls | grep $APP_NAME | tr -s ' ' | cut -d ' ' -f 2 | sort -rn | head -n 1)
NOVA_VERSAO=$((VERSAO_ANTERIOR+1))

IMAGE_NAME=$APP_NAME:$NOVA_VERSAO
echo $IMAGE_NAME
docker build -t $IMAGE_NAME .


docker container rm --force $APP_NAME
docker run --name $APP_NAME --restart always -p 8088:8000 -d -v $VOLUME_MAPPING $IMAGE_NAME
