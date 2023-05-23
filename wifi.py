import wifi
import matplotlib.pyplot as plt

def generate_wifi_heatmap():
    # Scan available Wi-Fi networks
    cells = wifi.Cell.all('wlan0')

    # Retrieve signal strength and coordinates
    signal_strengths = [cell.signal for cell in cells]
    latitudes = [cell.lat for cell in cells]
    longitudes = [cell.lon for cell in cells]

    # Create heatmap plot
    plt.scatter(longitudes, latitudes, c=signal_strengths, cmap='jet')
    plt.colorbar(label='Signal Strength (dBm)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Wi-Fi Signal Strength Heatmap')
    plt.show()

# Usage example
generate_wifi_heatmap()
