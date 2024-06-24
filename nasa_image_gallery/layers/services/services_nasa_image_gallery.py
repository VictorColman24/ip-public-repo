# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
from django.shortcuts import redirect

def getAllImages(input=None):
    json_collection = transport.getAllImages(input)
    images = []
    for json in json_collection: # recorre el listado de objetos JSON, lo transforma en una NASACard y lo agrega en el listado de images
        try: # se agrega un try para que en caso de que falte algun item en la creación de nasa card no tire error
            imagen=mapper.fromRequestIntoNASACard(json)
            if imagen.title and imagen.description and imagen.image_url and imagen.date:
                    images.append(imagen)
            else:
                return redirect('home')
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
    return images



def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = mapper.fromTemplateIntoNASACard(request)# transformamos un request del template en una NASACard.
    fav.user = get_user(request) # le seteamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.


# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated: # si el usuario no esta registrado
        return [] # retorna lista vacía
    else:
        user=get_user(request) # se asocia el usuario desde el request con la funcion GET
        favourite_list=repositories.getAllFavouritesByUser(user) # Se genera la lista de usuarios llamando a la funcion  desde el repositorio
        
        mapped_favourites=[] # se abre una lista vacía donde se colocara la nasa_card
        
        for favourite in favourite_list: #for para recorrer  la lista de favoritos
            nasa_card=mapper.fromRepositoryIntoNASACard(favourite) #se genera la nasa_card desde el repositorio
            mapped_favourites.append(nasa_card) # se agrega la nasa_card del favorito en la lista
    return mapped_favourites #la lista de favoritos en formato nasa_card


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.