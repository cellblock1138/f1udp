import sys
import struct
import socket
from teams import teams
from tracks import tracks
from flags import vehicle_fia_flags
from tyres import tyres
from gears import gears
from udppacket import UDPPacket
from ifdb_sender import send_request

# Configure listener IP & Port for UDP transmission of packed values
UDP_IP = "0.0.0.0"
UDP_PORT = 20777
BUFFER = 1289

# Receive packet from wire
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

def net_rx():
    data, addr = sock.recvfrom(BUFFER)  # receiving from socket
    return data

# Display helpers
def displaygear(gear):
    print("Current Gear: {}".format(gears[gear]))
    return

def displayspeed(mps):
    print("Current KPH: {:f} (MPH:{:f})".format(mps * 3.6, mps * 3.6 * 0.6))
    return

session_type = ["Unknown", "Practice", "Qualifying", "Race"]
era = {2017: "Modern", 1980: "Classic"}

def receiver():
    fmt = '<76f24bf5b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b9f9b13f' # define structure of packed data
    s = struct.Struct(fmt) # declare structure
    while True:
        # Get packets
        rx_data = net_rx()
        print("Packet data length: {} bytes".format(len(rx_data)))
        # print(rx_data)
        unpacked_data = s.unpack(rx_data)
        p = UDPPacket(unpacked_data)

        print("Unpacked data length: {}".format(len(unpacked_data)))
        #for index, value in enumerate(unpacked_data):
        #    print("{} : {}".format(index + 1, value))

        # Display data to console
        displaygear(p.m_gear)
        print("Current RPM: %d" % p.m_engineRate)
        displayspeed(p.m_speed)
        print("Lap: {} of {}".format(p.m_lap + 1, p.m_total_laps))
        print("Throttle position: {:f}".format(p.m_throttle))
        print("Race position: {}".format(p.m_car_position))
        print("Track length in meters: {}".format(p.m_track_size))
        print("Max gear: {}".format(p.m_max_gears))
        print("Session type: {}".format(session_type[int(p.m_sessionType)]))
        print("Total distance: {}".format(p.m_totalDistance))
        print("Distance remaining: {}".format(unpacked_data[61] * unpacked_data[60] - unpacked_data[3]))
        print("Track: {}".format(tracks[int(p.m_track_number)]))
        print("Flag: {}".format(vehicle_fia_flags[int(p.m_vehicleFIAFlags)]))
        print("Era: {}".format(era[p.m_era]))
        print("Team: {}".format(teams[p.m_era][int(p.m_team_info)]))

        # send processed datagram to Influx
        # send_request(p)

def main():
    print("Listenting on {}:{}".format(UDP_IP, UDP_PORT))
    receiver()

if __name__ == '__main__':
    main()
