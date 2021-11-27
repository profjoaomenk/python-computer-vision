from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

'''
Autenticação
Informe o ponto de extremidade (endpoint) e a chave de acesso ao Serviço (subscription_key)
'''
subscription_key = "277e71ed387a408d8c14027dce3e589b"
endpoint = "https://know-image-rm9999.cognitiveservices.azure.com/"

#Autenticar o cliente

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#
# Leitura de Imagem Remota
#

'''
Este exemplo irá extrair o texto em uma imagem remota e, em seguida, irá imprimir os resultados, linha por linha
'''
print("===== Lendo Arquivo - remoto =====")
# Pega uma imagem com um texto
read_image_url = "https://www.belasmensagens.com.br/wp-content/uploads/2012/08/a-imaginacao-400x300.jpg"
# Chama a API  com a URL e com resposta raw (bruta). Isso permite obter a localização da operação
read_response = computervision_client.read(read_image_url, raw=True)

# Obtenha o local da operação (URL com um ID no final) da resposta
read_operation_location = read_response.headers["Operation-Location"]
# Pegue o ID do URL
operation_id = read_operation_location.split("/")[-1]

# Chame a API "GET" e espere que ela recupere os resultados
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Imprime o texto detectado, linha por linha
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()


#
# Leitura de Imagem Local
#

# Pasta criada anterormente
images_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "images")

'''
Este exemplo extrai texto de uma imagem local e depois imprime os resultados
'''
print("===== Lendo Arquivo - Local =====")
# Obter caminho da imagem
read_image_path = os.path.join (images_folder, "Voltaire.jpeg")
# Abra a imagem
read_image = open(read_image_path, "rb")

# Chama a API  com a URL e com resposta raw (bruta). Isso permite obter a localização da operação
read_response = computervision_client.read_in_stream(read_image, raw=True)
# Obtenha o local da operação (URL com ID como último apêndice)
read_operation_location = read_response.headers["Operation-Location"]
# Recupere o ID e use para obter resultados
operation_id = read_operation_location.split("/")[-1]

# Chame a API "GET" e espere que ela recupere os resultados
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status.lower () not in ['notstarted', 'running']:
        break
    print ('Waiting for result...')
    time.sleep(10)

# Imprime o texto detectado, linha por linha
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()

#
# Analisar uma Imagem Remota
#

print("===== Analisando Imagem - Remota =====")

url = "https://quatrorodas.abril.com.br/wp-content/uploads/2017/06/568bd98882bee174ca3f64f8ferrari-488-gtb1.jpeg?quality=70&strip=info"

image_analysis = computervision_client.analyze_image(url,visual_features=[VisualFeatureTypes.tags, VisualFeatureTypes.description])

print("A imagem pode ser descrita como: {}\n".format(
    image_analysis.description.captions[0].text))

print("Tags associadas com essa imagem:\nTag\t\tConfidence")
for tag in image_analysis.tags:
    print("{}\t\t{}".format(tag.name, tag.confidence))
