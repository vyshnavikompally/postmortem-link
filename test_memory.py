from incidents import INCIDENTS
from memory import retain_incident, recall_incidents

print("Storing incidents in Hindsight...")

for incident in INCIDENTS:
    retain_incident(incident)
    print(f"Stored: {incident['id']}")

print("\nSearching memory...")

result = recall_incidents(
    "Improve payment timeout handling and retry logic"
)

print("\nRECALLED MEMORIES:")

for memory in result.results:
    print("-", memory.text)