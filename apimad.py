################################################################################
#  File under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Este fichero extrae el listaod de datasets del portal de datos abiertos de la comunidad de Madrid
# version 0.4

# Importamos dos librerías básicas
import json
import requests

# url base  del API del portal de datos de la comunidad de Madrid
base_url = "http://datos.comunidad.madrid/api/3/action/package_list"

# Realizamos la petición
result = requests.get(base_url)

# Si el resultado es exito de la conexión cargamos los resultados en una variable
if result.status_code == 200:
    catalogue_dict = json.loads(result.text)

# Listamos los resultados
for item in catalogue_dict["result"]:
    print(item)
    