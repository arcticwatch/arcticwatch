from folium import IFrame
import folium
import os

stations = open("templates/stations.csv", "r")
name = []
lat = []
lon = []
country = []
abbr = []

for station in stations.readlines():
    l = station.split(",")
    name.append(l[0])
    lat.append(l[1])
    lon.append(l[2])
    country.append(l[3])
    abbr.append(l[4].replace("\n", ""))

MAP = folium.Map(location=[78.906688, 11.889342], zoom_start=4, tiles="Stamen Terrain", zoomControl=False)
for c in range(len(name)):
    svg = open("static/graphs/ZEP/small/13-CO2.png.svg").read()
    gases = os.popen("ls ../datasets/" + abbr[c]).read().split("\n")

    html = """
<select style="position:fixed;" id="gasSelect" class="form-select form-select-sm" aria-label=".form-select-sm example" onchange="myFunction()">
<br>
<option selected>Select gas</option>
    """
    c2 = 0
    for gas in gases[:-1]:
        html += "\n<option value=\"{0}\">{1}</option>".format(str(c2), gas)
        c2 += 1

    html += "\n</select>\n</form>"

    c2 = 0
    for gas in gases[:-1]:
        html += "<span id={0}></span><br><br><div>".format(str(c2)) + open("static/graphs/{0}/small/{1}.png.svg".format(abbr[c], gas)).read() + "</div>"
        c2 += 1

    html += """
<script>
function myFunction() {
  var sel = document.getElementById("gasSelect");
  document.location.href = "#" + sel.value;
}
</script>
    """

    iframe = IFrame(html, width=650 + 20, height=325 + 50)
    popup = folium.Popup(iframe, max_width=650)

    icon = folium.Icon(color='blue', icon='ok')
    marker = folium.Marker(
             [lat[c], lon[c]], popup=popup, tooltip=name[c],
             icon=folium.Icon(icon="info-sign"))

    marker.add_to(MAP)

MAP.save("templates/map.html")
