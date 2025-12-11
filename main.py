from apts.models.location import Location
from apts.models.transit import Transit
from apts.models.object import Object

# Create locations
home = Location("Home", "A cozy little apartment.")
work = Location("Work", "The bustling office.")

# Create objects
keys = Object("Keys", "A set of keys for home and office.")
laptop = Object("Laptop", "A powerful work machine.")
wallet = Object("Wallet", "Contains ID and credit cards.")

# Place objects in a location
home.objects.append(keys)
home.objects.append(wallet)
print(f"At {home.name} ({home.description}):")
for obj in home.objects:
    print(f"- {obj.name} ({obj.description})")

# Create a transit between locations
commute = Transit(origin=home, destination=work)
print(f"\nPreparing for transit from {commute.origin.name} to {commute.destination.name}.")

# Move an object to the transit
home.objects.remove(wallet)
commute.objects.append(wallet)
commute.objects.append(laptop)

print(f"\nDuring transit:")
for obj in commute.objects:
    print(f"- {obj.name} ({obj.description})")

# Arrive at the destination
work.objects.extend(commute.objects)
commute.objects.clear()

print(f"\nArrived at {work.name}. Inventory:")
for obj in work.objects:
    print(f"- {obj.name} ({obj.description})")

print(f"\nRemaining at {home.name}:")
for obj in home.objects:
    print(f"- {obj.name} ({obj.description})")

print(f"\nFinal state of commute transit: {len(commute.objects)} objects.")
