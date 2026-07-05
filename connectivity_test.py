# connectivity_test.py
# ESZG517 IoT Lab — Pre-Lab Environment Check

import ssl
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient

print("=== ESZG517 Environment Check ===\n")

# ---- Your credentials ----
HIVEMQ_HOST  = "7249a6fd424e4fb288f0291ec7685503.s1.eu.hivemq.cloud"
HIVEMQ_USER  = "2025ca01037"
HIVEMQ_PASS  = "Shet@2302"

INFLUX_URL   = "https://eu-central-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "OVrfZS65yguS4JIgkCkqEKpf9MxFNqmTMLE8GQ1Kj9FZ04lAvXZfA0nXt3WsfcXJO8oirjimBOlmfb10nz967w=="
INFLUX_ORG   = "IoT-Lab-2025ca01037"
# --------------------------

# Test 1: HiveMQ
print("[1/2] Testing HiveMQ Cloud connection...")
result = {"connected": False}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        result["connected"] = True

client = mqtt.Client(client_id="test_check")
client.username_pw_set(HIVEMQ_USER, HIVEMQ_PASS)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect
try:
    client.connect(HIVEMQ_HOST, 8883, keepalive=5)
    client.loop_start()
    import time; time.sleep(3)
    client.loop_stop(); client.disconnect()
    if result["connected"]:
        print("    HiveMQ Cloud: CONNECTED\n")
    else:
        print("    HiveMQ Cloud: FAILED — check your credentials\n")
except Exception as e:
    print(f"    HiveMQ Cloud: ERROR — {e}\n")

# Test 2: InfluxDB (Actual Write Test with Clean Shutdown)
print("[2/2] Testing InfluxDB Cloud connection...")
try:
    # Initialize client
    influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    
    # Using 'with' statement guarantees the background batch writer 
    # flushes data and shuts down cleanly before moving forward
    with influx.write_api() as write_api:
        print("    Attempting to write test data point...")
        write_api.write(
            bucket="iotlab", 
            org=INFLUX_ORG, 
            record="test_measurement,tag_key=tag_val field_key=1.0"
        )
    
    print("    InfluxDB Cloud: CONNECTED & VERIFIED (Data written successfully!)\n")
    influx.close()

except Exception as e:
    print(f"    InfluxDB Cloud: FAILED — {e}\n")

print("=== Check Complete ===")
