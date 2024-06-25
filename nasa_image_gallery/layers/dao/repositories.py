# capa DAO de acceso/persistencia de datos.

from nasa_image_gallery.models import Favourite

def saveFavourite(image):
        fav = Favourite.objects.create(title=image.title, description=image.description, image_url=image.image_url, date=image.date, user=image.user)
        return fav

def getAllFavouritesByUser(user):
    favouriteList = Favourite.objects.filter(user=user).values('id', 'title', 'description', 'image_url', 'date')
    return list(favouriteList)

def deleteFavourite(id):
        favourite = Favourite.objects.get(id=id)
        favourite.delete()
        return True