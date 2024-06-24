# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    favourite_list =services_nasa_image_gallery.getAllFavouritesByUser(request)#llama a la funcion solo para traer los favoritos
    images = services_nasa_image_gallery.getAllImages()#llama a la funcion que trae todas las imagenes  
    paginator = Paginator(images, 5)  # Mostrar 5 imágenes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'favourite_list': favourite_list})

# función principal de la galería.
def home(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    images_per_page = int(request.GET.get('per_page', 5))  # Default 5 imágenes por página
    paginator = Paginator(images, images_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'page_obj': page_obj, 'favourite_list': favourite_list, 'images_per_page': images_per_page})

# función utilizada en el buscador.
def search(request):
    search_msg = request.GET.get('query', '')
    images = []

    if search_msg:
        images = services_nasa_image_gallery.getImagesBySearchInputLike(search_msg)
    else:
        images = services_nasa_image_gallery.getAllImages(None)
        #CODIGO PARA COLOCAR PAGINAS EN LA APP
    images_per_page = int(request.GET.get('per_page', 5))  #  avariable per_page que proviene del url

    paginator = Paginator(images, images_per_page) # Funcion paginatos images=total de imagenes, images_per_page= imagenes por pagina   
    page_number = request.GET.get('page')
    
    try: 
        page_obj = paginator.page(page_number)
    except PageNotAnInteger: #Error en caso de que no sea  un entero
        page_obj = paginator.page(1) #Ir a pagina 1
    except EmptyPage: # En caso de que la pagina este vacía
        page_obj = paginator.page(paginator.num_pages) 

    return render(request, 'home.html', {'page_obj': page_obj, 'query': search_msg, 'images_per_page': images_per_page})

@login_required
def getAllFavouritesByUser(request):
    favourite_list=services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)
    return redirect('favoritos') #redirecciona a favoritos para verificar que se haya agregado correctamente
    

@login_required
def deleteFavourite(request):
        services_nasa_image_gallery.deleteFavourite(request)
        return getAllFavouritesByUser(request)


@login_required
def exit(request):
    pass