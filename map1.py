import folium
import pandas
import math

def distanceBetweenTwo(lat1,lon1,lat2,lon2):
    R = 6373
    dlon = (lon2 - lon1) * math.pi / 180
    dlat = (lat2 - lat1) * math.pi / 180
    a = (math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1 * math.pi/180) * math.cos(lat2 * math.pi/180) * math.sin(dlon/2)* math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1



data = pandas.read_csv("location.txt", sep='\t')

i = 0

fg = folium.FeatureGroup(name="My Map")
map = folium.Map(location=[41.075671, 28.945197],zoom_start =10 ,tiles="Mapbox Bright")

fg.add_child(folium.Marker(location=[41.075671,28.945197], popup='Istanbul', icon=folium.Icon(color='black')))


lat = list(data["LAT"])
lon =  list(data["LON"])
elev = list(data["ELEV"])

for lt, ln in zip(lat,lon):
    data.set_value(i,'distance', math.sqrt( (41.075671 - lt)**2 + (28.945197 - ln)**2 ))
    i = i+1
    
data = data.sort_values('distance', ascending=True, inplace=False, kind='mergesort', na_position='last')

lat = list(data["LAT"])
lon =  list(data["LON"])
elev = list(data["ELEV"])

for i in range(0,100):
    fg.add_child(folium.Marker(location=[lat[i], lon[i]], popup= elev[i], icon=folium.Icon(color='green')))

map.add_child(fg)
map.save("Map1.html")