# Create Geo Visualizer and Analysis Tool Icon In Your Launcher
import os
os.system("chmod +x run")
Path = os.getcwd()
with open("GeoVisualizerAndAnalysisTool.desktop","w") as fh:
    with open("DesktopEntry", "r") as launchericon:
        fh.write(launchericon.read())
    fh.write("\nPath={path}/\n".format(path = Path))
    fh.write("Exec={path}/run\n".format(path = Path))
    fh.write("Icon={path}/icon/globe.png\n".format(path = Path))

os.system("chmod +x GeoVisualizerAndAnalysisTool.desktop")

os.system("cp GeoVisualizerAndAnalysisTool.desktop ~/.local/share/applications/")