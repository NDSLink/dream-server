import models
from app import db

print("---Recharge Fixer---")
print("""Currently, there is a bug in Dream Land that causes Dream World
To occasionally complain that "it must recharge". This script will solve 
that.""")
is_sleeping = input("Is there currently a sleeping Pokemon in this save? (y/N) ").lower().startswith("y")
tid = int(input("What is this save's TID? "))
print("Please wait...")
u = models.GSUser.query.filter_by(id=tid).first()
if u == None:
    print("Huh? There is no user with that TID.")
    exit(5)
is_right = input(f"The trainer's name is {u.name}, right? (y/N) ").lower().startswith("y")

if is_right:
    if u.poke_is_sleeping == is_sleeping:
        print("Error! The user's save is synced correctly. Wait one day, then try Game Sync again.")
        exit(1)
    u.poke_is_sleeping = is_sleeping
    try:
        db.session.add(u)
    except Exception as e:
        print(f"Error! Unable to add modded user. Error:{e}")
        exit(3)
    try:
        db.session.commit()
    except Exception as e:
        print(f"Error! Unable to commit modded user. Error:{e}")
        exit(4)
    exit(0)
else:
    print("Oh? There must of been a database related error.")
    exit(2)

    
